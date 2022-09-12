#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import glob
import ntpath


def get_module_name(module_path):
    """
    Return the module name of the module path
    """
    return ntpath.split(module_path)[1].split(".")[0]


def snake_to_camel(word):
    """
    Convert a word from snake_case to CamelCase
    """
    return ''.join(x.capitalize() or '_' for x in word.split('_'))


setup(
    name="fn_my_ldap",
    display_name="LDAP Functions for SOAR",
    version="1.0.0",
    license="MIT",
    author="IBM SOAR",
    author_email="",
    url="ibm.com",
    description="App to Search, and enable/disable users in LDAP system",
    long_description="""App provides functionality to search for users, enable users, and disable users in a LDAP system.""",
    install_requires=[
        "resilient-circuits>=46.0.0",
        "ldap3"
    ],
    python_requires='>=3.6',
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    classifiers=[
        "Programming Language :: Python",
    ],
    entry_points={
        "resilient.circuits.components": [
            # When setup.py is executed, loop through the .py files in the components directory and create the entry points.
            "{}FunctionComponent = fn_my_ldap.components.{}:FunctionComponent".format(snake_to_camel(get_module_name(filename)), get_module_name(filename)) for filename in glob.glob("./fn_my_ldap/components/[a-zA-Z]*.py")
        ]
        ,
        "resilient.circuits.configsection": ["gen_config = fn_my_ldap.util.config:config_section_data"],
        "resilient.circuits.customize": ["customize = fn_my_ldap.util.customize:customization_data"],
        "resilient.circuits.selftest": ["selftest = fn_my_ldap.util.selftest:selftest_function"]
    }
)