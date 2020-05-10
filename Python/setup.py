import setuptools

setuptools.setup(
     name='unusedImports',  
     version='0.1',
     scripts=['index.py'] ,
     author="Amal Jose",
     author_email="amaljose96@gmail.com",
     description="To figure out which JS/JSX files are not used by the node project",
     long_description="To figure out which JS/JSX files are not used by the node project",
     url="https://github.com/amaljose96/js-unused-imports",
     packages=setuptools.find_packages(),
     keywords = ['scanner', 'js', 'jsx', 'unused', 'stale imports', 'imports'], 
     classifiers=[ 
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Refactor Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 2',      #Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 2.7',
     ],
 )