import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="VegasInsiderPy",
    version="0.0.1",
    author="Brady Wyllie",
    author_email="bpewyllie@gmail.com",
    description="Scraper for Vegas Insider historical odds and betting pages.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bpewyllie/vipy",
    packages=setuptools.find_packages(),
    # package_data={'ViPy': ['assets/*.csv']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)