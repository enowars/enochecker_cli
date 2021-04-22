import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='enochecker_cli',
    version='0.5.0',
    entry_points = {
        "console_scripts": ['enochecker_cli = enochecker_cli.base:main']
    },
    author="Benedikt Radtke",
    author_email="benediktradtke@gmail.com",
    description="Enochecker CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/enowars/enochecker_cli",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
     python_requires=">=3.7",
 )
