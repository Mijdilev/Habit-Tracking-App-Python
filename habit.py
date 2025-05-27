# habit.py
from datetime import datetime

class Habit:
    """
    Represents a single habit, which user decided to track.
    """
    def __init__(self, name, periodicity, start_date):

        """ Initializes a Habit object.

        Params:
            name (str): The name of the habit.
            periodicity (str): The periodicity of the habit (e.g., "daily", "weekly", "monthly").
            start_date (date): The date when the habit tracking started."""

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Habit name must be a non-empty string.")
        if not isinstance(periodicity, str) or not periodicity.strip():
            raise ValueError("Habit periodicity must be a non-empty string.")
        if not isinstance(start_date, datetime):
            raise ValueError("Start date must be a datetime object.")

        self.name = name
        self.periodicity = periodicity
        self.start_date = start_date
        self.completion_dates = []

    def mark_completed(self, date):
        """
        Marks the habit as completed on the date provided by user.

        Params:
            date (date): The date of completion.
        """
        if not isinstance(date, datetime):
            raise ValueError("Completion date must be a datetime object.")
        if date < self.start_date:
            raise ValueError("Completion date cannot be earlier than the start date.")
        self.completion_dates.append(date)

    def get_completion_dates(self):
        """
        Returns the completion dates of the habit.
        """
        return self.completion_dates

    def get_longest_streak(self):
        """
        Calculates the longest consecutive streak of habit completion,
        considering the habit's periodicity.

        Returns:
            int: The longest streak.
        """
        if not self.completion_dates:
            return 0

        sorted_dates = sorted(self.completion_dates)
        current_streak = 1
        longest_streak = 1

        if self.periodicity == "daily":
            for i in range(1, len(sorted_dates)):
                if (sorted_dates[i] - sorted_dates[i - 1]).days == 1:
                    current_streak += 1
                    longest_streak = max(longest_streak, current_streak)
                else:
                    current_streak = 1
        elif self.periodicity == "weekly":
            for i in range(1, len(sorted_dates)):
                if (sorted_dates[i] - sorted_dates[i - 1]).days <= 7:  # Changed to <= 7 for weekly
                    current_streak += 1
                    longest_streak = max(longest_streak, current_streak)
                else:
                    current_streak = 1
        elif self.periodicity == "monthly":
            for i in range(1, len(sorted_dates)):
                if sorted_dates[i].year == sorted_dates[i - 1].year and sorted_dates[i].month == sorted_dates[i - 1].month:
                    current_streak += 1
                    longest_streak = max(longest_streak, current_streak)
                else:
                    current_streak = 1
        else:
                       raise ValueError(f"Unsupported periodicity: {self.periodicity}") # Code will rise an error
                       # if periodicity is different from the defined periodicity types

        return longest_streak

    def get_streak_duration_string(self, streak):
        """
        Gets the streak duration string based on periodicity. For proper streak displaying for habits
        with defferent periodicities.

        Params:
            streak (int): The streak value.

        Returns:
            str: The streak duration string (e.g., "days", "weeks", "months").
        """
        if self.periodicity == "daily":
            return f"{streak} day(s)"
        elif self.periodicity == "weekly":
            return f"{streak} week(s)"
        elif self.periodicity == "monthly":
            return f"{streak} month(s)"
        else:
            return f"{streak} (units)"  # Just default placeholder, if everething goes as planned this shoudn't happen

    def edit_habit(self, name=None, periodicity=None, start_date=None):
        """
        Updates habit details, based on new information from user.

        Params:
            name (str, optional): The new name of the habit. Defaults to None.
            periodicity (str, optional): The new periodicity of the habit. Defaults to None.
            start_date (date, optional): The new start date of the habit. Defaults to None.
        """
        if name is not None:
            if not isinstance(name, str) or not name.strip():
                raise ValueError("Habit name must be a non-empty string.")
            self.name = name
        if periodicity is not None:
            if not isinstance(periodicity, str) or not periodicity.strip():
                raise ValueError("Habit periodicity must be a non-empty string.")
            self.periodicity = periodicity
        if start_date is not None:
            if not isinstance(start_date, datetime):
                raise ValueError("Start date must be a datetime object.")
            self.start_date = start_date
            if self.completion_dates and any(date < start_date for date in self.completion_dates):
                self.completion_dates = [date for date in self.completion_dates if date >= start_date]

    def __repr__(self):
        """
        Returns a string representation of the Habit object.
        """

        return f"Habit(name='{self.name}', periodicity='{self.periodicity}', start_date='{self.start_date.strftime('%Y-%m-%d')}')"
