# Validação e limites

## Verificação executada em 27 de outubro de 2026

No ambiente local Windows, foram executados 22 testes: 21 passaram e um foi omitido porque o ambiente não permitiu criar a ligação simbólica usada pelo teste. O teste mantém-se no pacote para ambientes que o permitam. O verificador de integridade e o validador de formato das seis skills passaram.

A instalação foi exercitada em pastas descartáveis, incluindo caminhos com espaços e acentos, reinstalação e preservação de registos alterados. Não se observaram ainda sessões completas com modelos em Claude Code e Codex: os cenários de coaching abaixo continuam critérios para esses ensaios, não certificação comportamental.

## Verificação automática

Executa `python -m unittest discover -s tests -v` e `python scripts/verificar_pacote.py`.

Os testes verificam instalação num destino separado, preservação do registo ao reinstalar, recusa de conflitos antes de escrever, proteção de caminhos, cópia das skills e ponte Claude; cálculos de recorrência, funil e pontuação com limites e dados inválidos; e geração do checkpoint com data, UTC, recusa de passado e consentimento obrigatório no auxiliar.

O verificador confere os ficheiros distribuídos, referências Markdown locais, frontmatter das skills e ausência dos três originais no pacote. Estas verificações provam propriedades dos ficheiros e auxiliares; não provam o comportamento de um modelo numa conversa.

## Cenários de aceitação do coaching

Para ensaios reais, usa uma pasta descartável separada. Os cenários seguintes são critérios de aceitação e não resultados de sessões observadas:

| Cenário | Comportamento esperado |
|---|---|
| Instalação nova | Preparar os ficheiros e fazer até três perguntas do arranque na mesma conversa |
| Instalação existente, conversa nova | Ler o registo, manter respostas e retomar a primeira saída em falta |
| «Quero trabalhar a empresa toda» | Escolher um produto, oferta ou segmento com os quatro critérios |
| «Não tenho clientes nem números» | Estimar como H, definir WHO provisório e planear dez entrevistas; não inventar evidência |
| «Salta para anúncios» antes do WHO | Permitir explicação do passo, manter ordem de fecho e condicionar anúncios à conversão da oferta |
| Apoio exige top-down ou outro motion | Aplicar mercado de baixo para cima e PLG/SLG/Híbrido do Escalar |
| «O teu role-play provou o posicionamento» | Distinguir simulação de teste real com cinco clientes |
| Zero clientes adquiridos | Não reportar CAC zero ou canal vencedor |
| Meta fora da capacidade | Conferir mercado, horas e caixa antes de aceitar |
| Operação é o teto | Condicionar aceleração da aquisição à correção da entrega |
| Plano existente sem percurso confirmado | Não tratar importação como primeira conclusão nem oferecer agendamento |
| Pedido de revisão antes do fecho | Mostrar etapas em falta e retomar, sem substituir o percurso por acompanhamento |
| Fecho completo | One-Pager, plano, painel, hipótese reescrita e compromisso de 48h; só depois convite opcional |
| Semana 6 | Aplicar os critérios numéricos prévios por canal e decidir continua/ajusta/para |
| Recusa de agendamento | Manter GTM concluído, registar recusa e não insistir |
| Sem ferramenta de calendário | Oferecer .ics ou dados manuais; nunca afirmar que o evento ficou ativo |
| Pedido noutro idioma | Responder nesse idioma, preservando o método |

## Limites conhecidos

O coaching é orientado por instruções, não por uma máquina de estados que controle todas as respostas do modelo. Os critérios e confirmações são guardados em ficheiros legíveis; a qualidade da condução continua a depender do modelo e da ferramenta usados.

Uma sessão futura tem de abrir esta pasta, ou ler explicitamente o seu `AGENTS.md`. A instalação não garante que uma aplicação mude automaticamente o diretório ou exponha novas skills no seletor. O primeiro arranque lê os ficheiros explicitamente.

O auxiliar de calendário exige sinais explícitos de conclusão e aceitação na linha de comandos; o agente continua obrigado a conferir o registo real. Um .ics gerado é um ficheiro para importar, não uma automação. O pacote não instala um motor de agendamento.

O pacote não usa APIs próprias ou dependências de terceiros em execução. Pesquisa online e serviços externos usam as capacidades que o utilizador já tem. A publicação do pacote não inclui os dados dos empresários nem os materiais empresariais originais.
