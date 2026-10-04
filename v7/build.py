# Сборка варианта 7 (как v2): COPY.md -> template.html -> index.html
import re, json, html as H
copy = {}
for ln in open('COPY.md', encoding='utf-8'):
    m = re.match(r'\[([\w.]+)\] ?(.*)$', ln.rstrip('\n'))
    if m: copy[m.group(1)] = m.group(2)
# даты не рвать: «30 октября – 2 ноября 2026» переносится только после тире
MON = r'(января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря)'
def nbsp(v):
    v = re.sub(r'(\d) ' + MON, '\\1\u00a0\\2', v)
    v = re.sub(MON + r' (\d{4})', '\\1\u00a0\\2', v)
    v = re.sub(MON + r' – ', '\\1\u00a0– ', v)
    v = re.sub(r'(\d)–(\d)', '\\1–\u2060\\2', v)  # «1–22» не рвать после тире
    return v
copy = {k: nbsp(v) for k, v in copy.items()}
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
