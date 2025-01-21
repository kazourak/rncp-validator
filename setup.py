from setuptools import setup, find_packages
from os.path import exists

setup(
    name="rncp-validator",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "et_xmlfile==2.0.0",
        "gitdb==4.0.12",
        "GitPython==3.1.44",
        "openpyxl==3.1.5",
        "smmap==5.0.2"
    ],
    entry_points={
        'console_scripts': [
            'rncp-validator=rncp_validator.checker:main',
        ],
    },
    author="nskiba & leofarina",
    author_email="nskiba@student.42angouleme.fr",
    description="Validateur des commits RNCP",
    long_description=open("README.md").read() if exists("README.md") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/kazourak/rncp-validator",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)