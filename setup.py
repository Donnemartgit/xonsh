#!/usr/bin/env python
# coding=utf-8
"""The gitsome installer."""
from __future__ import print_function, unicode_literals
import os
import sys
try:
    from setuptools import setup
    from setuptools.command.sdist import sdist
    from setuptools.command.install import install
    from setuptools.command.develop import develop
    HAVE_SETUPTOOLS = True
except ImportError:
    from distutils.core import setup
    from distutils.command.sdist import sdist as sdist
    from distutils.command.install import install as install
    HAVE_SETUPTOOLS = False

from xonsh import __version__ as VERSION

TABLES = ['xonsh/lexer_table.py', 'xonsh/parser_table.py']

def clean_tables():
    for f in TABLES:
        if os.path.isfile(f):
            os.remove(f)
            print('Remove ' + f)

def build_tables():
    print('Building lexer and parser tables.')
    sys.path.insert(0, os.path.dirname(__file__))
    from xonsh.parser import Parser
    Parser(lexer_table='lexer_table', yacc_table='parser_table',
           outputdir='xonsh')
    sys.path.pop(0)

class xinstall(install):
    def run(self):
        clean_tables()
        build_tables()
        install.run(self)

class xsdist(sdist):
    def make_release_tree(self, basedir, files):
        clean_tables()
        build_tables()
        sdist.make_release_tree(self, basedir, files)

if HAVE_SETUPTOOLS:
    class xdevelop(develop):
        def run(self):
            clean_tables()
            build_tables()
            develop.run(self)


def main():
    if sys.version_info[0] < 3:
        sys.exit('gitsome currently requires Python 3.4+')
    try:
        if '--name' not in sys.argv:
            print(logo)
    except UnicodeEncodeError:
        pass
    with open(os.path.join(os.path.dirname(__file__), 'README.rst'), 'r') as f:
        readme = f.read()
    skw = dict(
        name='gitsome',
        description='gitsome shell forked from xonsh',
        long_description=readme,
        license='BSD',
        version=VERSION,
        author='Donne Martin',
        maintainer='Donne Martin',
        author_email='donne.martin@gmail.com',
        url='https://github.com/donnemartin/gitsome',
        platforms='Cross Platform',
        classifiers=['Programming Language :: Python :: 3'],
        packages=['gitsome'],
        scripts=['scripts/xonsh',
                 'scripts/gitsome'],
        cmdclass={'install': xinstall, 'sdist': xsdist},
        )
    if HAVE_SETUPTOOLS:
        skw['setup_requires'] = ['ply']
        skw['install_requires'] =[
            'numpydoc==0.5',
            'ply==3.4',
            'prompt-toolkit==0.51',
            'requests==2.8.1',
            'github3.py==0.9.4',
        ],
        skw['entry_points'] = {
            'pygments.lexers': ['gitsome = xonsh.pyghooks:XonshLexer',
                                'gitsomecon = xonsh.pyghooks:XonshConsoleLexer',
                                ],
            }
        skw['cmdclass']['develop'] = xdevelop
    setup(**skw)

logo = ''

if __name__ == '__main__':
    main()
