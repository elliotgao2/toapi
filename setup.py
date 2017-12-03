from setuptools import find_packages, setup

setup(
    name="toapi",
    version="0.1.2",
    description="Make existing web sites available with APIs.",
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
        'lxml',
        'requests',
        'flask'
    ],
    license='Apache',
    packages=find_packages(),
    py_modules=['toapi'],
    include_package_data=True,
    zip_safe=False
)
