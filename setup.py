from setuptools import find_packages, setup

setup(
    name="robo_sim",
    version="0.1.0",
    author="Camille Dunning",
    author_email="dunningcamille@gmail.com",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "matplotlib",
        "colorlog",
        "pydantic",
        "pyyaml",
        "pytest",
    ],
    entry_points={
        "console_scripts": [
            "robo_sim=robo_sim.cli.run:main",
        ],
    },
    description="A simple 2D robotics simulation package.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/camille-004/robo-sim",
)
