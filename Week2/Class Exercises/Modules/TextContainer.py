import re
import string

class TextContainer():
    def __init__(self, text):
        self.text = text

    def count_words(self):
        return len(re.findall(r'\w+', self.text))

    def count_chars(self):
        return len(self.text)

    def count_ascii(self):
        return len(re.findall('[' + string.ascii_letters + ']', self.text))

    def remove_punctation(self):
        return re.sub('[' + string.punctuation + ']', '', self.text)