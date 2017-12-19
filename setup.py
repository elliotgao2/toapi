import ast
import re

from setuptools import find_packages, setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('toapi/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name="toapi",
    version=version,
    description="Every web site provides APIs.",
    author="Gaojiuli",
    author_email="gaojiuli@gmail.com",
    url='https://github.com/gaojiuli/toapi',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'colorama',
        'lxml',
        'cssselect',
        'selenium',
        'cchardet',
        'requests',
        'flask',
        'records',
        'ujson',
        'redis',
        'pymemcache',
        'pycrypto',
        'click'
    ],
    license='Apache 2.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'toapi=toapi.cli:cli',
        ],
    },
    py_modules=['toapi'],
    include_package_data=True,
    zip_safe=False
)
