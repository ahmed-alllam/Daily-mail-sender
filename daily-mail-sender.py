import smtplib, ssl, time
import pyowm  # pip install pyowm
import wikiquotes  # pip install wikiquotes
from anydo_api.client import Client  # pip install anydo_api

email = input("Enter your email: ")
password = input("Enter your email's password: ")
any_do_email = input("Enter your anydo email: ")
any_do_password = input("Enter your anydo password: ")
tasks_num = 0


def get_anydo_tasks(email, password):
    user = Client(email=email, password=password).get_user()
    tasks = ""
    global tasks_num
    for task in user.tasks():
        if task.status == 'UNCHECKED':
            tasks_num += 1
            tasks += '{}- {}'.format(tasks_num, task['title'] + '.\n\t')
    return tasks


def get_weather():
    owm = pyowm.OWM('your-api-key')
    observation = owm.weather_at_place(input("Enter your city's name: "))  # 'London,GB'
    w = observation.get_weather()
    status = w.get_status()
    temp = int(w.get_temperature('celsius')['temp'])
    return '{} with temperature of {} celsius.'.format(status, temp)


def send_daily_mail():
    weather = get_weather() + '\n'
    quote = wikiquotes.quote_of_the_day("english")
    anydo_tasks = '\t' + get_anydo_tasks(any_do_email, any_do_password)

    port = 465
    smtp_server = "smtp.gmail.com"
    message = """Subject: Your automated daily tasks mail

Hi, how are you doing?

This E-Mail is sent to you from your python tasks bot.


The Weather today in your city is :

        {}

Your Daily quote is :

        {}
            - {}


Today you have {} task(s) :

{}

Spend your time wisely and set your next day's goals at night.

Have a nice Day, Guten Tag!""".format(weather, quote[0], quote[1], tasks_num, anydo_tasks)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(email, password)
        server.sendmail(email, email, message)


if __name__ == '__main__':
    while True:
        local_time = time.localtime(time.time())
        if local_time.tm_hour == 8 and local_time.tm_min == 0:
            extract_info()
            send_daily_mail()
            time.sleep(86400)
        time.sleep(59)
