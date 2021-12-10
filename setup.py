from setuptools import setup, find_packages

setup(
    name='typeidea',
    version='0.1',
    description='Blog System base on Django',
    author='liuhao',
    author_email='2226958871@qq.com',
    url='http://www.PurpleHin.cn',
    license='MIT',
    packages=find_packages('typeidea'),
    package_dir={'': 'typeidea'},
    package_data={
        '': [
            'themes/*/*/*/*',
        ]
    },
    install_requires=[
        'Django!=1.11',
        'django-autocomplete-light==3.2.10',
        'django-ckeditor==5.4.0',
        'django-redis==4.9.0',
        'django-silk==3.0.0',
        'djangorestframework==3.8.2',
        'mistune==2.0.0',
        'mysqlclient==2.1.0',
        'PyMySQL==1.0.2',
        'pypiserver==1.4.2',
    ],
    extras_require={
        'ipython': ['ipython==6.2.1']
    },
    scripts=[
        'typeidea/manage.py',
    ],
    entry_points={
        'console_scripts': [
            'typeidea_manage = manage:main'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Programming Language :: Python :: 3.6',
    ]
)