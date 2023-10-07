# antaeus

Desenvolvido como projeto passa-tempo no meu tempo livre para atender algumas demandas diárias e rotineiras de gerenciamento de projetos no GitLab.

A intenção é automatizar alguns alertas e validações de issues e MRs dos desenvolvedores baseada na realidade da minha empresa atual.

O projeto final visa atender de forma mais genérica possível projetos "hosteados" no GitLab.

## To-Dos

-   [x] Interface Http para Webhooks do GitLab
-   [x] Validar possibilidade de configurar labels para validação de forma dinâmica (env ?)
-   [ ] Análise de MRs
-   [x] Análise de issues
-   [x] Adicionar build docker
-   [x] Documentação de instalação e uso

## Instalação

Essa aplicação utiliza algumas variáveis de ambiente.

|  variável  |         descrição          | obrigatório |
| :--------: | :------------------------: | :---------: |
| GITLAB_URL |      A url do GitLab       |      x      |
|   TOKEN    |  Token de usuário do Bot   |      x      |
|   LABELS   | Labels que serão validadas |             |

O app pode também utilizar `.env` caso ele exista.

### Nativamente

Para utilizar nativamente em desenvolvimento deve executar o seguinte comando: \
`python -m flask --app main.py run --host=0.0.0.0`

Para deploy: \
`gunicorn --workers=1 main:app --bind 0.0.0.0:5000`

_Em ambos os casos é necessário utilizar as variáveis de ambiente obrigatórias._

### Docker

Para buildar localmente deve executar `docker build . -t antaeus`.

Caso deseje buscar a imagem nativa mais recente executar `docker pull filipenunez/antaeus:latest`.

Para executar executar o comando `docker run NOME_IMAGEM` substituindo NOME_IMAGEM pela tag.

_Em ambos os casos é necessário utilizar as variáveis de ambiente obrigatórias._

\
\
\
\
\
_Disclaimer_

Apesar de ser desenvolvido no meu tempo livre todo o desenvolvimento é estruturado e baseado na realidade da minha empresa atual (como usecase de exemplo) e pode não corresponder a outras realidades.
