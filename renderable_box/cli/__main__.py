import logging

from . import commands, CLI


def main():
  logging.basicConfig()

  logger = logging.getLogger('renderable-box')
  logger.setLevel(logging.INFO)

  subcommands = [
    commands.Render(),
  ]

  cli = CLI(subcommands)
  cli.run(logger)


if __name__ == '__main__':
  main()
