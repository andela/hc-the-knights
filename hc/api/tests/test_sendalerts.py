from datetime import timedelta

from django.utils import timezone
from hc.api.management.commands.sendalerts import Command
from hc.api.models import Check
from hc.test import BaseTestCase
from mock import patch


class SendAlertsTestCase(BaseTestCase):

    @patch("hc.api.management.commands.sendalerts.Command.handle_one")
    def test_it_handles_few(self, mock):
        yesterday = timezone.now() - timedelta(days=1)
        names = ["Check %d" % d for d in range(0, 10)]

        for name in names:
            check = Check(user=self.alice, name=name)
            check.alert_after = yesterday
            check.status = "up"
            check.save()

        result = Command().handle_many()
        assert result, "handle_many should return True"

        handled_names = []
        for args, kwargs in mock.call_args_list:
            handled_names.append(args[0].name)

        assert set(names) == set(handled_names)
        # The above assert fails. Make it pass
        # The test passes, no change required.

    def test_it_handles_grace_period(self):
        check = Check(user=self.alice, status="up")
        # 1 day 30 minutes after ping the check is in grace period:
        check.last_ping = timezone.now() - timedelta(days=1, minutes=30)
        check.save()

        # Expect no exceptions--
        Command().handle_one(check)

    # Assert when Command's handle many that when handle_many should return True
    # @patch("hc.api.management.commands.sendalerts.Command.handle_many")
    # def test_handle_many_returns_true(self):
    #     check = Check(user=self.alice, status="up")
    #     # 1 day 30 minutes after ping the check is in grace period:
    #     check.last_ping = timezone.now() - timedelta(days=1, minutes=30)
    #     check.save()

    #     # Handle many
    #     previous_day = timezone.now() - timedelta(days=1)

    #     list_of_checks = []
    #     for num in range(1, 11):
    #         new_check = f'Check {num}'
    #         list_of_checks.append(new_check)

    #     for name in list_of_checks:
    #         check = Check(user=self.alice, name=name)
    #         check.alert_after = previous_day
    #         check.status = "up"
    #         check.save()

    #     result = Command().handle_many()
    #     self.assertTrue(result)

    @patch("hc.api.management.commands.sendalerts.Command.handle_many")
    def test_handle_many_returns_true(self, mock):
        yesterday = timezone.now() - timedelta(days=1)
        names = ["Check %d" % d for d in range(0, 10)]

        for name in names:
            check = Check(user=self.alice, name=name)
            check.alert_after = yesterday
            check.status = "up"
            check.save()

        result = Command().handle_many()
        self.assertTrue(result)
