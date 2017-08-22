from datetime import datetime
def date(bad_date):
    if not bad_date: return bad_date
    good_date = datetime.strptime(bad_date, "%Y-%m-%d")
    return good_date.timestamp()
