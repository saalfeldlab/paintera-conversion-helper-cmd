from distutils.core import setup
from distutils.command.build_py import build_py

import os

install_requires=['jgo>=0.4.0']
entry_points={
    'console_scripts': [
        'extract-to-scalar=paintera_conversion_helper:launch_extract_to_scalar',
        'paintera-convert=paintera_conversion_helper:launch_paintera_convert'
    ]
}

name = 'paintera_conversion_helper'
here = os.path.abspath(os.path.dirname(__file__))
version_info = {}
with open(os.path.join(here, name, 'version.py')) as fp:
    exec(fp.read(), version_info)
version = version_info['_paintera_conversion_helper_version']

setup(
    name=name,
    version=version.python_version(),
    author='Philipp Hanslovsky',
    author_email='hanslovskyp@janelia.hhmi.org',
    description='paintera conversion helper',
    url='https://github.com/saalfeldlab/paintera-conversion-helper',
    packages=['paintera_conversion_helper'],
    entry_points=entry_points,
    install_requires=install_requires
)
