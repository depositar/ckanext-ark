import datetime

from ckan.common import _
from ckan.lib.plugins import DefaultTranslation
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckanext.ark import cli, views
from ckanext.ark.lib.helpers import build_erc_metadata, get_ark_url
from ckanext.ark.model.crud import ARKQuery


class ArkPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint, inherit=True)
    plugins.implements(plugins.IClick)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.ITranslation)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')

    # IBlueprint

    def get_blueprint(self):
        return [views.blueprints]

    # IClick

    def get_commands(self):
        return cli.get_commands()

    # IPackageController

    def after_update(self, context, pkg_dict):
        '''Dataset has been created/updated. Check status of the dataset to
        determine if we should mint ARK.
        '''
        # Is this active and public? If so we need to make sure we have
        # an active ARK
        if (pkg_dict.get('state', 'active') == 'active' and
                not pkg_dict.get('private', False)):
            package_id = pkg_dict['id']

            # Remove user-defined update schemas first (if needed)
            context.pop('schema', None)

            # Load the package_show version of the dict
            pkg_show_dict = toolkit.get_action('package_show')(context, {
                'id': package_id
            })

            erc_record = build_erc_metadata(pkg_show_dict)

            if not erc_record:
                return pkg_dict

            # Load or create the ARK (package may not have a ARK if
            # extension was loaded after package creation)
            ark = ARKQuery.read_package(package_id, create_if_none=True)

            if ark.last_modified is None:
                toolkit.h.flash_success(_('ARK identifier created'))

            ARKQuery.update_ark(identifier=ark.identifier,
                                last_modified=datetime.datetime.utcnow(),
                                **erc_record
                                )

        return pkg_dict

    def after_show(self, context, pkg_dict):
        '''Add the ARK details to the pkg_dict so it can be displayed.
        '''
        ark = ARKQuery.read_package(pkg_dict['id'])
        if ark:
            pkg_dict.update({
                'ark': f'ark:{ark.identifier}',
                'erc_who': ark.who,
                'erc_what': ark.what,
                'erc_when': ark.when,
                'erc_where': get_ark_url(ark.identifier)
            })
