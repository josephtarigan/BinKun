from setuptools import find_packages
from setuptools import setup

REQUIRED_PACKAGES = ['tflite==2.1.0',
                     'tflite-runtime==2.1.0'
                     'h5py==2.9.0',
                     'matplotlib==3.0.3',
                     'Pillow==6.2.1']

setup(
    name='automatic-trash-bin',
    version='0.1',
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    include_package_data=True,
    description='Automatic Trash Bin'
)