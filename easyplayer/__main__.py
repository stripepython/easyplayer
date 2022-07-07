"""
This is Easy Player's __main__.py
Command line program for easy player.

The function is to download mblock pictures or view versions.
"""

import shutil

import click

from easyplayer.version import version
from easyplayer.utils.mblock import clear, install


def _show_version(ctx, _, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(version.get_string())
    ctx.exit()
    
    
def _install_images(ctx, *_):
    if ctx.resilient_parsing:
        return
    try:
        install()
    except KeyboardInterrupt:   # The users can use Ctrl+c to interrupt the program.
        click.echo('ERROR: Keyboard interrupt.')
        ctx.exit()
    ctx.exit()
    

def _clear_images(ctx, *_):
    if ctx.resilient_parsing:
        return
    clear()
    ctx.exit()
    
    
def _uninstall_images(ctx, *_):
    if ctx.resilient_parsing:
        return
    try:
        shutil.rmtree('downloads')
    except OSError:
        click.echo('ERROR: not installed mblock-images')
    else:
        click.echo('INFO: deleted downloads')
    ctx.exit()


@click.command()
@click.option('--version', '-v', is_flag=True, callback=_show_version,
              expose_value=False, is_eager=True, help='View version information.')
@click.option('--install-images', '-i', is_flag=True, callback=_install_images,
              expose_value=False, is_eager=False, help='Install mblock picture.')
@click.option('--clear-images', '-c', is_flag=True, callback=_clear_images,
              expose_value=False, is_eager=False, help='Clear mblock picture.')
@click.option('--uninstall-images', '-u', is_flag=True, callback=_uninstall_images,
              expose_value=False, is_eager=False, help='Uninstall mblock picture.')
def main():
    click.echo()
            

if __name__ == '__main__':
    main()
