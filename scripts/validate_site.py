#!/usr/bin/env python3
"""Static quality checks for the GitHub Pages site. Uses only Python stdlib."""
from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
import tempfile
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
PAGES = [SITE / "index.html", SITE / "mostra-cultural.html"]

class AuditParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.references = []
        self.errors = []
        self.scripts = []
        self.in_script = False
        self.script_parts = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            if attrs["id"] in self.ids:
                self.errors.append(f"ID duplicado: {attrs['id']}")
            self.ids.add(attrs["id"])
        if tag == "img" and not attrs.get("alt", "").strip():
            self.errors.append("Imagem sem texto alternativo (alt).")
        if tag == "a":
            if attrs.get("href"):
                self.references.append(("href", attrs["href"]))
            if attrs.get("target") == "_blank":
                rel = set(attrs.get("rel", "").lower().split())
                if not {"noopener", "noreferrer"}.issubset(rel):
                    self.errors.append("Link target=_blank sem rel noopener noreferrer.")
        if tag in {"img", "script"} and attrs.get("src"):
            self.references.append(("src", attrs["src"]))
        if tag == "script" and not attrs.get("src"):
            self.in_script = True
            self.script_parts = []

    def handle_endtag(self, tag):
        if tag == "script" and self.in_script:
            self.scripts.append("".join(self.script_parts))
            self.in_script = False

    def handle_data(self, data):
        if self.in_script:
            self.script_parts.append(data)

def check_page(page):
    source = page.read_text(encoding="utf-8")
    parser = AuditParser()
    parser.feed(source)
    parser.close()
    errors = list(parser.errors)

    if not re.search(r"<title>\s*.+?\s*</title>", source, re.I | re.S):
        errors.append("Título da página ausente.")
    if 'name="viewport"' not in source.lower():
        errors.append("Meta viewport ausente.")

    for kind, value in parser.references:
        value = value.strip()
        if not value or value.startswith(("http://", "https://", "mailto:", "tel:", "data:", "javascript:")):
            continue
        if value.startswith("#"):
            if value[1:] and value[1:] not in parser.ids:
                errors.append(f"Âncora inexistente: {value}")
            continue
        local_path = value.split("#", 1)[0].split("?", 1)[0]
        target = (page.parent / local_path).resolve()
        if not target.exists():
            errors.append(f"Recurso local inexistente ({kind}): {value}")
        elif target.suffix.lower() == ".svg":
            try:
                ET.parse(target)
            except ET.ParseError as exc:
                errors.append(f"SVG inválido ({value}): {exc}")

    for doc in re.findall(r'doc:"([^"]+\.md)"', source):
        if not (ROOT / "11_Catalogo_Jogos" / doc).is_file():
            errors.append(f"Ficha de catálogo inexistente: {doc}")
    for cover in re.findall(r'cover:"([^"]+)"', source):
        asset = SITE / "assets" / "capas" / f"{cover}.svg"
        if not asset.is_file():
            errors.append(f"Capa de projeto inexistente: {asset.relative_to(ROOT)}")
        else:
            try:
                ET.parse(asset)
            except ET.ParseError as exc:
                errors.append(f"SVG inválido ({asset.relative_to(ROOT)}): {exc}")

    if not parser.scripts:
        errors.append("Nenhum script inline encontrado para verificação.")
    for number, script in enumerate(parser.scripts, 1):
        with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8") as tmp:
            tmp.write(script)
            tmp.flush()
            result = subprocess.run(["node", "--check", tmp.name], capture_output=True, text=True)
            if result.returncode:
                errors.append(f"JavaScript inline #{number}: {result.stderr.strip()}")
    return errors

def main():
    failures = []
    for page in PAGES:
        if not page.exists():
            failures.append(f"Página ausente: {page}")
            continue
        issues = check_page(page)
        failures.extend(f"{page.relative_to(ROOT)}: {issue}" for issue in issues)
        if not issues:
            print(f"OK: {page.relative_to(ROOT)}")
    if failures:
        print("\n".join(f"ERRO: {item}" for item in failures), file=sys.stderr)
        return 1
    print("Validação concluída: HTML, IDs, links locais, alt, segurança de links externos e sintaxe JavaScript.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
