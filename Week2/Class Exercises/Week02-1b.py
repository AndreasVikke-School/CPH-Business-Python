import argparse
import Modules.webget as webget
import mimetypes

if __name__ == '__main__':
 
    parser = argparse.ArgumentParser(description='A program that downloads a URL and stores it locally')
    parser.add_argument('url', help='an integer for the accumulator')
    parser.add_argument('-d', '--destination', default='default', help='The name of the file to store the url in')
    args = parser.parse_args()

    url = args.url
    destination = args.destination

    if destination == 'default':
        if url.split('/')[-1] != "":
            destination = url.split('/')[-1].split(".")[-2]
        else:
            destination = url.split("://")[1].split("/")[0].split(".")[-2]

        t, encoding = mimetypes.guess_type(url)
        if t != None:
            destination += '.{}'.format(t.split('/')[-1])
        else:
            destination += '.dat'

    path = webget.download(url, destination)
    print('Downloded file to: {}'.format(path))