# -*- coding: utf-8 -*-
"""
This module contains the tool of uqmc.types
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.1'

tests_require = ['zope.testing']

setup(name='uqmc.types',
      version=version,
      description="",
      long_description="",
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Intended Audience :: Developers',
        ],
      keywords='',
      author='Alex Stevens',
      author_email='alexander.stevens@uqconnect.edu.au',
      url='https://github.com/AlexStevens/uqmc.types/',
      license='gpl',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['uqmc'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
            'setuptools',
            'Products.CMFPlone',
            'five.grok',
            'plone.app.dexterity',
            'plone.directives.dexterity',
            'plone.directives.form',
            'plone.formwidget.autocomplete',
            'plone.api',
        ],
      tests_require=tests_require,
      extras_require=dict(test=tests_require),
      test_suite='uqmc.types.tests.test_docs.test_suite',
      entry_points="""
      # -*- entry_points -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["templer.localcommands"],
      )
