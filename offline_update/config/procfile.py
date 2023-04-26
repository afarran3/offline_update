# imports - standard imports
import os

# imports - third party imports
import click

# imports - module imports
import offline_update
from offline_update.app import use_rq
from offline_update.utils import which
from offline_update.bench import Bench


def setup_procfile(bench_path, yes=False, skip_redis=False):
	config = Bench(bench_path).conf
	procfile_path = os.path.join(bench_path, "Procfile")
	if not yes and os.path.exists(procfile_path):
		click.confirm(
			"A Procfile already exists and this will overwrite it. Do you want to continue?",
			abort=True,
		)

	procfile = (
		offline_update.config.env()
		.get_template("Procfile")
		.render(
			node=which("node") or which("nodejs"),
			use_rq=use_rq(bench_path),
			webserver_port=config.get("webserver_port"),
			CI=os.environ.get("CI"),
			skip_redis=skip_redis,
			workers=config.get("workers", {}),
		)
	)

	with open(procfile_path, "w") as f:
		f.write(procfile)
