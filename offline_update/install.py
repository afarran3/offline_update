from offline_update.bench import Bench
import subprocess, platform
import os
from frappe.utils import get_bench_path  # noqa

from offline_update import dirs

def after_install():
    download_reqs(Bench(get_bench_path()).apps, dirs)


def download_reqs(bench_apps, dirs):
    cllect_libs_names(dirs)
    if have_internet('8.8.8.8') or have_internet('google.com'):
        print(f"Downloading 'pip' Packages.....")
        subprocess.call(
                f"pip download -d {dirs['pip_dir']} --use-deprecated=legacy-resolver -r {os.path.join(dirs['pip_dir'], 'pip_requirements.txt')}",
                shell=True
        )

        for app in bench_apps:
            path = os.path.join(get_bench_path(), 'apps', app)
            if os.path.isfile(os.path.join(path, 'yarn.lock')):
                os.remove(os.path.join(path, 'yarn.lock'))
                print(f"Downloading {app} 'Node' Packages.....")
                subprocess.call(
                        "yarn install",
                        shell=True,
                        cwd=path
                )
    else:
        print("You don't have internet connection to download requirements libraries.")


def cllect_libs_names(dirs):
    check_dirs(dirs)
    bench = Bench(get_bench_path())
    bench_apps = bench.apps
    dev_dependencies = {}
    proj_dependencies = []
    requires = []
    
    with open(os.path.join(dirs['pip_dir'], 'pip_requirements.txt'), 'w+') as pip_req:
        for app in bench_apps:
            path = os.path.join(get_bench_path(), 'apps', app)
            if os.path.isfile(os.path.join(path, 'requirements.txt')):
                with open(os.path.join(path, 'requirements.txt'), 'r') as req:
                    deps = req.readlines()
                    for dep in deps:
                        dep = dep.strip()
                        if dep not in [
                            'frappe',
                            'erpnext',
                            "# frappe -- https://github.com/frappe/frappe is installed via 'bench init'"
                        ]:
                            pip_req.writelines([dep, '\n'])
            elif os.path.isfile(os.path.join(path, 'pyproject.toml')):
                try:
                    from tomli import load
                except ImportError:
                    from tomllib import load
                with open(os.path.join(path, 'pyproject.toml'), 'rb') as req:
                    toml_dict = load(req)
                    if toml_dict.get("project", {}).get("dependencies"):
                        for dep in list(toml_dict.get("project", {}).get("dependencies")):
                            proj_dependencies.append(dep.split(",")[0])
                    if toml_dict.get("build-system", {}).get("requires"):
                        for dep in list(toml_dict.get("build-system", {}).get("requires")):
                            requires.append(dep.split(",")[0])
                    if toml_dict.get("tool", {}).get("bench",{}).get("dev-dependencies", {}):
                        for k, v in toml_dict.get("tool", {}).get("bench",{}).get("dev-dependencies", {}).items():
                            dev_dependencies[k] = v
        if proj_dependencies:
            for v in proj_dependencies:
                pip_req.writelines([v, '\n'])
        if requires:
            for v in requires:
                pip_req.writelines([v, '\n'])
        if dev_dependencies:
            for k,v in dev_dependencies.items():
                pip_req.writelines([k + v, '\n'])

    subprocess.call(
            f"yarn --offline config set yarn-offline-mirror {dirs['yarn_dir']}",
            shell=True
    )


def have_internet(host):
	ping_str = "-n 1" if  platform.system().lower()=="windows" else "-c 1"
	args = "ping " + " " + ping_str + " " + "-w 2" + " " + host
	need_sh = False if  platform.system().lower()=="windows" else True
	with open(os.devnull, 'w') as DEVNULL:
		try:
			subprocess.check_call(
				args,
				shell=need_sh,
				stdout=DEVNULL,
				stderr=DEVNULL,
			)
			return True
		except subprocess.CalledProcessError:
			return False


def check_dirs(dirs):
	for k, v in dirs.items():
		if not os.path.isdir(v):
			os.mkdir(v)