from setuptools import setup, find_packages

setup(
    name='Genesys',
    version='1.0',
    packages=find_packages(),
    package_data={'': ['*.yaml']},
    author='Matheus Almeida Santos Mendonça',
    author_email='matheuzengenharia@gmail.com',
    description='é uma ferramenta para automatizar os processos dos fluxos do Genesys Cloud',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Matheus-Sueth/GenesysFlow.git',
    install_requires=[
        'python-dotenv',
        'PyYAML',
        'requests',
        'setuptools'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ],
)
