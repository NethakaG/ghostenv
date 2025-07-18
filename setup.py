from setuptools import setup, find_packages

setup(
    name="ghostenv",
    version="0.1.0",
    description="Temporary, disposable virtual environments for testing pip packages",
    author="Nethaka Himara Galagedera",
    author_email="nethaka.galagedera@gmail.com",
    packages=find_packages(),
    install_requires=[
        "typer>=0.9.0",
    ],
    entry_points={
        "console_scripts": [
            "ghostenv=ghostenv.main:app",
        ],
    },
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)