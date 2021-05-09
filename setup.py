import os
from setuptools import setup

with open("README.md") as fid:
    README = fid.read()

with open("requirements.txt") as reqf:
    reqs = map(lambda x: x.strip(), reqf.readlines())
    reqs = filter(lambda x: x != "pyinstaller", reqs)
    reqs = filter(lambda x: x, reqs)
    reqs = list(reqs)

setup(
    name="utsushis-charm",
    version="1.0.0",
    description="Read the latest Real Python tutorials",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/chpoit/utsushis-charm",
    author="chpoit",
    author_email="chpoit@chpoit.com",
    license="MIT",
    packages=["src"],
    include_package_data=True,
    install_requires=reqs,
    entry_points={"console_scripts": ["utsushis-charm=main:main"]},
    # console=["main.py"]
)

# setup(console=["main.py"])
