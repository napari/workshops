"""Mount the unified napari.org search widget into the built site.

mystmd/jupyter-book has no documented hook for adding arbitrary <head>/
<body> content, so this post-processes the built HTML directly: copies
the widget assets into the output directory and appends a mount point +
script tag to every page.

Run via: python docs/_scripts/inject_search_widget.py
Called automatically by: pixi run _docs-build (as a dependency).
"""

import os
import pathlib
import shutil

BUILD_DIR = pathlib.Path('docs/_build/html')
RESOURCES_DIR = pathlib.Path('docs/_resources')
BASE_URL = os.environ.get('BASE_URL', '')

WIDGET_SNIPPET = f'''
<link rel="stylesheet" href="{BASE_URL}/_static/napari-search-widget.css">
<div class="napari-search" style="position:fixed;top:0.75rem;right:0.75rem;width:320px;z-index:1000;"></div>
<script
  src="{BASE_URL}/_static/napari-search-widget.js"
  data-bundle-path="{BASE_URL}/pagefind/"
  data-merge-paths="/stable/pagefind/"
  data-mount=".napari-search"
  defer
></script>
</body>
'''

static_dir = BUILD_DIR / '_static'
static_dir.mkdir(parents=True, exist_ok=True)
for asset in ('napari-search-widget.js', 'napari-search-widget.css'):
    shutil.copy(RESOURCES_DIR / asset, static_dir / asset)

count = 0
for html_file in BUILD_DIR.rglob('*.html'):
    text = html_file.read_text(encoding='utf-8')
    if 'class="napari-search"' in text:
        continue
    if '</body>' not in text:
        continue
    html_file.write_text(text.replace('</body>', WIDGET_SNIPPET, 1), encoding='utf-8')
    count += 1

print(f'Injected search widget into {count} page(s)')
