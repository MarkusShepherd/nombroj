# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import argparse
import requests
import sys

with open('.api_key') as file:
    API_KEY = file.read().strip()

def chunks(iterable, size):
    count = 0
    for item in iterable:
        if count == 0:
            chunk = []
        chunk.append(item)
        count += 1
        if count == size:
            yield chunk
            count = 0
    if count > 0:
        yield chunk

def translate(queries, target, source=None, chunk_size=0, max_tries=3):
    url = 'https://www.googleapis.com/language/translate/v2'

    queries = list(queries)

    chunks_ = chunks(queries, chunk_size) if chunk_size else [queries]

    for chunk in chunks_:
        params = {
            'key': API_KEY,
            'q': chunk,
            'target': target,
        }

        if source:
            params['source'] = source

        for retry in range(max_tries):
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                body = response.json()
                translations = body['data']['translations']
                break
            except Exception as e:
                print(e, file=sys.stderr)
                print('retry {}'.format(retry + 1), file=sys.stderr)
        else: # will be executed if no break in loop
            raise ValueError('could not retrieve translations after {} tries'.format(max_tries))

        for translation in translations:
            yield translation['translatedText']

def detect_languages(target=None):
    url = 'https://www.googleapis.com/language/translate/v2/languages'
    params = {'key': API_KEY}
    if target:
        params['target'] = target
    response = requests.get(url, params=params)
    response.raise_for_status()
    body = response.json()
    return body['data']['languages']

def get_args():
    parser = argparse.ArgumentParser(description='Translate strings')
    parser.add_argument('queries', nargs='*',
        help='strings to be translated')
    parser.add_argument('-t', '--target',
        help='target language')
    parser.add_argument('-s', '--source',
        help='source language (if none specified will be detected)')
    parser.add_argument('-c', '--chunk-size', type=int, default=20,
        help='number of translated lines per request')
    parser.add_argument('-d', '--detect', action='store_true', default=False,
        help='detect supported languages and exit')
    parser.add_argument('-v', '--verbose', action='count', default=0,
        help='increase verbosity (specify multiple times for more)')

    return parser.parse_args()

def main():
    args = get_args()

    if args.detect:
        languages = detect_languages('en')
        for language in languages:
            print('{} ({})'.format(language['name'], language['language']))
        return

    if not args.target:
        raise AttributeError('target language is required')

    queries = args.queries if args.queries else sys.stdin
    queries = filter(None, map(lambda s: s.strip(), queries))

    for t in translate(queries, source=args.source, target=args.target, chunk_size=args.chunk_size):
        print(t)

if __name__ == '__main__':
    main()
