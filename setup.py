import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="regexploit",
    version="1.0.0",
    author="Ben Caller :: Doyensec",
    author_email="REMOVETHISPREFIX.ben@doyensec.com",
    description="Find regular expressions vulnerable to ReDoS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/doyensec/regexploit",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: Apache Software License',
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    extras_require={
        "yaml": ['pyyaml>=5.3.1']
    },
    scripts=[
        # Easy-install uses imports, so can miss findings
        "regexploit/bin/regexploit-python-env",
    ],
    entry_points={
        "console_scripts": [
            "regexploit=regexploit.bin.regexploit:main",
            "regexploit-js=regexploit.bin.regexploit_js:main",
            "regexploit-py=regexploit.bin.regexploit_python_ast:main",
            "regexploit-yaml=regexploit.bin.regexploit_yaml:main_yaml",
            "regexploit-json=regexploit.bin.regexploit_yaml:main",
            "regexploit-csharp=regexploit.bin.regexploit_csharp:main",
        ],
    },
)
