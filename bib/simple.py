# -*- coding:utf-8 -*-
import argparse
import os
import shutil
from distlib.wheel import Wheel


def simple(wheelhouse, simple_dir):
    for whl in os.listdir(wheelhouse):
        p = os.path.join(wheelhouse, whl)
        wheel = Wheel(p)
        name = wheel.name
        simple_dest = os.path.join(simple_dir, name)
        if not os.path.exists(simple_dest):
            os.makedirs(simple_dest)
        shutil.copy2(p, simple_dest)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('wheelhouse')
    parser.add_argument('simple')
    args = parser.parse_args()
    simple(args.wheelhouse, args.simple)
