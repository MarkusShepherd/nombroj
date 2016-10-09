# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

import argparse
import sys

from literumi import spell

from translate import detect_languages, translate

LANGUAGE_DESC = {
    'de': 'German',
    'dk': 'Danish (Denmark)',
    'en': 'English',
    'en_GB': 'English (Great Britain)',
    'en_IN': 'English (India)',
    'eo': 'Esperanto',
    'es': 'Spanish',
    'fr': 'French',
    'fr_CH': 'French (Switzerland)',
    'id': 'Indonesian',
    'lt': 'Lithuanian',
    'lv': 'Latvian',
    'no': 'Norwegian',
    'pl': 'Polish',
    'pt_BR': 'Portuguese (Brazil)',
    'ru': 'Russian',
}

def numbers(lang, start=0, end=100, chunk_size=None, google=None):
    if google:
        return translate(numbers('en', start, end, google=False),
                         source='en', target=lang, chunk_size=chunk_size)

    try:
        spell(0, lang=lang)
        return (spell(i, lang=lang) for i in range(start, end + 1))
    except:
        if google is None:
            return numbers(lang, start, end, chunk_size, google=True)

def get_args():
    parser = argparse.ArgumentParser(description='Print numbers in a number of languages')
    parser.add_argument('lang', nargs='?',
        help='target language')
    parser.add_argument('-s', '--start', type=int, default=0,
        help='first number to be translated')
    parser.add_argument('-e', '--end', type=int, default=100,
        help='last number to be translated')
    parser.add_argument('-c', '--chunk-size', type=int, default=20,
        help='number of translated lines per request if Google Translate is used')
    parser.add_argument('-o', '--offline', action='store_true', default=False,
        help='never use Google Translate')
    parser.add_argument('-g', '--google', action='store_true', default=False,
        help='always use Google Translate')
    parser.add_argument('-d', '--detect', action='store_true', default=False,
        help='detect supported languages and exit')
    parser.add_argument('-D', '--detect-short', action='store_true', default=False,
        help='detect supported languages (symbol only) and exit')
    parser.add_argument('-v', '--verbose', action='count', default=0,
        help='increase verbosity (specify multiple times for more)')

    return parser.parse_args()

def main():
    args = get_args()

    if args.detect or args.detect_short:
        languages = LANGUAGE_DESC.copy()
        if not args.offline:
            try:
                languages.update({language['language']: language['name']
                                 for language in detect_languages('en')})
            except:
                pass
        if args.detect_short:
            for language in sorted(languages.keys()):
                print(language)
        else:
            for symbol, name in sorted(languages.items(), key=lambda item: item[1]):
                print('{} ({})'.format(name, symbol))
        return

    if not args.lang:
        print('target language is required')
        return

    translations = numbers(args.lang, args.start, args.end, args.chunk_size,
                           False if args.offline else True if args.google else None)

    for t in translations:
        print(t)

if __name__ == '__main__':
    main()
