from unittest.mock import MagicMock, patch

from noid import pynoid as noid
import pytest

from ckanext.ark.lib.minter import Minter


@patch('ckanext.ark.lib.minter.ARKQuery')
class TestMinter(object):
    def test_mint_ark_without_template(self, mock_crud):
        mock_crud.read_ark = MagicMock(return_value=None)

        minter = Minter()
        noid_string = minter.mint_ark().split('/')[-1]

        assert noid.validate(noid_string)

    @pytest.mark.ckan_config('ckanext.ark.template', 'zek')
    def test_mint_ark_with_template(self, mock_crud):
        mock_crud.read_ark = MagicMock(return_value=None)

        minter = Minter()
        noid_string = minter.mint_ark().split('/')[-1]

        assert noid.validate(noid_string)

    def test_it_fails_when_it_failed_to_create_an_ark(self, mock_crud):
        mock_crud.read_ark = MagicMock(return_value=MagicMock())

        minter = Minter()

        with pytest.raises(Exception,
                           match='Failed to create an ARK identifier'):
            minter.mint_ark()

    def test_it_fails_when_naan_is_missing(self, mock_crud, ckan_config):
        del ckan_config['ckanext.ark.naan']

        with pytest.raises(TypeError,
                           match='You must set the ckanext.ark.naan ' +
                           'config value'):
            Minter()
