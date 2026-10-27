# Correspondência com os materiais do Escalar

Esta implementação traduz os três materiais fornecidos pelo Escalar Negócios para um projeto local com skills. O conteúdo pedagógico governa as adaptações técnicas. Os originais não são distribuídos neste repositório.

## Fontes e responsabilidade

- **Arquitetura de Receita**, PDF de 60 páginas: racional, restrições ao crescimento, mercado, escolhas de cliente/oferta, GTM e criação/retenção de valor.
- **GTM de A a Z · Escalar Negócios**, apresentação de 46 diapositivos, incluindo notas do orador: aplicação prática, ordem dos trabalhos, exercícios, critérios e saídas.
- **Agente GTM · Escalar Negócios**, documento de instruções: contrato de coaching, comandos e condução dos passos.
- Clarificações do responsável pelo projeto: precedência integral do Escalar sobre skills suplementares; simplicidade; independência da ferramenta; PT-PT por defeito; convite de agendamento apenas após a primeira conclusão; identificação do Escalar Negócios e dos seus responsáveis João Cortinhas e Vítor Brandão.

A correspondência abaixo identifica os conteúdos pedagógicos usados por etapa, com as páginas e os diapositivos relevantes.

## Racional que se mantém

Growth não é acumular atividade: começa em decisões sobre o negócio, mercado, cliente e economia. A escada de atividade, eficiência, escala, mercado e arquitetura ajuda a questionar se melhorar a atividade atual é o caminho certo. O diagnóstico antecede o investimento.

Mantêm-se os cinco tetos, o ciclo Mercado/Cliente/Oferta/Aquisição/Entrega/Expansão, as sete decisões de GTM e o resultado do canvas: um constrangimento, uma oportunidade prioritária e um resultado a 90 dias. A retenção, a expansão e a capacidade de entrega fazem parte da avaliação do crescimento. Não basta adquirir clientes ou aumentar faturação; interessa a margem, a caixa e a capacidade de crescer sem aumentar recursos na mesma proporção.

Os casos Swonkie, Swonkie.dev e Education Growth Loop ilustram esse raciocínio. Não são prescrições, pressupostos de preço, taxas ou resultados garantidos para outros negócios. O loop de educação é uma possibilidade do canal Educação, não um novo exercício obrigatório. Não se publicam aqui os números empresariais dos casos originais.

## Ordem e correspondência

| Etapa preservada | PDF: páginas | PowerPoint: diapositivos e notas | Agente original | Implementação |
|---|---|---|---|---|
| Papel, regras e âmbito | 13–21, 58–59 | 2–9 | Quem és; Regras; Comandos | `skills/escalar-gtm/SKILL.md` |
| COMEÇAR: oportunidade e hipótese de teste | 18, 58 | 10–11 | Arranque | `references/01-diagnosticar.md` |
| 0 · Um teto principal; 3 dados; refutação | 17–19 | 12–14 | PASSO 0 | `references/01-diagnosticar.md` |
| 1 · Mercado de baixo para cima; TAM/SAM/SOM | 22–30 | 16–17 | PASSO 1 | `references/02-escolher.md` |
| 2 · Dez melhores clientes; ICP e ANTI-ICP | 31–40 | 18–19 | PASSO 2 | `references/02-escolher.md` |
| 3 · Três dores; seis peças; escada com preços | 34, 37, 41 | 20–22 | PASSO 3 | `references/02-escolher.md` |
| 4 · Alternativas, frase e teste com 5 clientes | 37–41 | 23–25 | PASSO 4 | `references/02-escolher.md` |
| 5 · Mapa de canais, quatro pontuações, A/B/C | 42–44 | 27–30 | PASSO 5 | `references/03-desenhar.md` |
| 6 · PLG/SLG/Híbrido e jornada em seis etapas | 21, 43, 46 | 31–32 | PASSO 6 | `references/03-desenhar.md` |
| 7 · CAC, contribuição, payback, CAC máximo | 9, 47, 49–53 | 33–34 | PASSO 7 | `references/03-desenhar.md` |
| 8 · Meta, funil invertido e viabilidade | 30, 58 | 36–38 | PASSO 8 | `references/04-executar.md` |
| 9 · Seis blocos, decisão S6 e balanço S13 | 58 | 39–41 | PASSO 9 | `references/04-executar.md` |
| 10 · Ritual e painel; cadência semanal/mensal | 21, 49, 56 | 42 | PASSO 10 | `references/04-executar.md` |
| Fecho: One-Pager, desafio e compromisso 48h | 48, 58–59 | 43–46 | Fecho | `references/04-executar.md` |
| Revisões e decisão da semana 6 | 21, 49 | 39, 41–46 | REVISÃO SEMANAL | `references/05-acompanhar.md` |

Os caminhos `references/` na tabela são relativos a `skills/escalar-gtm/`.

## Decisões de adaptação explícitas

- **Hipóteses não bloqueiam o trabalho:** a saída de cada passo precisa de ser escrita e confirmada; não precisa de fingir que todos os dados já foram validados. As H importantes entram no plano.
- **PASSO n:** conserva a navegação por número dos slides. Consultar um passo posterior é permitido; fechar decisões respeita os anteriores. Isto concilia os comandos com «não saltes passos» e a confirmação exigida pelo agente.
- **Total da dor:** explicita-se frequência + urgência, correspondente ao «maior total» do exercício; não se introduz outra ponderação.
- **SOM:** mantém horizonte explícito de 12–36 meses como referência das notas. A meta de 90 dias e o volume de contas alcançáveis são calculados à parte.
- **Meta:** pode ser ajustada na verificação de viabilidade antes de aceite; depois mantém-se e ajustam-se táticas. Uma revisão expressamente pedida fica versionada e fundamentada.
- **Trabalho em trios:** conserva-se na utilização em grupo. No uso individual, o agente coloca as três perguntas de desafio sem fingir participantes ou validação por pares.
- **Instalação:** o projeto local e os registos substituem a instalação manual num projeto Claude/ChatGPT descrita no slide 7. Não mudam o percurso pedagógico.
- **Agendamento:** é um convite opcional após arranque, passos 0–10 e fecho confirmados. O checkpoint refere-se à semana 6 do plano. Uma proposta de fim da semana 6 usa início + 41 dias, sujeita à confirmação de data/hora/fuso. Não existe notificação automática por defeito.
- **Skills suplementares:** são adaptações curtas em PT-PT. Retiram-se top-down obrigatório, outras taxonomias de motion/jornada, outros checklists de oferta, novas pontuações e novos planos que concorram com o Escalar. Não é necessário carregar todas.

## Critério de aceitação

Uma melhoria não deve passar se alterar a ordem dos trabalhos, transformar o exercício num plano genérico de marketing, introduzir obrigações de uma skill externa ou atribuir ao Escalar uma opinião que vem de outra fonte. Mudanças ao método precisam de decisão explícita do responsável; alterações técnicas devem conservar esta correspondência.
