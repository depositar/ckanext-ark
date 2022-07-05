import pytest
import ckan.plugins as plugins
from ckan.tests import factories

from ckanext.ark.cli import ark


@pytest.mark.usefixtures('clean_db', 'with_plugins')
class TestCliInitDB(object):
    def test_init_db(self, cli):
        result = cli.invoke(ark, ['initdb'])

        assert 'ARK table created' in result.output

    def test_when_db_exists(self, cli):
        cli.invoke(ark, ['initdb'])
        result = cli.invoke(ark, ['initdb'])

        assert 'ARK table already exists' in result.output


@pytest.mark.usefixtures('with_ark_table', 'with_plugins')
class TestCli(object):
    def test_update_ark_when_no_datasets_to_update(self,
                                                   dataset_with_ark, cli):
        result = cli.invoke(ark, ['update-ark'])

        assert 'No datasets found to update' in result.output

    def test_update_ark(self, cli):
        plugins.unload('ark')
        org = factories.Organization()
        dataset = factories.Dataset()
        dataset_title = dataset['title']
        private_dataset = factories.Dataset(private=True, owner_org=org['id'])
        private_dataset_title = private_dataset['title']
        plugins.load('ark')

        result = cli.invoke(ark, ['update-ark'])

        assert f'Updated "{dataset_title}" with ARK identifier' \
            in result.output
        assert f'"{private_dataset_title}" is inactive or private; ignoring' \
            in result.output

    @pytest.mark.ckan_config('ckanext.ark.allow_missing_erc', False)
    @pytest.mark.ckan_config('ckanext.ark.erc_mappings', {'when': 'when'})
    def test_update_ark_missing_erc_is_not_allowed(self, cli):
        plugins.unload('ark')
        dataset = factories.Dataset()
        dataset_title = dataset['title']
        plugins.load('ark')

        result = cli.invoke(ark, ['update-ark'])

        assert f'"{dataset_title}" does not meet the erc requirements; ' + \
            'ignoring' in result.output

    def test_delete_ark_by_full_ark(self, dataset_with_ark, cli):
        to_delete_ark = dataset_with_ark['ark']

        result = cli.invoke(ark, ['delete-ark', to_delete_ark])

        assert f'Deleted ARK {to_delete_ark} from the database' \
            in result.output

    def test_delete_ark_by_ark_id(self, dataset_with_ark, cli):
        to_delete_ark = dataset_with_ark['ark'].replace('ark:', '')

        result = cli.invoke(ark, ['delete-ark', to_delete_ark])

        assert f'Deleted ARK {to_delete_ark} from the database' \
            in result.output

    def test_delete_ark_by_dataset_name(self, dataset_with_ark, cli):
        to_delete_ark = dataset_with_ark['ark']

        result = cli.invoke(ark, ['delete-ark', dataset_with_ark['name']])

        assert f'Deleted ARK {to_delete_ark} from the database' \
            in result.output

    def test_delete_ark_by_dataset_id(self, dataset_with_ark, cli):
        to_delete_ark = dataset_with_ark['ark']

        result = cli.invoke(ark, ['delete-ark', dataset_with_ark['id']])

        assert f'Deleted ARK {to_delete_ark} from the database' \
            in result.output

    def test_delete_ark_not_exist(self, cli):
        result = cli.invoke(ark, ['delete-ark', 'dataset-not-exist'])

        assert 'Nothing to delete' in result.output
