#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
import re

from setuptools import setup, find_packages


def get_file(*paths):
    path = os.path.join(*paths)
    try:
        with open(path, 'rb') as f:
            return f.read().decode('utf8')
    except IOError:
        pass


def get_version():
    init_py = get_file(os.path.dirname(__file__),
                       'pygoogletranslation', '__init__.py')
    pattern = r"{0}\W*=\W*'([^']+)'".format('__version__')
    version, = re.findall(pattern, init_py)
    return version


def get_description():
    init_py = get_file(os.path.dirname(__file__),
                       'pygoogletranslation', '__init__.py')
    pattern = r'"""(.*?)"""'
    description, = re.findall(pattern, init_py, re.DOTALL)
    return description


this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# def get_readme():
#     return get_file(os.path.dirname(__file__), 'README.rst')


def install():
    setup(
        name='pygoogletranslation',
        version=get_version(),
        description=get_description(),
        long_description=long_description,
        long_description_content_type='text/rst',
        license='MIT',
        author='superjavascrip',
        author_email='lronman1008000@gmail.com',
        url='https://github.com/superjavascrip/py-googletranslation',
        classifiers=['Development Status :: 5 - Production/Stable',
                     'Intended Audience :: Education',
                     'Intended Audience :: End Users/Desktop',
                     'License :: Freeware',
                     'Operating System :: OS Independent',
                     'Topic :: Education',
                     'Programming Language :: Python',
                     'Programming Language :: Python :: 3.6',
                     'Programming Language :: Python :: 3.7',
                     'Programming Language :: Python :: 3.8'],
        packages=find_packages(exclude=['docs', 'tests']),
        keywords='google translate translator',
        install_requires=[
            'requests',
            'unidecode',
            'nltk',
            'docx2txt',
            'PyPDF2',
        ],
        python_requires='>=3.6',
        tests_require=[
            'pytest',
            'coveralls',
        ],

    )


if __name__ == "__main__":
    install()
