from setuptools import setup, find_namespace_packages, __version__

setup(
    name='silmused',
    version=__version__,
    license='',
    author='',
    author_email='',
    packages=find_namespace_packages(),
    url='',
    install_requires=[
        'psycopg2-binary',
        'uuid',
    ]
)