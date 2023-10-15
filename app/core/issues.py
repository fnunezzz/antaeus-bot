import threading
from enum import Enum
from gitlab.v4.objects import ProjectIssue, ProjectIssueNote
import app.core.users as users
import app.core.projects as projects
import app.config.environment as config
from app.core.gitlab import gl
from app.common.logging import out
from app.common.bcolors import bcolors
from app.core.users import get_current_user

LABELS = config.LABELS


class IssueState(Enum):
    OPEN = 'opened'
    CLOSED = 'closed'


def _issue_description_guideline(issue: ProjectIssue) -> None:
    '''
    Recebe uma issue

    Efetua as validações de descrição na issue informada. 

    Caso não respeite as regras de descrição efetua um comentário informando ao usuário.
    '''
    if issue.description is not None and len(issue.description) > 15:
        return

    note = issue.notes.create(
        {'body': f'''
:wave: @{issue.author['username']}, vi aqui que faltaram algumas informações nessa issue. Segue o nosso guia:

- O conteúdo da issue não deve ser vazio
- Coloque o minímo de informação possível para que possamos atuar no problema/melhoria

Essas ações nos permitem manter uma estrutura organizada e informativa de tudo que acontece nas nossas aplicações.

*Essa mensagem foi gerada automaticamente*
'''})
    note.save()


def _issue_label_guideline(issue: ProjectIssue) -> None:
    '''
    Recebe uma issue

    Efetua as validações de label na issue informada. 

    Caso não respeite as regras de labels informadas efetua um comentário informando ao usuário as labels faltantes.
    '''
    if len(LABELS) <= 0:
        return

    if LABELS[0] == '':
        return

    text = ''
    for label in LABELS:
        if any(label in s for s in issue.labels):
            continue
        text += f'`{label}` '
    if text.strip() == '':
        return
    note = issue.notes.create(
        {'body': f'''
:wave: @{issue.author['username']}, adicione pelo menos uma label [{text.strip().replace(' ', ',')}]. Essas labels nos ajudam a manter nossos projetos organizados e categorizados corretamente para atuação.

Se você tiver dúvida de quais labels colocar fale com seu líder técnico, ele com certeza lhe ajudará!

*Essa mensagem foi gerada automaticamente*
'''})
    note.save()


def _notes(issue: ProjectIssue) -> None:
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
    i_notes: list[ProjectIssueNote] = issue.notes.list()
    for note in i_notes:
        note_author = note.author['name']
        if note_author == users.get_current_user().name:
            already_commented = True
            break

    if already_commented == False:
        _issue_description_guideline(issue=issue)
        _issue_label_guideline(issue=issue)


def process_issue(project, issue_iid):
    try:
        p = gl.projects.get(project['id'])
        issue = p.issues.get(issue_iid)
    except Exception as e:
        if '404' in str(e):
            print(out(
                message=f'{users.CURRENT_USER} não faz parte do projeto {project["name"]}', color=bcolors.FAIL))
        else:
            print(out(message=e, color=bcolors.FAIL))
    else:
        _notes(issue=issue)


def process_all_issues() -> None:
    projects_array = projects.all_projects(True)

    def projects_async(p):
        issues = p.issues.list(state=IssueState.OPEN.value)
        if issues is None:
            return
        for issue in issues:
            threading.Thread(target=_notes, args=(issue,)).start()
    for project in projects_array:
        threading.Thread(target=projects_async, args=(project,)).start()
