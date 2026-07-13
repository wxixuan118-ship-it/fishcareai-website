#!/usr/bin/env python3
"""
修复 guide 和 wiki 页面的白色背景问题。
将 .sec-w{background:#fff} 替换为浅蓝色，与品牌色统一。

运行方法：
  cd "/Users/viki/Documents/fishcareai/fishcare AI website/fishcareai-latest-2026-07-07"
  python3 fix-guide-backgrounds.py
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

REPLACEMENTS = [
    # guide/wiki 页面：白色分区改为品牌浅蓝
    ('.sec-w{background:#fff}',          '.sec-w{background:var(--bg)}'),
    ('.sec-w{background: #fff}',         '.sec-w{background:var(--bg)}'),
    ('.sec-w { background: #fff; }',     '.sec-w{background:var(--bg)}'),
    # card 保持白色但加轻微透明度，减少过于刺眼的纯白
    ('.card{background:#fff;',           '.card{background:rgba(255,255,255,0.92);'),
]

TARGET_DIRS = ['guides', 'wiki']

fixed = 0
for folder in TARGET_DIRS:
    folder_path = os.path.join(BASE_DIR, folder)
    if not os.path.isdir(folder_path):
        continue
    for root, dirs, files in os.walk(folder_path):
        for fname in files:
            if fname != 'index.html':
                continue
            fpath = os.path.join(root, fname)
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
            original = content
            for old, new in REPLACEMENTS:
                content = content.replace(old, new)
            if content != original:
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(content)
                rel = os.path.relpath(fpath, BASE_DIR)
                print(f'  Fixed: {rel}')
                fixed += 1

print(f'\n✅ Done — {fixed} files updated.')
