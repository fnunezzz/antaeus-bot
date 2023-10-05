import gitlab
from enum import Enum
import os
from dotenv import load_dotenv
# TODO criar interface HTTP para o webhook

load_dotenv()

TOKEN = os.environ['TOKEN']
GITLAB_URL = os.environ['GITLAB_URL']
GROUPS = os.environ['GROUPS']
MATCH_LABELS = os.environ['MATCH_LABELS'].split(',')


class IssueState(Enum):
    OPEN = 'opened'
    CLOSED = 'closed'


def issue_description_guideline(issue):
    '''
    Recebe uma issue

    Efetua as validações de descrição na issue informada. 

    Caso não respeite as regras de descrição efetua um comentário informando ao usuário.
    '''
    if issue.description is not None and len(issue.description) > 15:
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
    text = ''
    for label in MATCH_LABELS:
        if any(label in s for s in issue.labels):
            continue
        text += f'`{label}` '

    note = issue.notes.create(
        {'body': f''':wave: @{issue.author['username']}, adicione pelo menos uma label [{text.strip().replace(' ', ',')}]. Essas labels nos ajudam a organizar nossas issues.

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
        if note_author == BOT_NAME:
            already_commented = True
            break

    if already_commented == False:
        issue_description_guideline(issue=issue)
        issue_label_guideline(issue=issue)


def issues():
    projects = gl.projects.list(member=True)

    for project in projects:
        issues = project.issues.list(state=IssueState.OPEN.value)
        if issues is None:
            continue
        for issue in issues:
            notes(issue=issue)


def current_user():
    global BOT_NAME
    BOT_NAME = gl.user.name


def main():
    global gl
    gl = gitlab.Gitlab(url=GITLAB_URL,
                       private_token=TOKEN)
    # gl.enable_debug()
    gl.auth()
    current_user()
    issues()


if __name__ == '__main__':
    main()
