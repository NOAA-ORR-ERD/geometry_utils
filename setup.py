from setuptools import setup
import versioneer

# package requirements go here
requirements = ["numpy",
                ]

setup(
    name='geometry_utils',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Utilities for basic computational geometry directly with numpy arrays.",
    author="Christopher Barker, Rob Hetland",
    author_email='Chris.Barker@noaa.gov',
    url='https://github.com/NOAA-ORR-ERD/geometry_utils',
    packages=['geometry_utils'],
    install_requires=requirements,
    keywords='geometry_utils',
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ]
)
