// Режим правки текстов: открывается по ?edit=1, без параметра ничего не делает.
// Любой текст правится кликом; «Скачать правки» отдаёт файл «было → стало» по разделам.
(() => {
  if (!/[?&]edit=1(&|$)/.test(location.search)) return;

  const KEY = 'piu-v10-edits';
  const BLOCK = 'p,h1,h2,h3,blockquote,s,.btn,.qa-q';

  const css = document.createElement('style');
  css.textContent = `
    [data-reveal]{opacity:1!important;transform:none!important}
    .tape-track{animation:none!important}
    [data-ed]{outline:1px dashed transparent;outline-offset:4px;cursor:text;transition:outline-color .15s}
    [data-ed]:hover{outline-color:rgba(228,74,0,.45)}
    [data-ed]:focus{outline:2px solid #e44a00}
    [data-ed].ed-ch{outline:2px dashed #e44a00;background:rgba(228,74,0,.08)}
    #ed-panel{position:fixed;right:16px;bottom:16px;z-index:9999;width:min(340px,calc(100vw - 32px));padding:16px 18px;background:#222;color:#fff;font:14px/1.45 'Inter Tight',system-ui,sans-serif;box-shadow:0 10px 40px rgba(0,0,0,.35);border-top:3px solid #e44a00}
    #ed-panel b{font-weight:600}
    #ed-panel p{margin:6px 0 12px;color:rgba(255,255,255,.72);font-size:13px}
    #ed-panel .row{display:flex;flex-wrap:wrap;gap:8px}
    #ed-panel button{padding:9px 14px;border:1px solid #e44a00;background:transparent;color:#fff;font:inherit;font-size:13px;cursor:pointer}
    #ed-panel button.main{background:#e44a00}
    #ed-panel button:disabled{opacity:.4;cursor:default}
    #ed-panel .min{position:absolute;top:8px;right:10px;border:0;padding:2px 6px;font-size:16px;color:rgba(255,255,255,.6)}
    #ed-panel.mini p,#ed-panel.mini .row{display:none}
  `;
  document.head.appendChild(css);

  // Текст блока как видит читатель, но без text-transform (innerText вернул бы ПРОПИСНЫЕ)
  const text = (el) => {
    let out = '';
    const walk = (n) => {
      for (const c of n.childNodes) {
        if (c.nodeType === 3) out += c.data;
        else if (c.nodeName === 'BR') out += '\n';
        else if (c.nodeType === 1) {
          const block = /^(DIV|P)$/.test(c.nodeName);
          if (block && out && !out.endsWith('\n')) out += '\n';
          walk(c);
        }
      }
    };
    walk(el);
    return out.replace(/[ \t ]+/g, ' ').replace(/ *\n */g, '\n').trim();
  };

  const collect = (root) => {
    const tw = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: (t) => !t.data.trim() || t.parentElement.closest('script,style,svg,#ed-panel')
        ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT
    });
    const set = new Set();
    while (tw.nextNode()) {
      const p = tw.currentNode.parentElement;
      set.add(p.closest(BLOCK) || p);
    }
    // Вложенные убираем: правится внешний блок целиком
    return [...set].filter(el => ![...set].some(o => o !== el && o.contains(el)));
  };

  const start = () => {
    const root = document.querySelector('section[data-screen-label]').parentElement;
    const blocks = collect(root);
    let saved = {};
    try { saved = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) {}

    const items = blocks.map((el, i) => {
      const it = { el, orig: text(el), sec: (el.closest('[data-screen-label]') || {}).dataset?.screenLabel || '' };
      const s = saved[i];
      if (s && s.orig === it.orig) el.innerHTML = s.html;
      el.setAttribute('contenteditable', 'true');
      el.setAttribute('spellcheck', 'true');
      el.dataset.ed = i;
      return it;
    });

    const changed = () => items.filter(it => text(it.el) !== it.orig);

    const panel = document.createElement('div');
    panel.id = 'ed-panel';
    panel.innerHTML = `
      <button class="min" type="button" title="Свернуть">–</button>
      <b>Режим правки</b> · изменено: <b id="ed-n">0</b>
      <p>Кликните на любой текст и исправьте его прямо на странице. Правки хранятся в этом браузере, пока не нажмёте «Сбросить». Закончили — скачайте файл и пришлите его.</p>
      <div class="row">
        <button class="main" type="button" id="ed-dl">Скачать правки</button>
        <button type="button" id="ed-cp">Скопировать</button>
        <button type="button" id="ed-rs">Сбросить</button>
      </div>`;
    document.body.appendChild(panel);
    const $ = (id) => panel.querySelector('#' + id);

    const report = () => {
      const seen = new Set(), lines = [];
      const d = new Date();
      lines.push('Правки к странице «ПИУ*» (вариант 10)');
      lines.push(location.origin + location.pathname);
      lines.push(d.toLocaleString('ru-RU'), '');
      let n = 0;
      for (const it of changed()) {
        const now = text(it.el), k = it.sec + '\u0000' + it.orig + '\u0000' + now;
        if (seen.has(k)) continue; // бегущая строка повторена 4 раза
        seen.add(k);
        n++;
        lines.push(`${n}. Раздел «${it.sec}»`, 'Было:  ' + it.orig, 'Стало: ' + (now || '(удалить)'), '');
      }
      return { n, txt: lines.join('\n') };
    };

    const refresh = () => {
      const ch = new Set(changed());
      const store = {};
      items.forEach((it, i) => {
        it.el.classList.toggle('ed-ch', ch.has(it));
        if (ch.has(it)) store[i] = { orig: it.orig, html: it.el.innerHTML };
      });
      try { localStorage.setItem(KEY, JSON.stringify(store)); } catch (e) {}
      $('ed-n').textContent = report().n;
      $('ed-dl').disabled = $('ed-cp').disabled = !ch.size;
    };

    $('ed-dl').onclick = () => {
      const a = document.createElement('a');
      a.href = URL.createObjectURL(new Blob([report().txt], { type: 'text/plain;charset=utf-8' }));
      a.download = 'pravki-piu-' + new Date().toISOString().slice(0, 10) + '.txt';
      panel.appendChild(a); a.click(); a.remove(); // внутри панели — иначе клик заглушит перехватчик ниже
      setTimeout(() => URL.revokeObjectURL(a.href), 1000);
    };
    $('ed-cp').onclick = async () => {
      try { await navigator.clipboard.writeText(report().txt); $('ed-cp').textContent = 'Скопировано'; }
      catch (e) { $('ed-cp').textContent = 'Не вышло — скачайте файл'; }
      setTimeout(() => { $('ed-cp').textContent = 'Скопировать'; }, 2000);
    };
    $('ed-rs').onclick = () => {
      if (!confirm('Вернуть все тексты как было? Правки пропадут.')) return;
      try { localStorage.removeItem(KEY); } catch (e) {}
      location.reload();
    };
    panel.querySelector('.min').onclick = () => panel.classList.toggle('mini');

    document.addEventListener('input', refresh);
    // Вставка — только текстом, без чужого оформления
    document.addEventListener('paste', (e) => {
      if (!e.target.closest || !e.target.closest('[data-ed]')) return;
      e.preventDefault();
      document.execCommand('insertText', false, (e.clipboardData || window.clipboardData).getData('text/plain'));
    });
    // Ссылки и кнопки страницы в режиме правки не срабатывают
    window.addEventListener('click', (e) => {
      if (e.target.closest('#ed-panel')) return;
      if (e.target.closest('a,button')) { e.preventDefault(); e.stopPropagation(); }
    }, true);
    window.addEventListener('keydown', (e) => {
      if (e.key === ' ' && e.target.closest && e.target.closest('[data-ed]') && e.target.closest('a,button')) {
        e.preventDefault(); e.stopPropagation(); document.execCommand('insertText', false, ' ');
      }
    }, true);

    refresh();
  };

  // Страницу рисует support.js — ждём, пока появятся разделы и вопросы
  let tries = 0;
  const wait = () => {
    if (document.querySelector('section[data-screen-label]') && document.querySelector('.qa-q')) return setTimeout(start, 300);
    if (++tries < 100) setTimeout(wait, 100);
  };
  wait();
})();
