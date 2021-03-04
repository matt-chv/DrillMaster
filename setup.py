from setuptools import setup

setup(
    name='my_app',
    packages=['.'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)