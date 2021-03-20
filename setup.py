from setuptools import setup

PROJECT_NAME = "data_wallet.py"
DEPENDENCIES_FILE = "requirements.txt"


def _read_dependencies_file(file):
    return open(file).read().splitlines()


setup(
    name=PROJECT_NAME,
    packages=["data_wallet.blockchain",
              "data_wallet.common",
              "data_wallet.non_transactional",
              "data_wallet.transactional"
              ],
    authors=["Gabriel N. Mendes", "Karina Figueiró", "Caique Baracho"],
    authors_email=["nscbiel@gmail.com"],
    install_requires=_read_dependencies_file(file=DEPENDENCIES_FILE)
)
