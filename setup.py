from setuptools import setup, find_packages

setup(
	name='chenv',
	version='0.0.1',
	packages=find_packages(),
	entry_points={
		'console_scripts':[
			'chenv-core = chenv.core:main'
		]
	}
)