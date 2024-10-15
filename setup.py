from setuptools import setup, find_packages

setup(
    name="vgdbcli",
    description="""
    Ferramenta para automatizar o envio de informações
    para a aplicação Viral Genomes DataBase (VGDB)
    """,
    version="1.0.0",
    authors="Filipe Dezordi",
    authors_emails='zimmer.filipe@gmail.com"',
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.1.0,<8.2.0",
        "pandas>=2.1.0,<2.2.0",
        "numpy>=1.26.0,<1.27.0",
        "pydantic>=2.8.0,<2.9.0",
    ],
    entry_points={
        "console_scripts": [
            "vgdbcli = vgdbcli.cli.main:cli",
        ],
    },
)
