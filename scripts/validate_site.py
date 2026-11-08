#!/usr/bin/env python3
"""Static quality checks for the GitHub Pages site. Uses only Python stdlib."""
from html.parser import HTMLParser
from pathlib import Path
import subprocess
import tempfile
import sys

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
PAGES = [SITE / "index.html", SITE / "mostra-cultural.html"]

class AuditParser(HTMLParser):
    def __init__(self, page):
        super().__init__(convert_charrefs=True)
        self.page = page
        self.ids = set()
        self.errors = []
        self.scripts = []
        self.in_script = False
        self.script_parts = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            if a["id"] in self.ids:
                self.errors.append(f"ID duplicado: {a['id']}")
            self.ids.add(a["id"])
        if tag == "img" and not a.get("alt", "").strip():
            self.errors.append("Imagem sem texto alternativo (alt).")
        if tag == "a" and a.get("target") == "_blank":
            rel = set(a.get("rel", "").lower().split())
            if not {"noopener", "noreferrer"}.issubset(rel):
                self.errors.append("Link target=_blank sem rel noopener noreferrer.")
        if tag == "script" and not a.get("src"):
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
    parser = AuditParser(page)
    parser.feed(page.read_text(encoding="utf-8"))
    parser.close()
    errors = list(parser.errors)
    for tag in parser.find_all if False else []:
        pass
    source = page.read_text(encoding="utf-8")
    for match in __import__("re").finditer(r'\b(?:href|src)=[\'"]([^\'"]+)[\'"]', source):
        value = match.group(1).strip()
        if not value or value.startswith(("http://", "https://", "mailto:", "tel:", "data:", "javascript:")):
            continue
        if value.startswith("#"):
            if value[1:] and value[1:] not in parser.ids:
                errors.append(f"Âncora inexistente: {value}")
            continue
        target = (page.parent / value.split("#", 1)[0].split("?", 1)[0]).resolve()
        if not target.exists():
            errors.append(f"Recurso local inexistente: {value}")
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
    print("Validação concluída: HTML estrutural, IDs, links locais, alt, segurança de links externos e sintaxe JavaScript.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
