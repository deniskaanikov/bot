import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import os

def write_message(user_id, random_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random_id})


def callback_message(user_id, random_id, input_msg):
    if input_msg not in normal_msg:
        write_message(user_id, random_id, "Некорректный ответ. Повторите")
    else:
        if input_msg in normal_msg[1:len(normal_msg)]:
            num_question = len(feedback[user_id]) + 1
            feedback[user_id].append(str(num_question) + input_msg)
            num_question += 1
        else:
            num_question = len(feedback[user_id]) + 1
        if num_question <= len(quest_a):
            question = next_question(num_question)
            callback_msg = "ВОПРОС {}/{}\nВыберете ответ: a или б\n{}"\
                .format(num_question, len(quest_a), question)
            write_message(user_id, random_id, callback_msg)
        else:
            write_message(user_id, random_id, "Последний ответ получен! Анализ результатов")
            analyse(user_id, random_id)


def analyse(user_id, random_id):
    write_message(user_id, random_id, "РЕЗУЛЬТАТЫ")
    write_message(user_id, random_id, ' '.join(feedback[user_id]))
    res = feedback[user_id]
    feedback.pop(user_id)


def next_question(num):
    return "а) {}\tб) {}".format(quest_a[num - 1], quest_b[num - 1])


# token = os.environ.get('BOT_TOKEN')
token = 'e828d8ce2142893fd3383626875e9b59ca6f9b64c9e9edf28810ca7a2f9ac8d837708df1c829b67d17603'
normal_msg = ['Начать', 'а', 'б']
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
feedback = dict()
in_file = open('questions.txt', 'r')
rea = in_file.readlines()
in_file.close()
lines = []
for i in range(len(rea)):
    l = rea[i][:-1]
    lines.append(l)
quest_a = list(filter(lambda x: lines.index(x) % 2 == 0, lines))
quest_b = list(filter(lambda x: lines.index(x) % 2 != 0, lines))
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:

            user_id = event.user_id
            random_id = event.random_id
            request = event.text

            if user_id not in feedback.keys():
                if request == "Начать":
                    feedback[user_id] = []
                    callback_message(user_id, random_id, request)
                else:
                    write_message(user_id, random_id, "Я тебя не понимаю. Напиши \"Начать\" чтобы продолжить")
            else:
                callback_message(user_id, random_id, request)
