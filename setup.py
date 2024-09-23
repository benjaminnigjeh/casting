from setuptools import find_packages, setup

setup(
    name="casting",
    version="0.0.1",
    author="Ben Nigjeh",
    author_email="benjamin.nigjeh@gmail.com",
    install_requires=["fisher_py","pyteomics", "matplotlib", "pandas", "numpy", "wget", "h5py", "tensorflow", "keras", "spectrum_utils", "streamlit", "torch"],
    packages=find_packages()
)