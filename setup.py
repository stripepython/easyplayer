from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='easyplayer',
    author_email='stripe-python@139.com',
    author='stripe-python',
    maintainer='stripe-python',
    maintainer_email='stripe-python@139.com',
    py_modules=find_packages(),
    version='0.1.1',
    description='Easyplayer is a python library that encapsulates the complex API of pygame2 to help users build games faster.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=['pygame==2.1.2', 'click~=8.0.3', 'numpy~=1.21.0',
                      'opencv-python~=4.5.2.54', 'tqdm~=4.47.0', 'pydub~=0.24.1',
                      'pillow~=8.3.0', 'requests~=2.25.1', 'aiml~=0.9.2',
                      'pinyin2hanzi~=0.1.1', 'pyttsx3~=2.90', 'future~=0.18.2',
                      'dataclasses~=0.6'],
    python_requires='>=3.6',
    url='https://github.com/stripepython/easyplayer',
    download_url='https://github.com/stripepython/easyplayer',
)
