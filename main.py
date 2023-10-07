import gitlab
import threading
import time
import sys
import os
from enum import Enum
from dotenv import load_dotenv
from flask import Flask, request, Response


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def out(message: str, color: bcolors):
    return f'{color}{message}{bcolors.ENDC}'


load_dotenv()

TOKEN = os.environ['TOKEN']
GITLAB_URL = os.environ['GITLAB_URL']
LABELS = os.environ.get('LABELS', '').split(',')

app = Flask(__name__)
gl = gitlab.Gitlab(url=GITLAB_URL,
                   private_token=TOKEN)
# gl.enable_debug()


class IssueState(Enum):
    OPEN = 'opened'
    CLOSED = 'closed'


def auth():
    try:
        gl.auth()
    except Exception:
        print(out(message='\nERROR: Erro autenticando no GitLab', color=bcolors.FAIL))
        sys.stdout.write(
            out(message='Tentando novamente... ', color=bcolors.WARNING))
        for i in range(5, 0, -1):
            sys.stdout.write(
                out(message=f'{str(i)}  ', color=bcolors.WARNING))
            sys.stdout.flush()
            time.sleep(1)
        return auth()
    else:
        print(out(message='Conectado com sucesso', color=bcolors.OKGREEN))
        current_user()


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

Essas ações nos permitem manter uma estrutura organizada e informativa de tudo que acontece nas nossas aplicações.

*Essa mensagem foi gerada automaticamente*'''})
    note.save()


def issue_label_guideline(issue):
    '''
    Recebe uma issue

    Efetua as validações de label na issue informada. 

    Caso não respeite as regras de labels informadas efetua um comentário informando ao usuário as labels faltantes.
    '''
    text = ''
    for label in LABELS:
        if any(label in s for s in issue.labels):
            continue
        text += f'`{label}` '

    note = issue.notes.create(
        {'body': f''':wave: @{issue.author['username']}, adicione pelo menos uma label [{text.strip().replace(' ', ',')}]. Essas labels nos ajudam a manter nossos projetos organizados e categorizados corretamente para atuação.

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
    projects = gl.projects.list(member=True)

    def projects_async(p):
        issues = p.issues.list(state=IssueState.OPEN.value)
        if issues is None:
            return
        for issue in issues:
            threading.Thread(target=notes, args=(issue,)).start()
    for project in projects:
        threading.Thread(target=projects_async, args=(project,)).start()


def current_user():
    global BOT_NAME
    BOT_NAME = gl.user.name


@app.route("/full-scan", methods=['POST'])
def full_scan():
    response = Response('Running full scan')

    def webhook_async():
        process_all_issues()
    threading.Thread(target=webhook_async).start()
    return response


@app.route("/webhook/issue", methods=['POST'])
def webhook_issue():
    response = Response('Running issue webhook')

    def webhook_async(req):
        try:
            projects = gl.projects.get(req['project']['id'])
        except Exception as e:
            if '404' in str(e):
                print(out(
                    message=f'{BOT_NAME} não faz parte do projeto {req["project"]["name"]}', color=bcolors.FAIL))
            else:
                print(out(message=e, color=bcolors.FAIL))
        else:
            issue = projects.issues.get(
                req['object_attributes']['iid'])
            notes(issue=issue)
    threading.Thread(target=webhook_async, args=(request.json,)).start()
    return response


if __name__ == '__main__':
    auth()
    app.run()
