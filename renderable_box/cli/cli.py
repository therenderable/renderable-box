import argparse

from .. import package


class CLI:
  def __init__(self, commands):
    self.commands = commands
    self.command_map = {type(command).__name__.lower(): command for command in self.commands}

  def build_parser(self):
    parser = argparse.ArgumentParser(description = 'Renderable container image application.')

    parser.add_argument('-v', '--version',
      help = 'show version', action = 'version', version = package.__version__)

    subparsers = parser.add_subparsers(dest = 'command', metavar = '<command>')

    for command in self.commands:
      command.build_parser(subparsers)

    return parser

  def run(self, logger):
    parser = self.build_parser()
    args = parser.parse_args()

    command = args.command

    if command is None:
      parser.print_usage()
    else:
      self.command_map[command].execute(args, logger)
