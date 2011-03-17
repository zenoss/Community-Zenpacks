from setuptools import setup, find_packages

NAME="ZenPacks.community.LLDP"
setup(
    name=NAME,
    version="2011.03.17",
    author="Christoph Handel",
    license="GPL",

    compatZenossVers=">=3.0",
    prevZenPackName="",
    namespace_packages=['ZenPacks', 'ZenPacks.community'],
    # Tell setuptools what packages this zenpack provides.
    packages=find_packages(),

    # Tell setuptools to figure out for itself which files to include
    # in the binary egg when it is built.
    include_package_data=True,

    package_data={
        '': ['../*.txt'],
    },

    # Indicate dependencies on other python modules or ZenPacks.
    install_requires=[],

    # Every ZenPack egg must define exactly one zenoss.zenpacks entry point
    # of this form.
    entry_points={
        'zenoss.zenpacks': '%s = %s' % (NAME, NAME),
    },

    # All ZenPack eggs must be installed in unzipped form.
    zip_safe=False,
)
