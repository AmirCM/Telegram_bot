import jdatetime

x = jdatetime.datetime.now()

print(x.strftime("%x"), x.strftime('%X').split(':')[0:3])
