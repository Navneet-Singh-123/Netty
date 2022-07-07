import schedule
import requests

import environ
env = environ.Env()
environ.Env.read_env()

def job():
    print("Running...")
    url = env("URL")
    d = requests.delete(url + "/users")
    print(d.json())
    return

schedule.every().day.at("01:00").do(job)

while True:
    schedule.run_pending()
