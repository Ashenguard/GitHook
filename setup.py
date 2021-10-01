import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyGitHook",
    version="0.1.0",
    license='MIT License',
    author="Ashenguard",
    author_email="Ashenguard@agmdev.xyz",
    description="Simple professional github webhook manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ashengaurd/githook",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    include_package_data=True,
    install_requires=["flask", "requests", "json"],
)
