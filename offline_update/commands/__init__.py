# import click

# import frappe
# import logging
from frappe.commands import pass_context, get_site

# # from frappe_telegram.bot import start_polling, start_webhook
# # from frappe_telegram.utils.supervisor import add_supervisor_entry, remove_supervisor_entry


# @click.group("update")
# @click.option("-ol", is_flag=True, help="Start bot in Polling Mode")
# def update():
#     print("YYYYYYYYYYEEEEEEEEEEESSSSSSSSSS")

# file_path: frappe-bench/apps/flags/flags/commands.py
import click
import os
from frappe.utils import get_bench_path  # noqa

from offline_update.utils.cli import (
	MultiCommandGroup,
	print_bench_version,
	use_experimental_feature,
	setup_verbosity,
)


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


# import bench
# from offline_update.commands.update import update

# @click.command('set-flags')
# @click.argument('state', type=click.Choice(['on', 'off']))
@click.command("updatee")
# @click.get_command(ctx, "update")
# @click.option("--ol", is_flag=True, help="Start bot in Polling Mode")
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
def updatee(
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
    # from flags.utils import set_flags
    # set_flags(state=state)
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
    updatee
]
# @click.command("start-bot")
# @click.argument("telegram_bot")
# @click.option("--polling", is_flag=True, help="Start bot in Polling Mode")
# @click.option("--poll-interval", type=float, default=0,
#               help="Time interval between each poll. Default is 0")
# @click.option("--webhook", is_flag=True, help="Start Webhook Server")
# @click.option("--webhook-port", type=int, default=8080,
#               help="The port to listen on for webhook events. Default is 8080")
# @click.option("--webhook-url", type=str,
#               help="Explicitly specify webhook URL. Useful for NAT, reverse-proxy etc")
# @pass_context
# def start_bot(
#         context, telegram_bot,
#         polling=False, poll_interval=0,
#         webhook=False, webhook_port=8080, webhook_url=None):
#     """
#     Start Telegram Bot

#     \b
#     Args:
#         telegram_bot: The name of 'Telegram Bot' to start
#     """
#     site = get_site(context)

#     if not polling and not webhook:
#         print("Starting {} in polling mode".format(telegram_bot))
#         polling = True

#     if webhook and not webhook_port:
#         webhook_port = 8080

#     # Enable logging
#     logging.basicConfig(
#         format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
#     )

#     if polling:
#         start_polling(site=site, telegram_bot=telegram_bot, poll_interval=poll_interval)
#     elif webhook:
#         start_webhook(
#             site=site, telegram_bot=telegram_bot,
#             webhook_port=webhook_port, webhook_url=webhook_url)


# @click.command("list-bots")
# @pass_context
# def list_bots(context):
#     site = get_site(context=context)
#     frappe.init(site=site)
#     frappe.connect()

#     bots = frappe.get_all("Telegram Bot", fields=["name"])
#     print("No. of Telegram Bots:", len(bots))
#     for bot in bots:
#         print("-", bot.name)

#     frappe.destroy()


# @click.command("supervisor-add")
# @click.argument("telegram_bot")
# @click.option("--polling", is_flag=True, help="Start bot in Polling Mode")
# @click.option("--poll-interval", type=float, default=0,
#               help="Time interval between each poll. Default is 0")
# @click.option("--webhook", is_flag=True, help="Start Webhook Server")
# @click.option("--webhook-port", type=int, default=0,
#               help="The port to listen on for webhook events. Default is 8080")
# @click.option("--webhook-url", type=str,
#               help="Explicitly specify webhook URL. Useful for NAT, reverse-proxy etc")
# @pass_context
# def supervisor_add(
#         context, telegram_bot,
#         polling=False, poll_interval=0,
#         webhook=False, webhook_port=8080, webhook_url=None):
#     """
#     Sets up supervisor process
#     """
#     site = get_site(context)
#     frappe.init(site=site)
#     frappe.connect()

#     if webhook and not webhook_port:
#         webhook_port = 8080

#     add_supervisor_entry(
#         telegram_bot=telegram_bot, polling=polling, poll_interval=poll_interval,
#         webhook=webhook, webhook_port=webhook_port, webhook_url=webhook_url)

#     frappe.destroy()


# @click.command("supervisor-remove")
# @click.argument("telegram_bot")
# @pass_context
# def supervisor_remove(context, telegram_bot):
#     """
#     Removes supervisor entry of specific bot

#     \b
#     Args:
#         telegram_bot: The name of 'Telegram Bot' to remove
#     """
#     site = get_site(context)
#     frappe.init(site=site)
#     frappe.connect()

#     remove_supervisor_entry(telegram_bot=telegram_bot)

#     frappe.destroy()


# @click.command("nginx-add")
# @click.argument("telegram_bot")
# @click.option("--webhook-port", type=int, default=0,
#               help="The port to listen on for webhook events. Default is 8080")
# @click.option("--webhook-url", type=str,
#               help="Explicitly specify webhook URL. Useful for NAT, reverse-proxy etc")
# @click.option("--nginx-path", type=str,
#               help="Use custom nginx path for webhook reverse-proxy")
# @pass_context
# def nginx_add(context, telegram_bot, webhook_port=None, webhook_url=None, nginx_path=None):
#     """
#     Modifies existing nginx-config for telegram-webhook support.
#     You can specify webhook url, port & nginx_path to override existing value in TelegramBot Doc

#     \b
#     Args:
#         webhook_port: Specify the port to override
#         webhook_url: Specify the url to override existing webhook_url
#         nginx_path: Use custom path in nginx location block
#     """
#     from frappe_telegram.utils.nginx import add_nginx_config

#     site = get_site(context)
#     frappe.init(site=site)
#     frappe.connect()

#     add_nginx_config(
#         telegram_bot=telegram_bot,
#         webhook_url=webhook_url,
#         webhook_port=webhook_port,
#         webhook_nginx_path=nginx_path)
#     frappe.destroy()


# @click.command("nginx-remove")
# @click.argument("telegram_bot")
# @pass_context
# def nginx_remove(context, telegram_bot):
#     """
#     Removes nginx-config modifications made for telegram_bot
#     """
#     from frappe_telegram.utils.nginx import remove_nginx_config

#     site = get_site(context)
#     frappe.init(site=site)
#     frappe.connect()

#     remove_nginx_config(telegram_bot=telegram_bot)
#     frappe.destroy()


# telegram.add_command(start_bot)
# telegram.add_command(list_bots)
# telegram.add_command(supervisor_add)
# telegram.add_command(supervisor_remove)
# telegram.add_command(nginx_add)
# telegram.add_command(nginx_remove)
# commands = [set_flags]
