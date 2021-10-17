from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='p5Launcher', 
    version='0.1.1', 
    author='LF', 
    description='launches p5 sketches into a standalone window',
    long_description=long_description,
    long_description_content_type = 'text/markdown',
    install_requires=['pywebview==3.4', 'pyp5js', 'livereload'],
    url='https://github.com/lorenzoferrone/p5Launcher',
    keywords=['p5js', 'creative coding', 'processing'],
)
