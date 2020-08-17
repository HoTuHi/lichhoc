from __future__ import print_function
import pandas as pd
import datetime as dt
import json
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from bs4 import BeautifulSoup
import codecs


# element
subject = {"class": "s15c47abe", "colspan": "6"}
room = {"class": "s8b00c82e", "colspan": "6"}
start = {"class": "s8b00c82e", "style": "height:20px;width:42px;"}
onweek = {"class": "s83bee661", "colspan": "7"}
onday = {"class": "s8b00c82e", "colspan": "2"}

req = codecs.open("Report.html", 'r', 'utf-8')
soup = BeautifulSoup(req.read(), "html5lib")
x = soup.findAll('td')[12]

# _______________________
# find all class monhoc
# _______________________

all_subject = soup.find_all('td', subject)
all_room = soup.find_all('td', room)
all_start = soup.find_all('td', start)
all_week = soup.find_all('td', onweek)
all_day = soup.find_all('td', onday)

# _______________________


SCOPES = ['https://www.googleapis.com/auth/calendar']

x = dt.datetime.now()
print(x)
thgian1 = ['6:30:00', '8:30:00',
           '11:30:00', '13:30:00', '15:30:00', '17:30:00']
thgian2 = ['8:30:00', '11:30:00',
           '13:30:00', '15:30:00', '17:30:00', '19:30:00']


def mess():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    thu = int(x.strftime("%w")) + 1
    if thu == 1:
        thu = 8
    """ thu 2 la ngay dau buoi, cn la ngay 0,ptit k hoc chu nhat,
        công thức là cộng 1 thôi hé """
    # tuan bat dau la tuan 13 cua mam
    for i in range(0,len(all_week)):
        for j in range(0, len(all_week[i].text)):
            if all_week[i].text[j] != '-':
                # thời gian
                tgian1 = thgian1[int(int(all_start[i].text) / 2)]
                tgian2 = thgian2[int(int(all_start[i].text) / 2)]
                # ngày tháng năm
                dung = x + dt.timedelta(weeks=j +3,
                                        days=int(all_day[i].text) - 2)
                day = dung.strftime("%Y-%m-%d")
                # lời nhắn
                text = day + " " + str(tgian1) + " học " + \
                    all_subject[i].text + " tại " + all_room[i].text
                event = {
                    'summary': all_subject[i].text,
                    'location': 'home',
                    'description': text,
                    'start': {
                        'dateTime': day + 'T' + tgian1 + '+07:00',
                        'timeZone': 'Asia/Ho_Chi_Minh',
                    },
                    'end': {
                        'dateTime': day + 'T' + tgian2 + '+07:00',
                        'timeZone': 'Asia/Ho_Chi_Minh',
                    },
                    'recurrence': [
                        'RRULE:FREQ=DAILY;COUNT=1'
                    ],
                }
                event = service.events().insert(calendarId='primary', body=event).execute()
                print('Event created: %s' % (event.get('htmlLink')))
                print(text)
                # f.write(json.dumps(event))


if __name__ == '__main__':
    mess()
