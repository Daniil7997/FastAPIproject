from datetime import datetime, timedelta


def get_time_for_jwt(now: datetime,
                     minutes: int = 0, 
                     hours: int = 0, 
                     days: int = 0) -> int:
    get_minutes = timedelta(minutes=minutes).total_seconds()
    get_hours = timedelta(hours=hours).total_seconds()
    get_days = timedelta(days=days).total_seconds()
    result = int(now + get_days + get_hours + get_minutes)
    return result
