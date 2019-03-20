import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="HeimdallMultiwii",
    version="1.1.5.dev1",
    author="Roger Moreno",
    author_email="rgrdevelop@gmail.com",
    description="Adapter for FCB Multiwii communications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/roger357/HeimDallMultiwii",
    packages=setuptools.find_packages(),
    keywords=['MultiWii', 'drone', 'HeimdallMultiWii'],
    python_requires='>=3.6',
    install_requires=[
        'pyserial==3.4',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
)