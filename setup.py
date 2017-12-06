from setuptools import find_packages, setup

setup(
    name="toapi",
    version="0.1.5",
    description="A library letting any web site provide APIs.",
    author="Gaojiuli",
    author_email="gaojiuli@gmail.com",
    url='https://github.com/gaojiuli/toapi',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'lxml',
        'cssselect',
        'selenium',
        'cchardet',
        'requests',
        'flask'
    ],
    license='Apache',
    packages=find_packages(),
    py_modules=['toapi'],
    include_package_data=True,
    zip_safe=False
)
