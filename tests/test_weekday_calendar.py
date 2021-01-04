from unittest import TestCase

import pandas as pd
from pytz import UTC

from trading_calendars.weekday_calendar import WeekdayCalendar
from trading_calendars.utils.pandas_utils import testing
from .test_trading_calendar import ExchangeCalendarTestBase

assert_index_equal = testing.assert_index_equal


class WeekdayCalendarTestCase(ExchangeCalendarTestBase, TestCase):

    answer_key_filename = '24-5'
    calendar_class = WeekdayCalendar
    start_date = pd.Timestamp('2018-01-01', tz=UTC)
    end_date = pd.Timestamp('2018-12-31', tz=UTC)
    MAX_SESSION_HOURS = 24
    GAPS_BETWEEN_SESSIONS = False
    HAVE_EARLY_CLOSES = False

    MINUTE_INDEX_TO_SESSION_LABELS_START = pd.Timestamp('2018-01-01', tz=UTC)
    MINUTE_INDEX_TO_SESSION_LABELS_END = pd.Timestamp('2018-04-04', tz=UTC)

    DAYLIGHT_SAVINGS_DATES = ['2018-04-05', '2018-11-01']

    def get_session_block(self):
        # This range is chosen specifically because it is "enclosed" by
        # adjacent days that are also sessions. This prevents any edge case
        # issues when looking at market opens or closes.
        return self.calendar.all_sessions[1:4]

    def test_open_every_weekday(self):
        calendar = self.calendar

        dates = pd.date_range(self.start_date, self.end_date, tz=UTC)
        assert_index_equal(
            calendar.sessions_in_range(dates[0], dates[-1]),
            # The pandas weekday is defined as Monday=0 to Sunday=6.
            dates[dates.weekday <= 4],
        )

    def test_open_every_weekday_minute(self):
        calendar = self.calendar

        minutes = pd.date_range(
            self.start_date,
            # Our calendar should include all the minutes of this last session.
            self.end_date + pd.Timedelta('1 Day') - pd.Timedelta('1 Minute'),
            freq='min',
            tz=UTC,
        )
        assert_index_equal(
            calendar.minutes_for_sessions_in_range(
                self.start_date,
                self.end_date,
            ),
            # The pandas weekday is defined as Monday=0 to Sunday=6.
            minutes[minutes.weekday <= 4],
        )
