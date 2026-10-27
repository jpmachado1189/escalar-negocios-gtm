"""Verificações executáveis dos auxiliares; não simulam validação do modelo."""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

RAIZ = Path(__file__).resolve().parents[1]


def carregar(nome: str, relativo: str):
    spec = importlib.util.spec_from_file_location(nome, RAIZ / relativo)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


instalador = carregar("instalador", "scripts/instalar.py")
contas = carregar("contas", "skills/escalar-gtm/scripts/contas.py")
calendario = carregar("calendario", "skills/escalar-gtm/scripts/checkpoint.py")
verificador = carregar("verificador", "scripts/verificar_pacote.py")


class Instalacao(unittest.TestCase):
    def setUp(self):
        self.temporaria = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporaria.cleanup)
        self.base = Path(self.temporaria.name)
        self.destino = self.base / "projeto com espaços e acentos á"

    def test_instala_skill_ponte_e_registo(self):
        resultado = instalador.instalar(self.destino)
        self.assertGreater(resultado["ficheiros_criados"], 10)
        self.assertEqual((self.destino / ".agents/skills/escalar-gtm/SKILL.md").read_bytes(), (RAIZ / "skills/escalar-gtm/SKILL.md").read_bytes())
        self.assertTrue((self.destino / ".claude/skills/escalar-gtm/SKILL.md").is_file())
        self.assertTrue((self.destino / "REGISTO.md").is_file())
        self.assertFalse((self.destino / ".git").exists())

    def test_reinstalacao_preserva_dados_e_registo(self):
        instalador.instalar(self.destino)
        registo = self.destino / "REGISTO.md"
        registo.write_text("# Decisões reais\nWHO confirmado pelo empresário\n", encoding="utf-8")
        (self.destino / "dados/clientes.txt").write_text("dados privados", encoding="utf-8")
        resultado = instalador.instalar(self.destino)
        self.assertEqual(resultado["ficheiros_criados"], 0)
        self.assertIn("Decisões reais", registo.read_text(encoding="utf-8"))
        self.assertEqual((self.destino / "dados/clientes.txt").read_text(encoding="utf-8"), "dados privados")

    def test_recusa_pasta_nao_identificada(self):
        self.destino.mkdir()
        (self.destino / "AGENTS.md").write_text("instruções anteriores", encoding="utf-8")
        with self.assertRaises(ValueError):
            instalador.instalar(self.destino)
        self.assertFalse((self.destino / ".escalar-gtm.json").exists())

    def test_conflito_nao_repara_antes_de_conferir_tudo(self):
        instalador.instalar(self.destino)
        (self.destino / "CLAUDE.md").unlink()
        (self.destino / ".agents/skills/apoio-mercado/SKILL.md").write_text("alterado pelo utilizador", encoding="utf-8")
        with self.assertRaises(ValueError):
            instalador.instalar(self.destino)
        self.assertFalse((self.destino / "CLAUDE.md").exists())

    def test_repara_ficheiro_de_pacote_em_falta(self):
        instalador.instalar(self.destino)
        alvo = self.destino / ".agents/skills/escalar-gtm/references/02-escolher.md"
        alvo.unlink()
        self.assertEqual(instalador.instalar(self.destino)["ficheiros_criados"], 1)
        self.assertTrue(alvo.is_file())

    def test_pai_ficheiro_nao_causa_instalacao_parcial(self):
        instalador.instalar(self.destino)
        import shutil
        pasta = self.destino / ".agents"
        # O alvo foi criado pelo teste e está dentro da sua pasta temporária.
        self.assertTrue(pasta.resolve().is_relative_to(self.base.resolve()))
        shutil.rmtree(pasta)
        pasta.write_text("ficheiro do utilizador", encoding="utf-8")
        (self.destino / "CLAUDE.md").unlink()
        with self.assertRaises(ValueError):
            instalador.instalar(self.destino)
        self.assertFalse((self.destino / "CLAUDE.md").exists())

    def test_identificacao_versao_errada_preservada(self):
        instalador.instalar(self.destino)
        marcador = self.destino / ".escalar-gtm.json"
        marcador.write_text('{"pacote":"escalar-negocios-gtm","versao":"0.1.0"}', encoding="utf-8")
        with self.assertRaises(ValueError):
            instalador.instalar(self.destino)
        self.assertIn("0.1.0", marcador.read_text(encoding="utf-8"))

    def test_nao_personaliza_o_pacote_ou_pasta_mae(self):
        for alvo in (RAIZ, RAIZ / "projeto", RAIZ.parent):
            with self.subTest(alvo=alvo), self.assertRaises(ValueError):
                instalador.instalar(alvo)

    def test_link_para_fora_nao_e_seguido(self):
        instalador.instalar(self.destino)
        alvo = self.destino / "AGENTS.md"
        alvo.unlink()
        fora = self.base / "fora.md"
        fora.write_text("não alterar", encoding="utf-8")
        try:
            alvo.symlink_to(fora)
        except OSError:
            self.skipTest("O sistema não permite criar symlinks neste contexto.")
        with self.assertRaises(ValueError):
            instalador.instalar(self.destino)
        self.assertEqual(fora.read_text(encoding="utf-8"), "não alterar")


class Calculos(unittest.TestCase):
    def test_economia_recorrente(self):
        resultado = contas.economia("54", "70", "12", "25000", "5")
        self.assertEqual(Decimal(resultado["contribuicao_mensal_eur"]), Decimal("37.8"))
        self.assertEqual(Decimal(resultado["cac_eur"]), Decimal("5000"))
        self.assertEqual(Decimal(resultado["cac_maximo_eur"]), Decimal("453.6"))
        self.assertGreater(Decimal(resultado["payback_meses"]), 132)

    def test_zero_clientes_nao_e_cac_zero(self):
        resultado = contas.economia(100, 70, 6, 1000, 0)
        self.assertIsNone(resultado["cac_eur"])
        self.assertIsNone(resultado["payback_meses"])

    def test_zero_margem_nao_e_payback_finito(self):
        resultado = contas.economia(100, 0, 6, 1000, 2)
        self.assertEqual(Decimal(resultado["cac_maximo_eur"]), 0)
        self.assertIsNone(resultado["payback_meses"])

    def test_margem_negativa_nao_suporta_aquisicao(self):
        resultado = contas.economia(100, -20, 6, 1000, 2)
        self.assertEqual(Decimal(resultado["contribuicao_mensal_eur"]), -20)
        self.assertEqual(Decimal(resultado["cac_maximo_eur"]), 0)
        self.assertIsNone(resultado["payback_meses"])

    def test_funil_arredonda_para_nao_subdimensionar(self):
        resultado = contas.funil(10001, 1000, 30, 20, 10)
        self.assertEqual(resultado, {"clientes": 11, "oportunidades": 37, "contas": 185, "contas_por_semana": 19})
        self.assertGreaterEqual(resultado["clientes"] * 1000, 10001)
        self.assertGreaterEqual(Decimal(resultado["oportunidades"]) * Decimal("0.3"), resultado["clientes"])

    def test_pontuacoes_nos_limites(self):
        for pontos, total, prioridade in (([1, 1, 1, 1], 4, "C"), ([2, 2, 3, 3], 10, "C"), ([2, 3, 3, 3], 11, "B"), ([3, 4, 4, 4], 15, "B"), ([4, 4, 4, 4], 16, "A"), ([5, 5, 5, 5], 20, "A")):
            with self.subTest(pontos=pontos):
                self.assertEqual(contas.canais(pontos), {"total": total, "prioridade": prioridade})

    def test_entradas_invalidas(self):
        casos = [lambda: contas.economia(100, 101, 6), lambda: contas.economia(-1, 70, 6),
                 lambda: contas.economia("NaN", 70, 6), lambda: contas.economia(100, 70, 6, 10),
                 lambda: contas.economia(100, 70, 6, 10, "1.5"),
                 lambda: contas.funil(1000, 100, 0, 20, 12), lambda: contas.funil(1000, 100, 20, 101, 12),
                 lambda: contas.funil(1000, 0, 20, 20, 12), lambda: contas.funil(1000, 100, 20, 20, "1.5"),
                 lambda: contas.canais([1, 2, 3, 6]), lambda: contas.canais([1, 2, 3, "4.5"])]
        for caso in casos:
            with self.subTest(caso=caso), self.assertRaises(ValueError):
                caso()

    def test_decimal_portugues(self):
        self.assertEqual(Decimal(contas.economia("19,99", "70", "12")["contribuicao_mensal_eur"]), Decimal("13.993"))


class Calendario(unittest.TestCase):
    def test_data_refere_semana_seis_do_plano(self):
        self.assertEqual(calendario.data_semana_seis(date(2026, 10, 27)), date(2026, 12, 7))

    def test_utc_duracao_e_utf8(self):
        agora = datetime(2026, 1, 1, tzinfo=timezone.utc)
        quando = datetime.fromisoformat("2026-12-07T10:00:00+01:00")
        evento = calendario.gerar_evento(quando, agora)
        self.assertIn("DTSTART:20261207T090000Z", evento)
        self.assertIn("DTEND:20261207T093000Z", evento)
        self.assertTrue(all(len(l.encode("utf-8")) <= 75 for l in evento.split("\r\n")))
        self.assertIn("BEGIN:VEVENT", evento)

    def test_hora_sem_fuso_e_passado_recusados(self):
        agora = datetime(2026, 1, 1, tzinfo=timezone.utc)
        for quando in (datetime(2027, 1, 1), agora - timedelta(seconds=1)):
            with self.subTest(quando=quando), self.assertRaises(ValueError):
                calendario.gerar_evento(quando, agora)

    def test_cli_exige_conclusao_e_aceitacao(self):
        with tempfile.TemporaryDirectory() as temp:
            saida = Path(temp) / "checkpoint.ics"
            comando = [sys.executable, str(RAIZ / "skills/escalar-gtm/scripts/checkpoint.py"), "--quando", "2099-01-01T10:00:00+00:00", "--saida", str(saida)]
            for extra in ([], ["--percurso-concluido"], ["--aceite"]):
                resultado = subprocess.run(comando + extra, capture_output=True)
                self.assertNotEqual(resultado.returncode, 0)
                self.assertFalse(saida.exists())
            resultado = subprocess.run(comando + ["--percurso-concluido", "--aceite"], capture_output=True)
            self.assertEqual(resultado.returncode, 0, resultado.stderr)
            self.assertTrue(saida.exists())
            original = saida.read_bytes()
            resultado = subprocess.run(comando + ["--percurso-concluido", "--aceite"], capture_output=True)
            self.assertNotEqual(resultado.returncode, 0)
            self.assertEqual(saida.read_bytes(), original)


class Pacote(unittest.TestCase):
    def test_referencias_e_distribuicao(self):
        self.assertEqual(verificador.verificar(), [])


if __name__ == "__main__":
    unittest.main()
