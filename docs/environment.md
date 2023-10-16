# Variáveis de ambiente

Documentação sobre as variáveis de ambiente do bot `antaeus`.

[Voltar para o README](https://github.com/fnunezzz/antaeus)

As variáveis de ambiente abaixo pode ser informadas utilizando um arquivo `.env`.

<div align="center">

|       Variável       |                  Descrição                   | Obrigatório |
| :------------------: | :------------------------------------------: | :---------: |
|      GITLAB_URL      |               A url do GitLab                |      x      |
|        TOKEN         |           Token de usuário do Bot            |      x      |
|        LABELS        |          Labels que serão validadas          |             |
| OLD_ISSUE_TIME_DELTA |     Delta em semanas para issues antigas     |             |
| OLD_ISSUE_OLD_LABELS | Labels a serem removidas das issues antigas  |             |
| OLD_ISSUE_NEW_LABELS | Labels a serem adicionada nas issues antigas |             |

</div>

## GITLAB_URL

A URL da instância do GitLab.

-   Exemplo: `localhost:8929`

## TOKEN

Token gerado para o usuário do GitLab

-   Exemplo: `glpat-XXXXXXXXXXXXXXXXX`

## LABELS

Essas são as labels a serem validadas como parte dos guidelines na abertura de uma issue. A label pode ser completa ou parcial. Caso **não** encontre uma dessas labels irá informar o usuário a incluir na issue pelo menos uma delas.

Para adicionar mais, separe por virgula.

-   Exemplo completo: `Type::bug`
-   Exemplo Parcial: `Type`

## OLD_ISSUE_TIME_DELTA

Delta em semanas para considerar uma issue como "parada". Por default são 10 semanas.

-   Exemplo: `3`

## OLD_ISSUE_OLD_LABELS

Labels de uma issue considerada antiga que serão removidas. Aceita labels completas ou parciais.

Para adicionar mais, separe por virgula.

-   Exemplo completo: `Type::bug,State::priorizado`
-   Exemplo parcial: `Type,State`

## OLD_ISSUE_NEW_LABELS

Labels de uma issue considerada antiga que serão adicionadas.

Para adicionar mais, separe por virgula.

-   Exemplo: `Type::bug,State::priorizado`
