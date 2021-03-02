from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="twobodyproblem",
    version="0.2.0",
    description="This is a little simulation for the gravitational two body problem.",
    long_description=long_description,
    author="Florian Frauenfelder",
    author_email="florian.l.frauenfelder@gmail.com",
    url="https://github.com/flopsi-l-f/two-body-problem_simulation",
    keywords="simulation, gravitation, pyside, vpython",
    python_requires=">=3.8",
    package_data={"twobodyproblem": ["ui"]},
    packages=["twobodyproblem", "twobodyproblem.visualization"],
    install_requires=[
        "pyyaml>=5.4.1",
        "pyside6>=6.0.1",
        "vpython>=7.6.1"
    ],
)
