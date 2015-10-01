#! /usr/bin/env python2


from setuptools import setup


setup(
    name='html5lib_typogrify',
    version='0.1a3',
    author='Alexandre Leray',
    author_email='alexandre@stdin.fr',
    description=('Corrects common typographical mistakes.'),
    url='https://github.com/aleray/html5lib_typogrify',
    packages=[
        'html5lib_typogrify',
        'html5lib_typogrify.french',
        'html5lib_typogrify.french.filters'
    ],
    include_package_data = True,
    install_requires=[
        'html5lib==0.999',
        'regex==2014.12.24',
        'Pyphen==0.9.1'
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: Markup :: HTML'
    ]
)
