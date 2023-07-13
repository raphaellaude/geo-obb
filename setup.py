from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='geoobb',
    version='0.1',
    description='Utility for calculating the oriented bounding boxes of shapely features.',
    author='Raphael Laude',
    author_email='raphlaude@gmail.com',
    url='https://github.com/raphaellaude/geo-obb',
    packages=find_packages(exclude=('tests', 'docs', 'examples')),
    install_requires=requirements,
)
