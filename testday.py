import datetime as dt

x = dt.datetime.now()
a = x + dt.timedelta(weeks=2, days= - 2)
print(a)
print(a.strftime("%A"))
