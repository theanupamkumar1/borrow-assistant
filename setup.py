from setuptools import setup, find_packages
from typing import List

hypen_e_dot = "-e ."

def get_req(file_path: str) -> List[str]:
    req = []
    with open(file_path, 'r', encoding='utf-8') as f:
        req = f.readlines()
        req = [r.strip() for r in req]
        if hypen_e_dot in req:
            req.remove(hypen_e_dot)
    return req

setup(
    name="borrow assistant",
    description="An assistant to help you keep track of your borrowings",
    author="Anupma Kumar",
    packages=find_packages(),
    install_requires=get_req('requirements.txt')
)