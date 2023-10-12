from gitlab.v4.objects import CurrentUser


CURRENT_USER: CurrentUser


def configure_current_user(user: CurrentUser):
    global CURRENT_USER
    CURRENT_USER = user


def get_current_user() -> CurrentUser:
    return CURRENT_USER.name
