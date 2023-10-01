import threading

import loguru
import os

import cv2
from deepface import DeepFace
import telebot
import datetime
from dotenv import find_dotenv, load_dotenv

if not find_dotenv():
    exit("File .env wasn't found")
else:
    load_dotenv()

bot_token = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(bot_token)

chat_id = ''


@bot.message_handler(commands=['start'])
def start(message):
    global chat_id
    bot.send_message(message.from_user.id, 'Starting security system...')
    chat_id = message.chat.id
    system()


@bot.message_handler(commands=['logs'])
def logs(message):
    with open('data.txt', 'r') as file:
        data = file.readlines()
    data = ''.join(data)
    if len(data) == 0:
        bot.send_message(message.from_user.id, 'Security logs are empty!')
    else:
        bot.send_message(message.from_user.id, f'{data}')


def send_face(photo, flag):
    bot.send_photo(chat_id=chat_id, photo=photo)
    now = datetime.datetime.now()
    bot.send_message(chat_id=chat_id, text=f'{str(now)[:19]} - {flag}')




logger = loguru.logger
logger.add('data.txt', format="{time} {message}", level='INFO')


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

counter = 0

face_match = False
ban_face = False
no_flood = True

reference_img = cv2.imread("your_photo.jpg")
ban_img = cv2.imread("banned_photo.jpg")


def check_face(frame):
    global face_match, ban_face, no_flood
    try:
        if DeepFace.verify(frame, ban_img.copy())['verified']:
            no_flood = True
            ban_face = True
            return
        elif DeepFace.verify(frame, reference_img.copy())['verified']:
            face_match = True
        else:
            face_match = False
            ban_face = False
    except ValueError:
        face_match = False



def system():
    global counter, no_flood, ban_face
    while True:
        ret, frame = cap.read()
        if ret:
            if counter % 30 == 0:
                try:
                    threading.Thread(target=check_face, args=(frame.copy(),)).start()
                except ValueError:
                    pass
            counter += 1
            if face_match:
                cv2.putText(frame, "Match!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
                no_flood = True
            elif ban_face and no_flood:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame_bytes = buffer.tobytes()
                send_face(frame_bytes, 'Banned face detected!')
                logger.critical('Banned face detected!')
                no_flood = False
                ban_face = False
            elif not face_match and no_flood:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame_bytes = buffer.tobytes()
                send_face(frame_bytes, 'Unrecognized face!')
                logger.warning('Unrecognized face!')
                no_flood = False
            cv2.imshow("video", frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

cv2.destroyAllWindows()

bot.polling(none_stop=True, interval=0)