import imaplib
import os
import time
import re
import email
from dotenv import load_dotenv


def get_login_code():
    load_dotenv()
    user = os.getenv("USER_EMAIL")
    password = os.getenv("GMAIL_PASSWORD")

    if not user or not password:
        print("Can't find USER_EMAIL OR GMAIL_PASSWORD")
        return None

    imap_server = "imap.gmail.com"
    mail = None

    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(user, password)
        print("Connected to Gmail")

        start_time = time.time()
        while (time.time() - start_time) < 60:
            mail.select("inbox")
            status, data = mail.search(None, '(UNSEEN SUBJECT "Megaphone")')
            email_ids = data[0].split()

            if email_ids:
                for email_id in reversed(email_ids):
                    print(f"[EMAIL] Проверяю письмо с ID {email_id.decode()}...")

                    status, data = mail.fetch(email_id, '(RFC822)')
                    raw_email = data[0][1]
                    msg = email.message_from_bytes(raw_email)

                    body = ""

                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == 'text/plain':
                                payload_bytes = part.get_payload(decode=True)
                                if payload_bytes:
                                    body = payload_bytes.decode()
                                    break
                    else:
                        payload_bytes = msg.get_payload(decode=True)
                        if payload_bytes:
                            body = payload_bytes.decode()

                    if not body:
                        print("[Пошта] ...тело пустое, пропускаю...")
                        continue  # Переходим к следующему письму в цикле for

                    match = re.search(r'\b(\d{6})\b', body)

                    if match:
                        code = match.group(1)
                        print(f"[EMAIL] Успешно вытянул код: {code} из письма {email_id.decode()}")

                        # ▼▼▼ ИЗМЕНЕНИЕ 2: Помечаем письмо как прочитанное ▼▼▼
                        try:
                            mail.store(email_id, '+FLAGS', r'(\Seen)')
                            print(f"[EMAIL] Письмо {email_id.decode()} помечено как прочитанное.")
                        except Exception as e_store:
                            print(f"[EMAIL] Не удалось пометить письмо как прочитанное: {e_store}")

                        return code  # Нашли код, выходим из *всей* функции
                    else:
                        print("[EMAIL] ...в этом письме код не найден.")
                        # Цикл 'for' продолжится и проверит следующее (более старое) письмо

                # Если мы проверили ВСЕ письма в цикле 'for' и не нашли код
                print("[EMAIL] Проверил все непрочитанные, кодов нет. Жду 10 секунд...")
                time.sleep(10)

            else:  # Это 'else' для 'if email_ids:'
                print("[EMAIL] No new letters... waiting 10 seconds...")
                time.sleep(10)

        # Если мы вышли из цикла 'while' (прошло 60 секунд)
        print("[EMAIL] Waiting time has expired. List with the special code did not arrive.")
        return None

    except Exception as e:
        print(f"Что-то пошло не так: {e}")
        return None

    finally:
        if mail:
            mail.close()
            mail.logout()
            print("Disconnected from Gmail")