import click
from ckan import model
from ckan.plugins import toolkit

from ckanext.ark.lib.helpers import build_erc_metadata
from ckanext.ark.model import ark as ark_model
from ckanext.ark.model.crud import ARKQuery
from ckanext.ark.model.ark import ARK


def get_commands():
    return [ark]


@click.group()
def ark():
    '''Ark commands.
    '''
    pass


@ark.command(name='initdb')
def init_db():
    if ark_model.ark_table.exists():
        click.secho('ARK table already exists', fg='green')
    else:
        ark_model.ark_table.create()
        click.secho('ARK table created', fg='green')


@ark.command(name='update-ark',
             short_help='Give ARK identifiers to existed datasets')
def update_ark():
    '''Mint ARKs for existed packages.
    '''
    context = {'model': model, 'ignore_auth': True, 'use_cache': False}

    package_ids = [r[0] for r in model.Session.query(model.Package.id).
                   filter(model.Package.type == 'dataset').all()]

    pkg_ids_with_arks = [r[0] for r in
                         model.Session.query(ARK.package_id).all()]

    pkgs_to_update = set(package_ids) - set(pkg_ids_with_arks)

    if len(pkgs_to_update) == 0:
        click.secho('No datasets found to update', fg='green')
        return

    for package_id in pkgs_to_update:
        pkg_dict = toolkit.get_action('package_show')(context, {
            'id': package_id
        })
        title = pkg_dict.get('title', package_id)

        if (pkg_dict.get('state', 'active') != 'active' or
                pkg_dict.get('private', False)):
            click.secho(f'"{title}" is inactive or private; ignoring',
                        fg='yellow')
            continue

        erc_record = build_erc_metadata(pkg_dict)

        if not erc_record:
            click.secho(
                f'"{title}" does not meet the erc requirements; ignoring',
                fg='yellow')
            continue

        ark = ARKQuery.read_package(package_id, create_if_none=True)

        click.secho(
            f'Updated "{title}" with ARK identifier "{ark.identifier}"',
            fg='green')


@ark.command(name='delete-ark',
             short_help='Delete ARK identifier for existed dataset')
@click.argument('name')
def delete_ark(name):
    '''Delete ARK for existed package. Accept package's id (name) and
    ARK identifier (with and without ark:).
    '''
    identifier = name.replace('ark:', '')
    if ARKQuery.delete_ark(identifier):
        click.secho(f'Deleted ARK {name} from the database')
        return
    dataset = model.Package.get(name)
    if dataset:
        ark = ARKQuery.read_package(dataset.id, create_if_none=True)
        if ARKQuery.delete_ark(ark.identifier):
            click.secho(f'Deleted ARK ark:{ark.identifier} from the database')
            return
    click.secho('Nothing to delete', fg='green')
