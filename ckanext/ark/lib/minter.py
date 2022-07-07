from noid import pynoid as noid
from ckan.plugins import toolkit

from ckanext.ark.model.crud import ARKQuery


class Minter:
    '''A minter for ARK.
    '''
    def __init__(self):
        self.naan = toolkit.config.get('ckanext.ark.naan')
        self.shoulder = toolkit.config.get('ckanext.ark.shoulder', '')
        self.template = toolkit.config.get('ckanext.ark.template')

        if self.naan is None:
            raise TypeError('You must set the ckanext.ark.naan config value')

    def mint_ark(self):
        '''Create a new ARK which isn't currently in use.
        '''
        attempts = 5

        while attempts > 0:
            if self.template:
                blade = noid.mint(template=self.template)
            else:
                blade = noid.mint()
            ark = f'{self.naan}/{self.shoulder}{blade}'

            if ARKQuery.read_ark(ark) is None:
                return ark
            attempts -= 1
        raise Exception('Failed to create an ARK identifier')
