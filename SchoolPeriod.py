from datetime import date, datetime


class SchoolPeriod:
    def __init__(self, start: date, end: date):
        self.start = start
        self.end = end

    def in_date_range(self, date_to_compare: date):
        start_date = datetime.combine(self.start, datetime.min.time())
        end_date = datetime.combine(self.end, datetime.min.time())
        compare_date = datetime.combine(date_to_compare, datetime.min.time())
        return start_date <= compare_date <= end_date
