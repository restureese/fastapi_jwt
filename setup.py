import setuptools

with open("requirements.txt", "r") as fh:
    requirements = fh.read()
setuptools.setup(
     name='fastapi_jwt',
     version='0.0.1',
     scripts=['dokr'] ,
     author="Restu Reese",
     author_email="restureese@gmail.com",
     description="library for FastAPI JWT",
     url="https://github.com/restureese/fastapi_jwt",
     packages=setuptools.find_packages(),
     install_requires=requirements.splitlines(),
     classifiers=[
         "Programming Language :: Python :: 3.6",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )