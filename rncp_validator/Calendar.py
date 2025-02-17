"""
Simple class to convert a xlsx as a usable object.
"""

from datetime import datetime, time, timedelta

from openpyxl import workbook

from rncp_validator.SchoolPeriod import SchoolPeriod
from rncp_validator.tools import MONTH_TO_NB, to_date


class Calendar:
    """
    Simple class to convert a xlsx as a usable object.
    """

    def __init__(self, calendar_file: workbook):
        """
        Build the class object.
        :param calendar_file: The calendar as a workbook object.
        """
        self.calendar = calendar_file
        self.periods = []

    def get_periods(self):
        """
        Extract all the periods from the calendar.
        """
        for sheet in self.calendar.sheetnames:
            for column in self.calendar[sheet].iter_cols(
                min_row=6, max_row=38, min_col=1, max_col=12
            ):
                periods = []
                current_period = []
                prev_date = None

                for cell in column:
                    if cell.fill.bgColor.rgb == "0061b3ff" or cell.fill.bgColor.rgb == "002cf28f":
                        current_date = to_date(
                            MONTH_TO_NB[column[0].value],
                            cell.value.split()[1],
                            sheet,
                        )

                        if not current_period:
                            current_period.append(current_date)
                        elif prev_date and current_date == prev_date + timedelta(days=1):
                            current_period.append(current_date)
                        else:
                            periods.append((current_period[0], current_period[-1]))
                            current_period = [current_date]

                        prev_date = current_date

                if current_period:
                    periods.append((current_period[0], current_period[-1]))

                for start_date, end_date in periods:
                    self.periods.append(SchoolPeriod(start_date, end_date))

    def date_in_period(self, date_to_compare: datetime) -> bool:
        """
        Check if the given date is in the period.
        :param date_to_compare:
        :return: True if the date is in the period, False otherwise.
        """
        if not 8 <= date_to_compare.hour < 20:
            return False
        for period in self.periods:
            if period.in_date_range(date_to_compare):
                return True
        return False

    def nearest_date(self, target_date: datetime) -> datetime:
        """
        Find the nearest SchoolPeriod to a given date.

        :param target_date: The target date to compare.
        :return: The nearest SchoolPeriod object.
        """
        nearest_period = min(
            self.periods,
            key=lambda period: min(
                abs((period.start - target_date).days), abs((period.end - target_date).days)
            ),
        )

        closest_date = min(
            nearest_period.start, nearest_period.end, key=lambda d: abs((d - target_date).days)
        )

        # Convert it to a datetime with the time set to 10 AM
        return datetime.combine(closest_date, time(10, 0))
