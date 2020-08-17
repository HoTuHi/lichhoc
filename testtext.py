from __future__ import print_function
import datetime as dt
import datetime
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
x = dt.datetime.now()
print(x)
thgian1 = ['6:30:00', '8:30:00',
           '11:30:00', '13:30:00', '15:30:00', '17:30:00']
thgian2 = ['8:30:00', '11:30:00',
           '13:30:00', '15:30:00', '17:30:00', '19:30:00']


def mess():
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
                print(text)


if __name__ == '__main__':
    mess()
