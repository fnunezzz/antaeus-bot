import gitlab
import threading
from enum import Enum
import os
from dotenv import load_dotenv
from flask import Flask, request, Response

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
        {'body': f''':wave: @{issue.author['username']}, adicione pelo menos uma label [{text.strip().replace(' ', ',')}]. Essas labels nos ajudam a manter nossos projetos organizados.

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


def process_all_issues():
    print('bbbb')
    projects = gl.projects.list(member=True)

    def projects_async():
        for project in projects:
            issues = project.issues.list(state=IssueState.OPEN.value)
            if issues is None:
                continue
            for issue in issues:
                threading.Thread(target=notes, args=(issue,)).start()
    threading.Thread(target=projects_async).start()


def current_user():
    global BOT_NAME
    BOT_NAME = gl.user.name


app = Flask(__name__)
gl = gitlab.Gitlab(url=GITLAB_URL,
                   private_token=TOKEN)
# gl.enable_debug()
gl.auth()
current_user()


@app.route("/full-scan", methods=['POST'])
def full_scan():
    response = Response('Running full scan')

    def webhook_async():
        process_all_issues()
    threading.Thread(target=webhook_async).start()
    return response


@app.route("/webhook/issue", methods=['POST', 'PUT', 'GET', 'OPTIONS'])
def webhook_issue():
    response = Response('Running issue webhook')

    def webhook_async(req):
        projects = gl.projects.get(req['project']['id'], lazy=True)
        issue = projects.issues.get(
            req['object_attributes']['id'])
        notes(issue=issue)

    threading.Thread(target=webhook_async, args=(request.json,)).start()
    return response


if __name__ == '__main__':
    app.run()
