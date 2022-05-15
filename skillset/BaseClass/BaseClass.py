from queue import Queue

import telebot


def save_r():
    try:
        with open('data.txt', "r", newline='') as f:
            ttt = f.readlines()
            if ttt == "" or ttt == [] or len(ttt) == 1:
                return None
            return ttt
    except FileNotFoundError:
        return None


def read_time():
    try:
        with open("time.txt", "r", newline='') as f:
            rt = [i.replace("\n", "").split(": ") for i in f.readlines()]
        return rt
    except FileNotFoundError:
        return None


def save_w():
    temp = BaseClass.QueueList.get()
    BaseClass.QueueList.put(temp)
    Name, Date = temp
    with open('data.txt', 'w', newline='') as f:
        f.write(";".join(Name) + "\n")
        f.write(";".join(Date))


def save_time(text):
    with open("time.txt", "w", newline='') as f:
        f.write(text)


class BaseClass:
    token: str = "" # токен
    bot: telebot.TeleBot = telebot.TeleBot(token)
    QueueList: Queue = Queue()
    nameList: list = []
    dateList: list = ["2020-12-12"]
    timeDict: dict = {"Понедельник": "0-24", "Вторник": "0-24", "Среда": "0-24", "Четверг": "0-24",
                      "Пятница": "0-24", "Суббота": "0-24", "Воскресенье": "0-24"}
    rt = read_time()
    if rt is not None:
        for i in rt:
            timeDict[i[0]] = i[1]
    a = save_r()
    if a is not None:
        Names, Dates = [i.replace("\n", "").replace(";", ",").replace(" ", "") for i in a]
        nameList = Names.split(",")
        dateList = Dates.split(",")
        st = (nameList, dateList)
        QueueList.put(st)
    Id: list = []
    try:
        with open("dannie", "r", encoding="UTF-8-sig") as f:
            dannie = f.readlines()
            Id = dannie[2].split(":")[-1].replace("\n", "").replace(" ", "").strip().split(",")
            Id = list(map(int, Id))
    except FileNotFoundError:
        Id = [] # id кому отсылаються данные
    inquiryData = {"dateTime": 0, "teacherId": 0, "online": 1}
    inquiry: str = "https://skillset-online.com/measures/individualLessonsBook"
    urlPeople: str = "https://skillset-online.com/measures/getIndividual"
    data: dict = {}
    baseUrl: str = "https://skillset-online.com"
    url: str = baseUrl + "/user/login"
    getLastOfSet = "https://skillset-online.com/measures/individual"
    del a, rt, dannie
