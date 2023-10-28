import threading
import datetime
from enum import Enum
from app.config.parser import IssueConfigParser
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


def _issue_guidelines(issue: ProjectIssue) -> None:
    '''
    Recebe uma issue

    Efetua as regras definidas no arquivo de config
    '''
    for rule in ISSUE_RULES:
        parser = IssueConfigParser(**rule)
        should_comment = parser.parse(issue=issue)
        if should_comment is True:
            note = issue.notes.create(
                {'body': parser.comment})

            note.save()


def _notes(issue: ProjectIssue) -> None:
    '''
    Recebe uma issue

    Passos:
    - valida se já foi comentado pelo bot 
        - caso já comentado efetua as validações necessárias nas rules do arquivo de config
    '''
    already_commented = False
    i_notes: list[ProjectIssueNote] = issue.notes.list()
    for note in i_notes:
        note_author = note.author['name']
        if note_author == users.get_current_user().name:
            already_commented = True
            break

    if already_commented == False:
        _issue_guidelines(issue=issue)


def _old_issues(issue: ProjectIssue) -> None:
    '''
    Recebe uma issue

    Efetua novamente todas as validações de issue
    '''

    _issue_guidelines(issue=issue)


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

    def projects_async(p: Project):
        issues = p.issues.list(get_all=True,
                               state=IssueState.OPEN.value)

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
