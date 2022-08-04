from bs4 import BeautifulSoup
import requests
import psycopg2
import datetime

conn = psycopg2.connect(database = "postgres", user = "postgres", password = "123456.", host = "host.docker.internal", port = "5432")

try:
    cur = conn.cursor()
    cur.execute("DROP TABLE EVENTS")
    conn.commit()
except:
    pass

conn.commit()
cur.execute('''CREATE TABLE EVENTS
      (ID SERIAL PRIMARY KEY     NOT NULL,
      TITLE           TEXT    NOT NULL,
      LOCATION            TEXT     NOT NULL,
      DATE        DATE,
      TIME        TIME,
      IMAGE_LINK  TEXT,
      ARTISTS     TEXT[],
      WORKS_LIST     TEXT[]);''')

conn.commit()


def insert_to_postgresql(title,date,time,location,performers_list,works_list,image_link):

    time = time.replace(".",":")
    date = datetime.datetime.strptime(date, '%d.%m.%Y').strftime('%m-%d-%Y')
    cur.execute(
        'INSERT INTO EVENTS (title,date, time, location, image_link, artists, works_list) VALUES (%s,%s, %s, %s, %s, %s, %s)',
        (title,date, time.replace(".",":"), location, image_link,performers_list, works_list))

    conn.commit()

def find_date_time_place(info_string):
    info_string = info_string[14:]
    info_string = info_string.strip()
    fields = info_string.split("|")
    date = fields[0]
    date = date[date.index(" ") + 1:-1] + "2022"
    time = fields[1].strip()
    #there are some cases like 10.00 / 11.00
    time = time[0:5]
    location = fields[2].strip()
    return date,time,location


def find_performers(performers_info):
    performer_list = []

    for performer in performers_info:
        performer = performer.find("strong").text.strip()
        performer_list.append(performer)

    return performer_list


def find_program(program_info):
    works_list = []

    for program_part in program_info:
        program_it = program_part.find_all("div", class_="program-item p")[1:]
        for program_item in program_it:
            program_item_list = program_item.text.split()
            work_info = " ".join(program_item_list)
            if work_info != "This concert has no intermission.":
                works_list.append(work_info)
    return works_list



html_text = requests.get("https://www.lucernefestival.ch/en/program/summer-festival-22").text
html_text = BeautifulSoup(html_text, "lxml")
events = html_text.find_all("p", class_="event-title h3")

for event in events:
    title = event.find(href=True).text
    event_page_url = "https://www.lucernefestival.ch/" + event.find(href=True)["href"]
    event_html = requests.get(event_page_url).text
    event_html = BeautifulSoup(event_html, "lxml")
    image_link = event_html.find("figure", class_="fullscreen-image").find("img")
    image_link = "https://www.lucernefestival.ch" + image_link["src"]
    general_info = event_html.find("div", class_="cell large-6 subtitle")
    general_info = str(general_info.text)
    date,time,location = find_date_time_place(general_info)
    performers_info = event_html.find_all("li", class_="cell medium-6 p")
    performers_list = find_performers(performers_info)
    program_info = event_html.find_all("div", class_="grid-x grid-margin-x align-right")
    works_list = find_program(program_info)
    insert_to_postgresql(title,date, time, location, performers_list, works_list, image_link)

cur = conn.cursor()
cur.execute("SELECT * from events")
print(cur.fetchall())
conn.close()