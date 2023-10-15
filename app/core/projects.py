from gitlab.v4.objects import Project
from app.core.gitlab import gl


def all_projects(member: bool = True):
    return gl.projects.list(member=member)


def project(id) -> Project:
    return gl.projects.get(id)
