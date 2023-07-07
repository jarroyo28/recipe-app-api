"""
Test custom Django management commands.
"""
# Used to mock or replace certain functions or methods during testing
from unittest.mock import patch

# call_command is used to invoke Django management commands during testing
from django.core.management import call_command
# OperationalError is used to simulate an error when waiting for the DB
from django.db.utils import OperationalError
# Test Case Class that provides basic testing functionality
from django.test import SimpleTestCase
# Error class is used to simulate an error when waiting for the DB
from psycopg2 import OperationalError as Psycopg2Error


# patch decorator is used to mock the check method inside the
# core.management.commands.wait_for_db.Command class
# It patches the check command with a mock object
# (original implementation of the check method is temporarily replaced
# with a mock implementation during execution of the test)
@patch("core.management.commands.wait_for_db.Command.check")
class CommandTests(SimpleTestCase):
    """Test commands."""

    # Method takes two params: self (Instance of the test case) and
    # patched_check (mock object that is replacing the check method)
    # We take the mocked method and set its value to true
    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        patched_check.return_value = True

        # Invokes the custom Django management command named "wait_for_db"
        call_command('wait_for_db')

        # Asserts the mock has been called once with
        # the correct db configuration
        patched_check.assert_called_once_with(databases=['default'])

    # Note that when using patch, they go into arguments in order of inside out
    # (time.sleep is furthest inside so it goes first, then check)
    # All we're doing is raising Operational and Psycopg2 Errors
    # multiple times before returning true.
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError"""
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        # Asserting the patched_check mock has been called 6 times
        self.assertEqual(patched_check.call_count, 6)
        # Asserting it has been called at least once with the right argument
        patched_check.assert_called_with(databases=['default'])
