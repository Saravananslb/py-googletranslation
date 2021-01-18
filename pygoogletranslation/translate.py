# -*- coding: utf-8 -*-
"""
A Translation module.

You can translate text using this module.
"""
import os
import json
import requests
import unidecode
import docx2txt
import PyPDF2
import time
from pygoogletranslation import utils, urls
from pygoogletranslation.constants import (
    LANGCODES, LANGUAGES, RPCIDS
)
from pygoogletranslation import gauthtoken
from pygoogletranslation.models import Translated, Detected


class Translator:

    def __init__(self, host=urls.TRANSLATE, proxies=None, timeout=None,
                retry=3, sleep=5, retry_messgae=False):
        self.host = host if 'http' in host else 'https://' + host
        self.rpcids = RPCIDS
        self.transurl = urls.TRANSLATEURL
        if proxies is not None:
            self.proxies = proxies
        else:
            self.proxies = None
        
        if timeout is not None:
            self.timeout = timeout

        self.retry = retry
        self.retry_messgae = retry_messgae
        self.sleep = sleep

    def translate(self, text, src='auto', dest='en'):
        if type(text) == list:
            i = 0
            for _text in text:
                _text = _text.replace('"', '')
                _text = _text.replace("'", "")
                _text = _text.replace("“", "")
                _text = _text.replace("”", "")
                text[i] = _text
                i += 1
        else:
            text = text.replace('"', '')
            text = text.replace("'", "")
            text = text.replace("“", "")
            text = text.replace("”", "")
        
        if src != 'auto':
            if src.lower() in LANGCODES:
                src = LANGCODES[src]
            elif src.lower() in LANGUAGES:
                src = src
            else:
                raise ValueError('invalid source language')

        if dest != 'en':
            if dest.lower() in LANGCODES:
                dest = LANGCODES[src.lower()]
            elif dest.lower() in LANGUAGES:
                dest = dest
            else:
                raise ValueError('invalid destination language')

        data = self._translate(text, src=src, dest=dest)
        return self.extract_translation(data, text)

    
    def extract_translation(self, _data, text, src='auto', dest='en'):
        if type(text) != list:
            text = [text]
        result_list = []
        c = 0
        for data in _data:
            try:
                translated = data[0][2][1][0][0][5][0][0]
            except:
                translated = ""
            extra_data = {}
            try:
                src = data[0][2][3][5][0][0][3]
            except Exception:  # pragma: nocover
                pass

            try:
                dest = data[0][2][3][5][0][0][2]
            except Exception:  # pragma: nocover
                pass

            pron = None
            try:
                pron = unidecode.unidecode(data[0][2][1][0][0][1])
            except Exception:  # pragma: nocover
                pass
            # put final values into a new Translated object
            result = Translated(src=src, dest=dest, origin=text[c],
                                text=translated, pronunciation=pron, extra_data=extra_data)
            result_list.append(result)
            c += 1
        if len(result_list) == 1:
            return result_list[0]
        else:
            return result_list

    def detect(self, text, **kwargs):
        """Detect language of the input text

        :param text: The source text(s) whose language you want to identify.
                     Batch detection is supported via sequence input.
        :type text: UTF-8 :class:`str`; :class:`unicode`; string sequence (list, tuple, iterator, generator)

        :rtype: Detected
        :rtype: :class:`list` (when a list is passed)

        Basic usage:
            >>> from googletrans import Translator
            >>> translator = Translator()
            >>> translator.detect('이 문장은 한글로 쓰여졌습니다.')
            <Detected lang=ko confidence=0.27041003>
            >>> translator.detect('この文章は日本語で書かれました。')
            <Detected lang=ja confidence=0.64889508>
            >>> translator.detect('This sentence is written in English.')
            <Detected lang=en confidence=0.22348526>
            >>> translator.detect('Tiu frazo estas skribita en Esperanto.')
            <Detected lang=eo confidence=0.10538048>

        Advanced usage:
            >>> langs = translator.detect(['한국어', '日本語', 'English', 'le français'])
            >>> for lang in langs:
            ...    print(lang.lang, lang.confidence)
            ko 1
            ja 0.92929292
            en 0.96954316
            fr 0.043500196
        """
        if isinstance(text, list):
            result = []
            for item in text:
                lang = self.detect(item)
                result.append(lang)
            return result

        data = self._translate(text, 'auto', 'en')

        # actual source language that will be recognized by Google Translator when the
        # src passed is equal to auto.
        src = ''
        confidence = 0.0
        try:
            src = data[0][0][2][3][5][0][0][3]
            # confidence = data[8][-2][0]
        except Exception:  # pragma: nocover
            pass
        result = Detected(lang=src, confidence=confidence)

        return result
          
    def _translate(self, text, src, dest):
        """ Generate Token for each Translation and post requset to
        google web api translation and return an response

        If the status code is 200 the request is considered as an success
        else other status code are consider as translation failure.

        """
        if type(text) != list:
            text = [text]        
        translated_list = []
        url = self.transurl
        params = utils.format_param(self.rpcids)
        for _text in text:
            trans_list = []
            tokenized_text = utils.tokenize_sentence(_text)
            for _tokenized_text in tokenized_text:
                data = utils.format_data(self.rpcids, _tokenized_text, src, dest)
                response = requests.request("POST", url, data=data, params=params, proxies=self.proxies)
                if response.status_code == 200:
                    _format_data = utils.format_response(str(response.text))
                    trans_list.append(_format_data)
                elif response.status_code == 429:
                    _format_data = self.retry_request(data, params)
                    trans_list.append(_format_data)
                else:
                    raise Exception('Unexpected status code {} from {}'.format(response.status_code, self.transurl))
                    return False
            translated_list.append(utils.format_translation(trans_list))
        return translated_list

    def retry_request(self, data, params):
        """ 
        For bulk translation some times translation might failed
        beacuse of too many attempts. for such a case before hitting
        translation api wait for some time and retrying again
        """
        retry = self.retry
        sleep = self.sleep
        response = requests.request("POST", url=self.transurl, data=data, params=params, proxies=self.proxies)
        for i in range(0, retry):
            if response.status_code == 200:
                _format_data = utils.format_response(str(response.text))
                return _format_data
            elif response.status_code == 429:
                if self.retry_messgae:
                    print('retrying translation after {}s'.format(sleep))
                time.sleep(sleep)
                sleep = i * sleep
            else:
                raise Exception('Unexpected status code {} from {}'.format(response.status_code, self.transurl))
                return False
        raise Exception('Unexpected status code {} from {} after retried {} loop with {}s delay'.format(response.status_code, self.transurl, retry, self.sleep))

    def bulktranslate(self, file, src='auto', dest='en'):
        """Translation from document (.doc, .docx, .pdf, .txt):
        ---------------------------------------------
            >>> from pygoogletranslation import Translator
            >>> translator = Translator()
            >>> translator.bulktranslate('test.txt', dest="ta")
            # <bulk translated text>
        """
        if src != 'auto':
            if src.lower() in LANGCODES:
                src = LANGCODES[src.lower()]
            elif src.lower() in LANGUAGES:
                src = src
            else:
                raise ValueError('invalid source language')

        if dest != 'en':
            if dest.lower() in LANGCODES:
                dest = LANGCODES[src.lower()]
            elif dest.lower() in LANGUAGES:
                dest = dest
            else:
                raise ValueError('invalid destination language')
        
        if not os.path.exists(file):
            raise FileNotFoundError('file {} does not exists !'.format(file))

        # Read document file, pdf file, text file
        if file.endswith('.doc') or file.endswith('.docx'):
            text = docx2txt.process(file)
        elif file.endswith('.txt'):
            _file = open(file, 'r')
            text = _file.read()
            _file.close()
        elif file.endswith('.pdf'):
            text = ''
            pdfFileObj = open(file, 'rb') 
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
            for i in range(0, pdfReader.numPages):
                pageObj = pdfReader.getPage(0) 
                text += pageObj.extractText()
            pdfFileObj.close() 
        else:
            raise FileNotFoundError('unsupported file format .{}.'.format(file.split('.'))[len(file.split('.') - 1)])
        text = text.replace('"', '')
        text = text.replace("'", "")
        text = text.replace("“", "")
        text = text.replace("”", "")
        data = self._translate(text, src=src, dest=dest)
        return self.extract_translation(data, text)
  
    def glanguage(self):
        """ Get request from google and return language and their lang codes.
        Example:
        >>> translate = Translator()
        >>> translate.glanguage()
        >>> {
                "sl": {
                    "auto": "Detect language",
                    "af": "Afrikaans",
                    "sq": "Albanian",
                },
                "tl": {
                    "af": "Afrikaans",
                    "sq": "Albanian",
                    "am": "Amharic",
                    "ar": "Arabic",
                },
                "al": {}
            }
        """
        querystring = utils.format_querystringlang()
        response = requests.get(url=self.host + 'l', params=querystring, proxies=self.proxies)
        if response.status_code == 200:
            glang = json.loads(response.content)
            return glang
        else:
            raise Exception('Unexpected status code {} from {}'.format(response.status_code, self.host))
            return False