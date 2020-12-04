import argparse
from pathlib import Path

from renderable_core.models import State, TaskMessage
from renderable_core.services import Configuration, APIClient, Renderer, WorkQueue, Executor


class Render:
  def build_parser(self, subparsers):
    parser = subparsers.add_parser('render', description = 'Renderable command to process rendering tasks.',
      help = 'render tasks from queue')

    parser.add_argument('-c', '--command_template',
      help = 'command template for renderer application', type = str, required = True)

    parser.add_argument('-t', '--temporary_directory',
      help = 'temporary resource directory, default is "/data/renderable-box/"',
      type = str,
      default = '/data/renderable-box/')

    parser.add_argument('-f', '--cache_factor',
      help = 'resource cache factor, default is 0.75', type = float, default = 0.75)

    return parser

  def execute(self, args, logger):
    command_template = args.command_template
    temporary_directory = args.temporary_directory
    cache_factor = args.cache_factor

    configuration = Configuration(Path('/run/secrets/'))

    container_name = configuration.get('CONTAINER_NAME')
    api_secure = configuration.get('API_SECURE') == 'on'

    if container_name == 'renderable-box':
      logger.error('cannot process tasks from abstract container.')
      exit(1)

    client = APIClient(
      configuration.get('API_HOSTNAME'),
      configuration.get('API_PORT'),
      configuration.get('API_VERSION'),
      api_secure,
      configuration.get('API_ACCESS_KEY'),
      temporary_directory)

    renderer = Renderer(command_template, temporary_directory, cache_factor)

    task_queue = WorkQueue(
      configuration.get('TASK_QUEUE_HOSTNAME'),
      configuration.get('TASK_QUEUE_PORT'),
      configuration.get('TASK_QUEUE_USERNAME'),
      configuration.get('TASK_QUEUE_PASSWORD'))

    executor = Executor()

    def callback(channel, method, task_message):
      executor.begin_atomic()

      try:
        task = client.get_task(task_message.id)

        if task.state in [State.ready, State.running]:
          logger.info(f'processing task "{task.id}"...')

          if client.update_task_state(task, State.running):
            if not renderer.has_cache(task):
              client.download_task_resource(task)

            renderer.render(task)

            task = client.get_task(task_message.id)

            if task.state == State.running:
              client.upload_task_resources(task)
              client.update_task_state(task, State.done)

              logger.info('task done.')
            else:
              logger.info('task already completed.')

            renderer.delete_cache(task)
          else:
            logger.info('task error.')
        else:
          logger.warning(f'skipping invalid task {task.id}...')

        channel.basic_ack(delivery_tag = method.delivery_tag)
      except:
        logger.warning(f'failed to process task.')
        logger.info(f'rescheduling...')

        channel.basic_nack(delivery_tag = method.delivery_tag)

      executor.end_atomic()

    logger.info('starting...')

    executor.run(task_queue.consume, callback, container_name, TaskMessage)

    logger.info('exiting...')
