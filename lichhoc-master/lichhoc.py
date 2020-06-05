from __future__ import print_function
import pandas
import datetime as dt
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SCOPES = ['https://www.googleapis.com/auth/calendar']

xl = pandas.ExcelFile('Report.xls')
df = pandas.read_excel(xl, 0, header=None)
x = dt.datetime.now()
print((df.iloc[28,28]))
'''
    iloc[, 1] : mã MH
    iloc[, 6] : tên môn học
    iloc[, 12]: nhóm
    iloc[, 26]: thứ
    iloc[, 28]: tiết BĐ
    iloc[, 34]: phòng
    iloc[, 40]: thời gian học( tuan )
    cột bắt đầu từ 11- 30
    '''
print(x)
thgian1 = ['7:00:00', '9:00:00',
           '12:00:00', '14:00:00', '16:00:00', '18:00:00']
thgian2 = ['8:50:00', '10:50:00',
           '13:50:00', '15:50:00', '17:50:00', '19:50:00']

def mess():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
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
    for i in range(13, 30):
        for j in range(0, len(str(df.loc[i, 40]))):
            if str(df.loc[i, 40])[j] != '-':
                # thời gian
                tgian1 = thgian1[int(int(df.iloc[i, 28]) / 2)]
                tgian2 = thgian2[int(int(df.iloc[i, 28]) / 2)]
                # ngày tháng năm
                dung = x + dt.timedelta(weeks=j - 10,
                                        days=int(df.iloc[i, 26]) - 6)
                day = dung.strftime("%Y-%m-%d")
                # lời nhắn
                text = day + " " + str(tgian1) + " học " + \
                    df.iloc[i, 6] + " tại " + df.iloc[i, 34]
                event = {
                    'summary': df.iloc[i, 6],
                    'location': df.iloc[i, 34],
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
