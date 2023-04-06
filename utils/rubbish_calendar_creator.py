import datetime

startDate = datetime.date.fromisoformat('2023-01-02')
endDate = datetime.date.fromisoformat('2023-11-30')
delta = datetime.timedelta(days=7)
rubbish=True

while True:
    print("    \'" + startDate.isoformat() + "\' : \'", end="")
    if rubbish:
        rubbish=False
        print("rubbish\' ,")
    else:
        rubbish=True
        print("recycle\' ,")

    startDate = startDate + delta
    if startDate > endDate:
        break
