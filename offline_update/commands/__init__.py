
from frappe.commands import pass_context, get_site
import subprocess, platform
import click
import os
from frappe.utils import get_bench_path  # noqa
from offline_update.utils.cli import (
	MultiCommandGroup,
	print_bench_version,
	use_experimental_feature,
	setup_verbosity,
)
from offline_update import dirs
# dirs = {
# 	'pip_dir': os.path.join(get_bench_path(), "pip_lib"),
# 	'yarn_dir': os.path.join(get_bench_path(), "yarn_lib")
# }
# pip_dir = os.path.join(get_bench_path(), "pip_lib")

@click.group(cls=MultiCommandGroup)
@click.option(
	"--version",
	is_flag=True,
	is_eager=True,
	callback=print_bench_version,
	expose_value=False,
)
@click.option(
	"--use-feature",
	is_eager=True,
	callback=use_experimental_feature,
	expose_value=False,
)
@click.option(
	"-v",
	"--verbose",
	is_flag=True,
	callback=setup_verbosity,
	expose_value=False,
)
def bench_command(bench_path=get_bench_path()):
	import offline_update

	offline_update.set_frappe_version(bench_path=bench_path)


@click.command("d-reqs", help="Download all python and node requirements run after online update immediately while you still have internet connection to update offline libraries.")
@click.option("--no-cache", is_flag=True, help="Disable the cache for pip.")
@pass_context
def download_reqs(context, no_cache):
	from offline_update.install import download_reqs
	from offline_update.bench import Bench
 
	download_reqs(
    	Bench(get_bench_path()).apps,
    	dirs,
    	no_cache=no_cache
    )


@click.command("offline-update", help="Trigger Offline Update")
@click.option("--pull", is_flag=True, help="Pull updates for all the apps in bench")
@click.option("--apps", type=str)
@click.option("--patch", is_flag=True, help="Run migrations for all sites in the bench")
@click.option("--build", is_flag=True, help="Build JS and CSS assets for the bench")
@click.option(
	"--requirements",
	is_flag=True,
	help="Update requirements. If run alone, equivalent to `bench setup requirements`",
)
@click.option(
	"--restart-supervisor", is_flag=True, help="Restart supervisor processes after update"
)
@click.option(
	"--restart-systemd", is_flag=True, help="Restart systemd units after update"
)
@click.option(
	"--no-backup",
	is_flag=True,
	help="If this flag is set, sites won't be backed up prior to updates. Note: This is not recommended in production.",
)
@click.option(
	"--no-compile",
	is_flag=True,
	help="If set, Python bytecode won't be compiled before restarting the processes",
)
@click.option("--force", is_flag=True, help="Forces major version upgrades")
@click.option(
	"--reset",
	is_flag=True,
	help="Hard resets git branch's to their new states overriding any changes and overriding rebase on pull",
)
@pass_context
def offline_update(
    context,
	pull,
	apps,
	patch,
	build,
	requirements,
	restart_supervisor,
	restart_systemd,
	no_backup,
	no_compile,
	force,
	reset,
):
    
	from offline_update.utils.bench import update

	update(
		pull=pull,
		apps=apps,
		patch=patch,
		build=build,
		requirements=requirements,
		restart_supervisor=restart_supervisor,
		restart_systemd=restart_systemd,
		backup=not no_backup,
		compile=not no_compile,
		force=force,
		reset=reset,
	)


commands = [
    offline_update,
	download_reqs
]

	# from offline_update.bench import Bench
	
	# # if not have_internet("8.8.8.8"):
	# # 	pip_dir = None
	# bench = Bench(get_bench_path())
	# bench_apps = bench.apps
	# dev_dependencies = {}
	# proj_dependencies = []
	# requires = []
	# with open(os.path.join(dirs['pip_dir'], 'pip_requirements.txt'), 'w+') as pip_req:
	# 	for app in bench_apps:
	# 		path = os.path.join(get_bench_path(), 'apps', app)
	# 		if os.path.isfile(os.path.join(path, 'requirements.txt')):
	# 			with open(os.path.join(path, 'requirements.txt'), 'r') as req:
	# 				# if req.readlines()
	# 				dep = req.readline().strip()
	# 				if dep not in [
	# 					'frappe',
	# 					'erpnext',
	# 					"# frappe -- https://github.com/frappe/frappe is installed via 'bench init'"
	# 				]:
	# 					pip_req.writelines([dep, '\n'])
	# 		elif os.path.isfile(os.path.join(path, 'pyproject.toml')):
	# 			try:
	# 				from tomli import load
	# 			except ImportError:
	# 				from tomllib import load
	# 			with open(os.path.join(path, 'pyproject.toml'), 'rb') as req:
	# 				toml_dict = load(req)
	# 				for dep in list(toml_dict.get("project", {}).get("dependencies")):
	# 					proj_dependencies.append(dep.split(",")[0])
	# 				for dep in list(toml_dict.get("build-system", {}).get("requires")):
	# 					requires.append(dep.split(",")[0])
	# 				for k, v in toml_dict.get("tool", {}).get("bench",{}).get("dev-dependencies", {}).items():
	# 					dev_dependencies[k] = v
	# 	if proj_dependencies:
	# 		for v in proj_dependencies:
	# 			# print(re.findall(r'\w+', v))
	# 			pip_req.writelines([v, '\n'])
	# 	if requires:
	# 		for v in requires:
	# 			pip_req.writelines([v, '\n'])
	# 	if dev_dependencies:
	# 		for k,v in dev_dependencies.items():
	# 			pip_req.writelines([k + v, '\n'])
	
	# subprocess.call(
	# 		f"pip download -d {dirs['pip_dir']} -r {os.path.join(dirs['pip_dir'], 'pip_requirements.txt')}",
	# 		shell=True
	# 	)

	# subprocess.call(
	# 		f"yarn config set yarn-offline-mirror {dirs['yarn_dir']}",
	# 		shell=True
	# 	)

	# for app in bench_apps:
	# 	path = os.path.join(get_bench_path(), 'apps', app)
	# 	if os.path.isfile(os.path.join(path, 'yarn.lock')):
	# 		os.remove(os.path.join(path, 'yarn.lock'))
	# 		print(f"Downloading {app} Node Packages.....")
	# 		subprocess.call(
	# 				"yarn install",
	# 				shell=True,
	# 				cwd=path
	# 		)

# def ping(host):
#     """
#     Returns True if host responds to a ping request
#     """
#     import subprocess, platform

#     # Ping parameters as function of OS
#     ping_str = "-n 1" if  platform.system().lower()=="windows" else "-c 1"
#     args = "ping " + " " + ping_str + " " + host
#     need_sh = False if  platform.system().lower()=="windows" else True

#     # Ping
#     return subprocess.call(args, shell=need_sh) == 0


@click.command("offline-new-app", help="Create a new Frappe application under apps folder")
@click.option(
	"--no-git",
	is_flag=True,
	flag_value="--no-git",
	help="Do not initialize git repository for the app (available in Frappe v14+)",
)
@click.argument("app-name")
def new_app(app_name, no_git=None):
	from offline_update.app import new_app

	new_app(app_name, no_git)



@click.command("offline-install-app", help="Install App OFFLINE",)
@click.argument("apps", nargs=-1)
@click.option("--force", is_flag=True, default=False)
@pass_context
def install_app(context, apps, force=False):
	"Install a new app to site, supports multiple apps"
	from offline_update.app import install_app as _install_app
	from frappe.utils.synchronization import filelock

	exit_code = 0

	if not context.sites:
		raise SiteNotSpecifiedError

	for site in context.sites:
		frappe.init(site=site)
		frappe.connect()

		with filelock("install_app", timeout=1):
			for app in apps:
				try:
					_install_app(app, verbose=context.verbose, force=force)
				except frappe.IncompatibleApp as err:
					err_msg = f":\n{err}" if str(err) else ""
					print(f"App {app} is Incompatible with Site {site}{err_msg}")
					exit_code = 1
				except Exception as err:
					err_msg = f": {err!s}\n{frappe.get_traceback(with_context=True)}"
					print(f"An error occurred while installing {app}{err_msg}")
					exit_code = 1

			if not exit_code:
				frappe.db.commit()

		frappe.destroy()

	sys.exit(exit_code)


@click.command(
	["offline-get", "offline-get-app"],
	help="OFFLINE Clone an app from the internet or filesystem and set it up in your bench",
)
@click.argument("name", nargs=-1)  # Dummy argument for backward compatibility
@click.argument("git-url")
@click.option("--branch", default=None, help="branch to checkout")
@click.option("--overwrite", is_flag=True, default=False)
@click.option("--skip-assets", is_flag=True, default=False, help="Do not build assets")
@click.option(
	"--soft-link",
	is_flag=True,
	default=False,
	help="Create a soft link to git repo instead of clone.",
)
@click.option(
	"--init-bench", is_flag=True, default=False, help="Initialize Bench if not in one"
)
@click.option(
	"--resolve-deps",
	is_flag=True,
	default=False,
	help="Resolve dependencies before installing app",
)
@click.option(
	"--cache-key",
	type=str,
	default=None,
	help="Caches get-app artifacts if provided (only first 10 chars is used)",
)
@click.option(
	"--compress-artifacts",
	is_flag=True,
	default=False,
	help="Whether to gzip get-app artifacts that are to be cached",
)
def get_app(
	git_url,
	branch,
	name=None,
	overwrite=False,
	skip_assets=False,
	soft_link=False,
	init_bench=False,
	resolve_deps=False,
	cache_key=None,
	compress_artifacts=False,
):
	"clone an app from the internet and set it up in your bench"
	from offline_update.app import get_app

	get_app(
		git_url,
		branch=branch,
		skip_assets=skip_assets,
		overwrite=overwrite,
		soft_link=soft_link,
		init_bench=init_bench,
		resolve_deps=resolve_deps,
		cache_key=cache_key,
		compress_artifacts=compress_artifacts,
	)