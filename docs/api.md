# API

Aqui segue uma documentação básica dos endpoints do bot `antaeus`.

[Voltar para o README](https://github.com/fnunezzz/antaeus)

## Issues

### POST `/issue/scan/full`

Efetua um scan completo em todos os projetos que o usuário dessa aplicação possui acesso. Irá verificar se já houve comentário do Bot, caso não tenha, irá verificar as regras de validações do arquivo de configuração.

-   Retorno: `200`

### POST `/issue/webhook`

Endpoint para o webhook de eventos `issue` no GitLab. Só será possível validar a issue se o usuário possuir acesso ao projeto. Irá verificar se já houve comentário do Bot, caso não tenha, irá verificar as guidelines de descrição e labels.

-   Retorno: `200`

### POST `/issue/scan/old`

Efetua a varredura de todas as issues abertas e refaz todas as regras de validações do arquivo de configuração.

-   Retorno: `200`
