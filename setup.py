from setuptools import setup

setup(
    name='p5Launcher', 
    version='0.1.0', 
    author='LF', 
    description='launches p5 sketches into a standalone window',
    install_requires=['pywebview', 'pyp5js', 'transcrypt', 'livereload']
)