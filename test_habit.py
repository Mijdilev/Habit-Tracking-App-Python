# test_habit.py
import pytest
from datetime import datetime, timedelta
from habit import Habit


class TestHabit:

    def setup_method(self):
        self.today = datetime.today()
        self.habit = Habit("Exercise", "daily", self.today)

    def test_initialization_valid(self):
        assert self.habit.name == "Exercise"
        assert self.habit.periodicity == "daily"
        assert self.habit.start_date == self.today
        assert self.habit.completion_dates == []

    def test_initialization_invalid_name(self):
        with pytest.raises(ValueError):
            Habit("", "daily", self.today)

    def test_initialization_invalid_periodicity(self):
        with pytest.raises(ValueError):
            Habit("Exercise", "", self.today)

    def test_initialization_invalid_start_date(self):
        with pytest.raises(ValueError):
            Habit("Exercise", "daily", "2023-01-01")  # Not a datetime object

    def test_mark_completed_valid(self):
        self.habit.mark_completed(self.today + timedelta(days=1))
        assert len(self.habit.completion_dates) == 1

    def test_mark_completed_invalid_type(self):
        with pytest.raises(ValueError):
            self.habit.mark_completed("2024-01-01")  # Not a datetime object

    def test_mark_completed_before_start(self):
        with pytest.raises(ValueError):
            self.habit.mark_completed(self.today - timedelta(days=1))

    def test_get_longest_streak_daily(self):
        self.habit.mark_completed(self.today)
        self.habit.mark_completed(self.today + timedelta(days=1))
        self.habit.mark_completed(self.today + timedelta(days=2))
        assert self.habit.get_longest_streak() == 3

    def test_get_longest_streak_weekly(self):
        weekly_habit = Habit("Jog", "weekly", self.today)
        weekly_habit.mark_completed(self.today)
        weekly_habit.mark_completed(self.today + timedelta(days=6))
        weekly_habit.mark_completed(self.today + timedelta(days=12))
        assert weekly_habit.get_longest_streak() == 3

    def test_get_longest_streak_monthly(self):
        monthly_habit = Habit("Report", "monthly", datetime(2024, 1, 1))
        monthly_habit.mark_completed(datetime(2024, 1, 5))
        monthly_habit.mark_completed(datetime(2024, 1, 20))
        monthly_habit.mark_completed(datetime(2024, 2, 5))
        assert monthly_habit.get_longest_streak() == 2

    def test_get_streak_duration_string(self):
        assert self.habit.get_streak_duration_string(5) == "5 day(s)"

    def test_edit_habit_name_and_periodicity(self):
        self.habit.edit_habit(name="Read", periodicity="weekly")
        assert self.habit.name == "Read"
        assert self.habit.periodicity == "weekly"

    def test_edit_habit_start_date_removes_old_completions(self):
        self.habit.mark_completed(self.today + timedelta(days=1))
        new_start = self.today + timedelta(days=2)
        self.habit.edit_habit(start_date=new_start)
        assert all(date >= new_start for date in self.habit.completion_dates)

    def test_repr_output(self):
        output = repr(self.habit)
        assert isinstance(output, str)
        assert "Habit(name=" in output


