# Сборка варианта 2: COPY.md -> template.html -> index.html
import re, json, html as H
copy = {}
for ln in open('COPY.md', encoding='utf-8'):
    m = re.match(r'\[([\w.]+)\] ?(.*)$', ln.rstrip('\n'))
    if m: copy[m.group(1)] = m.group(2)
t = open('template.html', encoding='utf-8').read()
missing = set()
def js(m):
    k = m.group(1)
    if k not in copy: missing.add(k); return '""'
    return json.dumps(copy[k], ensure_ascii=False)
def ht(m):
    k = m.group(1)
    if k not in copy: missing.add(k); return ''
    return H.escape(copy[k], quote=False)
# «—» в COPY.md = убрать абзац <p> целиком (или пустой пункт списка в JS)
for k, v in list(copy.items()):
    if v.strip() == '—':
        t = re.sub(r'<p[^>]*>⟦' + re.escape(k) + r'⟧</p>\s*', '', t)
        copy[k] = ''
t = re.sub(r'⟦js:([\w.]+)⟧', js, t)
t = re.sub(r'⟦([\w.]+)⟧', ht, t)
if missing: raise SystemExit('нет ключей в COPY.md: ' + ', '.join(sorted(missing)))
open('index.html', 'w', encoding='utf-8').write(t)
print('index.html собран')
