[![License](https://img.shields.io/github/license/depositar/ckanext-ark)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/depositar/ckanext-ark/workflows/Tests/badge.svg)](https://github.com/depositar/ckanext-ark/actions)
[![Codecov](https://codecov.io/gh/depositar/ckanext-ark/branch/main/graph/badge.svg)](https://codecov.io/gh/depositar/ckanext-ark)
[![Python](https://img.shields.io/pypi/pyversions/ckanext-ark)](https://pypi.org/project/ckanext-ark)
[![CKAN](https://img.shields.io/badge/ckan-2.9-orange.svg)](https://github.com/ckan/ckan)

# ckanext-ark

This extension provides minter and resolver of the [ARK Identifier](https://datatracker.ietf.org/doc/draft-kunze-ark/). Inspired by [ckanext-doi](https://github.com/NaturalHistoryMuseum/ckanext-doi).

## Requirements

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.7 and earlier | no            |
| 2.8             | not tested    |
| 2.9             | yes           |

This extension is compatible with Python 3.7 and 3.8.

## Installation

To install ckanext-ark:

1. Activate your CKAN virtual environment, for example:

```bash
  . /usr/lib/ckan/default/bin/activate
```

2. Install the ckanext-ark Python package into your virtual environment:

```bash
  pip install ckanext-ark
```

3. Add `ark` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

4. Add a file `templates/package/read_base.html` in your custom extension
   (or modify `/usr/lib/ckan/default/src/ckan/ckan/templates/package/read_base.html` if
   you are not using a custom extension):

```html
  {% ckan_extends %}

  {% block secondary_content %}
    {{ super() }}
    {% snippet "ark/snippets/ark.html" %}
  {% endblock %}
```

5. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

```bash
  sudo service apache2 reload
```

6. Initialize the database:

```bash
  ckan -c /etc/ckan/default/ckan.ini ark initdb
```

## Development Installation

To install ckanext-ark for development, activate your CKAN virtualenv and
do:

```bash
  git clone https://github.com/depositar/ckanext-ark.git
  cd ckanext-ark
  python setup.py develop
  pip install -r dev-requirements.txt
```

## Config settings

### ARK NAAN **[REQUIRED]**

You can request a Name Assigning Authority Number (NAAN) through this [form](https://goo.gl/forms/bmckLSPpbzpZ5dix1).

```ini
  ckanext.ark.naan = 99999 # This NAAN is for test purpose only
```

### Other ARK configs

Name | Description | Default
-- | -- | --
`ckanext.ark.nma_url`  | The URL of NMA (Name Mapping Authority) | The same URL as `ckan.site_url`
`ckanext.ark.shoulder` | The [Shoulder](https://arks.org/about/shoulders/) for subdividing a NAAN namespace |
`ckanext.ark.template` | The template for generating ARKs | zek

### ERC record (ARK metadata) configs

Name | Description | Default
-- | -- | --
`ckanext.ark.erc_mappings` | A mapping from ERC record to CKAN fields[^mapping_when] | {"who": "author", "what": "title", "when": ""}
`ckanext.ark.allow_missing_erc` | This controls if still assigning ARKs even if the fields defined in the `ckanext.ark.erc_mappings` is missing or empty[^missing_when] | True
`ckanext.ark.erc_support.who` | Who made the ARK support commitment |
`ckanext.ark.erc_support.what` | What the nature of the ARK support commitment was |
`ckanext.ark.erc_support.when` | When the ARK support commitment was made |
`ckanext.ark.erc_support.commitment` | A fuller explanation of the ARK support commitment |

[^mapping_when]: For the mapping of `when` field, the ISO 8601 YYYY-MM-DD is recommended. The date string will be converted to [Temporal Enumerated Ranges (TEMPER)](https://datatracker.ietf.org/doc/draft-kunze-temper/) format (YYYYMMDD-YYYYMMDD). Note that the date validation is omitted.
[^missing_when]: For the `when` field, a list containing a single value is not viewed as an empty value.

## Commands

### `ark`

1. `delete-ark`: delete ARK identifier for existed dataset. Accept package's id (name) and ARK identifier (with and without `ark:`).

```bash
  ckan -c /etc/ckan/default/ckan.ini ark delete-ark [NAME]
```

2. `update-ark`: give ARK identifiers to existed datasets.

```bash
  ckan -c /etc/ckan/default/ckan.ini ark update-ark
```

## Tests

To run the tests, do:

```bash
  pytest --ckan-ini=test.ini
```

## Releasing a new version of ckanext-ark

ckanext-ark is available on PyPI as  https://pypi.python.org/pypi/ckanext-ark. You can follow these steps to publish a new version:

1. Update the version number in the `setup.py` file. See [PEP 440](http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers) for how to choose version numbers.

2. Make sure you have the latest version of necessary packages:

```bash
  pip install --upgrade build twine
```

3. Create a source and binary distributions of the new version:

```bash
  python -m build
```

   Fix any errors you get.

4. Upload the source distribution to PyPI:

```bash
  twine upload dist/*
```

5. Commit any outstanding changes:

```bash
  git commit -a
  git push
```

6. Tag the new release of the project on GitHub with the version number from
   the `setup.py` file. For example if the version number in `setup.py` is
   1.0.1 then do:

```bash
  git tag v1.0.1
  git push --tags
```

## License

[MIT](https://opensource.org/licenses/MIT)
