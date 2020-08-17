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
# find all class monhoc
# _______________________

for i in all_week:
    if i.text:
        print(i.text)
