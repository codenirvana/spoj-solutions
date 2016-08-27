from setuptools import setup

setup(
    name='spojsol',
    version='0.0.1',
    description='Download your spoj solutions',
    author='Udit Vasu',
    author_email='admin@codenirvana.in',
    license='MIT',
    url='https://github.com/codenirvana/spoj-solutions',
    packages=['spojsol'],
    install_requires=[
        'grequests==0.3.0',
        'beautifulsoup4==4.5.1',
        'Requests==2.11.1'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    keywords="spoj solutions command line tool",
    entry_points={
        'console_scripts': [
            'spojsol = spojsol.spojsol:main'
        ],
    }
)
