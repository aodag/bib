# -*- coding:utf-8 -*-
import argparse
import os
import venv
import subprocess
from distlib.metadata import Metadata


def make_metadata(project_dir):
    md = Metadata()
    md.name = input('name >>> ')
    md.version = input('version >>> ')
    md.summary = input('summary >>> ')
    dist_path = os.path.join(project_dir, 'dist-info')
    if not os.path.exists(dist_path):
        os.makedirs(dist_path)
    md.write(path=os.path.join(dist_path,
                               'pydist.json'))
    return md


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('project_dir')
    args = parser.parse_args()
    md = make_metadata(args.project_dir)
    modules_dir = os.path.abspath(os.path.join(args.project_dir,
                                               'python_modules'))
    os.makedirs(modules_dir)
    builder = venv.EnvBuilder()
    venv_dir = os.path.join(args.project_dir, 'venv')
    builder.create(venv_dir)
    x = subprocess.run([os.path.join(venv_dir, 'bin', 'python'),
                        '-c', 'import site;print(site.getsitepackages()[0])'],
                       stdout=subprocess.PIPE,
                       universal_newlines=True)
    site_packages = x.stdout.strip()

    with open(os.path.join(site_packages, 'bib.pth'), 'w') as f:
        f.write(modules_dir)
    os.makedirs(os.path.join(args.project_dir, 'src'))
    pack = os.path.join(args.project_dir, 'src', md.name)
    os.makedirs(pack)
    with open(os.path.join(pack, '__init__.py'), 'w') as f:
        f.write("#")
