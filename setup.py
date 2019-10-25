import re
from setuptools import setup, find_packages
from pathlib import Path


def find_version(path: Path):
    version_file = path.read_text()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


__version__ = find_version(Path(__file__).parent / 's3_fdw' / '__init__.py')

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
    install_requires=['multicorn', 'boto3', 'pandas'],
    extras_require={'test': ['pytest', 'black']},
    scripts=[],
)
