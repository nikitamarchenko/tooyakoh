__author__ = 'nmarchenko'

import unittest

from tooyakoh import Conveyor
from tooyakoh import ConveyorError
from tooyakoh import ConveyorFatalError
from tooyakoh import Command
from tooyakoh import CommandError
from tooyakoh import CommandState


class Ok(Command):
    def __str__(self):
        return "Always Ok Command"


class Failed(Command):

    def __str__(self):
        return "Always Failed Command"

    def execute(self):
        raise CommandError(Exception())


class FailedOnlyFirstCall(Command):

    def __init__(self):
        super(Command, self).__init__()
        self._first = True

    def __str__(self):
        return "Failed Only First Call"

    def execute(self):
        if self._first:
            self._first = False
        else:
            raise CommandError(Exception())


class FailedRevert(Command):

    def __str__(self):
        return "Failed Revert Command"

    def execute(self):
        raise CommandError(Exception())

    def revert(self):
        raise CommandError(Exception())


class FailedRevertNonFatal(Command):

    def __str__(self):
        return "Failed Revert Non Fatal Command"

    def execute(self):
        raise CommandError(Exception())

    def revert(self):
        raise CommandError(Exception())

    @property
    def failed_on_revert_is_fatal(self):
        return False


class FailedRevertOnlyFirstTime(Command):

    def __init__(self):
        super(Command, self).__init__()
        self._first = True

    def __str__(self):
        return "Failed Revert Only First Time"

    def execute(self):
        raise CommandError(Exception())

    def revert(self):
        if self._first:
            self._first = False
        else:
            raise CommandError(Exception())


class ConveyorTest(unittest.TestCase):

    def test_positive_0(self):
        conveyor = Conveyor([Ok(), Ok(), Ok()])
        conveyor.power_on()
        self.assertTrue(all([c.state == CommandState.Done for c in conveyor.commands]))

    def test_positive_1(self):
        conveyor = Conveyor([Ok(), FailedOnlyFirstCall(), Ok()])
        conveyor.power_on()
        self.assertTrue(all([c.state == CommandState.Done for c in conveyor.commands]))

    def _do(self, commands, exspected_states, exception):
        conveyor = Conveyor(commands)
        with self.assertRaises(exception):
            conveyor.power_on()
        states = [c.state for c in conveyor.commands]
        self.assertListEqual(exspected_states, states)

    def test_negative_0(self):
        self._do([Ok(), Ok(), Failed()],
                 [CommandState.Reverted]*3,
                 ConveyorError)

    def test_negative_1(self):
        self._do([Ok(), Failed(), Ok()],
                 [CommandState.Reverted, CommandState.Reverted, CommandState.New],
                 ConveyorError)

    def test_negative_3(self):
        self._do([Ok(), FailedRevertOnlyFirstTime(), Ok()],
                 [CommandState.Reverted, CommandState.Reverted, CommandState.New],
                 ConveyorError)

    def test_failed_revert_0(self):
        self._do([Ok(), FailedRevert(), Ok()],
                 [CommandState.Done, CommandState.ErrorOnRevert, CommandState.New],
                 ConveyorFatalError)

    def test_failed_revert_1(self):
        self._do([Ok(), FailedRevertNonFatal(), Ok()],
                 [CommandState.Reverted, CommandState.ErrorOnRevert, CommandState.New],
                 ConveyorError)
