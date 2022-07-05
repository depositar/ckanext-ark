import json

import pytest
from ckan.lib.helpers import url_for
from ckan.tests import factories, helpers


@pytest.mark.usefixtures('with_ark_table')
class TestViews(object):
    def test_ark(self, app, dataset_with_ark):
        ark_url = url_for('ark.read', path=dataset_with_ark['ark'].
                          replace('ark:', ''))
        dataset_url = url_for('dataset.read', id=dataset_with_ark['id'])

        assert app.get(ark_url).body == app.get(dataset_url).body

    def test_ark_erc_info(self, app, ckan_config, dataset_with_ark):
        site_url = ckan_config['ckan.site_url']
        erc_metadata = {
            'erc': {
                'who': dataset_with_ark['erc_who'],
                'what': dataset_with_ark['erc_what'],
                'when': dataset_with_ark['erc_when'],
                'where': dataset_with_ark['erc_where']
            },
            'erc-support': {
                'who': '',
                'what': '',
                'when': '',
                'where': f'{site_url}/ark:99999'
            }
        }

        url = url_for('ark.read', path=dataset_with_ark['ark'].
                      replace('ark:', ''))
        response = app.get(f'{url}?info')
        old_response = app.get(url,
                               environ_overrides={'REQUEST_URI': f'{url}?'})

        assert response.headers['Content-Type'] == \
            'application/json; charset=UTF-8'
        assert json.loads(response.get_data()) == \
            erc_metadata
        assert old_response.headers['Content-Type'] == \
            'application/json; charset=UTF-8'
        assert json.loads(old_response.get_data()) == \
            erc_metadata

    @pytest.mark.ckan_config('ckanext.ark.erc_support.commitment', 'test')
    def test_ark_erc_support_commitment(self, app):
        response = app.get('/ark:99999/')

        assert response.headers['Content-Type'] == \
            'text/plain; charset=UTF-8'
        assert 'test' in response.body

    def test_ark_not_exist(self, app):
        url = url_for('ark.read', path='ark:99999/abc')

        assert 'ARK not found' in app.get(url).body

    def test_deleted_dataset(self, app, dataset_with_ark):
        user = factories.User()

        response = app.post(
            url_for('dataset.delete', id=dataset_with_ark['name']),
            extra_environ={'REMOTE_USER': user['name']}
        )
        assert 200 == response.status_code

        url = url_for('ark.read', path=dataset_with_ark['ark'].
                      replace('ark:', ''))

        assert 'Defunct ARK' in app.get(url).body

    @pytest.mark.ckan_config('package_edit_return_url', None)
    def test_private_dataset(self, app):
        user = factories.User()
        org = factories.Organization(user=user)
        dataset = factories.Dataset()

        app.post(
            url_for('dataset.edit', id=dataset['id']),
            extra_environ={'REMOTE_USER': user['name']},
            data={'title': 'new-title'}
        )
        app.post(
            url_for('dataset.edit', id=dataset['id']),
            extra_environ={'REMOTE_USER': user['name']},
            data={'owner_org': org['id'], 'private': True}
        )
        dataset = helpers.call_action('package_show', id=dataset['id'])

        url = url_for('ark.read', path=dataset['ark'].replace('ark:', ''))

        assert 'Defunct ARK' in app.get(url).body
