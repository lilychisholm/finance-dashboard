def chartSet(charty):
    if timeframe == 'Week':
        charty = data.head(findDuration(data, 7))
    elif timeframe == 'Month':
        charty = data.head(findDuration(data, 30))
    elif timeframe == 'Year':
        charty = data.head(findDuration(data, 365))
    else:
        charty = data

    charty = charty[(charty['Account Name'] == 'CHECKING')]