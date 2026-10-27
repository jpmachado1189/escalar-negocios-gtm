# Coach GTM · Escalar Negócios

Constrói o Go-to-Market de um produto, oferta ou segmento e transforma-o num plano de 90 dias, com decisões escritas e acompanhamento semanal.

Metodologia do **Escalar Negócios**, empresa de educação empresarial de **João Cortinhas e Vítor Brandão**. Português de Portugal, salvo se pedires outro idioma.

## Começar com uma mensagem

Copia esta mensagem para o agente com acesso a ficheiros que já utilizas:

```text
Prepara o meu projeto GTM a partir de https://github.com/jpmachado1189/escalar-negocios-gtm. Lê o SETUP.md, cria o espaço de trabalho local, configura o Coach GTM do Escalar Negócios e começa logo a orientar-me, na mesma conversa.
```

O agente prepara uma pasta própria e começa por perguntar a empresa, o que vendes e o que queres testar. Se já tiveres um projeto instalado, retoma os registos existentes. Não precisas de instalar outro agente, criar uma conta nesta aplicação ou fornecer uma chave de API a este pacote. Continuas a usar a tua ferramenta e as respetivas condições de acesso.

O núcleo é composto por ficheiros Markdown. Codex e Claude Code têm instruções de entrada próprias; qualquer outro agente que consiga ler e escrever ficheiros pode seguir `AGENTS.md` e ler a skill explicitamente. A navegação na Internet e o agendamento dependem das ferramentas disponíveis. A preparação não cria, por si só, um projeto na interface da aplicação.

## O percurso

**COMEÇAR:** escolher uma oportunidade concreta e escrever a hipótese de teste.

| Bloco | Passos, por ordem |
|---|---|
| Diagnosticar | 0 · Teto de crescimento |
| Escolher | 1 · Mercado; 2 · Cliente; 3 · Dor e oferta; 4 · Posicionamento |
| Desenhar | 5 · Canais; 6 · Motion; 7 · Economia |
| Executar | 8 · Conta da meta; 9 · Plano de 90 dias; 10 · Ritual semanal |

No fecho: One-Pager, hipótese reescrita e primeira ação nas próximas 48 horas. Depois da primeira conclusão do percurso, podes escolher agendar o checkpoint da semana 6 do plano e as revisões semanais.

## Comandos

Podes falar normalmente ou escrever: `COMEÇAR`, `PASSO 0` a `PASSO 10`, `ONDE ESTOU`, `ONE-PAGER`, `PLANO` e `REVISÃO SEMANAL`.

Cada passo termina numa decisão escrita e confirmada por ti. O que ainda não foi provado fica como hipótese, com uma tarefa para validar. Pedir um passo posterior permite consultá-lo, mas não fecha os anteriores.

## O que fica no teu computador

`REGISTO.md` guarda o estado atual, as decisões e a evidência. `entregaveis/` recebe o One-Pager, o plano e o painel. `revisoes/` guarda o acompanhamento. `dados/` pode receber os materiais que queiras fornecer. Os registos do empresário não são enviados para este repositório. Como acontece com qualquer agente, o conteúdo lido fica sujeito ao tratamento de dados da ferramenta escolhida.

## Skills suplementares

Cinco apoios curtos, adaptados de material selecionado de Corey Haines e Paweł Huryn: mercado; clientes; oferta e posicionamento; canais e jornada; validação e métricas. Só são lidos quando ajudam o passo atual. **A metodologia, as opiniões e as saídas do Escalar prevalecem sempre sobre estes apoios.**

Não se instala nenhuma coleção completa. Não há outro questionário de onboarding nem outro framework obrigatório. Fontes e adaptações: [TERCEIROS.md](TERCEIROS.md).

## Para verificar ou manter o pacote

```text
python -m unittest discover -s tests -v
python scripts/verificar_pacote.py
```

Python 3.10 ou superior apenas para o instalador e os auxiliares opcionais; sem dependências externas. O agente também pode preparar os ficheiros seguindo a alternativa manual de [SETUP.md](SETUP.md).

Consulta a [correspondência com os três materiais originais](docs/FIDELIDADE.md) e os [limites da validação](docs/VALIDACAO.md). Os materiais originais e os seus casos empresariais não estão incluídos no pacote público.
