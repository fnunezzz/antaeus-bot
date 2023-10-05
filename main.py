import gitlab
from enum import Enum
import os
from dotenv import load_dotenv
# TODO criar interface HTTP para o webhook

load_dotenv()

TOKEN = os.environ['TOKEN']
GITLAB_URL = os.environ['GITLAB_URL']
GROUPS = os.environ['GROUPS']
MATCH_LABELS = os.environ['MATCH_LABELS']


class IssueState(Enum):
    OPEN = 'opened'
    CLOSED = 'closed'


def issue_description_guideline(issue):
    '''
    Recebe uma issue

    Efetua as validações de descrição na issue informada. 

    Caso não respeite as regras de descrição efetua um comentário informando ao usuário.
    '''
    if issue.description is not None:
        return
    note = issue.notes.create(
        {'body': f''':wave: @{issue.author['username']}, vi aqui que faltaram algumas informações nessa issue. Segue o nosso guia:

- O conteúdo da issue não deve ser vazio
- Coloque o minímo de informação possível para que possamos atuar no problema/melhoria

*Essa mensagem foi gerada automaticamente*'''})
    note.save()


def issue_label_guideline(issue):
    '''
    Recebe uma issue

    Efetua as validações de label na issue informada. 

    Caso não respeite as regras de labels informadas efetua um comentário informando ao usuário as labels faltantes.
    '''
    # TODO criar labels como parametros dinâmicos configuraveis
    text = ''
    type_label = False
    system_label = False
    squad_label = False
    for l in issue.labels:
        if 'type::' in l:
            type_label = True
        if 'system::' in l:
            system_label = True
        if 'squad::' in l:
            squad_label = True
    if type_label == False:
        text += '`type::` '
    if system_label == False:
        text += '`squad::` '
    if squad_label == False:
        text += '`squad::`'
    if text == '':
        return

    note = issue.notes.create(
        {'body': f''':wave: @{issue.author['username']}, adicione pelo menos uma label [{text}]. Essas labels nos ajudam a organizar nossas issues.

Se você tiver dúvida de quais labels colocar fale com seu líder técnico, ele com certeza lhe ajudará!

*Essa mensagem foi gerada automaticamente*'''})
    note.save()


def notes(issue):
    '''
    Recebe uma issue

    Passos:
    - valida se já foi comentado pelo bot 
        - caso já comentado efetua as validações necessárias e comenta baseado no que falta

    Guidelines:
    - Issue deve possuir conteúdo
    - Issue deve ter X labels
    '''
    already_commented = False
    i_notes = issue.notes.list()
    for note in i_notes:
        note_author = note.author['name']
        if note_author == 'Antaeus-bot':
            already_commented = True
            break

    if already_commented == False:
        issue_description_guideline(issue=issue)
        issue_label_guideline(issue=issue)


def issues():
    groups = gl.groups.list()

    for group in groups:
        if group.name.upper() not in GROUPS.upper():
            continue
        projects = group.projects.list(include_subgroups=True)
        for project in projects:
            issues = project.issues.list(state=IssueState.OPEN.value)
            for issue in issues:
                notes(issue=issue)


def main():
    global gl
    gl = gitlab.Gitlab(url=GITLAB_URL,
                       private_token=TOKEN)
    # gl.enable_debug()
    gl.auth()
    issues()


if __name__ == '__main__':
    main()
