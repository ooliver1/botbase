import re
from setuptools import setup


_version_regex = (
    r"^__version__ = ('|\")((?:[0-9]+\.)*[0-9]+(?:\.?([a-z]+)(?:\.?[0-9])?)?)\1$"
)

try:
    with open("botbase/__init__.py") as f:
        match = re.search(_version_regex, f.read(), re.MULTILINE)
        assert match is not None
        version = match.group(2)
except FileNotFoundError:
    version = "0.0.0"


setup(
    name="botbase",
    version=version,
    author="ooliver",
    author_email="oliverwilkes2006@hotmail.com",
    description="A personal nextcord bot base package for bots.",
    url="https://github.com/chit-chat-devs/botbase",
    packages=[
        "botbase",
    ],
    install_requires=open("requirements.txt").read().splitlines(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "botbase = botbase.cli:main",
        ],
    },
)
