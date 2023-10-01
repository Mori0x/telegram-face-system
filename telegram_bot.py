import datetime

from logger import setup_logger
from face_recognition import setup_face_recognition
from face_recognition import face_match
import cv2

from face_system import send_face

# Set up the logger
logger = setup_logger()

chat_id = ''

def setup_telegram_bot(bot):
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

    return bot, send_face


def system():
    global counter, no_flood, ban_face
    while True:
        ret, frame = cv2.cap.read()
        if ret:
            if counter % 30 == 0:
                try:
                    setup_face_recognition.check_face(frame.copy())
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
