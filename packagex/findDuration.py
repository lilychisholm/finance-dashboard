def findDuration(dataset, length):
    from datetime import datetime
    thirtyone = ['04', '06', '09', '11']
    thirty = ['01', '03', '05', '07', '08', '10', '12']
    count = 0
    days = 1
    today = datetime.now()
    for i in range(len(dataset)):
        today2 = str(today)[0:10].split('-')
        row = dataset.loc[i]
        if len(row['Date']) < 10:
            x = row['Date'].split('/')
            if len(x[0]) == 1:
                x[0] = '0' + x[0]
            if len(x[1]) == 1:
                x[1] = '0' + x[1]
            row['Date'] = x[0] + '/' + x[1] + '/' + x[2]
        rowList = row['Date'].split('/')
        if row['Date'][0:2] == str(today)[5:7]:
            x = int(str(today)[8:10]) - int(row['Date'][3:5])
            days += x
        else:
            toMonth = 0
            if row['Date'][0:2] in thirtyone:
                toMonth = 31 - int(row['Date'][3:5])
            elif row['Date'][0:2] in thirty:
                toMonth = 30 - int(row['Date'][3:5])
            else:
                toMonth = 28 - int(row['Date'][3:5])
            days += toMonth + int(str(today)[8:-1])
        today = row['Date'][6:10] + '-' + row['Date'][0:2] + '-' + row['Date'][3:5]
        if days > length:
            break
        count += 1
    return count