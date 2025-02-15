# setup.py in the top-level "my_agent_monorepo" directory
from setuptools import setup, find_packages

setup(
    name="agent_monorepo",     # or whatever you choose
    version="0.1.0",
    packages=find_packages(),     # will find agent_core, interfaces, etc.
)
