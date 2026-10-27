"""Conferir integridade do pacote e referências locais, sem dependências externas."""

from __future__ import annotations

from pathlib import Path
import re
import sys

RAIZ = Path(__file__).resolve().parents[1]


def verificar(raiz: Path = RAIZ) -> list[str]:
    erros: list[str] = []
    obrigatorios = ("README.md", "SETUP.md", "AGENTS.md", "CLAUDE.md", "TERCEIROS.md", "LICENSE",
                    "docs/FIDELIDADE.md", "docs/fontes-suplementares.json",
                    "templates/workspace/REGISTO.md", "templates/claude-skill.md")
    for relativo in obrigatorios:
        if not (raiz / relativo).is_file():
            erros.append(f"Falta {relativo}")
    for origem in raiz.rglob("*.md"):
        if ".git" in origem.parts or "__pycache__" in origem.parts:
            continue
        texto = origem.read_text(encoding="utf-8")
        if origem.name == "SKILL.md":
            cabecalho = re.match(r"\A---\n(.*?)\n---", texto, re.S)
            if not cabecalho or not re.search(r"^name: [a-z0-9-]+$", cabecalho.group(1), re.M) or not re.search(r"^description: .+", cabecalho.group(1), re.M):
                erros.append(f"Frontmatter inválido: {origem.relative_to(raiz)}")
        for referencia in re.findall(r"\]\(([^)]+)\)", texto):
            if re.match(r"^(https?://|mailto:|#)", referencia):
                continue
            destino = referencia.split("#", 1)[0]
            if not (origem.parent / destino).is_file():
                erros.append(f"Referência em falta: {origem.relative_to(raiz)} -> {destino}")
    for origem in raiz.rglob("*"):
        if origem.is_file() and (origem.name == "fontes-originais.json" or origem.suffix.lower() in (".pdf", ".pptx")):
            erros.append(f"Material original no pacote público: {origem.relative_to(raiz)}")
    skills = list((raiz / "skills").glob("*/SKILL.md"))
    if len(skills) != 6:
        erros.append(f"Esperadas uma skill principal e cinco suplementares; encontradas {len(skills)}.")
    return erros


if __name__ == "__main__":
    problemas = verificar()
    if problemas:
        print("\n".join(problemas))
        sys.exit(1)
    print("Pacote íntegro: referências locais e seis skills verificadas; originais fora da distribuição.")
