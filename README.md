# Показ заказчику: два варианта лендинга «Праксеология менеджмента»

**Сначала прочитать `../PUT-K-IDEALU.md`** — все требования и правки заказчика по этому лендингу.

`index.html` — стартовая страница с двумя кнопками.

- `v1/` — «Балтика» (из `../final-baltika/`, текст проверен na-pero 27.09.2026). Текст — `v1/COPY.md`, сборка `cd v1 && python3 build.py`. Версии без квиза: `v1/?exp=first|been&sphere=manager|owner|artist`, квиз заново: `v1/?quiz=1`.
- `v2/` — «Будущее» (выгрузка Claude Design «Landing page project.zip», текст переписан na-pero 27.09.2026, видеофоны заменены статичными кадрами; видео предпринимателя в выгрузке было битое). Текст — `v2/COPY.md` (`[ключ] текст`; «—» убирает абзац), вёрстка — `v2/template.html`, сборка `cd v2 && python3 build.py`. Работает только онлайн (React/Babel с unpkg, шрифты Google).

Правки: поменять COPY.md → build.py → коммит и пуш, GitHub Pages обновится сам.
- `v6/` — вариант C из Claude Design (артефакт claude.ai/artifact/VEfgZvsZsLEkvW4hHxBzyE, ТЗ `v5/C-etalon.md`), переверстан в стиле «Балтики» (токены, Geist + Spectral, скругления и анимация из `v1/`). Текст и фото — из артефакта дословно. Статичный `index.html`, без сборки и внешних запросов.
- `v7/` — «Влево руля», форсайт-практикум (ТЗ заказчика 04.10.2026: `../v7-zadanie/ZADANIE.md`). Дизайн и сборка как у `v2/` (COPY.md → template.html → `cd v7 && python3 build.py` → index.html, React/Babel с unpkg), фото из `v6/` (+ «сосны у моря» из `v1/`), без квиза. Текст — `v7/COPY.md`, дословно из ТЗ. https://antioz.github.io/praxeology-pokaz/v7/
- `v9/` — «Обновление ПО», редизайн v7 из Claude Design (выгрузка «Правки дизайна Praxeology.zip», файл «Обновление ПО v7 редизайн.dc.html», 05.10.2026). Статичный `index.html` как есть, только ссылки на фото переведены с живой v7 на свою `v9/media/`. Рантайм `support.js` — тот же, что в v7. Шрифт Inter Tight с Google. https://antioz.github.io/praxeology-pokaz/v9/
- Режим правки текстов v10: `v10/?edit=1` (скрипт `v10/edit.js`). Текст правится кликом, кнопка «Скачать правки» сохраняет txt «было → стало» по разделам, правки живут в localStorage браузера. Без `?edit=1` страница прежняя. Правки из файла переносить в `v10/index.html` руками (вопросы FAQ — в массиве `FAQ` внизу файла).
- `tilda/` — v10 для Тильды (08.10.2026): `tilda-code.txt` — код для блока T123 «HTML-код» (без support.js, стили под `.piu108`, фото с GitHub Pages), `index.html` — инструкция по шагам со скриншотами и кнопкой «Скопировать код» (https://antioz.github.io/praxeology-pokaz/tilda/, PDF — `INSTRUKCIYA.pdf`, скрины в `img/`), `INSTRUKCIYA.txt` — то же текстом, `preview.html` — проверка со стилями Тильды. Пересборка после правок v10: `python3 tilda/build.py`.
- v10 сверен с 108.community/imanagement 08.10.2026: добавлены «Замысел», «Расписание», кнопка «Регистрация», «Founder & Art Director», промокод sixseven, до 12 октября, начало 15:00; форма заявки заменена кнопкой оплаты https://payform.ru/3ncKT9o/. Что было только в v10 (п. 04 результата, «Один инструмент вместо двадцати инсайтов», регалии и цитата Орлова, «Что я увезу?», финал и подвал) — оставлено.
