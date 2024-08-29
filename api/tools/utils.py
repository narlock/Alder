from datetime import datetime, timezone

class DateTimeUtils():

    @staticmethod
    def get_utc_date_now():
        now_utc = datetime.now(timezone.utc)
        d = now_utc.day
        mth = now_utc.month
        yr = now_utc.year
        string = f"{mth:02d}-{d:02d}-{yr}"
        return mth, d, yr, string
    
    @staticmethod
    def get_utc_month_year_now():
        now_utc = datetime.now(timezone.utc)
        mth = now_utc.month
        yr = now_utc.year
        return mth, yr