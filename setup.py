from setuptools import setup

setup(
    name='mysql_object',
    version='0.0.3',    
    description='Simple way to query MySQL',
    url='https://github.com/diversen/python-mysql-object',
    author='Dennis Iversen',
    author_email='dennis.iversen@gmail.com',
    license='MIT',
    packages=['mysql_object'],
    install_requires=['mysql-connector-python>=8.0.31'],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.10',
    ],
)
