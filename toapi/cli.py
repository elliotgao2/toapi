import importlib
import os
import sys

import click
from colorama import Fore

from toapi import __version__
from toapi.log import logger


@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(__version__, '-v', '--version')
def cli():
    """
    Toapi - Every web site provides APIs.
    """


@cli.command(name="new")
@click.argument('output_dir')
def new(output_dir):
    """Create a new Toapi project."""

    if os.path.exists(output_dir):
        logger.error('New project', 'Directory already exists.')
        return

    logger.info(Fore.GREEN, 'New project', 'Creating project directory "%s"' % output_dir)
    os.system('git clone https://github.com/toapi/toapi-template %s' % output_dir)
    os.system('rm -rf %s/.git' % output_dir)
    logger.info(Fore.GREEN, 'New project', 'Success!')
    click.echo('')
    click.echo('     cd %s' % output_dir)
    click.echo('     toapi run')
    click.echo('')


@cli.command(name="run")
@click.option('-a', '--addr',
              default='127.0.0.1:5000',
              help='IP and Port to serve documentation locally (default:"127.0.0.1:5000")',
              metavar='<IP:PORT>')
def run(addr):
    """Run app server."""
    base_path = os.getcwd()
    app_path = os.path.join(base_path, 'app.py')

    if not os.path.exists(app_path):
        logger.error('Run', 'Cannot find file "app.py"!')
        return

    try:
        ip, port = addr.split(':')
    except:
        logger.error('Run', 'The "addr" parameter should be like "IP:PORT"')
        return

    sys.path.append(base_path)
    app = importlib.import_module('app', base_path)
    app.api.serve(ip=ip, port=port)
