from requests import Response
import time as tm
from BaseClass.BaseClass import BaseClass
from bs4 import BeautifulSoup
import datetime
from BaseClass import BaseClass as BS
import json


def bs4Pars(r) -> BeautifulSoup:
    return BeautifulSoup(r, "html.parser")


class Pars(BaseClass):
    def __init__(self, session) -> None:
        self.session = session

    def reg_bron(self, id_people, date_time, online=1) -> Response:
        self.inquiryData["dateTime"] = date_time
        self.inquiryData["teacherId"] = id_people
        self.inquiryData["online"] = online
        r = self.session.post(self.inquiry, data=self.inquiryData)
        return r

    def start(self) -> None:
        true = True
        false = False
        null = None
        while 1:
            tm.sleep(10)
            if not self.QueueList.empty():
                now = datetime.datetime.now()
                print(f"Начал проверять: {tm.strftime('%a, %d %b %Y %H:%M:%S')}")
                while 1:
                    try:
                        number3 = self.session.get(self.getLastOfSet)
                        break
                    except:
                        tm.sleep(5)
                soup3 = bs4Pars(number3.text)
                number3 = soup3.find("input", id="jsData").get("value")
                decoded = json.loads(number3)
                number3_1 = int(decoded["individualOffset"])
                try:
                    r = self.session.post(self.urlPeople, data={"lastOffset": number3_1, "offset": 10})
                except:
                    continue
                soup = bs4Pars(r.json()["content"])
                List = self.QueueList.get()
                try:
                    humans, dates = List
                except ValueError:
                    continue
                dictListTemp = {"Mon": BaseClass.timeDict["Понедельник"], "Tue": BaseClass.timeDict["Вторник"],
                                "Wed": BaseClass.timeDict["Среда"], "Thu": BaseClass.timeDict["Четверг"],
                                "Fri": BaseClass.timeDict["Пятница"], "Sat": BaseClass.timeDict["Суббота"],
                                "Sun": BaseClass.timeDict["Воскресенье"]}
                humans = [i.replace(" ", "") for i in humans]
                dates = [i.replace(" ", "") for i in dates]
                if len(humans) == 0 or len(dates) == 0:
                    continue
                self.QueueList.put(List)
                blocks = soup.find_all("div", class_="block_cont")
                for block in blocks:
                    for human in humans:
                        times = set()
                        people = block.find("span", class_="tutor_name").get_text(strip=True)
                        try:
                            date_time = block.find("div", class_="me_btn me_btn_individual").get("data-time")
                        except AttributeError:
                            continue
                        id_people = block.find("div", class_="me_btn me_btn_individual").get("data-teacher").strip()
                        dt = date_time.split(" ")[0]
                        td = int(date_time.split(" ")[-1].split(":")[0].strip())
                        dt1 = str(datetime.date.fromisoformat(dt).strftime("%a"))
                        rtt = dictListTemp[dt1].strip().split(",")
                        for i in rtt:
                            try:
                                for tt in range(int(i.split("-")[0]), int(i.split("-")[-1]) + 1):
                                    times.add(tt)
                            except ValueError:
                                for idd in self.Id:
                                    self.bot.send_message(idd, "Упс что-то со временем не так")
                                break

                        if human == people and dt in dates and td in times:

                            Names, Data = BaseClass.QueueList.get()
                            BaseClass.QueueList.put((Names, Data))
                            try:
                                del Data[Data.index(dt)]
                            except ValueError:
                                break
                            while not BaseClass.QueueList.empty():
                                BaseClass.QueueList.get()
                            BaseClass.QueueList.put((Names, Data))
                            BS.save_w()
                            r = self.reg_bron(id_people, date_time)
                            if r.json()["result"] is True:
                                for i in self.Id:
                                    self.bot.send_message(i, f"Урок забронирован к {people} на "
                                                             f"{dt} в {date_time.split(' ')[-1]}")
                            else:
                                for i in self.Id:
                                    self.bot.send_message(i, f"По какой-то причине мне не удалось сделать бронь(")
