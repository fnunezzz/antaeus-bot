import gitlab
import sys
import time
import app.core.users as users
import app.config.environment as config
from app.common.logging import out
from app.common.bcolors import bcolors

gl = gitlab.Gitlab(url=config.GITLAB_URL,
                   private_token=config.TOKEN)
# gl.enable_debug()


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
        users.configure_current_user(gl.user)
