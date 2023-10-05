import gitlab
from enum import Enum
import os
from dotenv import load_dotenv
# TODO criar interface HTTP para o webhook

load_dotenv()

TOKEN = os.environ['TOKEN']
GITLAB_URL = os.environ['GITLAB_URL']


class IssueState(Enum):
    OPEN = 'opened'
    CLOSED = 'closed'


class NoteGuidelines(Enum):
    NO_DESCRIPTION = '21419sandqwiou31'


def issueDescriptionGuideline(issue):
    if issue.description is not None:
        return
    note = issue.notes.create(
        {'body': f''':wave: @{issue.author['username']}, vi aqui que faltaram algumas informações nessa issue. Segue o nosso guia:

- O conteúdo da issue não deve ser vazio
- Coloque o minímo de informação possível para que possamos atuar no problema/melhoria

*Essa mensagem foi gerada automaticamente*'''})
    note.save()


def issueLabelGuideline(issue):
    # TODO criar labels como parametros dinâmicos configuraveis
    text = ''
    typeLabel = False
    systemLabel = False
    squadLabel = False
    for l in issue.labels:
        if 'type::' in l:
            typeLabel = True
        if 'system::' in l:
            systemLabel = True
        if 'squad::' in l:
            squadLabel = True
    if typeLabel == False:
        text += '`type::` '
    if systemLabel == False:
        text += '`squad::` '
    if squadLabel == False:
        text += '`squad::`'
    if text == '':
        return

    note = issue.notes.create(
        {'body': f''':wave: @{issue.author['username']}, adicione pelo menos uma label [{text}]. Essas labels nos ajudam a organizar nossas issues.

Se você tiver dúvida de quais labels colocar fale com seu líder técnico, ele com certeza lhe ajudará!

*Essa mensagem foi gerada automaticamente*'''})
    note.save()


def notes(issue):
    alreadyCommented = False
    i_notes = issue.notes.list()
    for note in i_notes:
        noteAuthor = note.author['name']
        if noteAuthor == 'Antaeus-bot':
            alreadyCommented = True
            break

    if alreadyCommented == False:
        issueDescriptionGuideline(issue=issue)
        issueLabelGuideline(issue=issue)


def issues():
    # projects = gl.projects.list(iterator=True)

    project = gl.projects.get(653)
    print(project.id, project.name)
    # for project in projects:
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
