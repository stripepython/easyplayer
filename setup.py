from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()
with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = f.read().split('\n')

setup(
    name='easyplayer',
    author_email='stripe-python@139.com',
    author='stripe-python',
    maintainer='stripe-python',
    maintainer_email='stripe-python@139.com',
    packages=find_packages(),
    version='0.2.1',
    description='Easyplayer is a python library that encapsulates the complex API of pygame2 to help users build games faster.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    url='https://github.com/stripepython/easyplayer',
    download_url='https://github.com/stripepython/easyplayer',
    install_requires=requirements,
)
