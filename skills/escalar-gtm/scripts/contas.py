"""Contas didáticas do GTM Escalar. Não fornece dados nem confirma decisões."""

from __future__ import annotations

import argparse
from decimal import Decimal, InvalidOperation, ROUND_CEILING
import json


def numero(valor: object, nome: str, minimo: Decimal | None = Decimal(0), maximo: Decimal | None = None) -> Decimal:
    try:
        if isinstance(valor, bool):
            raise ValueError
        n = Decimal(str(valor).replace(",", "."))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"{nome}: indica um número válido.") from exc
    if not n.is_finite() or (minimo is not None and n < minimo) or (maximo is not None and n > maximo):
        raise ValueError(f"{nome}: valor fora do intervalo permitido.")
    return n


def percentagem(valor: object, nome: str) -> Decimal:
    return numero(valor, nome, maximo=Decimal(100)) / 100


def inteiro_positivo(valor: object, nome: str) -> int:
    n = numero(valor, nome, Decimal(1))
    if n != n.to_integral_value():
        raise ValueError(f"{nome}: indica um número inteiro.")
    return int(n)


def economia(receita_mensal: object, margem_pct: object, payback_alvo: object,
             custo_aquisicao: object | None = None, novos_clientes: object | None = None) -> dict[str, object]:
    receita = numero(receita_mensal, "Receita mensal")
    margem = numero(margem_pct, "Margem bruta (%)", minimo=None, maximo=Decimal(100)) / 100
    alvo = numero(payback_alvo, "Payback alvo", Decimal("0.000001"))
    contribuicao = receita * margem
    resultado: dict[str, object] = {
        "contribuicao_mensal_eur": str(contribuicao),
        "cac_maximo_eur": str(max(Decimal(0), contribuicao * alvo)),
        "cac_eur": None,
        "payback_meses": None,
        "nota": "Aproximação didática. Avalia também churn, recebimentos e caixa; resultados não validam hipóteses.",
    }
    if (custo_aquisicao is None) != (novos_clientes is None):
        raise ValueError("Para calcular CAC, indica custos e novos clientes do mesmo período.")
    if custo_aquisicao is not None:
        custo = numero(custo_aquisicao, "Custos de aquisição")
        clientes = numero(novos_clientes, "Novos clientes")
        if clientes != clientes.to_integral_value():
            raise ValueError("Novos clientes: indica um número inteiro.")
        if clientes == 0:
            resultado["nota"] = "Sem novos clientes, CAC e payback não são calculáveis; CAC não é zero."
        else:
            cac = custo / clientes
            resultado["cac_eur"] = str(cac)
            if contribuicao > 0:
                resultado["payback_meses"] = str(cac / contribuicao)
            else:
                resultado["nota"] = "Sem contribuição mensal positiva, não há payback finito nesta aproximação."
    return resultado


def funil(meta: object, receita_por_cliente: object, fecho_pct: object,
          oportunidade_pct: object, semanas: object) -> dict[str, int]:
    objetivo = numero(meta, "Meta", Decimal("0.000001"))
    ticket = numero(receita_por_cliente, "Receita por cliente", Decimal("0.000001"))
    fecho = percentagem(fecho_pct, "Fecho (%)")
    conversao = percentagem(oportunidade_pct, "Conversão em oportunidade (%)")
    n_semanas = inteiro_positivo(semanas, "Semanas de execução")
    if fecho == 0 or conversao == 0:
        raise ValueError("Taxas zero não permitem atingir a meta neste funil.")
    ceil = lambda x: int(x.to_integral_value(rounding=ROUND_CEILING))
    clientes = ceil(objetivo / ticket)
    oportunidades = ceil(Decimal(clientes) / fecho)
    contas = ceil(Decimal(oportunidades) / conversao)
    return {"clientes": clientes, "oportunidades": oportunidades, "contas": contas,
            "contas_por_semana": ceil(Decimal(contas) / n_semanas)}


def canais(pontos: list[object]) -> dict[str, object]:
    if len(pontos) != 4:
        raise ValueError("São necessárias as quatro pontuações do Escalar.")
    valores = [inteiro_positivo(p, "Pontuação") for p in pontos]
    if any(p > 5 for p in valores):
        raise ValueError("As pontuações vão de 1 a 5.")
    total = sum(valores)
    return {"total": total, "prioridade": "A" if total >= 16 else "B" if total >= 11 else "C"}


def main() -> None:
    parser = argparse.ArgumentParser(description="Contas Escalar; percentagens em 0–100, valores na mesma moeda/base.")
    sub = parser.add_subparsers(dest="operacao", required=True)
    eco = sub.add_parser("economia", help="Receita mensal, margem e CAC/payback aproximados")
    eco.add_argument("--receita-mensal", required=True)
    eco.add_argument("--margem-pct", required=True)
    eco.add_argument("--payback-alvo", required=True)
    eco.add_argument("--custo-aquisicao")
    eco.add_argument("--novos-clientes")
    fun = sub.add_parser("funil", help="Meta e receita por cliente devem usar a mesma base temporal")
    for nome in ("meta", "receita-por-cliente", "fecho-pct", "oportunidade-pct", "semanas"):
        fun.add_argument("--" + nome, required=True)
    canal = sub.add_parser("canais", help="Quatro pontuações, 1–5")
    canal.add_argument("pontos", nargs=4)
    args = vars(parser.parse_args())
    operacao = args.pop("operacao")
    try:
        resultado = {"economia": economia, "funil": funil, "canais": canais}[operacao](**args)
    except ValueError as exc:
        parser.exit(1, f"Não foi possível calcular: {exc}\n")
    print(json.dumps(resultado, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
