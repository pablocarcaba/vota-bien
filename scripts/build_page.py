"""Inserta data/generado/dataset.json en site/template.html y genera site/index.html."""
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
tpl = open(os.path.join(ROOT, "site", "template.html"), encoding="utf-8").read()
data = open(os.path.join(ROOT, "data", "generado", "dataset.json"), encoding="utf-8").read().replace("</", "<\\/")
out = os.path.join(ROOT, "site", "index.html")
open(out, "w", encoding="utf-8").write(tpl.replace("__DATA__", data))
print("Generado", out)
