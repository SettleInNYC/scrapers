# Automatically created by: scrapyd-deploy

from setuptools import setup, find_packages

setup(
    name='settleinnyc',
    version='0.1.0',
    packages=find_packages(),
    zip_safe=False,
    package_data={'settleinnyc': ['useragents.txt']},
    entry_points={'scrapy': ['settings = settleinnyc.settings']},
)
