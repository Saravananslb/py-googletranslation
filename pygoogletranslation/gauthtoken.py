import re
import requests
from pygoogletranslation import urls

class TokenAcquirer:
    """Google Translate API token generator

    translate.google.com uses a token to authorize the requests. If you are
    not Google, you do have this token and will have to pay for use.
    This class is the result of reverse engineering on the obfuscated and
    minified code used by Google to generate such token.

    The token is based on a seed which is updated once per hour and on the
    text that will be translated.
    Both are combined - by some strange math - in order to generate a final
    token (e.g. 464393.115905) which is used by the API to validate the
    request.

    This operation will cause an additional request to get an initial
    token from translate.google.com.

    Example usage:
        >>> from pygoogletranslation.gauthtoken import TokenAcquirer
        >>> acquirer = TokenAcquirer()
        >>> text = 'test'
        >>> tk = acquirer.do(text)
        >>> tk
        464393.115905
    """

    def __init__(self, tkk='0', tkk_url=urls.TOKEN, proxies=None):

        if proxies is not None:
            self.proxies = proxies
        else:
            self.proxies = None

        r = requests.get(tkk_url, proxies=self.proxies)

        if r.status_code == 200:
            re_tkk = re.search("(?<=tkk=\\')[0-9.]{0,}", str(r.content.decode("utf-8")))            
            if re_tkk:
                self.tkk = re_tkk.group(0)
            else:
                self.tkk = '0'
        else:
            self.tkk = '0'


    def _xr(self, a, b):
            size_b = len(b)
            c = 0
            while c < size_b - 2:
                d = b[c + 2]
                d = ord(d[0]) - 87 if 'a' <= d else int(d)
                d = self.rshift(a, d) if '+' == b[c + 1] else a << d
                a = a + d & 4294967295 if '+' == b[c] else a ^ d

                c += 3
            return a

    def acquire(self, text):
        a = []
        # Convert text to ints
        for i in text:
            val = ord(i)
            if val < 0x10000:
                a += [val]
            else:
                # Python doesn't natively use Unicode surrogates, so account for those
                a += [
                    math.floor((val - 0x10000) / 0x400 + 0xD800),
                    math.floor((val - 0x10000) % 0x400 + 0xDC00)
                ]

        b = self.tkk
        d = b.split('.')
        b = int(d[0]) if len(d) > 1 else 0

        # assume e means char code array
        e = []
        g = 0
        size = len(a)
        while g < size:
            l = a[g]
            # just append if l is less than 128(ascii: DEL)
            if l < 128:
                e.append(l)
            # append calculated value if l is less than 2048
            else:
                if l < 2048:
                    e.append(l >> 6 | 192)
                else:
                    # append calculated value if l matches special condition
                    if (l & 64512) == 55296 and g + 1 < size and \
                            a[g + 1] & 64512 == 56320:
                        g += 1
                        l = 65536 + ((l & 1023) << 10) + (a[g] & 1023)  # This bracket is important
                        e.append(l >> 18 | 240)
                        e.append(l >> 12 & 63 | 128)
                    else:
                        e.append(l >> 12 | 224)
                    e.append(l >> 6 & 63 | 128)
                e.append(l & 63 | 128)
            g += 1
        a = b
        for i, value in enumerate(e):
            a += value
            a = self._xr(a, '+-a^+6')
        a = self._xr(a, '+-3^+b+-f')
        a ^= int(d[1]) if len(d) > 1 else 0
        if a < 0:  # pragma: nocover
            a = (a & 2147483647) + 2147483648
        a %= 1000000  # int(1E6)
        return '{}.{}'.format(a, a ^ b)

    def do(self, text):
        tk = self.acquire(text)
        return tk

    
    def rshift(self, val, n):
        """python port for '>>>'(right shift with padding)
        """
        return (val % 0x100000000) >> n

        

