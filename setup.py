from setuptools import setup, find_packages

setup(
    name='flask-rq',
    version='0.0.1',
    description='Practice setting up flask with rq for async jobs.',
    url='https://github.com/alysivji/flask-rq',
    author='Aly Sivji',
    author_email='alysivji@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(exclude=['tests', ]),
    install_requires=[''],
    download_url='https://github.com/alysivji/flask-rq',
)
