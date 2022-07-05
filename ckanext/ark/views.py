from flask import Blueprint, make_response, request
from ckan.common import _
from ckan.lib import base
from ckan.plugins import toolkit

from ckanext.ark.lib.helpers import get_ark_url, get_erc_support, \
    get_erc_support_commitment
from ckanext.ark.model.crud import ARKQuery

blueprints = Blueprint('ark', __name__)


@blueprints.route('/ark:/<path:path>/')
@blueprints.route('/ark:<path:path>/')
def read(path):
    # Show NAA metadata
    if path == toolkit.config.get('ckanext.ark.naan'):
        response = make_response(get_erc_support_commitment())
        response.headers['Content-type'] = 'text/plain; charset=UTF-8'
        return response
    ark = ARKQuery.read_ark(path)
    if not ark:
        return base.abort(404, _('ARK not found'))
    # Show ERC metadata
    if 'info' in request.args or request.environ['REQUEST_URI'][-2:] == '/?':
        response = {
            'erc': {
                'who': ark.who,
                'what': ark.what,
                'when': ark.when,
                'where': get_ark_url(ark.identifier)
            },
            'erc-support': get_erc_support()
        }
        response = make_response(response)
        response.headers['Content-type'] = 'application/json; charset=UTF-8'
        return response
    else:
        try:
            toolkit.get_action('package_show')({}, {
                'id': ark.package_id
            })
            return toolkit.redirect_to('dataset.read',
                                       id=ark.package_id)
        except (toolkit.ObjectNotFound, toolkit.NotAuthorized):
            # Show defunct page
            return toolkit.render('ark/snippets/defunct.html',
                                  {'ark': ark.identifier})
