"""Preparar um projeto GTM separado. Python 3.10+, biblioteca padrão apenas."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

PACOTE = Path(__file__).resolve().parents[1]
VERSAO = "1.0.0"
IDENTIFICADOR = "escalar-negocios-gtm"


def dentro(caminho: Path, raiz: Path) -> bool:
    try:
        caminho.resolve().relative_to(raiz.resolve())
        return True
    except ValueError:
        return False


def ficheiros_origem() -> dict[Path, bytes]:
    ficheiros: dict[Path, bytes] = {}
    for origem in (PACOTE / "templates" / "workspace").rglob("*"):
        if origem.is_file():
            ficheiros[origem.relative_to(PACOTE / "templates" / "workspace")] = origem.read_bytes()
    for origem in (PACOTE / "skills").rglob("*"):
        if origem.is_file() and "__pycache__" not in origem.parts and origem.suffix != ".pyc":
            ficheiros[Path(".agents/skills") / origem.relative_to(PACOTE / "skills")] = origem.read_bytes()
    ficheiros[Path(".claude/skills/escalar-gtm/SKILL.md")] = (PACOTE / "templates/claude-skill.md").read_bytes()
    return ficheiros


def escrever_novo(caminho: Path, dados: bytes) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    # Nunca abre um ficheiro existente para escrita.
    with caminho.open("xb") as stream:
        stream.write(dados)


def instalar(destino: Path) -> dict[str, object]:
    destino = destino.expanduser().resolve()
    if dentro(destino, PACOTE) or dentro(PACOTE, destino):
        raise ValueError("Escolhe uma pasta separada do pacote de instalação.")
    if destino.exists() and not destino.is_dir():
        raise ValueError("O destino não é uma pasta.")
    marcador = destino / ".escalar-gtm.json"
    if marcador.is_symlink() or not dentro(marcador, destino):
        raise ValueError("O identificador de instalação não pode apontar para fora do projeto.")
    existente = marcador.is_file()
    if existente:
        try:
            identificacao = json.loads(marcador.read_text(encoding="utf-8"))
        except (ValueError, OSError) as exc:
            raise ValueError("Não foi possível ler o identificador do projeto.") from exc
        if not isinstance(identificacao, dict) or identificacao.get("pacote") != IDENTIFICADOR:
            raise ValueError("A pasta pertence a outro pacote.")
        if identificacao.get("versao") != VERSAO:
            raise ValueError("A versão instalada é diferente. Preserva-a; esta operação não faz atualizações.")
    elif destino.exists() and any(destino.iterdir()):
        raise ValueError("A pasta tem conteúdo e não é um projeto GTM identificado. Usa uma pasta nova.")

    fontes = ficheiros_origem()
    novos: list[tuple[Path, bytes]] = []
    preservados = 0
    # Verificar todos os conflitos antes de escrever seja o que for.
    for relativo, dados in fontes.items():
        alvo = destino / relativo
        if alvo.is_symlink() or not dentro(alvo, destino):
            raise ValueError(f"Caminho fora do projeto: {relativo.as_posix()}")
        for pai in alvo.parents:
            if pai == destino:
                break
            if pai.exists() and not pai.is_dir():
                raise ValueError(f"Era esperada uma pasta: {pai.relative_to(destino).as_posix()}")
        if alvo.exists():
            if not alvo.is_file():
                raise ValueError(f"Era esperado um ficheiro: {relativo.as_posix()}")
            if relativo == Path("REGISTO.md"):
                preservados += 1
            elif alvo.read_bytes() != dados:
                raise ValueError(f"Ficheiro diferente preservado: {relativo.as_posix()}. Não foi feita nenhuma alteração.")
            else:
                preservados += 1
        else:
            novos.append((alvo, dados))
    for pasta in ("dados", "entregaveis", "revisoes"):
        alvo = destino / pasta
        if alvo.is_symlink() or not dentro(alvo, destino) or (alvo.exists() and not alvo.is_dir()):
            raise ValueError(f"Pasta de dados inválida: {pasta}")

    destino.mkdir(parents=True, exist_ok=True)
    if not existente:
        dados = json.dumps({"pacote": IDENTIFICADOR, "versao": VERSAO}, ensure_ascii=False, indent=2) + "\n"
        escrever_novo(marcador, dados.encode("utf-8"))
    for alvo, dados in novos:
        escrever_novo(alvo, dados)
    for pasta in ("dados", "entregaveis", "revisoes"):
        (destino / pasta).mkdir(exist_ok=True)
    return {
        "destino": str(destino),
        "ficheiros_criados": len(novos) + (0 if existente else 1),
        "ficheiros_preservados": preservados,
        "proximo_passo": "Ler AGENTS.md, .agents/skills/escalar-gtm/SKILL.md e REGISTO.md; iniciar ou retomar agora, na mesma conversa.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Instalar o Coach GTM sem substituir trabalho existente.")
    parser.add_argument("--destino", required=True, type=Path, help="Pasta local separada para o projeto GTM")
    args = parser.parse_args()
    try:
        resultado = instalar(args.destino)
    except (ValueError, OSError) as exc:
        parser.exit(1, f"Instalação interrompida: {exc}\n")
    print(json.dumps(resultado, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
