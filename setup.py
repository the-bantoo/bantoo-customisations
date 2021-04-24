# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in bantoo_customisations/__init__.py
from bantoo_customisations import __version__ as version

setup(
	name='bantoo_customisations',
	version=version,
	description='Bantoo Site Customisations',
	author='Bantoo',
	author_email='hello@thebantoo.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
