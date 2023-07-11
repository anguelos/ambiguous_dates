from setuptools import setup, find_packages

setup(
    name='tkinter_probabilistic_date',
    version='0.0.1',
    author='Anguelos Nicolaou',
    author_email='anguelos.nicolaou@gmail.com',
    description='A tkinter widget for entering a date range with uncertainty',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'probable_date_demo=bin.probable_date_demo:main'
        ]
    },
    install_requires=[
        'tkinter', 'matplotlib', 'numpy', 'typing_extensions', 'fargv'
    ],
)
