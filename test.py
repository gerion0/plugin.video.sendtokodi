#!/usr/bin/env python3
"""Test yt-dlp extraction"""
import argparse
import distutils.util
import sys

from lib.extractor import extract

if __name__ == "__main__":
    def onoff(x):
        return bool(distutils.util.strtobool(x))

    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description=sys.modules[__name__].__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('URL', help="URL that should be extracted.")
    parser.add_argument('--with-dash', type=onoff, default=True,
                        help="Enable DASH support.")
    parser.add_argument('--only-audio', type=onoff, default=False,
                        help="Extract only an audio stream.")
    args = parser.parse_args()

    print(extract(args.URL, with_dash=args.with_dash, only_audio=args.only_audio))
