from datetime import datetime
import locale

def get_formatted_datetime() -> str:
    now = datetime.now()
    return now.strftime("%A, %B %d, %Y %H:%M")
