import argparse
import tempfile
import os
import shutil
from urllib import request
from distlib.locators import SimpleScrapingLocator
from distlib.wheel import Wheel
from distlib.scripts import ScriptMaker


def locate(simple_url, pkg, dest, work):
    locator = SimpleScrapingLocator(simple_url)
    dist = locator.locate(pkg)
    url = list(dist.download_urls)[0]
    download = request.urlopen(url)
    fname = url.split('/')[-1]
    with open(os.path.join(work, fname), 'wb') as f:
        f.write(download.read())
    wheel = Wheel(os.path.join(work, fname))
    print(wheel.name)
    paths = {
        'purelib': dest,
        'platlib': dest,
        'prefix': dest,
        'headers': dest,
        'scripts': dest,
        'data': dest,
    }
    maker = ScriptMaker(None, None)
    wheel.install(paths, maker)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default='https://pypi.python.org/simple/')
    parser.add_argument('pkg')
    parser.add_argument('dest')
    args = parser.parse_args()

    work = tempfile.mkdtemp()
    try:
        locate(args.url, args.pkg, args.dest, work)
    finally:
        shutil.rmtree(work)
