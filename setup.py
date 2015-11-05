__author__ = 'nmarchenko'

#import uuid
from setuptools import setup, find_packages
# from pip.req import parse_requirements
#
#
# install_requires_pip = parse_requirements('requirements.txt',
#                                           session=uuid.uuid1())
#
install_requires_setuptools = []
dependency_links_setuptools = []
#
# for ir in install_requires_pip:
#     if ir.url and ir.url.startswith('git'):
#         dependency_links_setuptools.append(ir.url)
#     install_requires_setuptools.append(str(ir.req))

setup(
    name='tooyakoh',
    version='0.0.1',
    packages=find_packages(),
    url='',
    license='',
    author='nmarchenko',
    author_email='nmarchenko@mirantis.com',
    description='',
    setup_requires=[],
    entry_points={
        'console_scripts': [
            #'proviant-config-set = proviant.cmd.config:set_path',
        ]
    },
    install_requires=install_requires_setuptools,
    dependency_links=dependency_links_setuptools,
    include_package_data=True
)
