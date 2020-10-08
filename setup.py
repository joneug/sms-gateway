from setuptools import setup, find_packages
import io


def readme():
    with io.open('README.md', encoding='utf-8') as f:
        return f.read()


setup(
    name='sms-gateway',
    description='Web App Serving as an SMS Gateway based on Gammu',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/joneug/sms-gateway',
    author='joneug',
    packages=find_packages('.'),
    keywords=['SMS', 'gateway', 'gammu'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Environment :: Console",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=' >= 3.5',
    version='0.1.4',
    license='MIT',
    install_requires=[
        "falcon >= 2.0.0",
        "falcon_auth >= 1.1.0",
        "python-gammu >= 3.1"
    ],
    entry_points={
        'console_scripts': [
            'sms-gateway = sms_gateway.__main__:main'
        ]
    },
    project_urls={
        'Documentation': 'https://github.com/joneug/sms-gateway',
        'Source': 'https://github.com/joneug/sms-gateway',
        'Tracker': 'https://github.com/joneug/sms-gateway/issues',
    }
)
