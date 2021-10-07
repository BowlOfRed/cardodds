from setuptools import setup

setup(
    name='cardodds',
    version='0.1',
    py_modules=['cardodds'],
    install_requires=[
        'Click',
        'tabulate',
    ],
    entry_points='''
        [console_scripts]
        cardodds=cardodds:report
    ''',
)
