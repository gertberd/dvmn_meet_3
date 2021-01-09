import os
import smtplib
from email.message import EmailMessage

import click
import requests
from dotenv import load_dotenv


def get_template_from_gist(gist_url) -> str:
    response = requests.get(gist_url)
    response.raise_for_status()
    template = response.text
    return template


def render_body(template, email_vars) -> str:
    for key, value in email_vars.items():
        template = template.replace(key, value)
    return template


def build_email_message(email_from, email_to, subject, body) -> EmailMessage:
    message = EmailMessage()
    message['From'] = email_from
    message['To'] = email_to
    message['Subject'] = subject
    message.set_content(body)
    return message


@click.command()
@click.option('--my_name', required=True,
              prompt='Как тебя зовут?',
              help='Твоё имя')
@click.option('--friend_name', required=True,
              prompt='Как зовут твоего друга?',
              help='Имя друга')
@click.option('--friend_email', required=True,
              prompt='Укажи e-mail друга',
              help='email твоего друга')
@click.option('--website', required=True,
              prompt='Укажи имя веб-сайта',
              help='Веб-сайт')
@click.option('--gist_url', required=True,
              prompt='Укажи URL гиста с шаблоном в формате RAW',
              help='URL гиста с шаблоном в формате RAW')
@click.option('--subject', default='Invite', required=False, help="Заголовок письма")
def main(friend_name, my_name, friend_email, website, gist_url, subject):
    load_dotenv()
    my_email = os.getenv('SMTP_LOGIN')
    email_password = os.getenv('SMTP_PASSWORD')
    smtp_server = os.getenv("SMTP_SERVER")
    email_vars = {
        '%friend_name%': friend_name,
        '%website%': website,
        '%my_name%': my_name
    }
    try:
        template = get_template_from_gist(gist_url)
    except requests.exceptions.RequestException as error:
        print(f"Произошла ошибка при попытке получить текст шаблона по ссылке: {gist_url}. Перепроверьте ссылку!")
        print(error)
        exit(1)
    body = render_body(template, email_vars)
    email_message = build_email_message(email_from=my_email, email_to=friend_email, subject=subject, body=body)
    try:
        server = smtplib.SMTP_SSL(smtp_server)
        try:
            server.login(my_email, email_password)
            server.sendmail(my_email, friend_email, email_message.as_string())
        except smtplib.SMTPAuthenticationError:
            print('Ошибка аутентификации, проверьте почтовый адрес и пароль!')
        except smtplib.SMTPException as error:
            print(f'Произошла ошибка при отправке письма:\n{error}')
        finally:
            server.quit()
    except TimeoutError:
        print('Неудачная попытка подключения к SMTP-серверу.\n'
              'Проверьте правильно ли вы указали имя сервера и порт подключения.')


if __name__ == '__main__':
    main()
