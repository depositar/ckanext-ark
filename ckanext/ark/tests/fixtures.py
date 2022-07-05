import pytest

from ckan.lib.helpers import url_for
from ckan.tests import factories, helpers

from ckanext.ark.model.ark import ark_table


@pytest.fixture(autouse=True)
def initial_data(monkeypatch, ckan_config):
    monkeypatch.setitem(ckan_config, 'ckanext.ark.naan', '99999')


@pytest.fixture
def with_ark_table(reset_db):
    '''Simple fixture which resets the database and creates the ark table.
    '''
    reset_db()
    ark_table.create(checkfirst=True)


@pytest.fixture
def dataset_with_ark(app, monkeypatch, ckan_config):
    monkeypatch.setitem(ckan_config, 'package_edit_return_url', None)
    user = factories.User()
    dataset = factories.Dataset()

    app.post(
        url_for('dataset.edit', id=dataset['id']),
        extra_environ={'REMOTE_USER': user['name']},
        data={'title': 'new-title'}
    )
    dataset = helpers.call_action('package_show', id=dataset['id'])

    return dataset
