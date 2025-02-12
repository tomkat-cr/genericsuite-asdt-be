from setuptools import setup

version = '0.1.0'
description = 'GenericSuite Agentic Software Development Team (ASDT) backend.'
long_description = '''
The GenericSuite ASDT
=====================

GenericSuite Agentic Software Development Team (backend version) provides a
 team of autonomous entities designed to solve software development problems
 using AI to make decisions, learn from interactions, and adapt to changing
 conditions without human intervention.
'''.lstrip()

# https://pypi.org/classifiers/

classifiers = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: ISC License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',
    "Operating System :: OS Independent",
    'Topic :: Software Development',
]

setup(
    name='genericsuite_asdt',
    python_requires='>=3.10,<=3.13',
    version=version,
    description=description,
    long_description=long_description,
    author='Carlos J. Ramirez',
    author_email='tomkat_cr@yahoo.com',
    url='https://github.com/tomkat-cr/genericsuite-asdt-be',
    license='ISC License',
    py_modules=['genericsuite_asdt'],
    classifiers=classifiers,
)
