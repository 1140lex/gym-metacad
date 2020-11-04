from setuptools import setup

setup(name='gym_metacad',
	version='0.0.1',
	author="Jasper Yao"
	author_email="jasper.yao.iso@gmail.com"
	description='OpenAI gym (and universe) integration into MetaCAD'
	install_requires=['numpy','gym', 'universe', 'pyzmq', 'python-socketio']
)