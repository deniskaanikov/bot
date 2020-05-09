import vk_api
import apiai
import json
from vk_api.longpoll import VkLongPoll, VkEventType
import os


def write_message(user_id, random_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random_id})


def text_message(user_id, random_id, input_msg):
    request = apiai.ApiAI('483bb5a7b9f44853b1054678c337a866').text_request()
    request.lang = 'ru'
    request.session_id = 'BatlabAIBot'
    request.query = input_msg
    response_Json = json.loads(request.getresponse().read().decode('utf-8'))
    response = response_Json['result']['fulfillment']['speech']
    if response:
        write_message(user_id, response, random_id)
    else:
        write_message(user_id, 'Я Вас не совсем понял!', random_id)


token = os.environ.get('BOT_TOKEN')

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            rid = event.random_id
            request = event.text
            id = event.user_id
            text_message(id, rid, request)

