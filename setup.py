"""Setuptools entry point."""
import codecs
import os
import pathlib
from typing import Dict, List

try:
    from setuptools import setup        # type: ignore
except ImportError:
    from distutils.core import setup

package_name = 'lib_doctest_pycharm'                                                # type: str
required = list()                                                                   # type: List[str]
required_for_tests = list()                                                         # type: List[str]
entry_points = dict()                                                               # type: Dict[str, str]


def get_version(dist_directory: str) -> str:
    with open(str(pathlib.Path(__file__).parent / f'{dist_directory}/version.txt'), mode='r') as version_file:
        version = version_file.readline()
    return version


def is_travis_deploy() -> bool:
    if 'travis_deploy' in os.environ:
        if os.environ['travis_deploy'] == 'True':
            return True
    return False


def strip_links_from_required(l_required: List[str]) -> List[str]:
    """
    >>> required = ['lib_regexp @ git+https://github.com/bitranox/lib_regexp.git', 'test']
    >>> assert strip_links_from_required(required) == ['lib_regexp', 'test']

    """
    l_req_stripped = list()                                        # type: List[str]
    for req in l_required:
        req_stripped = req.split('@')[0].strip()
        l_req_stripped.append(req_stripped)
    return l_req_stripped


if is_travis_deploy():
    required = strip_links_from_required(required)


CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules'
]

path_readme = pathlib.Path(__file__).parent / 'README.rst'
long_description = package_name
if path_readme.exists():
    # noinspection PyBroadException
    try:
        readme_content = codecs.open(str(path_readme), encoding='utf-8').read()
        long_description = readme_content
    except Exception:
        pass


setup(name=package_name,
      version=get_version(package_name),
      url=f'https://github.com/bitranox/{package_name}',
      packages=[package_name],
      package_data={package_name: ['version.txt']},
      description=package_name,
      long_description=long_description,
      long_description_content_type='text/x-rst',
      author='Robert Nowotny',
      author_email='bitranox@gmail.com',
      classifiers=CLASSIFIERS,
      entry_points=entry_points,
      # minimally needs to run tests - no project requirements here
      tests_require=['typing',
                     'pathlib',
                     'mypy ; platform_python_implementation != "PyPy" and python_version >= "3.5"',
                     'pytest',
                     'pytest-pep8 ; python_version < "3.5"',
                     'pytest-pycodestyle ; python_version >= "3.5"',
                     'pytest-mypy ; platform_python_implementation != "PyPy" and python_version >= "3.5"'
                     ] + required_for_tests,

      # specify what a project minimally needs to run correctly
      install_requires=['typing', 'pathlib'] + required + required_for_tests,
      # minimally needs to run the setup script, dependencies needs also to put here for setup.py install test
      # dependencies must not be put here for pip install
      setup_requires=['typing',
                      'pathlib',
                      'pytest-runner']
      )
