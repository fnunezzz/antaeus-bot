from app.common.bcolors import bcolors


def out(message: str, color: bcolors):
    return f'{color}{message}{bcolors.ENDC}'
