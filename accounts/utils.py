from lunar_python import Lunar, Solar
from datetime import date, time, datetime # Import datetime

def convert_gregorian_to_lunar(gregorian_date: date, gregorian_time: time = None):
    """
    Converts a Gregorian date and optional time to Lunar date and Chinese hour (時辰).

    Args:
        gregorian_date (datetime.date): The Gregorian date.
        gregorian_time (datetime.time, optional): The Gregorian time. Defaults to None.

    Returns:
        tuple: A tuple containing (lunar_date_str, lunar_time_str).
               lunar_date_str: Lunar date in YYYY年MM月DD日 format.
               lunar_time_str: Chinese hour (時辰) or "吉時" if time is None.
    """
    # Create a datetime object from date and time for Solar.fromYmdHms
    # If no time, use a default time (e.g., midnight) for conversion,
    # but the shichen will be "吉時" if gregorian_time is None
    if gregorian_time:
        hour = gregorian_time.hour
        minute = gregorian_time.minute
        second = gregorian_time.second
    else:
        hour = 0
        minute = 0
        second = 0

    solar = Solar.fromYmdHms(
        gregorian_date.year,
        gregorian_date.month,
        gregorian_date.day,
        hour,
        minute,
        second
    )
    lunar = solar.getLunar()

    lunar_date_str = f"{lunar.getYearInChinese()}年{lunar.getMonthInChinese()}月{lunar.getDayInChinese()}日"

    lunar_time_str = "吉時"
    if gregorian_time:
        # Get the EightChar object and then the time (時辰地支)
        eight_char = lunar.getEightChar()
        ganzhi_shichen = eight_char.getTime() # This gives the GanZhi of the hour (e.g., "己丑")
        
        # Extract the Earthly Branch (second character) and append "時"
        if len(ganzhi_shichen) == 2:
            lunar_time_str = f"{ganzhi_shichen[1]}時"
        else:
            # Fallback if format is unexpected
            lunar_time_str = ganzhi_shichen

    return lunar_date_str, lunar_time_str