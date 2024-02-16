""" SwanSDK setup code """

from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "PIPRELEASEDOC.md").read_text()


# There are some placeholder for future needs
# TODO: Delete/Modify placeholders as needed
setup(
    name="swan-sdk",
    version="0.1.0",
    author="FilSwan",  # Placeholder for author's name
    author_email="author@email.com",  # Placeholder for author's email
    install_requires=["web3==5.31.1", "requests==2.28.1", "requests_toolbelt==0.10.1"],
    packages=["swan", "swan.common", "swan.api"],
    license="MIT",
    include_package_data=True,
    description="A python software development kit for Swan services",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/username/package",  # Placeholder for URL
    python_requires=">=3.10",  # Specifies the required Python version
    classifiers=[
        # Placeholder for classifiers
        # EXAMPLE
        # "Development Status :: 3 - Alpha",
        # "Intended Audience :: Developers",
        # "License :: OSI Approved :: MIT License",
        # "Programming Language :: Python :: 3.10",
    ],
    entry_points={
        "console_scripts": [
            # Placeholder for entry points
            # "our_command = our_package.module:main_function",
        ],
    },
    extras_require={
        # Placeholder for extras
        # "extra_feature": ["extra_dependency"],
    },
    package_data={
        "package": [
            # Placeholder for package data
            # "data/*.txt",
        ],
    },
    scripts=[
        # Placeholder for scripts
        # "bin/script.py",
    ],
)
