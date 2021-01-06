# Скрипт для отправки письма-приглашения
Скрипт берёт шаблон из этого [гиста](https://gist.github.com/dvmn-tasks/a2aa921d3e594fc7f49dca656b44062b).

Подставляет указанные значения в необходимые места и отправляет приглашение на указанный почтовый адрес.

## Как установить
Необходимо:
1. Иметь электронный почтовый ящик
2. Внести необходимые данные в файл ```.env``` в корне проекта в таком виде:
```
SMTP_SERVER=<smtp.your-mail-provider.com:465>
SMTP_LOGIN=<your-email-address@your-mail-provider.com>
SMTP_PASSWORD=<your-email-password>
```
Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```
## Использование
```
Usage: send_invite.py [OPTIONS]

Options:
  --friend_name TEXT   Имя друга  [required]
  --my_name TEXT       Твоё имя  [required]
  --friend_email TEXT  email твоего друга  [required]
  --website TEXT       Веб-сайт  [required]
```
Или можно просто запустить скрипт:
```
python send_invite.py
```
Скрипт попросит ввести необходимые параметры.
## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
