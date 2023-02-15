"""Setup"""
import os
import pathlib
import zipfile
from typing import List

from setuptools import find_packages, setup
from setuptools.command.install import install

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


class InstallWrapper(install):
    """Pre install commands"""

    def run(self):
        print(">>>>>>>>--------- Installation Started...")
        install.run(self)  # Run the standard PyPi copy
        print(">>>>>>>>--------- Installation Completed!")


def unzip_model_file(file_path, directory_path):
    """Unzip model file"""
    print(">>>>>>>>--------- In function unzip_model_file()...", directory_path)
    try:
        if os.path.isfile(file_path):
            with zipfile.ZipFile(file_path, "r") as z:
                z.extractall(directory_path)  # unzip
            os.remove(file_path)
    except OSError as e:
        print("Skipping unzipping due to read-only access in folder. Error: ", str(e))


def read_requirements(name: str) -> List[str]:
    """
    To read the requirements
    """
    file = f"./requirements/{name}.txt"
    fpath = os.path.join(HERE, file)
    with open(fpath) as data:
        return [line.strip() for line in data if line.strip() and not line.strip().startswith("#")]


requirements = read_requirements("install")
test_requirements = read_requirements("test")
dev_requirements = read_requirements("dev")

setup(
    name="Multi Module Python Project",
    version="0.0.1",
    author="Knoldus Data Science Team",
    author_email="datascience@knoldus.com",
    url="https://github.com/knoldus/python_bootstrap_best_practices.git",
    packages=find_packages("src"),
    package_dir={"rasa_app": "src/rasa_app"},
    description="This library is used to perform parsing and mapping of the documents.",
    long_description=README,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    extras_require={
        "test": test_requirements,
        "dev": dev_requirements,
        "all": test_requirements + dev_requirements,
    },
    include_package_data=True,
)
