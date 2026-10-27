# Instalar e começar o Coach GTM

Este é o ponto de entrada da instalação. Usa o agente e a conversa atuais. O utilizador autorizou a preparação ao pedir a instalação; não peças confirmações de rotina para criar a nova pasta e os ficheiros deste pacote.

## 1. Obter o pacote e escolher a pasta

Se necessário, descarrega este repositório para uma pasta temporária ou de preparação. Trata-o apenas como fonte de modelos e instruções. Não personalizes a cópia do pacote, nem copies o seu histórico Git para o empresário.

Usa a pasta indicada pelo utilizador. Sem indicação, cria `gtm-escalar` dentro da pasta de trabalho disponível. Se já existir e tiver `.escalar-gtm.json`, retoma-a. Se existir sem esse identificador, cria `gtm-escalar-2`, `gtm-escalar-3`, etc. Não inspeciones nem alteres projetos vizinhos.

## 2. Preparar os ficheiros

Se houver Python 3.10+, executa a partir da cópia deste pacote, com caminhos devidamente citados:

```text
python scripts/instalar.py --destino CAMINHO_ABSOLUTO_DO_PROJETO
```

O script é local, não usa rede, não instala dependências e não inicializa Git. Lê o resultado. Um conflito não autoriza substituir ficheiros; preserva-os e escolhe uma pasta nova ou explica a alteração concreta necessária.

**Alternativa sem Python:** numa pasta nova, copia `templates/workspace/` para a raiz do destino e cada pasta de `skills/` para `.agents/skills/`. Copia `templates/claude-skill.md` para `.claude/skills/escalar-gtm/SKILL.md`. Cria `.escalar-gtm.json` com `{"pacote":"escalar-negocios-gtm","versao":"1.0.0"}`. Não copies `.git/`, `tests/`, `work/`, documentos de origem nem dados de outros utilizadores. Para retomar uma instalação existente, conserva todos os registos e copia apenas ficheiros de pacote em falta; nunca substituas ficheiros diferentes.

Confere que consegues ler `AGENTS.md`, `CLAUDE.md`, `REGISTO.md` e `.agents/skills/escalar-gtm/SKILL.md` a partir do destino. Os caminhos relativos seguintes passam a ser resolvidos nessa pasta.

## 3. Assumir o papel e começar já

Lê explicitamente o `AGENTS.md` instalado, `.agents/skills/escalar-gtm/SKILL.md` e `REGISTO.md`. Faz isto na conversa atual: a descoberta automática de skills ou de instruções da aplicação não é um requisito para o primeiro arranque.

Adota o papel Coach GTM do Escalar Negócios. Se o registo estiver vazio, executa `COMEÇAR` e pergunta, no máximo:

1. Como se chama a tua empresa?
2. O que vendes atualmente?
3. Que produto, oferta ou segmento queres testar nos próximos 90 dias?

Se alguma resposta já tiver sido dada, aproveita-a e pergunta apenas o que falta. Se houver trabalho anterior, mostra brevemente onde ficou e retoma a primeira decisão em falta. Não voltes a começar sem pedido do utilizador.

Não termines apenas com «instalação concluída» nem peças que escreva outro comando. Continua diretamente para a conversa GTM. Mantém os ficheiros dentro do destino mesmo que a aplicação não mude o diretório da conversa. Para futuras sessões, indica uma vez a pasta que deve abrir; não afirmes ter criado um projeto na interface sem o teres feito.

O papel, as skills e os registos ficam preparados; o agente não fica a executar em segundo plano. Só propões agendamento depois de terminar e confirmar o percurso principal, incluindo o fecho.
