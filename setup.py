import os
import sys
from setuptools import setup, find_packages

share_dir = os.getenv("SHAREDIR", "/usr/share")


def get_requirements(filename: str) -> list:
    return open(os.path.join(filename)).read().splitlines()


install_requires = get_requirements('requirements.txt')
if sys.version_info < (3, 0):
    install_requires.append('futures')

setup(
    name='xscreensaver-bouncing-text',
    version='1.1.8',
    packages=find_packages(exclude=['tests', 'tests.*']),
    package_data={'xscreensaver_bouncing_text': ['py.typed']},
    install_requires=install_requires,
    url='https://github.com/Salamek/xscreensaver-bouncing-text',
    license='LGPL-3.0 ',
    author='Adam Schubert',
    author_email='adam.schubert@sg1-game.net',
    description='Simple bouncing text screensaver for xscreensaver with UTF-8 support.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    test_suite='tests',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development',
    ],
    python_requires='>=3.4',
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest',
        'pylint',
        'tox',
        'pytest-cov'
    ].extend(install_requires),
    entry_points={
        'console_scripts': [
            'xscreensaver-bouncing-text = xscreensaver_bouncing_text.__main__:main',
        ],
    },
    data_files=[
        (os.path.join(share_dir, 'xscreensaver', 'config'), [
            'usr/share/xscreensaver/config/xscreensaver-bouncing-text.xml'
        ])
    ],
    project_urls={
        'Release notes': 'https://github.com/Salamek/xscreensaver-bouncing-text/releases',
    },
)
