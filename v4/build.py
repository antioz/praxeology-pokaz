# Сборка v4: COPY.md -> template.html -> index.html  (запуск из папки v4: python3 build.py)
import re, html as H
from pathlib import Path
here = Path(__file__).resolve().parent
copy = {}
for ln in (here / 'COPY.md').read_text(encoding='utf-8').splitlines():
    m = re.match(r'\[([\w.]+)\] ?(.*)$', ln.rstrip())
    if m: copy[m.group(1)] = m.group(2).strip()
# даты и суммы не рвать: перенос только после тире
MON = r'(января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря)'
def nbsp(v):
    v = re.sub(r'(\d) ' + MON, '\\1\u00a0\\2', v)
    v = re.sub(MON + r' (\d{4})', '\\1\u00a0\\2', v)
    v = re.sub(MON + r' – ', '\\1\u00a0– ', v)
    v = re.sub(r'(\d)–(\d)', '\\1–\u2060\\2', v)
    v = re.sub(r'(\d) (\d{3})', '\\1\u00a0\\2', v)          # 108 000
    v = re.sub(r'(\d) ₽', '\\1\u00a0₽', v)
    v = re.sub(r'(\d{1,2}:\d{2}) ', '\\1\u00a0', v)          # «18:00 пятницы»
    v = re.sub(r'(?<=\s)(с|в|до|и|а|о|у|к|на|по|за|из|от|не) ', '\\1\u00a0', v)  # висячие предлоги
    return v
copy = {k: nbsp(v) for k, v in copy.items()}
t = (here / 'template.html').read_text(encoding='utf-8')
missing = set()
for k, v in list(copy.items()):
    if v.strip() == '—':
        t = re.sub(r'<p[^>]*>⟦' + re.escape(k) + r'⟧</p>\s*', '', t)
        copy[k] = ''
def ht(m):
    k = m.group(1)
    if k not in copy: missing.add(k); return ''
    return H.escape(copy[k], quote=False)
t = re.sub(r'⟦([\w.]+)⟧', ht, t)
if missing: raise SystemExit('нет ключей в COPY.md: ' + ', '.join(sorted(missing)))
(here / 'index.html').write_text(t, encoding='utf-8')
print('index.html собран')
