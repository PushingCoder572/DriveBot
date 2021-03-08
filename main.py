from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sys import exit
from time import sleep
from datetime import datetime
import smtplib, ssl
from os import environ

"""chrome_options = ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')"""
driver = webdriver.Chrome()


class two_or_more_elements(object):
    def __init__(self, tag):
        self.tag = tag

    def __call__(self, driver):
        temp = driver.find_elements_by_tag_name(self.tag)
        if len(temp) > 1:
            return temp
        else:
            return False


def main(plats):
    driver.get("https://fp.trafikverket.se/boka/#/search/amAAMtMoTeIpM/5/0/0/0")
    id_list = ["examination-type-select", "id-control-searchText-1-1", "vehicle-select"]
    for index, id in enumerate(id_list):
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, id))
            )
        except:
            driver.quit()
            exit()

        if index == 1:
            element.clear()
            element.send_keys(plats)
        else:
            select = Select(element)
            select.select_by_index(2)

        sleep(0.5)

    driver.find_element_by_id("id-control-searchText-1-1").send_keys(Keys.RETURN)

    wait = WebDriverWait(driver, 10)
    lista_av_tider = wait.until(two_or_more_elements("strong"))

    return lista_av_tider[1].text, plats


sender_email = "DevGodTom1337@gmail.com"
receiver_email = "tom.rehnstrom@student.tabyenskilda.se"
message = """\
Subject: NY TID i {}

HEJ DETTA E ETT MEDDELANDE ATT JAG HITTAT EN NY TID {} i {}."""


def send_email(info):
    port = 465  # For SSL
    password = environ.get("EMAIL_PASS")

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("DevGodTom1337@gmail.com", password)
        server.sendmail(sender_email, receiver_email, message.format(info[1], info[0], info[1]))


if __name__ == '__main__':
    iterations = 0
    while iterations < 10000:
        with open("tid", "r+") as file:
            tidigaste = 0

            for i in ["Sollentuna", "Farsta", "Uppsala"]:
                tid, plats = main(i)
                date_tid = datetime.strptime(tid.strip(), "%Y-%m-%d %H:%M")
                if tidigaste == 0:
                    tidigaste = [date_tid, plats]
                elif date_tid < tidigaste[0]:
                    tidigaste = [date_tid, plats]

            file.seek(0)
            if tidigaste[0] < datetime.strptime(file.readline().strip(), "%Y-%m-%d %H:%M"):
                send_email(tidigaste)
                file.truncate()
                file.write(tidigaste[0].strftime("%Y-%m-%d %H:%M"))
                print("WIN", tidigaste[0].strftime("%Y-%m-%d %H:%M"))
            else:
                print("FAIL", tidigaste[0].strftime("%Y-%m-%d %H:%M"))

        iterations += 1
        sleep(60)

    driver.quit()

