__author__ = 'nmarchenko'

import sys
import getopt

import zerorpc

import common


class ServerRPC(object):

    def start_new_conveyor(self):
        commands = [common.Ok(), common.Failed(), common.Ok()]
        conveyor = common.Conveyor(commands)
        try:
            conveyor.power_on()
            return conveyor._commands
        finally:
            print 'Server Commands'
            for i, c in enumerate(conveyor.commands):
                print i, c, c.state

    def rollback_conveyor(self):
        pass


def server():
    s = zerorpc.Server(ServerRPC())
    s.bind("tcp://127.0.0.1:4242")
    s.run()


class RpcCall(common.Command):

    def __str__(self):
        return 'Rpc Call Command'

    def execute(self):
        try:
            c = zerorpc.Client()
            c.connect("tcp://127.0.0.1:4242")
            self.commands = c.start_new_conveyor()
        except Exception as ex:
            raise common.CommandError(ex)

    def revert(self):
        try:
            c = zerorpc.Client()
            c.connect("tcp://127.0.0.1:4242")
            c.rollback_conveyor(self.commands)
        except Exception as ex:
            raise common.CommandError(ex)


def client():
    commands = [common.Ok(), RpcCall(), common.Ok()]
    conveyor = common.Conveyor(commands)
    try:
        conveyor.power_on()
    finally:
        print 'Client Commands'
        for i, c in enumerate(conveyor.commands):
            print i, c, c.state


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "cs", ["client", "server"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-c", "--client"):
            client()
            sys.exit()
        if opt in ("-s", "--server"):
            server()
            sys.exit()


def usage():
    print 'run rpc with -s for server or -c for client'


if __name__ == "__main__":
    main(sys.argv[1:])