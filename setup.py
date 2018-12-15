import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='netlify_deployer',
    version='0.0.1',
    author='Cyryl Płotnicki',
    author_email='cyplo@cyplo.net',
    description='Package to help with deploying Netlify',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cyplo/netlify_deployer',
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
