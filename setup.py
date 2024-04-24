from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT='-e .'    # we have to avoid -e . to be read from requirements
def get_requirements(file_path:str)->List[str]:
    '''
    returns the list of requirements
    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","")for req in requirements]   #avoid the newline character in each line of requirement.txt

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requirements

setup(
    name='mode choice prediction',
    version='0.0.1',
    author='Gavaskar',
    author_email='mgavaskar24@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'),
)


