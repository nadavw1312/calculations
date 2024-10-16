from setuptools import setup, find_packages

setup(
    name="calculations",  # The name of your package
    version="0.1.0",    # Version of the package
    packages=find_packages(),  # Automatically find all packages inside the directory
    install_requires=[
        "requests",   # List your dependencies here
        "polars"
    ],
    description="A simple package for my project",
    url="https://github.com/nadavw1312/calculations",  # URL to your repository
    author="Nadav Bourla",
    author_email="nadavw1312@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
