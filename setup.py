from setuptools import setup, find_packages

setup(
    name="PythonFences",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        'PyQt6>=6.0.0',
        'pywin32>=305',
        'watchdog>=2.1.0',
        'mouse>=0.7.1',
        'requests>=2.25.0'
    ],
    author="Minhkha85",
    author_email="your.email@example.com",
    description="A desktop organization tool inspired by Stardock Fences",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Minhkha85/python-fences",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Development Status :: 4 - Beta",
    ],
    python_requires='>=3.7',
) 