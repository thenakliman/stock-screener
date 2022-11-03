import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="screener",
    version="0.0.1",
    author="Fake User",
    author_email="thenakliman@gmail.com",
    description="A package for stock screening",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thenakliman/stock-screener",
    packages=setuptools.find_packages(exclude=['tests']),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    python_requires='>=3.8',
    install_requires=[
        "configparser==4.0.2",
        "pymongo==3.10.1",
        "PyYAML>=5.3.1",
        "requests>=2.24.0",
        "six>=1.15.0"
    ],
    entry_points={
        'console_scripts': [
            'screener = screener.cli.cli:main'
        ]
    }
)
