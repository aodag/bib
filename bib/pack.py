# -*- coding:utf-8 -*-
import os
import argparse
import shutil
from tempfile import mkdtemp
from distlib.metadata import Metadata
from distlib.wheel import Wheel


def pack(project_dir, wheelhouse, work_dir):
    dist_path = os.path.join(project_dir, 'dist-info', 'pydist.json')

    md = Metadata(path=dist_path)
    wheel = Wheel()
    wheel.name = md.name
    wheel.version = md.version

    dest_dist = os.path.join(work_dir, '{}.dist-info'.format(md.name))
    os.makedirs(dest_dist)
    shutil.copyfile(dist_path, os.path.join(dest_dist, 'pydist.json'))
    for pkg_dir in os.listdir(os.path.join(project_dir, 'src')):
        shutil.copytree(os.path.join(project_dir, 'src', pkg_dir),
                        os.path.join(work_dir, pkg_dir))
    paths = {
        'purelib': work_dir,
    }

    wheel.dirname = wheelhouse
    wheel.build(paths)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('project_dir')
    parser.add_argument('--wheelhouse',
                        default=os.getcwd())
    args = parser.parse_args()
    try:
        work_dir = mkdtemp()
        pack(args.project_dir, args.wheelhouse, work_dir)
    finally:
        shutil.rmtree(work_dir)
