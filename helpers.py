from datetime import datetime


def datereader(date: str) -> str:
    try:
        new_date = datetime.strptime(date, "%m/%d/%Y").strftime("%Y-%m-%d")
        return new_date
    except:
        return date
