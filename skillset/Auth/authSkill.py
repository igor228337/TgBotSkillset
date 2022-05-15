from __future__ import annotations

import pickle
from typing import Union

from BaseClass.BaseClass import BaseClass
from fake_useragent import UserAgent
from requests_html import HTMLSession


class AuthSkillSet(BaseClass):
    def __init__(self):
        try:
            with open('session.pkl', 'rb') as f:
                self.session: HTMLSession = pickle.load(f)
        except Union[FileNotFoundError, OSError]:
            self.session: HTMLSession = HTMLSession()
            self.session.headers = {"User-Agent": UserAgent().random}
            login = ""
            password = ""
            try:
                with open("dannie", "r", encoding="UTF-8-sig") as f:
                    dannie = f.readlines()
                    login = dannie[0].split(":")[-1].replace("\n", "").replace(" ", "").strip()
                    password = dannie[1].split(":")[-1].replace("\n", "").replace(" ", "").strip()
            except FileNotFoundError:
                pass
            self.data = {"UserLogin[username]": login, "UserLogin[password]": password}

    def auth(self) -> HTMLSession | None:
        r = self.session.post(self.url, data=self.data)
        if r.ok and "Имя пользователя".lower() in r.text.lower():
            with open('session.pkl', 'wb') as f:
                pickle.dump(self.session, f)
            return self.session
        else:
            import os
            os.remove("session.pkl")
            return None
