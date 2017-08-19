from datetime import datetime
def date(badDate):
    if not badDate: return badDate
    goodDate = datetime.strptime(badDate, "%Y-%m-%d")
    return goodDate.timestamp()
