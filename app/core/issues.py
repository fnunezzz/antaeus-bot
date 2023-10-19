import threading
import datetime
from enum import Enum
from app.config.parser import Parser
from gitlab.v4.objects import ProjectIssue, ProjectIssueNote, Project
import app.core.users as users
import app.core.projects as projects
import app.config.environment as config
from app.core.gitlab import gl
from app.common.logging import out
from app.common.bcolors import bcolors
from app.core.users import get_current_user

ISSUE_RULES = config.CONFIG['resource_rules']['issues']['rules']


class IssueState(Enum):
    OPEN = 'opened'
    CLOSED = 'closed'


def _old_issue_guideline(issue: ProjectIssue) -> None:
    note = issue.notes.create(
        {'body': f'''
:wave: @{issue.author['username']} essa issue está parada a mais de {config.OLD_ISSUE_TIME_DELTA} semanas.

Label de `state` alterada para ~"state::pendente-analise"

*Essa mensagem foi gerada automaticamente*
    '''})
    note.save()


def _issue_description_guideline(issue: ProjectIssue) -> None:
    '''
    Recebe uma issue

    Efetua as validações de descrição na issue informada. 

    Caso não respeite as regras de descrição efetua um comentário informando ao usuário.
    '''
    for rule in ISSUE_RULES:
        parser = Parser(**rule)
        should_comment = False
        conditions = rule.get('conditions')
        if conditions is None:
            continue
        comment = rule['comment'].replace(
            '{{author}}', issue.author['username'])
        description = conditions.get('description')
        if description is not None:
            should_comment = parser.description(attr=issue.description)

        # date = conditions.get('date')
        # if date is not None:
        #     should_comment = Parser.date(attr=issue, rule=date)

        # labels = conditions.get('labels')
        # if labels is not None:
        #     should_comment = Parser.labels(attr=issue.labels, rule=labels)
        if should_comment is True:
            note = issue.notes.create(
                {'body': comment})
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
        # _issue_label_guideline(issue=issue)


def _old_issues(issue: ProjectIssue) -> None:
    '''
    Recebe uma issue

    Valida se esta issue esta a X semanas sem atualizacao. Caso nao tenha atualizacao remove as labels de state e adiciona a label de pendente analise.
    '''

    _old_issue_guideline(issue=issue)

    for i, label in enumerate(issue.labels):
        for old_label in config.OLD_ISSUE_OLD_LABELS:
            if old_label in label:
                issue.labels.pop(i)
    issue.labels.extend(config.OLD_ISSUE_NEW_LABELS)
    issue.save()


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


def process_old_issues() -> None:
    projects_array = projects.all_projects(True)
    now = datetime.datetime.now()
    before = now - datetime.timedelta(weeks=config.OLD_ISSUE_TIME_DELTA)

    def projects_async(p: Project):
        issues = p.issues.list(get_all=True,
                               state=IssueState.OPEN.value,
                               updated_before=before.isoformat())

        if issues is None:
            return
        for issue in issues:
            threading.Thread(target=_old_issues,
                             args=(issue,)).start()
    for project in projects_array:
        threading.Thread(target=projects_async, args=(project,)).start()


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
