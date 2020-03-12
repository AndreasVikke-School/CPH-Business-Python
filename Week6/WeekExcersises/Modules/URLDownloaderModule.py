import wget
import os
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor

class NotFoundException(ValueError):
    def __init__(self, *args, **kwargs):
        ValueError.__init__(self, *args, **kwargs)

class URLDownloader():
    def __init__(self, url_list):
        self.url_list = url_list
        self.files = []
        self.vowels = "AaEeIiOoUu"

    def download(self, url, filename=None):
        try:
            return wget.download(url, filename)
        except:
            raise NotFoundException('Error: 404 file not found')

    def multi_download(self):
        def multithreading(func, args, workers=5):
            with ThreadPoolExecutor(workers) as ex:
                res = ex.map(func, args)
            return list(res)

        self.files = multithreading(self.download, self.url_list, 5)

    def filelist_generator(self):
        for f in self.url_list:
            yield f

    def __iter__(self):
        self.idx = 0
        return self

    def __next__(self):
        cidx = self.idx
        self.idx += 1
        if cidx < len(self.files):
            return self.files[cidx]
        else:
            raise StopIteration
            
    def avg_vowels(self, txt):
        return sum([*map(txt.lower().count, 'aeiYouæøå')])/len(txt.split())

    def hardest_read(self):
        def multithreading(func, args, names, workers=os.cpu_count()):
            with ProcessPoolExecutor(workers) as ex:
                res = ex.map(func, args)
            return dict(zip(names, res))
        
        texts = []
        for filename in self.files:
            with open(filename, 'rb') as file_obj:
                texts.append(file_obj.read().decode(errors='replace'))

        return {k: v for k,v in sorted(multithreading(self.avg_vowels, texts, self.files).items(), key=lambda item: item[1], reverse=True)}

        