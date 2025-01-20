"""Simple class to define a school period as an object."""

from datetime import date, datetime


class SchoolPeriod:
    """
    Simple class to define a school period as an object.
    """

    def __init__(self, start: date, end: date):
        """
        Build a SchoolPeriod object.
        :param start: The start date of the school period.
        :param end: The end date of the school period.
        """
        self.start = start
        self.end = end

    def in_date_range(self, date_to_compare: date) -> bool:
        """
        Check if a date is in the school period.
        :param date_to_compare: The date to compare.
        :return: True if the date is in the school period, False otherwise.
        """
        start_date = datetime.combine(self.start, datetime.min.time())
        end_date = datetime.combine(self.end, datetime.min.time())
        compare_date = datetime.combine(date_to_compare, datetime.min.time())
        return start_date <= compare_date <= end_date
