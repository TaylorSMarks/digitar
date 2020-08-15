from setuptools import setup

version = '0.1.1'

setup(
    name='digitar',
    version=version,
    url='https://github.com/TaylorSMarks/digitar/',
    author='Taylor S. Marks',
    author_email='tayor@marksfam.com',
    description='A python library for easily playing notes - possibly even composing songs.',
    keywords = 'audio music notes synthesis guitar',
    py_modules=['digitar'],
    platforms='any',
    install_requires=[
        'musical',
        'pygame'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Artistic Software',
        'Topic :: Multimedia :: Sound/Audio :: Sound Synthesis',
    ],
)
