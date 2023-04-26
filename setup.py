from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in offline_update/__init__.py
from offline_update import __version__ as version

setup(
	name="offline_update",
	version=version,
	description="/erpnext/frappe-bench$ bench new-app offline_update",
	author="App Title [Offline Update]: Frappe Offline Updater",
	author_email="afarran1992@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
