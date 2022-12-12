from setuptools import setup, find_packages

setup(
    name="mygls-client",
    version="1.0.0",
    author="Adam Kornafeld",
    description="MyGLS python client",
    long_description="Python client to create parcel labels using the MyGLS API",
    url="https://github.com/adamkornafeld/mygls-client",
    keywords="gls, api, rest, package, parcel, label" "print",
    python_requires=">=3.8",
    packages=find_packages(
        include=[
            "gls",
        ]
    ),
    install_requires=[
        "pydantic>=1.10.2,<2.0.0",
        "requests>=2.28.1,<3.0.0",
    ],
    package_data={}
)
