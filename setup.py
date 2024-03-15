""" SwanSDK setup code """

from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "PIPRELEASEDOC.md").read_text()


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
        name="orchestrator-sdk",
        version="0.1.0",
        packages=find_packages(),
        description="A python developer tool kit for Swan Orchestrator services.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/swanchain/orchestrator-sdk",
        author="Filswan",
        author_email="zhchen@nbai.io",
        license="MIT",
        classifiers=[
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
        ],
        install_requires=[
            "requests==2.28.1",
            "requests-toolbelt==0.10.1",
            "web3==6.15.1",
            "tqdm==4.64.1"
            ],
        entry_points={
            # placeholder
        },
        )