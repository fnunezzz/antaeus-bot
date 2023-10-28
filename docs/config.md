# Arquivo de configuração

Documentação sobre o arquivo de configuração `.yml`.

[Voltar para o README](https://github.com/fnunezzz/antaeus)

Essa aplicação utiliza um arquivo `.yml` de configuração de regras.

-   [Arquivo de configuração](#arquivo-de-configuração)
    -   [Issues](#issues)
        -   [Campos](#campos)
            -   [name](#name)
            -   [conditions](#conditions)
                -   [description-conditions](#description-conditions)
                -   [labels-conditions](#labels-conditions)
                -   [date-conditions](#date-conditions)
            -   [actions](#actions)
                -   [labels-action](#labels-action)
                -   [comment-action](#comment-action)

## Issues

Exemplo:

```yml
issues:
    rules:
        - name: Guideline de abertura (conteudo)
          conditions:
              description:
                  length: 25
          actions:
              comment: |
                  :wave: @{{author}}, vi aqui que faltaram algumas informações nessa issue. Segue o nosso guia:

                  - O conteúdo da issue não deve ser vazio
                  - Coloque o minímo de informação possível para que possamos atuar no problema/melhoria

                  Essas ações nos permitem manter uma estrutura organizada e informativa de tudo que acontece nas nossas aplicações.

                  *Essa mensagem foi gerada automaticamente*
        - name: Guideline de abertura (labels)
          conditions:
              labels:
                  must:
                      - state
                      - type
                      - squad
          actions:
              comment: |
                  :wave: @{{author}}, adicione pelo menos uma label {{labels}}. Essas labels nos ajudam a manter nossos projetos organizados e categorizados corretamente para atuação.

                  Se você tiver dúvida de quais labels colocar fale com seu líder técnico, ele com certeza lhe ajudará!

                  *Essa mensagem foi gerada automaticamente*
        - name: Guideline de inatividade
          conditions:
              date:
                  attribute: updated_at
                  condition: older_than
                  interval_type: weeks
                  interval: 3
          actions:
              labels:
                  remove: state
              comment: |
                  :wave: {{author}} essa issue está parada a mais de {{interval}} {{interval_type}}.

                  Label de `state` alterada para ~"state::pendente-analise"

                  /label ~"state::priorizado"

                  *Essa mensagem foi gerada automaticamente*
```

### Campos

#### name

Nome da regra.

#### conditions

Grupo de condições a serem validadas para efetuar o comentário.

##### description-conditions

| Condition |      Descrição       | Valores |
| :-------: | :------------------: | :-----: |
|  length   | Tamanha da descrição | Integer |

##### labels-conditions

| Condition |                   Descrição                    | Valores |
| :-------: | :--------------------------------------------: | :-----: |
|   must    | Labels que devem existir (parcial ou completo) | String  |

##### date-conditions

|   Condition   |        Descrição        |        Valores         |
| :-----------: | :---------------------: | :--------------------: |
|   attribute   | Atributo a ser validado | updated_at, created_at |
|   condition   |    Tipo de validação    |       older_than       |
| interval_type |    Tipo de intervalo    |  weeks, days, months   |
|   interval    |   Intervalo de tempo    |        Integer         |

#### actions

Labels a serem modificadas na issue.

##### labels-action

| Condition |           Descrição            | Valores |
| :-------: | :----------------------------: | :-----: |
|  remove   | Labels que devem ser removidas | String  |

##### comment-action

Comentário que deve ser feito caso as regras de validação estejam de acordo.

|   Variáveis   |             Descrição             |
| :-----------: | :-------------------------------: |
|    author     |          Autor da issue           |
|    labels     |  Labels da condição labels->must  |
|   interval    |   Interval da condição de date    |
| interval_type | Interval_type da condição de date |
