import pytest
from ckan.tests import factories

from ckanext.ark.lib.helpers import build_erc_metadata


@pytest.mark.usefixtures('with_ark_table', 'with_plugins')
class TestHelpers(object):
    def test_default_mappings(self):
        dataset = factories.Dataset()
        erc_metadata_dict = build_erc_metadata(dataset)

        assert isinstance(erc_metadata_dict, dict)
        assert erc_metadata_dict['who'] == dataset['author']
        assert erc_metadata_dict['what'] == dataset['title']

    @pytest.mark.ckan_config('ckanext.ark.erc_mappings',
                             {'when': ['when_1', 'when_2', 'when_3']})
    def test_handles_bad_mappings(self):
        dataset = factories.Dataset()
        erc_metadata_dict = build_erc_metadata(dataset)

        assert erc_metadata_dict is None

    @pytest.mark.ckan_config('ckanext.ark.allow_missing_erc', False)
    @pytest.mark.ckan_config('ckanext.ark.erc_mappings', {'who': 'test'})
    def test_missing_erc_is_not_allowed(self):
        dataset = factories.Dataset()
        erc_metadata_dict = build_erc_metadata(dataset)

        assert erc_metadata_dict is None

    @pytest.mark.ckan_config('ckanext.ark.allow_missing_erc', False)
    @pytest.mark.ckan_config('ckanext.ark.erc_mappings',
                             {'when': ['when_from', 'when_to']})
    def test_missing_erc_when_is_not_allowed(self):
        dataset = factories.Dataset()
        erc_metadata_dict = build_erc_metadata(dataset)

        assert erc_metadata_dict is None

    @pytest.mark.ckan_config('ckanext.ark.erc_mappings',
                             {'when': 'test'})
    def test_single_when_field(self):
        dataset = factories.Dataset()
        dataset['test'] = '2022'
        erc_metadata_dict = build_erc_metadata(dataset)

        assert erc_metadata_dict['when'] == '2022'

    @pytest.mark.ckan_config('ckanext.ark.erc_mappings',
                             '{"when": ["when_from", "when_to"]}')
    def test_paired_when_fields(self):
        dataset = factories.Dataset()
        dataset.update({'when_from': '2022', 'when_to': '2023'})
        erc_metadata_dict = build_erc_metadata(dataset)

        assert erc_metadata_dict['when'] == '2022-2023'

    @pytest.mark.ckan_config('ckanext.ark.erc_mappings',
                             '{"when": ["when_from", "when_to"]}')
    def test_paired_when_fields_with_one_filled(self):
        dataset = factories.Dataset()
        dataset.update({'when_from': '2022'})
        erc_metadata_dict = build_erc_metadata(dataset)

        assert erc_metadata_dict['when'] == '2022'
