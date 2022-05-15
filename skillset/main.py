from Auth.authSkill import AuthSkillSet
from tg_bot.BotTg import run_bot

from Pars.Pars import Pars
import threading
import time


if __name__ == '__main__':
    print("============Запущен============")
    auth_session: AuthSkillSet = AuthSkillSet()
    session = auth_session.auth()
    while session is None:
        print("Повторная попытка")
        time.sleep(5)
        auth_session: AuthSkillSet = AuthSkillSet()
        session = auth_session.auth()
    north: threading = threading.Thread(target=run_bot)
    north.start()
    Pars(session).start()
