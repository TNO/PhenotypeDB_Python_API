import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="phenodb_api", 
    version="0.0.1",
    author="Serdar Ozsezen",
    author_email="serdar.ozsezen@tno.nl",
    description="Python API for collecting data from Phenotype Database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab-dv.tno.nl/DataScience-MSB/Tools/phenotypedb_python_api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)