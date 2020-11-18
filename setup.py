from setuptools import setup

setup(name='gym_metacad',
	version='0.0.1',
	author="Jasper",
	author_email="Ethycs@users.noreply.github.com",
	description='OpenAI gym integration into MetaCAD',
	install_requires=['numpy','gym', 'pyppeteer', 'python-socketio', 'uvicorn']
)