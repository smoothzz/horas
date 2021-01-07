import datetime

time = '13:30'
time_obj = datetime.datetime.strptime(time, '%H:%M')
time2 = '15:30'
time_obj2 = datetime.datetime.strptime(time2, '%H:%M')

result = time_obj2 - time_obj
print(time_obj.time())
print(time_obj2.time())
print(result)
