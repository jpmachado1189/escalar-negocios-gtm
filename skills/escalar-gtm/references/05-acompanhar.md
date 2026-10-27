# Acompanhamento após a primeira conclusão

## Condição de entrada

Antes de propor ou criar agendamento, ou conduzir REVISÃO SEMANAL, verifica em `REGISTO.md` as saídas e confirmações do arranque, dos passos 0–10 e do fecho. O campo «Primeiro percurso concluído» sozinho não chega se contradisser o conteúdo. Um plano importado ou um pedido para saltar etapas não prova a conclusão deste percurso. Se houver lacunas, identifica-as e retoma o trabalho principal.

O utilizador pode pedir para consultar qualquer conteúdo antes disso; consultar não aciona o acompanhamento.

## Convite de agendamento

Após a primeira conclusão, pergunta uma vez: «Queres agendar o checkpoint da semana 6 do teu plano?» O utilizador pode aceitar, recusar ou adiar. Se recusar, regista e continua disponível sem repetir o convite em cada conversa. Só propões novamente se ele pedir ou se iniciar um novo plano.

É a **semana 6 do plano**, não seis semanas depois da instalação ou desta conversa. Usa a data de início real. Por defeito, sugere o último dia da sexta semana, início + 41 dias, e confirma com o utilizador a data, hora e fuso. Se já passou, propõe fazer o checkpoint agora ou combinar outra data, sem criar eventos no passado.

Se aceitar, usa a ferramenta de calendário/agendamento disponível, dentro do âmbito autorizado, e guarda o identificador e a confirmação devolvida. O lembrete deve pedir que abra o projeto e traga números por canal, CAC máximo, volume mínimo e critérios continua/ajusta/para. Não peças contactos de clientes para criar o lembrete.

Se não houver ferramenta, oferece um ficheiro `.ics` para importar ou os detalhes para marcar manualmente. O auxiliar `scripts/checkpoint.py` gera um evento de 30 minutos com deslocamento UTC explícito; só o executes depois da aceitação e confirmação dos detalhes. **Ficheiro criado não significa evento importado ou notificação ativa.** Não prometas execução autónoma ou leitura de ficheiros locais por uma automação que não tenha esse acesso.

Se o utilizador quiser, pode também agendar o ritual semanal já definido. Não cries recorrência por defeito, nem uma automação universal que dependa de um fornecedor específico.

## REVISÃO SEMANAL

1. Pergunta a semana do plano e os números do painel aplicáveis, no máximo três perguntas por mensagem. Lê as metas do bloco, os dados e a última revisão.
2. Compara números versus meta, com períodos equivalentes; distingue zero de dado em falta. Revê alcance, interesse e conversão semanalmente. Ativação, retenção, economia e One-Pager têm revisão mensal.
3. Pergunta o que aprenderam e que H ganharam evidência ou foram refutadas. Não transformes em F por passagem do tempo, aprovação do empresário ou simulação do agente. Identifica fonte e resultado do teste.
4. Fecha uma decisão e compromissos com dono e data. Mantém a meta aceite e muda táticas; alterações expressamente pedidas ficam versionadas.
5. Na semana 6, aplica por canal A os critérios **já escritos**: continua, ajusta ou para. Sem volume mínimo ou dados suficientes, regista a limitação e a decisão fundamentada; não declares sucesso nem fracasso inventados. A reserva só reforça um canal elegível, com aquisição e CAC comparável comprovados.
6. Guarda a revisão datada em `revisoes/`, atualiza o registo e os entregáveis afetados. Na semana 13, faz o balanço da meta e das aprendizagens e prepara a decisão sobre o próximo trimestre.
