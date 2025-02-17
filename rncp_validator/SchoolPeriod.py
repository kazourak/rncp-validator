"""Simple class to define a school period as an object."""

import random
from datetime import date, datetime, timedelta


class SchoolPeriod:
    """
    Simple class to define a school period as an object.
    """

    def __init__(self, start: datetime, end: datetime):
        """
        Build a SchoolPeriod object.
        :param start: The start date of the school period.
        :param end: The end date of the school period.
        """
        self.start = start
        self.end = end

    def in_date_range(self, date_to_compare: datetime) -> bool:
        """
        Check if a date is in the school period.
        :param date_to_compare: The date to compare.
        :return: True if the date is in the school period, False otherwise.
        """
        start_date = datetime.combine(self.start, datetime.min.time())
        end_date = datetime.combine(self.end, datetime.min.time())
        compare_date = datetime.combine(date_to_compare, datetime.min.time())
        return start_date <= compare_date <= end_date

    def random_date(self) -> datetime:
        """
        Generate a random date within the school period.
        :return: A random date between start and end.
        """
        delta_days = (self.end - self.start).days
        random_days = random.randint(0, delta_days)
        return self.start + timedelta(days=random_days)
