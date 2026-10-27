"""Gerar um .ics opcional, depois da conclusão e aceitação do utilizador."""

from __future__ import annotations

import argparse
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
import uuid


def data_semana_seis(inicio: date) -> date:
    return inicio + timedelta(days=41)


def escapar(texto: str) -> str:
    return texto.replace("\\", "\\\\").replace("\r\n", "\n").replace("\r", "\n").replace("\n", "\\n").replace(";", "\\;").replace(",", "\\,")


def dobrar(linha: str) -> list[str]:
    # RFC 5545: no máximo 75 octetos por linha, sem quebrar caracteres UTF-8.
    partes: list[str] = []
    atual = ""
    for caractere in linha:
        if len((atual + caractere).encode("utf-8")) > 75:
            partes.append(atual)
            atual = " "
        atual += caractere
    partes.append(atual)
    return partes


def gerar_evento(quando: datetime, agora: datetime | None = None) -> str:
    if quando.tzinfo is None or quando.utcoffset() is None:
        raise ValueError("Confirma a hora com deslocamento UTC explícito, por exemplo +00:00 ou +01:00.")
    agora = agora or datetime.now(timezone.utc)
    inicio = quando.astimezone(timezone.utc)
    if inicio <= agora.astimezone(timezone.utc):
        raise ValueError("O checkpoint está no passado; combina uma nova data.")
    formato = "%Y%m%dT%H%M%SZ"
    linhas = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Escalar Negocios//Coach GTM//PT",
              "CALSCALE:GREGORIAN", "METHOD:PUBLISH", "BEGIN:VEVENT",
              f"UID:{uuid.uuid4()}@escalar-gtm.local",
              "DTSTAMP:" + agora.astimezone(timezone.utc).strftime(formato),
              "DTSTART:" + inicio.strftime(formato),
              "DTEND:" + (inicio + timedelta(minutes=30)).strftime(formato),
              "SUMMARY:" + escapar("Checkpoint GTM · Semana 6 · Escalar Negócios"),
              "DESCRIPTION:" + escapar("Abre o teu projeto GTM e pede o checkpoint da semana 6. Traz os resultados por canal, CAC máximo, volume mínimo e critérios escritos: continua, ajusta ou para."),
              "END:VEVENT", "END:VCALENDAR"]
    return "\r\n".join(parte for linha in linhas for parte in dobrar(linha)) + "\r\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Criar ficheiro de calendário; não agenda nem importa um evento.")
    parser.add_argument("--inicio-plano", type=date.fromisoformat, help="AAAA-MM-DD; sugere o fim da semana 6")
    parser.add_argument("--quando", type=datetime.fromisoformat, help="Data/hora com UTC confirmado: AAAA-MM-DDTHH:MM:SS+01:00")
    parser.add_argument("--saida", type=Path, help="Ficheiro .ics a criar sem substituir outro")
    parser.add_argument("--percurso-concluido", action="store_true", help="Só depois de verificar o registo completo")
    parser.add_argument("--aceite", action="store_true", help="Só após aceitação explícita do agendamento")
    args = parser.parse_args()
    if args.inicio_plano:
        print("Fim da semana 6:", data_semana_seis(args.inicio_plano).isoformat())
    if args.quando is None and args.saida is None:
        if args.inicio_plano is None:
            parser.error("Indica --inicio-plano para sugerir uma data, ou --quando e --saida para gerar um evento.")
        return
    if args.quando is None or args.saida is None:
        parser.error("Para gerar um evento, indica --quando e --saida.")
    if not (args.percurso_concluido and args.aceite):
        parser.error("É necessário concluir o percurso e obter aceitação antes de criar o ficheiro.")
    try:
        evento = gerar_evento(args.quando)
        with args.saida.open("xb") as stream:
            stream.write(evento.encode("utf-8"))
    except (ValueError, OSError) as exc:
        parser.exit(1, f"Ficheiro não criado: {exc}\n")
    print("Ficheiro criado:", args.saida.resolve())
    print("É necessário importá-lo no calendário. Não foi criado nenhum agendamento ativo.")


if __name__ == "__main__":
    main()
