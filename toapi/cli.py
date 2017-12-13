import os

import click

from toapi.log import logger


@click.group(context_settings={'help_option_names': ['-h', '--help']})
def cli():
    """
    Toapi - Every web site provides APIs.
    """


@cli.command(name="new")
@click.argument('output_dir')
def new(output_dir):
    """Create a new Toapi project"""

    if os.path.exists(output_dir):
        logger.warning('Directory already exists.')
        return

    logger.error('Creating project directory: %s', output_dir)
    logger.info('Success!')


@cli.command(name="run")
@click.option('-a', '--addr',
              help='IP and Port to serve documentation locally (default:"127.0.0.1:8000")',
              metavar='<IP:PORT>')
def run(addr="127.0.0.1:5000"):
    """Run the builtin development server"""
    base_path = os.getcwd()
    app_path = os.path.join(base_path, 'app.py')

    if not os.path.exists(app_path):
        return logger.error('Cannot find file "app.py"!')

    try:
        ip, port = addr.split(':')
    except:
        return logger.error('The "addr" parameter should be like "IP:PORT"')

    try:
        app = getattr(module, 'app')
    except:
        return logger.error('The "app.py" should contains a Api instance')

    print(app.__dict__)
