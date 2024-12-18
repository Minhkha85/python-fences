from setuptools import setup, find_packages

setup(
    name="PythonFences",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'PyQt6>=6.0.0',
        'pywin32>=305',
        'watchdog>=2.1.0',
        'mouse>=0.7.1'
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A desktop organization tool inspired by Stardock Fences",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/python-fences",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.7',
) 