from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vloginit",
    version="0.0.2",
    author="Vladislav Borshch, Shekhalev Denis",
    author_email="borchsh.vn@mail.com, diod2003@list.ru",
    description="Simple script for verilog/systemverilog module templates generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license ='MIT',
    url="https://gitlab.com/vborshch/vloginit",
    project_urls={
        "Bug Tracker": "https://gitlab.com/vborshch/vloginit/issues",
    },
    packages=find_packages(),
    entry_points ={
        'console_scripts': [
            'vloginit = vloginit.main:main'
        ]
    },
    zip_safe=False,
    include_package_data=True,
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
