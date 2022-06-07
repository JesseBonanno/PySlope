from setuptools import setup
import os
import versioneer

_here = os.path.abspath(os.path.dirname(__file__))

# Store the README.md file
with open(os.path.join(_here, "README.md"), encoding="utf-8") as f:
    longDescription = f.read()

version = versioneer.get_version()

setup(
    name="pyslope",  # How you named your package folder (MyLib)
    packages=["pyslope"],  # Chose the same as "name"
    version=version,  # Start with a small number and increase it with every change you make
    cmdclass=versioneer.get_cmdclass(),
    license="MIT",  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description="A 2D Slope Stability Software using bishops method",  # Give a short description about your library
    # Long description from README.md
    long_description=longDescription,
    long_description_content_type="text/markdown",
    author="Jesse Bonanno",  # Type in your name
    author_email="jessebonanno@gmail.com",  # Type in your E-Mail
    url="https://github.com/JesseBonanno/pyslope",  # Provide either the link to your github or to your website
    download_url="https://github.com/JesseBonanno/pyslope/archive/"
    + version
    + ".tar.gz",
    keywords=[
        "geotechnical",
        "slope",
        "stability",
        "civil",
        "engineering",
        "bishops",
    ],  # Keywords that define your package best
    install_requires=[
        "colour>=0.1.5",
        "tqdm>=4.54.1",
        "plotly>=4.14.1",
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",  # Again, pick a license
        "Programming Language :: Python :: 3",  # Specify which pyhton versions that you want to support
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
