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


def parse_requirements_file(path):
    with open(path) as fp:
        dependencies = (d.strip() for d in fp.read().split("\n") if d.strip())
        return [d for d in dependencies if not d.startswith("#")]


setup(
    name="botbase",
    version=version,
    author="ooliver",
    author_email="oliverwilkes2006@hotmail.com",
    description="TODO:",
    url="https://github.com/chit-chat-devs/botbase",
    packages=[
        "botbase",
    ],
    install_requires=parse_requirements_file("requirements.txt"),
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
