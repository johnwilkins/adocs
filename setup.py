from setuptools import find_packages
from setuptools import setup

setup (
    name='adocs',
    version='0.0.1',
    description='A cli tool for creating asciidoc documents with automatic include statements in assemblies.',
    author='John Wilkins',
    author_email='jowilkin@redhat.com',
    url='https://github.com/johnwilkins/adocs',
    packages=find_packages(),
    include_package_data=True,

    install_requires=[
        'jinja2',
    ],
    entry_points={
        'console_scripts': [
            'adocs = adocs.main:main',
        ],
    }
)