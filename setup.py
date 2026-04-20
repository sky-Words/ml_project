from typing import List

from setuptools import find_packages, setup


HYPHEN_E_DOT = "-e ."


def get_requirements(file_path: str) -> List[str]:
    """Return requirements from a requirements file."""
    requirements = []

    with open(file_path, encoding="utf-8") as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.strip() for req in requirements]
        requirements = [req for req in requirements if req and not req.startswith("#")]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)

    return requirements


if __name__ == "__main__":
    setup(
        name="first_ml_project",
        version="0.1.0",
        author="Elmehidi",
        author_email="mehdi.sadki.dev@gmail.com",
        packages=find_packages(),
        install_requires=get_requirements("requirements.txt"),
    )
