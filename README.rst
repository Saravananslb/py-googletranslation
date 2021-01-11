PYGOOGLETRANSLATION
===================

https://pypi.org/project/pygoogletranslation/

|GitHub license| |travis status| |Documentation Status| |PyPI version|
|Coverage Status| |Code Climate|

pygoogletranslation is a **free** and **unlimited** python library that
implemented Google Translate API. This uses the `Google Translate Ajax
API <https://translate.google.com>`__ to make calls to such methods as
detect and translate.

Compatible with Python 3.6+.


Features
--------

-  Fast and reliable - it uses the same servers that
   translate.google.com uses
-  Auto language detection
-  Bulk translations
-  Request

TODO
~~~~

more features are coming soon.

-  Proxy support
-  Internal session management (for better bulk translations)

Python Request Module
~~~~~~~~~~~~~~

This library uses request to get an data from google.

Request :
   POST
   GET
   


How does this library work
~~~~~~~~~~~~~~~~~~~~~~~~~~

You may wonder how this library works properly, whereas other
python translation package use the token mechanism but that is
failling because google has changed their token mechanism.

--------------

Installation
------------

To install, either use things like pip with the package "googletrans"
or download the package and put the "googletrans" directory into your
python path.

.. code:: bash

    $ pip install pygoogletranslation

Basic Usage
-----------

If source language is not given, google translate attempts to detect the
source language.

.. code:: python

    >>> from pygoogletranslation import Translator
    >>> translator = Translator()
    >>> translator.translate('Good Morning', dest='ta')
    # <Translated src=ko dest=ta text=காலை வணக்கம். pronunciation=Good evening.>
    >>> translator.translate('안녕하세요.', dest='ja')
    # <Translated src=ko dest=ja text=こんにちは。 pronunciation=Kon'nichiwa.>
    >>> translator.translate('veritas lux mea', src='la')
    # <Translated src=la dest=en text=The truth is my light pronunciation=The truth is my light>

Customize service URL
~~~~~~~~~~~~~~~~~~~~~

You can use proxies in the translation.

.. code:: python

    >>> from pygoogletranslation import Translator
    >>> translator = Translator(proxies=YOUR_PROXIES)

Advanced Usage (Bulk)
~~~~~~~~~~~~~~~~~~~~~

Array can be used to translate a batch of strings in a single method
call and a single HTTP session. The exact same method shown above works
for arrays as well.

.. code:: python

    >>> translations = translator.translate(['this is google translation', 'Tamil language' ], dest='ta')
    >>> for translation in translations:
    ...    print(translation.origin, ' -> ', translation.text)
    

Language detection
~~~~~~~~~~~~~~~~~~

The detect method, as its name implies, identifies the language used in
a given sentence.

.. code:: python

    >>> from pygoogletranslation import Translator
    >>> translator = Translator()
    >>> translator.detect('காலை வணக்கம்,')
    # <Detected lang=ta confidence=0.72041003>
    >>> translator.detect('この文章は日本語で書かれました。')
    # <Detected lang=ja confidence=0.64889508>
    >>> translator.detect('This sentence is written in English.')
    # <Detected lang=en confidence=0.22348526>
    >>> translator.detect('Tiu frazo estas skribita en Esperanto.')
    # <Detected lang=eo confidence=0.10538048>
    
Translation from document (.doc, .pdf, .txt):
---------------------------------------------
    >>> from pygoogletranslation import Translator
    >>> translator = Translator()
    >>> translator.bulktranslate('test.txt', dest="ta")
    # <bulk translated text>


pygoogletranslation to get Language and Language Codes
-------------------------------------------------------
               >>> from pygoogletranslation import Translator
               >>> translator = Translator()
               >>> translator.glanguage()
               >>> {
                  "sl": {
                  "auto": "Detect language",
                  "af": "Afrikaans",
                  "sq": "Albanian",
                  "am": "Amharic",
                  "ar": "Arabic",
                  "hy": "Armenian",
                  "az": "Azerbaijani",
                  "eu": "Basque",
                  "be": "Belarusian",
                  "bn": "Bengali",
                  "bs": "Bosnian",
                  "bg": "Bulgarian",
                  "ca": "Catalan",
                  "ceb": "Cebuano",
                  "ny": "Chichewa",
                  "zh-CN": "Chinese",
                  "co": "Corsican",
                  "hr": "Croatian",
                  "cs": "Czech",
                  "da": "Danish",
                  "nl": "Dutch",
                  "en": "English",
                  "eo": "Esperanto",
                  "et": "Estonian",
                  "tl": "Filipino",
                  "fi": "Finnish",
                  "fr": "French",
                  "fy": "Frisian",
                  "gl": "Galician",
                  "ka": "Georgian",
                  "de": "German",
                  "el": "Greek",
                  "gu": "Gujarati",
                  "ht": "Haitian Creole",
                  "ha": "Hausa",
                  "haw": "Hawaiian",
                  "iw": "Hebrew",
                  "hi": "Hindi",
                  "hmn": "Hmong",
                  "hu": "Hungarian",
                  "is": "Icelandic",
                  "ig": "Igbo",
                  "id": "Indonesian",
                  "ga": "Irish",
                  "it": "Italian",
                  "ja": "Japanese",
                  "jw": "Javanese",
                  "kn": "Kannada",
                  "kk": "Kazakh",
                  "km": "Khmer",
                  "rw": "Kinyarwanda",
                  "ko": "Korean",
                  "ku": "Kurdish (Kurmanji)",
                  "ky": "Kyrgyz",
                  "lo": "Lao",
                  "la": "Latin",
                  "lv": "Latvian",
                  "lt": "Lithuanian",
                  "lb": "Luxembourgish",
                  "mk": "Macedonian",
                  "mg": "Malagasy",
                  "ms": "Malay",
                  "ml": "Malayalam",
                  "mt": "Maltese",
                  "mi": "Maori",
                  "mr": "Marathi",
                  "mn": "Mongolian",
                  "my": "Myanmar (Burmese)",
                  "ne": "Nepali",
                  "no": "Norwegian",
                  "or": "Odia (Oriya)",
                  "ps": "Pashto",
                  "fa": "Persian",
                  "pl": "Polish",
                  "pt": "Portuguese",
                  "pa": "Punjabi",
                  "ro": "Romanian",
                  "ru": "Russian",
                  "sm": "Samoan",
                  "gd": "Scots Gaelic",
                  "sr": "Serbian",
                  "st": "Sesotho",
                  "sn": "Shona",
                  "sd": "Sindhi",
                  "si": "Sinhala",
                  "sk": "Slovak",
                  "sl": "Slovenian",
                  "so": "Somali",
                  "es": "Spanish",
                  "su": "Sundanese",
                  "sw": "Swahili",
                  "sv": "Swedish",
                  "tg": "Tajik",
                  "ta": "Tamil",
                  "tt": "Tatar",
                  "te": "Telugu",
                  "th": "Thai",
                  "tr": "Turkish",
                  "tk": "Turkmen",
                  "uk": "Ukrainian",
                  "ur": "Urdu",
                  "ug": "Uyghur",
                  "uz": "Uzbek",
                  "vi": "Vietnamese",
                  "cy": "Welsh",
                  "xh": "Xhosa",
                  "yi": "Yiddish",
                  "yo": "Yoruba",
                  "zu": "Zulu"
                  },
                  "tl": {
                  "af": "Afrikaans",
                  "sq": "Albanian",
                  "am": "Amharic",
                  "ar": "Arabic",
                  "hy": "Armenian",
                  "az": "Azerbaijani",
                  "eu": "Basque",
                  "be": "Belarusian",
                  "bn": "Bengali",
                  "bs": "Bosnian",
                  "bg": "Bulgarian",
                  "ca": "Catalan",
                  "ceb": "Cebuano",
                  "ny": "Chichewa",
                  "zh-CN": "Chinese (Simplified)",
                  "zh-TW": "Chinese (Traditional)",
                  "co": "Corsican",
                  "hr": "Croatian",
                  "cs": "Czech",
                  "da": "Danish",
                  "nl": "Dutch",
                  "en": "English",
                  "eo": "Esperanto",
                  "et": "Estonian",
                  "tl": "Filipino",
                  "fi": "Finnish",
                  "fr": "French",
                  "fy": "Frisian",
                  "gl": "Galician",
                  "ka": "Georgian",
                  "de": "German",
                  "el": "Greek",
                  "gu": "Gujarati",
                  "ht": "Haitian Creole",
                  "ha": "Hausa",
                  "haw": "Hawaiian",
                  "iw": "Hebrew",
                  "hi": "Hindi",
                  "hmn": "Hmong",
                  "hu": "Hungarian",
                  "is": "Icelandic",
                  "ig": "Igbo",
                  "id": "Indonesian",
                  "ga": "Irish",
                  "it": "Italian",
                  "ja": "Japanese",
                  "jw": "Javanese",
                  "kn": "Kannada",
                  "kk": "Kazakh",
                  "km": "Khmer",
                  "rw": "Kinyarwanda",
                  "ko": "Korean",
                  "ku": "Kurdish (Kurmanji)",
                  "ky": "Kyrgyz",
                  "lo": "Lao",
                  "la": "Latin",
                  "lv": "Latvian",
                  "lt": "Lithuanian",
                  "lb": "Luxembourgish",
                  "mk": "Macedonian",
                  "mg": "Malagasy",
                  "ms": "Malay",
                  "ml": "Malayalam",
                  "mt": "Maltese",
                  "mi": "Maori",
                  "mr": "Marathi",
                  "mn": "Mongolian",
                  "my": "Myanmar (Burmese)",
                  "ne": "Nepali",
                  "no": "Norwegian",
                  "or": "Odia (Oriya)",
                  "ps": "Pashto",
                  "fa": "Persian",
                  "pl": "Polish",
                  "pt": "Portuguese",
                  "pa": "Punjabi",
                  "ro": "Romanian",
                  "ru": "Russian",
                  "sm": "Samoan",
                  "gd": "Scots Gaelic",
                  "sr": "Serbian",
                  "st": "Sesotho",
                  "sn": "Shona",
                  "sd": "Sindhi",
                  "si": "Sinhala",
                  "sk": "Slovak",
                  "sl": "Slovenian",
                  "so": "Somali",
                  "es": "Spanish",
                  "su": "Sundanese",
                  "sw": "Swahili",
                  "sv": "Swedish",
                  "tg": "Tajik",
                  "ta": "Tamil",
                  "tt": "Tatar",
                  "te": "Telugu",
                  "th": "Thai",
                  "tr": "Turkish",
                  "tk": "Turkmen",
                  "uk": "Ukrainian",
                  "ur": "Urdu",
                  "ug": "Uyghur",
                  "uz": "Uzbek",
                  "vi": "Vietnamese",
                  "cy": "Welsh",
                  "xh": "Xhosa",
                  "yi": "Yiddish",
                  "yo": "Yoruba",
                  "zu": "Zulu"
                  },
                  "al": {}
                  }

--------------

Note on library usage
---------------------

DISCLAIMER: this is an unofficial library using the web API of translate.google.com
and also is not associated with Google.

-  **The maximum character limit on a single text is 15k.**

-  Due to limitations of the web version of google translate, this API
   does not guarantee that the library would work properly at all times
   (so please use this library if you don't care about stability).

-  **Important:** If you want to use a stable API, I highly recommend you to use
   `Google's official translate
   API <https://cloud.google.com/translate/docs>`__.

-  If you get HTTP 5xx error or errors like #6, it's probably because
   Google has banned your client IP address.

--------------

Versioning
----------

This library follows `Semantic Versioning <http://semver.org/>`__ from
v2.0.0. Any release versioned 0.x.y is subject to backwards incompatible
changes at any time.

Contributing
-------------------------

Contributions are more than welcomed. See
`CONTRIBUTING.md <CONTRIBUTING.md>`__

-----------------------------------------

License
-------

pygoogletranslation is licensed under the MIT License. The terms are as
follows:

::
MIT License

Copyright (c) 2021 Saravananslb

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


.. |GitHub license| image:: https://img.shields.io/github/license/mashape/apistatus.svg
   :target: http://opensource.org/licenses/MIT
.. |travis status| image:: https://travis-ci.org/ssut/py-googletrans.svg?branch=master
   :target: https://travis-ci.org/Saravananslb/py-googletranslation
.. |Documentation Status| image:: https://readthedocs.org/projects/py-googletrans/badge/?version=latest
  
.. |PyPI version| image:: https://badge.fury.io/py/pygoogletranslation.svg
   :target: http://badge.fury.io/py/pygoogletranslation
.. |Coverage Status| image:: https://coveralls.io/repos/github/ssut/py-googletrans/badge.svg
   
.. |Code Climate| image:: https://codeclimate.com/github/ssut/py-googletrans/badges/gpa.svg
   
