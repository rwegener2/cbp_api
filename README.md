# CBP API

The Chesapeake Bay Program (CBP) maintains a wide variety of data monitoring stations across the Chesapeake Bay. They also provide an API for accessing the data. This Python library is a Python wrapper for accessing the API and associated data. Currently implemented functionality includes:

- Retrieving Water Quality data

Resources:
- [CBP Datahub](https://datahub.chesapeakebay.net/Home)
- [CBP API docs](https://datahub.chesapeakebay.net/API)

Readthedocs

Sphinx
https://www.sphinx-doc.org/en/master/usage/quickstart.html#running-the-build

`make html` from the docs folder
`python -m http.server --directory /_build/html/` to serve

Building
https://setuptools.pypa.io/en/latest/userguide/quickstart.html#
`python -m build` --> uses `pyproject.toml`

References

HUC8 data from: https://www.hydroshare.org/resource/b832a6c2f96541808444ec9562c5247e/

Testing

`pytest .` from the root folder
