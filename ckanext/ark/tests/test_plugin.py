import pytest
from ckan.lib.helpers import url_for
from ckan.tests import factories


@pytest.mark.ckan_config('package_edit_return_url', None)
@pytest.mark.usefixtures('with_ark_table', 'with_request_context')
class TestPlugin(object):
    @pytest.fixture
    def user_env(self):
        try:
            # CKAM >= 2.10
            from ckantoolkit.tests.factories import UserWithToken
            user = UserWithToken()
            return {'Authorization': user['token']}
        except ImportError:
            # CKAN < 2.10
            user = factories.User()
            return {'REMOTE_USER': user['name'].encode('ascii')}

    def test_after_update(self, app, user_env):
        response = app.post(
            url_for('dataset.new'),
            environ_overrides=user_env,
            data={'name': 'new-dataset', 'save': ''},
            follow_redirects=False
        )
        response = app.post(
            url_for('dataset.edit', id='new-dataset'),
            extra_environ=user_env,
            data={'title': 'new-title'}
        )

        assert 'ARK identifier created' in response.body

    def test_after_update_private_dataset(self, app, user_env):
        org = factories.Organization()
        dataset = factories.Dataset(private=True, owner_org=org['id'])

        response = app.post(
            url_for('dataset.edit', id=dataset['id']),
            extra_environ=user_env,
            data={'title': 'new-title'}
        )

        assert 'ARK identifier created' not in response.body

    @pytest.mark.ckan_config('ckanext.ark.allow_missing_erc', False)
    @pytest.mark.ckan_config('ckanext.ark.erc_mappings', {'when': 'test'})
    def test_after_update_missing_erc_is_not_allowed(self, app, user_env):
        dataset = factories.Dataset()

        response = app.post(
            url_for('dataset.edit', id=dataset['id']),
            extra_environ=user_env,
            data={'title': 'new-title'}
        )

        assert 'ARK identifier created' not in response.body
