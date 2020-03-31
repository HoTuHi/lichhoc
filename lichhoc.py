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


SCOPES = ['https://www.googleapis.com/auth/calendar']

f = open("demofile.txt", "w")
xl = pd.ExcelFile('Report.xlsx')
x = dt.datetime.now()
df = pd.read_excel(xl, 0, header=None)
'''
    iloc[, 0] : mã MH
    iloc[, 5] : tên môn học
    iloc[, 11]: nhóm
    iloc[, 25]: thứ
    iloc[, 27]: tiết BĐ
    iloc[, 33]: phòng
    iloc[, 39]: thời gian học( tuan )
    cột bắt đầu từ 2- 18
    '''
print(x)
thgian1 = ['7:20:00', '9:20:00',
           '12:20:00', '14:20:00', '16:20:00', '19:20:00']
thgian2 = ['7:25:00', '9:25:00',
           '12:25:00', '14:25:00', '16:25:00', '19:25:00']


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
    # tuan = int(x.strftime("%W")) - 12
    # gio = x.strftime("%H:%M")
    # tuan bat dau la tuan 13 cua mam
    for i in range(2, 19):
        for j in range(0, len(df.loc[i, 39])):
            if df.loc[i, 39][j] != '-':
                # thời gian
                tgian1 = thgian1[int(int(df.iloc[i, 27]) / 2)]
                tgian2 = thgian2[int(int(df.iloc[i, 27]) / 2)]
                # ngày tháng năm
                dung = x + dt.timedelta(weeks=j - 1,
                                        days=int(df.iloc[i, 25]) - 3)
                day = dung.strftime("%Y-%m-%d")
                # lời nhắn
                text = day + " " + str(tgian1) + " học " + \
                    df.iloc[i, 5] + " tại " + df.iloc[i, 33]
                event = {
                    'summary': df.iloc[i, 5],
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
                f.write(json.dumps(event))


if __name__ == '__main__':
    mess()
