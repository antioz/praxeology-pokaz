#!/usr/bin/env python3
"""v10/index.html → tilda/tilda-code.txt: один кусок кода для блока Тильды T123 «HTML-код».

Без support.js: стили под обёрткой .piu108 (чтобы не спорить со стилями Тильды),
вопросы-ответы — обычная разметка, анимации и раскрытие ответов — свой маленький скрипт,
картинки — по полным адресам GitHub Pages.

Запуск: python3 tilda/build.py  (из папки pokaz/)
"""
import html, json, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / 'v10' / 'index.html'
OUT = ROOT / 'tilda' / 'tilda-code.txt'
PREVIEW = ROOT / 'tilda' / 'preview.html'
MEDIA = 'https://antioz.github.io/praxeology-pokaz/v10/media/'
W = '.piu108'

s = SRC.read_text(encoding='utf-8')

# --- стили ---
css = re.search(r'<style>(.*?)</style>', s, re.S).group(1)
css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)


def scope_sel(sel):
    sel = sel.strip()
    if sel in (':root', 'html,body', 'body'):
        return W
    if sel == 'html':
        return None  # scroll-behavior оставляем Тильде
    if sel == '*':
        return f'{W},{W} *,{W} *::before,{W} *::after'
    return ','.join(f'{W} {x.strip()}' for x in sel.split(','))


def scope(block):
    out, i = [], 0
    while i < len(block):
        j = block.find('{', i)
        if j < 0:
            break
        head = block[i:j].strip()
        if head.startswith('@media') or head.startswith('@supports'):
            depth, k = 1, j + 1
            while depth:
                depth += {'{': 1, '}': -1}.get(block[k], 0)
                k += 1
            out.append(f'{head}{{{scope(block[j + 1:k - 1])}}}')
            i = k
        elif head.startswith('@keyframes'):
            depth, k = 1, j + 1
            while depth:
                depth += {'{': 1, '}': -1}.get(block[k], 0)
                k += 1
            out.append(block[i:k].strip())
            i = k
        else:
            k = block.find('}', j)
            sel = scope_sel(head)
            if sel:
                out.append(f'{sel}{{{block[j + 1:k].strip()}}}')
            i = k + 1
    return '\n'.join(out)


css = scope(css)
css += f'''
{W}{{display:block;position:relative;width:100%}}
{W} .qa-a{{display:none}}
{W} .qa.open .qa-a{{display:block}}
'''

# --- разметка ---
body = s[s.index('<div style="font-family:var(--f-sans)'):s.index('</x-dc>')]
body = body[body.index('>') + 1:body.rindex('</div>')]  # снять внешнюю обёртку — её роль берёт .piu108
body = body.replace('src="media/', f'src="{MEDIA}')

faq = re.search(r'FAQ = \[(.*?)\];', s, re.S).group(1)
items = re.findall(r'\{ q: "(.*?)", a: "(.*?)" \}', faq)
assert items, 'не нашёл FAQ'
qa = ''.join(f'''        <div class="qa">
          <button type="button" aria-expanded="false">
            <span style="font-size:calc(var(--fs) * 1.22);line-height:1.35;font-weight:400;">{html.escape(q)}</span>
            <span class="pm" aria-hidden="true">+</span>
          </button>
          <p class="muted qa-a" style="margin:0;padding:0 60px 28px 0;max-width:var(--tw);text-wrap:pretty;">{html.escape(a)}</p>
        </div>
''' for q, a in items)
body = re.sub(r'\s*<sc-for .*?</sc-for>\n', '\n' + qa, body, flags=re.S)
assert '{{' not in body and '<sc-' not in body, 'остался шаблон support.js'

js = '''(function(){
  var root=document.getElementById('piu108'); if(!root) return;
  root.querySelectorAll('.qa button').forEach(function(b){
    b.addEventListener('click',function(){
      var q=b.parentNode, o=!q.classList.contains('open');
      root.querySelectorAll('.qa.open').forEach(function(x){x.classList.remove('open');x.querySelector('button').setAttribute('aria-expanded','false');x.querySelector('.pm').textContent='+';});
      if(o){q.classList.add('open');b.setAttribute('aria-expanded','true');q.querySelector('.pm').textContent='\\u2212';}
    });
  });
  root.querySelectorAll('.play[data-yt]').forEach(function(b){
    b.addEventListener('click',function(){
      var box=b.parentNode, f=document.createElement('iframe');
      f.src='https://www.youtube.com/embed/'+b.getAttribute('data-yt')+'?autoplay=1&rel=0';
      f.setAttribute('allow','autoplay; encrypted-media; picture-in-picture; fullscreen'); f.setAttribute('allowfullscreen','');
      f.style.cssText='position:absolute;inset:0;width:100%;height:100%;border:0;';
      box.innerHTML=''; box.appendChild(f);
    });
  });
  var still=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(still||!('IntersectionObserver' in window)) return;
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.style.opacity='1';e.target.style.transform='none';io.unobserve(e.target);}});},{threshold:0.12,rootMargin:'0px 0px -40px 0px'});
  root.querySelectorAll('[data-reveal]').forEach(function(el){
    var sib=[].filter.call(el.parentNode.children,function(x){return x.hasAttribute('data-reveal');});
    var d=Math.min(Math.max(sib.indexOf(el),0),4)*0.08;
    el.style.opacity='0'; el.style.transform='translateY(28px)';
    el.style.transition='opacity 1s ease '+d+'s, transform 1.1s cubic-bezier(.2,.7,.2,1) '+d+'s';
    io.observe(el);
  });
})();'''

code = f'''<!-- ПИУ — форсайт-практикум. Код для блока Тильды T123 «HTML-код». Собрано из praxeology-pokaz/v10 скриптом tilda/build.py -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@200;300;400;500;600;700&display=swap">
<style>
{css}
</style>
<div id="piu108" class="piu108" style="font-family:var(--f-sans);font-size:var(--fs);line-height:var(--lh);">
{body.strip()}
</div>
<script>
{js}
</script>
'''
OUT.write_text(code, encoding='utf-8')

# Проверочная страница: тот же код внутри разметки блока T123 и со стилями Тильды
PREVIEW.write_text(f'''<!DOCTYPE html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex"><title>ПИУ — проверка кода для Тильды</title>
<link rel="stylesheet" href="https://static.tildacdn.com/css/tilda-grid-3.0.min.css">
<link rel="stylesheet" href="https://static.tildacdn.com/ws/project422516/tilda-blocks-page282920009.min.css">
</head><body class="t-body" style="margin:0;">
<div id="allrecords" class="t-records"><div id="rec1" class="r t-rec" data-record-type="131">
<div class="t123"><div class="t-container_100"><div class="t-width t-width_100">
{code}
</div></div></div></div></div>
</body></html>
''', encoding='utf-8')
print(f'{OUT.relative_to(ROOT)}: {len(code):,} символов; FAQ: {len(items)}')
