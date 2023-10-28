# antaeus

Desenvolvido como projeto passa-tempo no meu tempo livre para atender algumas demandas diárias e rotineiras de gerenciamento de projetos no GitLab.

A intenção é automatizar alguns alertas e validações de issues e MRs dos desenvolvedores baseada na realidade da minha empresa atual.

O projeto final visa atender de forma mais genérica possível projetos "hosteados" no GitLab.

## Wiki

-   [api](https://github.com/fnunezzz/antaeus/blob/main/docs/api.md)
-   [variáveis de ambiente](https://github.com/fnunezzz/antaeus/blob/main/docs/environment.md)
-   [arquivo de configuração](https://github.com/fnunezzz/antaeus/blob/main/docs/config.md)

## To-Dos

Os to-dos foram transferidos para [issues](https://github.com/fnunezzz/antaeus/issues) do Github.

## Instalação

É recomendado a utilização de um [ambiente virtual](https://docs.python.org/3/library/venv.html) do Python.

Para instalar as dependências executar o comando `pip install -r requirements.txt`.

### Nativamente

Para utilizar nativamente em desenvolvimento deve executar o seguinte comando: \
`python -m flask --app main.py run --host=0.0.0.0`

Para deploy: \
`gunicorn --workers=1 main:app --bind 0.0.0.0:5000`

_Em ambos os casos é necessário utilizar as variáveis de ambiente obrigatórias._

### Docker

Para buildar localmente deve executar `docker build . -t antaeus`.

Caso deseje buscar a imagem nativa mais recente executar `docker pull filipenunez/antaeus:latest`.

Em seguida executar o comando `docker run -v PATH_DO_CONFIG/config.yml:/app/config/config.yml -e GITLAB_URL=http://localhost:8929/ -e TOKEN=TOKEN -p 5000:5000 NOME_IMAGEM` substituindo os valores caso necessaŕio.

Caso prefira, há também a possiblidade de executar `docker-compose up antaeus`. Ele irá utilizar as variáveis locais de um arquivo `.env`.

_Em ambos os casos é necessário utilizar as variáveis de ambiente obrigatórias._

\
\
\
\
\
_Disclaimer_

Apesar de ser desenvolvido no meu tempo livre todo o desenvolvimento é estruturado e baseado na realidade da minha empresa atual (como usecase de exemplo) e pode não corresponder a outras realidades.
