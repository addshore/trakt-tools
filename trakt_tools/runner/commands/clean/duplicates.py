from trakt_tools.core.authentication import authenticate
from trakt_tools.tasks.clean.duplicates.main import CleanDuplicatesTask
import click


@click.command('clean:duplicates', )
@click.option('--token', default=None, help='Trakt.tv authentication token.')
@click.option('--delta-max', default=10 * 60, help='Maximum delta between history records to consider as duplicate (in seconds) (default: 600)')
@click.option('--backup/--no-backup', default=None, help='Backup profile before applying any changes')
@click.option('--review/--no-review', default=None, help='Review each action before applying them')
@click.pass_context
def clean_duplicates(ctx, token, delta_max, backup, review):
    "Remove duplicate scrobbles from a Trakt.tv profile."

    if not token:
        success, token = authenticate()

        if not success:
            print 'Authentication failed'
            exit(1)

    # Run task
    success = CleanDuplicatesTask(
        ctx.parent.backup_dir,
        ctx.parent.rate_limit,
        delta_max
    ).run(
        token=token,
        backup=backup,
        review=review
    )

    if not success:
        exit(1)
