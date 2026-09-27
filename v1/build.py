#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Сборка index.html: текст из COPY.md (скилл na-pero) + шаблон template.html. Запуск: python3 build.py"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
copy_text = (HERE / "COPY.md").read_text(encoding="utf-8").split("\n---\n")[0]

copy = {}
for m in re.finditer(r"\[([a-z0-9_.]+)\]\s*(.*?)(?=\s*\[[a-z0-9_.]+\]|\n|$)", copy_text):
    key, val = m.group(1), m.group(2).strip()
    if val:
        copy[key] = val

# подпись по лицензиям — дословно из ТЗ, раздел 4.13
copy["footer.credits"] = ("Фото и видео: Alexander Grebenkov (CC BY 3.0), Karlheinz Schreiber, Kirill.uyutnov, "
                          "Николай Ягунов (CC BY-SA 4.0) — Wikimedia Commons; Pexels.")

required = ["hero.title", "hero.sub.manager", "hero.sub.owner", "hero.sub.artist", "facts.price",
            "cta.button", "footer", "quiz.welcome.title"]
missing = [k for k in required if k not in copy]
if missing:
    raise SystemExit(f"нет ключей: {missing}")

html = (HERE / "template.html").read_text(encoding="utf-8")
html = html.replace("/*COPY*/{}", json.dumps(copy, ensure_ascii=False))
(HERE / "index.html").write_text(html, encoding="utf-8")
print(f"index.html собран, ключей: {len(copy)}")
