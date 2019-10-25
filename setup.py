from setuptools import setup, find_packages
from s3_fdw import __version__

setup(
    name='s3_fdw',
    version=__version__,
    description='PostgreSQL foreign data wrapper for columnar data files stored on Amazon S3',
    url='https://github.com/smomni/s3_fdw_py',
    python_requires='>=3.5',
    author='Simo Tumelius',
    author_email='simo.tumelius@gmail.com',
    license='TBD',
    packages=find_packages(),
    install_requires=['multicorn'],
    extras_require={'test': ['pytest', 'black']},
    scripts=[],
)
