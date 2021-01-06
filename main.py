import os
import click
import requests
import smtplib
from dotenv import load_dotenv


def get_template_from_gist(gist_url) -> str:
    response = requests.get(gist_url)
    template = response.text
    return template


def render_body(template, email_vars) -> str:
    for key, value in email_vars.items():
        template = template.replace(key, value)
    return template


@click.command()
@click.option('--friend_name', prompt='Как зовут твоего друга? ',
              help='Имя друга')
@click.option('--my_name', prompt='Как тебя зовут? ',
              help='Твоё имя')
@click.option('--friend_email', prompt='Укажи e-mail друга: ',
              help='email твоего друга')
@click.option('--website', prompt='Укажи имя веб-сайта: ',
              help='Веб-сайт')
def main(friend_name, my_name, friend_email, website):
    load_dotenv()
    my_email = os.getenv('SMTP_LOGIN')
    email_password = os.getenv('SMTP_PASSWORD')
    smtp_server = os.getenv("SMTP_SERVER")
    email_vars = {
        '%friend_name%': friend_name,
        '%website%': f'<a src={website}>{website}</a>',
        '%my_name%': my_name
    }
    gist_url = 'https://gist.githubusercontent.com/dvmn-tasks/a2aa921d3e594fc7f49dca656b44062b/' \
               'raw/9da7b7e0fc1ba0e93b6c0390a2e71f8ce9b800bb/mail.txt'
    template = get_template_from_gist(gist_url)
    body = render_body(template, email_vars)
    subject = body.splitlines()[0]
    email_message = f'From: {my_email}\n' \
                    f'To: {friend_email}\n' \
                    f'Subject: {subject}\n' \
                    f'Content-Type: text/plain; charset="UTF-8";\n' \
                    f'{body}'
    server = smtplib.SMTP_SSL(smtp_server)
    server.login(my_email, email_password)
    server.sendmail(my_email, friend_email, email_message.encode("UTF-8"))
    server.quit()


if __name__ == '__main__':
    main()
