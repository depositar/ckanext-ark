import pytest
from ckan.model import Session

from ckanext.ark.model.ark import ARK


@pytest.mark.usefixtures('with_ark_table', 'with_plugins')
def test_ark_is_created_automatically(dataset_with_ark):
    found_record = (Session.query(ARK).
                    filter(ARK.package_id == dataset_with_ark['id']).one())

    assert found_record is not None
