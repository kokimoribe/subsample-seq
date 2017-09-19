"""
Subsample FASTA and FASTQ files.
"""
from setuptools import find_packages, setup


setup(
    name='subsample-seq',
    version='0.1.0',
    url='https://gitlab.com/koki.moribe/subsample-seq',
    license='MIT',
    author='Koki Moribe',
    author_email='koki.moribe+coding@gmail.com',
    description='Subsample FASTA and FASTQ files.',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=['biopython', 'click'],
    tests_require=['pytest', 'pylint'],
    entry_points={
        'console_scripts': [
            'subsample-seq = subsample_seq.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
