#!/usr/bin/env python3
"""
Синхронизирует корневые pageNNNNNNNN.html с копиями в подпапках для GitHub Pages
(GitHub Pages не умеет .htaccess rewrite, поэтому у каждого красивого URL
есть папка со своим index.html - копией соответствующего pageNNNNNNNN.html
с абсолютными путями к ассетам).

Запускать из корня репозитория после любого редактирования page*.html,
которые входят в маппинг ниже, и перед git push.
"""
import os
import re

PAIRS = {
    "uzi": "page26771114.html",
    "gynekolog_odintsovo_vniissok": "page41681879.html",
    "massazh_vniissok": "page41765976.html",
    "kosmetolog_vniissok": "page41778691.html",
    "spetsialist-po-gv": "page41947785.html",
}
HOMEPAGE_SRC = "page26655203.html"

def fix_paths(t: str) -> str:
    t = re.sub(r'href="css/', 'href="/css/', t)
    t = re.sub(r'src="js/', 'src="/js/', t)
    t = re.sub(r'src="images/', 'src="/images/', t)
    t = re.sub(r'href="images/', 'href="/images/', t)
    t = re.sub(r'data-original="images/', 'data-original="/images/', t)
    t = re.sub(r'content="images/', 'content="/images/', t)
    t = re.sub(r"url\('images/", "url('/images/", t)
    t = re.sub(r'url\("images/', 'url("/images/', t)
    return t

def main():
    changed = []
    # root index.html (homepage) - no path fixing needed, already root-relative
    t = open(HOMEPAGE_SRC, encoding='utf-8').read()
    old = open('index.html', encoding='utf-8').read() if os.path.exists('index.html') else None
    if old != t:
        open('index.html', 'w', encoding='utf-8').write(t)
        changed.append('index.html')

    for slug, src in PAIRS.items():
        if not os.path.exists(src):
            print('MISSING SOURCE:', src)
            continue
        t = open(src, encoding='utf-8').read()
        t = fix_paths(t)
        dst = os.path.join(slug, 'index.html')
        old = open(dst, encoding='utf-8').read() if os.path.exists(dst) else None
        if old != t:
            os.makedirs(slug, exist_ok=True)
            open(dst, 'w', encoding='utf-8').write(t)
            changed.append(dst)

    print(f'Updated {len(changed)} file(s):')
    for c in changed:
        print(' ', c)

if __name__ == '__main__':
    main()
