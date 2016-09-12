from trakt_tools.core.authentication import authenticate
from trakt_tools.tasks.backup.create.main import Download
import click


@click.command('backup:create')
@click.option('--token', default=None, help='Trakt.tv authentication token.')
@click.pass_context
def backup_create(ctx, token):
    "Create backup of a Trakt.tv profile."

    if not token:
        success, token = authenticate()

        if not success:
            print 'Authentication failed'
            exit(1)

    # Download data from profile
    task = Download(ctx.parent.backup_dir)
    task.run(token)
