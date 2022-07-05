import json

from ckan.plugins import toolkit


def _get_nma_url():
    '''Return the NMA URL. Try and use ckanext.ark.nma_url but if that's not set
    use ckan.site_url.

    :returns: the NMA URL
    :rtype: string
    '''
    nma_url = toolkit.config.get('ckanext.ark.nma_url',
                                 toolkit.config.get('ckan.site_url'))
    return nma_url.rstrip('/')


def _get_mapping_fields_dict():
    '''Return a mapping from CKAN fields to ERC metadata fields.

    :returns: a mapping from CKAN fields to ERC metadata fields
    :rtype: dictionary
    '''
    ckan_to_erc = {'who': 'author', 'what': 'title'}
    erc_fields = ['who', 'what', 'when']
    mappings = toolkit.config.get('ckanext.ark.erc_mappings')
    if mappings:
        if isinstance(mappings, str):
            ckan_to_erc.update(json.loads(mappings))
        elif isinstance(mappings, dict):
            ckan_to_erc.update(mappings)
    return {k: v for k, v in ckan_to_erc.items() if k in erc_fields}


def _is_allow_missing_erc():
    '''Return True if missing ERC metadata is allowed for assigning ARKs.

    :returns: True if missing ERC metadata is allowed, False if not
    :rtype: bool
    '''
    return toolkit.asbool(
        toolkit.config.get('ckanext.ark.allow_missing_erc', True))


def build_erc_metadata(pkg_show_dict):
    '''Return the ERC metadata.

    :param pkg_show_dict: the package dictionary
    :type pkg_show_dict: dictionary

    :returns: the ERC metadata
    :rtype: dictionary
    '''
    erc_record = {}
    allow_missing_erc = _is_allow_missing_erc()

    for erc_field, ckan_field in _get_mapping_fields_dict().items():
        if erc_field == 'when' and isinstance(ckan_field, list):
            if len(ckan_field) != 2:
                return
            when_from = pkg_show_dict.get(ckan_field[0], '')
            when_to = pkg_show_dict.get(ckan_field[1], '')
            if not when_from and not when_to and not allow_missing_erc:
                return
            when_from = when_from.replace('-', '')
            when_to = when_to.replace('-', '')
            if when_from and when_to:
                when_from += '-'
            erc_record[erc_field] = f'{when_from}{when_to}'
        elif ckan_field in pkg_show_dict.keys():
            erc_record[erc_field] = pkg_show_dict[ckan_field]
        elif not allow_missing_erc:
            return

    return erc_record


def get_ark_url(identifier):
    '''Return the ARK URL.

    :param identifier: the compact ARK without the 'ark:' part
    :type identifier: string

    :returns: the ARK URL
    :rtype: string
    '''
    return f'{_get_nma_url()}/ark:{identifier}'


def get_erc_support():
    '''Return the ERC support metadata.

    :returns: the ERC support metadata
    :rtype: dictionary
    '''
    naan = toolkit.config.get('ckanext.ark.naan')
    erc_support = {
        'who': toolkit.config.get('ckanext.ark.erc_support.who', ''),
        'what': toolkit.config.get('ckanext.ark.erc_support.what', ''),
        'when': toolkit.config.get('ckanext.ark.erc_support.when', ''),
        'where': f'{_get_nma_url()}/ark:{naan}'
    }
    return erc_support


def get_erc_support_commitment():
    '''Return the persistence statement from the NMA.

    :returns: the persistence statement from the NMA
    :rtype: string
    '''
    return toolkit.config.get('ckanext.ark.erc_support.commitment', '')
