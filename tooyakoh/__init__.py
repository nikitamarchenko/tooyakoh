__author__ = 'nmarchenko'

from enum import Enum


class ConveyorError(Exception):
    pass


class ConveyorFatalError(Exception):
    pass


class Conveyor(object):

    def __init__(self, commands):
        self._commands = commands

    def power_on(self):
        if not self._headway():
            self._revert()

    def _headway(self):
        for i, command in enumerate(self._commands):
            while True:
                try:
                    command.execute()
                except CommandError as ex:
                    command.state = CommandState.Error
                    if not command.can_retry_execute:
                        return False
                else:
                    command.state = CommandState.Done
                    break
        return True

    def _revert(self):
        for i, command in reversed(list(enumerate(self._commands))):
            if command.state != CommandState.New:
                while True:
                    try:
                        command.revert()
                    except CommandError as ex:
                        command.state = CommandState.ErrorOnRevert
                        if command.can_retry_revert:
                            continue
                        elif command.failed_on_revert_is_fatal:
                            raise ConveyorFatalError()
                        else:
                            break
                    else:
                        command.state = CommandState.Reverted
                        break

        raise ConveyorError()

    @property
    def commands(self):
        return self._commands


class CommandError(Exception):
    def __init__(self, exception):
        super(Exception, self).__init__()
        self._exception = exception

    def __str__(self):
        return str(self._exception)

    @property
    def inner_exception(self):
        return self._exception


class CommandState(Enum):
    New = 1
    Done = 2
    Reverted = 3
    Error = 4
    ErrorOnRevert = 5


class Command(object):

    def __init__(self):
        self._state = CommandState.New

    def execute(self):
        pass

    def revert(self):
        pass

    @property
    def state(self):
        return self._state

    @property
    def failed_on_revert_is_fatal(self):
        return True

    @state.setter
    def state(self, value):
        self._state = value

    @property
    def can_retry_execute(self):
        return False

    @property
    def can_retry_revert(self):
        return False
