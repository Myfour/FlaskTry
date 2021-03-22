import re
from unidecode import unidecode
_punct_re = re.compile(
    r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')  # 字符串前的r表示该字符串中的转义符不转义


def slugfy(text, delim='-'):
    '''Generate an ASCII-only slug'''
    result = []
    for word in _punct_re.split(text.lower()):
        result.extend(unidecode(word).lower().split())
    return delim.join(result)
