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
            callback_msg = "ВОПРОС {}/{}\nВыберете ответ: a или б\n{}" \
                .format(num_question, len(quest_a), question)
            write_message(user_id, random_id, callback_msg)
        else:
            write_message(user_id, random_id, "Последний ответ получен! Анализ результатов")
            analyse(user_id, random_id)


def rezult_of_analiticks(results):
    Real_type_list = {'1а', '2а', '3а', '4а', '5а', '16а', '17а', '18а', '19а', '21а', '31а', '32а', '33а', '34а'}
    IQ_type_list = {'1б', '6а', '7а', '8а', '9а', '16б', '20а', '22а', '23а', '24а', '31б', '35а', '36а', '37а'}
    Social_type_list = {'2б', '6б', '10а', '11а', '12а', '17б', '29б', '25а', '26а', '27а', '36б', '38а', '39а',
                           '41б'}
    Konvenc_type_list = {'3б', '7б', '10б', '13а', '14а', '18б', '22б', '25б', '28а', '29а', '32б', '38б', '40а',
                            '42а'}
    Buiseness_type_list = {'4б', '8б', '11б', '13б', '15а', '23б', '28б', '30а', '33б', '35б', '37б', '39б', '40б'}
    Artist_type_list = {'5б', '9б', '12б', '14б', '15б', '19б', '21б', '24а', '27б', '29б', '30б', '34б', '41а',
                           '42б'}
    type_list = [Real_type_list, IQ_type_list, Social_type_list, Konvenc_type_list, Buiseness_type_list,
                 Artist_type_list]
    rez = list()
    for i in type_list:
        rez.append(results.intersection(i))
    answers = ['Реалистический тип', 'Интеллектуальный тип', 'Социальный тип', 'Конвенциальный тип',
                   'Предприимчивый тип', 'Артистический тип']
    return ', '.join([answers[i] for i in range(len(answers)) if rez[i] == max(rez)])


def analyse(user_id, random_id):
    write_message(user_id, random_id, "РЕЗУЛЬТАТЫ")
    write_message(user_id, random_id, ' '.join(feedback[user_id]))
    write_message(user_id, random_id, rezult_of_analiticks(set(feedback[user_id])))
    feedback.pop(user_id)


def next_question(num):
    return "а) {}\tб) {}".format(quest_a[num - 1], quest_b[num - 1])


token = os.environ.get('BOT_TOKEN')
normal_msg = ['Начать', 'а', 'б']
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
feedback = dict()
in_file = open('questions.txt', 'r', encoding='utf-8')
rea = in_file.readlines()
in_file.close()
lines = []
for i in range(len(rea) - 1):
    l = rea[i][:-1]
    lines.append(l)
lines.append(rea[-1])
quest_a = list(filter(lambda x: lines.index(x) % 2 == 0, lines))[:5]
quest_b = list(filter(lambda x: lines.index(x) % 2 != 0, lines))[:5]
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
