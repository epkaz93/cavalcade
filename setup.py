import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cavalcade",
    version="1.0.1",
    author="Thomas Wilmot",
    author_email="thomaswilmot@gmail.com",
    description="A lightweight, asynchronous event library for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/epkaz93/cavalcade",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True
)
