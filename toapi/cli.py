import click

from toapi import __version__


@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(__version__, '-v', '--version')
def cli():
    """
    Toapi - Every web site provides APIs.
    """
