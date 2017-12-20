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
@click.argument('dir_or_project')
def new(dir_or_project):
    """Create a new Toapi project.

    Giving a dir means start a default template,

    Example: toapi new api

    Giving a github project means start a github template.

    Example: toapi new toapi/toapi-one
    """

    if '/' in dir_or_project:
        dir_name = dir_or_project.split('/')[-1]
        logger.info(Fore.GREEN, 'New project', 'Creating project directory "%s"' % dir_name)
        os.system('git clone https://github.com/%s %s' % (dir_or_project, dir_name))
        os.system('rm -rf %s/.git' % dir_name)
        logger.info(Fore.GREEN, 'New project', 'Success!')
        click.echo('')
        click.echo('     cd %s' % dir_name)
        click.echo('     toapi run')
        click.echo('')

    else:
        if dir_or_project != '.' and os.path.exists(dir_or_project):
            logger.error('New project', 'Directory already exists.')
            return

        logger.info(Fore.GREEN, 'New project', 'Creating project directory "%s"' % dir_or_project)
        os.system('git clone https://github.com/toapi/toapi-template %s' % dir_or_project)
        os.system('rm -rf %s/.git' % dir_or_project)
        logger.info(Fore.GREEN, 'New project', 'Success!')
        click.echo('')
        click.echo('     cd %s' % dir_or_project)
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
    except Exception:
        logger.error('Run', 'The "addr" parameter should be like "IP:PORT"')
        return
    port = int(port)
    sys.path.append(base_path)
    app = importlib.import_module('app', base_path)
    app.api.serve(ip=ip, port=port)
