from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import time as tmi

from BaseClass.BaseClass import BaseClass as BaseClass
from BaseClass import BaseClass as Bs

bot = BaseClass.bot
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton("Сделать запись")
item2 = types.KeyboardButton("Посмотреть все записи")
item3 = types.KeyboardButton("Удалить одну запись")
item4 = types.KeyboardButton("Удалить все записи")
item5 = types.KeyboardButton("Задать время (пн-вс)")
item6 = types.KeyboardButton("Посмотреть время(пн-вс)")
markup.add(item1)
markup.add(item2)
markup.add(item3)
markup.add(item4)
markup.add(item5)
markup.add(item6)


def decorProv(func):
    def wrapper(message, *args, **kwargs):
        if int(message.from_user.id) not in BaseClass.Id:
            bot.send_message(message.chat.id, "Этот бот предназначен не для вас!")
        else:
            func(message, *args, **kwargs)

    return wrapper


@bot.message_handler(commands=['start'])
@decorProv
def send_welcome(message) -> None:
    bot.reply_to(message,
                 "Приветствую, {0.first_name}\nСмотрю, ты меня активировал, значит я не зря существую".format(
                     message.from_user), reply_markup=markup)


@decorProv
def get_List(message) -> None:
    if BaseClass.QueueList.empty():
        bot.send_message(message.chat.id, "Настройки пусты", reply_markup=markup)
    else:
        a = BaseClass.QueueList.get()
        BaseClass.QueueList.put(a)
        nameList = "\n".join(a[0])
        dateList = "\n".join(a[1])
        bot.send_message(message.chat.id,
                         f"========\nИмена: \n{nameList}\n=======\nДаты: \n{dateList}\n=======",
                         reply_markup=markup)


@decorProv
def stop_people_date_time(message) -> None:
    if BaseClass.QueueList.empty():
        bot.send_message(message.chat.id, "Настройки и так пустые :) ", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Что хотите удалить: ",
                         reply_markup=gen_markup("Имя", "delete_name", "Дату", "delete_data"))


@decorProv
def delete_what(message) -> None:
    text = message.text
    Names, Data = BaseClass.QueueList.get()
    BaseClass.QueueList.put((Names, Data))
    index = None
    if len(text.split("-")) == 3:
        try:
            index = Data.index(text)
            del Data[index]
        except ValueError:
            bot.send_message(message.chat.id, "Сорян не смог найти эту дату")
            return
    else:
        try:
            index = Names.index(text)
            del Names[index]
        except ValueError:
            bot.send_message(message.chat.id, "Сорян не смог найти это имя")
            return
    while not BaseClass.QueueList.empty():
        BaseClass.QueueList.get()
    BaseClass.QueueList.put((Names, Data))
    bot.send_message(message.chat.id, f"Удалил {text}")
    bot.reply_to(message, 'Сохранить: ', reply_markup=gen_markup("Да", "save_zaps_yes", "Нет", "save_zaps_no"))


@decorProv
def stopList(message) -> None:
    if BaseClass.QueueList.empty():
        bot.send_message(message.chat.id, "Настройки и так пустые :) ", reply_markup=markup)
    else:
        while not BaseClass.QueueList.empty():
            BaseClass.QueueList.get()
        BaseClass.nameList.clear()
        BaseClass.dateList.clear()
        bot.send_message(message.chat.id, "Удалить все сохранения?",
                         reply_markup=gen_markup("Да", "del_all_yes", "Нет", "del_all_no"))


@decorProv
def send_welcomes(message) -> None:
    bot.reply_to(message, 'Что ты хочешь добавить: ', reply_markup=gen_markup("Имя", "Name", "Даты", "Date"))


def process_step_2_Name(message) -> None:
    Data = BaseClass.dateList
    Names = BaseClass.nameList
    while not BaseClass.QueueList.empty():
        Names, Data = BaseClass.QueueList.get()
    while not BaseClass.QueueList.empty():
        BaseClass.QueueList.get()
    ttt = str(message.text.strip().replace(" ", "")).split(",")
    for i in ttt:
        if i in Names:
            bot.send_message(message.chat.id, f"Имя {i} уже есть")
            BaseClass.QueueList.put((Names, Data))
            return
        for t in i:
            if ord("a") <= ord(t) <= ord("z") or ord("A") <= ord(t) <= ord("Z"):
                continue
            else:
                return

        Names.append(i)
    BaseClass.nameList = Names
    BaseClass.QueueList.put((Names, Data))
    bot.send_message(message.chat.id, "Запись изменена", reply_markup=markup)
    bot.reply_to(message, 'Сохранить: ', reply_markup=gen_markup("Да", "save_zaps_yes", "Нет", "save_zaps_no"))


def gen_markup(*args):
    mar_kup = InlineKeyboardMarkup()
    mar_kup.row_width = 2
    mar_kup.add(InlineKeyboardButton(args[0], callback_data=args[1]),
                InlineKeyboardButton(args[2], callback_data=args[3]))
    return mar_kup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "save_zaps_yes":
        save_zaps(call)
    elif call.data == "save_zaps_no":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="А жаль что не захотел :(", reply_markup=None)
    elif call.data == "del_all_yes":
        try:
            os.remove(os.getcwd() + "\\data.txt")
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Всё удалено, кроме времени :)", reply_markup=None)
        except OSError:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Хммм странно файла с данными уже не было....", reply_markup=None)
    elif call.data == "del_all_no":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="На всё твоя воля", reply_markup=None)
    elif call.data == "save_time_yes":
        save_time123(call)
    elif call.data == "save_time_no":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Ну как хочешь )", reply_markup=None)
    elif call.data == "Name":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Хорошо", reply_markup=None)
        msg = bot.send_message(call.message.chat.id, f'Введите имена через запятую: ')
        bot.register_next_step_handler(msg, process_step_2_Name)
    elif call.data == "Date":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Хорошо", reply_markup=None)
        msg = bot.send_message(call.message.chat.id, f'Введите даты через запятую: ')
        bot.register_next_step_handler(msg, process_step_3_date_last)

    elif call.data == "delete_name":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Как скажешь )", reply_markup=None)
        msg = bot.send_message(call.message.chat.id, f'Вводи имя: ')
        bot.register_next_step_handler(msg, delete_what)
    elif call.data == "delete_data":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Как скажешь )", reply_markup=None)
        msg = bot.send_message(call.message.chat.id, f'Вводи дату: ')
        bot.register_next_step_handler(msg, delete_what)
    elif call.data == "Понедельник" or call.data == "Вторник" or call.data == "Среда" or call.data == "Четверг"\
            or call.data == "Пятница" or call.data == "Суббота" or call.data == "Воскресенье":
        msg = bot.send_message(call.message.chat.id, f'Вводи время для {call.data}(Пример: 1-19): ')
        bot.register_next_step_handler(msg, saveTimeSet, call.data)


def save_zaps(call):
    Bs.save_w()
    bot.answer_callback_query(call.id, "Запись сохранена :)")
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Запись сохранена :)",
                          reply_markup=None)


def process_step_3_date_last(message) -> None:
    Data = BaseClass.dateList
    Names = BaseClass.nameList
    while not BaseClass.QueueList.empty():
        Names, Data = BaseClass.QueueList.get()
    if len(message.text.split("-")) < 3:
        bot.send_message(message.chat.id, "Ты как-то не так ввёл, по этому начинай с начала :)")
        return
    ttt = str(message.text.strip().replace(" ", "")).split(",")
    for i in ttt:
        if i in Data:
            bot.send_message(message.chat.id, f"Дата {i} уже есть")
            BaseClass.QueueList.put((Names, Data))
            return
        Data.append(i)
    BaseClass.dateList = Data
    BaseClass.QueueList.put((Names, Data))
    bot.send_message(message.chat.id, "Запись изменена", reply_markup=markup)
    bot.reply_to(message, 'Сохранить: ', reply_markup=gen_markup("Да", "save_zaps_yes", "Нет", "save_zaps_no"))


@decorProv
def save_time123(call):
    try:
        Bs.save_time("\n".join([i[0] + ": " + i[1] for i in BaseClass.timeDict.items()]))
    except IndexError:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Я не знаю почему но мне не удалось сохранить (", reply_markup=None)
        return
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Собственно говоря я сохранил", reply_markup=None)


@decorProv
def saveTimeSet(msg, i):
    if "-" not in msg.text:
        bot.send_message(msg.chat.id, "Ты как-то не так ввёл, по этому начинай с начала :)")
        return
    BaseClass.timeDict[i] = msg.text.replace(" ", "")
    bot.send_message(msg.chat.id, "Запись сделана", reply_markup=markup)
    bot.send_message(msg.chat.id, "Хотите сохранить время?",
                     reply_markup=gen_markup("Да", "save_time_yes", "Нет", "save_time_no"))


@decorProv
def viewsTime(message):
    bot.send_message(message.chat.id, "\n".join([i[0] + ": " + i[1] for i in BaseClass.timeDict.items()]),
                     reply_markup=markup)


def gen_markup_time():
    mar_kup = InlineKeyboardMarkup()
    mar_kup.row_width = 2
    for i in BaseClass.timeDict.keys():
        mar_kup.add(InlineKeyboardButton(i, callback_data=i))
    return mar_kup


@bot.message_handler(content_types='text')
def message_reply(message) -> None:
    if message.text == "Сделать запись":
        send_welcomes(message)
    elif message.text == "Посмотреть все записи":
        get_List(message)
    elif message.text == "Удалить все записи":
        stopList(message)
    elif message.text == "Удалить одну запись":
        stop_people_date_time(message)
    elif message.text == "Ид":
        bot.send_message(message.chat.id, message.from_user.id)
    elif message.text == "Задать время (пн-вс)":
        bot.send_message(message.chat.id, "Выберите время которое хотите изменить: ", reply_markup=gen_markup_time())
    elif message.text == "Посмотреть время(пн-вс)":
        viewsTime(message)
    else:
        bot.send_message(message.chat.id, "Извини я тебя не понимаю :( ", reply_markup=markup)


def run_bot() -> None:
    try:
        bot.polling(none_stop=True)
    except:
        tmi.sleep(5)
        run_bot()
