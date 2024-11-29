# -*- coding: utf-8 -*-

"""Console script for sixtron_flash."""
import sys
import click
import pathlib
import os
import json


@click.command()
@click.argument("JLINK_DEVICE", nargs=1, required=False)
@click.argument("FILE_PATH", type=click.Path(exists=True), required=False)
@click.option('-ip', '--jlink-server-ip', help='J-Link remote server IP (will discard jlink-probe option)')
@click.option('-j', '--jlink-probe', help='J-Link probe nickname or serial number')
@click.version_option()
def main(jlink_server_ip, jlink_probe, jlink_device, file_path):
    """Console tool to flash 6TRON boards."""
    click.echo("6TRON Flash Tool")

    config = {}

    if file_path is not None:
        file_path = os.path.abspath(file_path).replace("\\", "/")
    elif pathlib.Path(".mbed").exists():
        click.echo("  No argument provided: finding binary automatically...")

        with open(".mbed", "r") as f:
            for key, value in [line.split("=") for line in f]:
                config[key] = value.strip().upper()

        if pathlib.Path("mbed_app.json").exists():
            with open("mbed_app.json", "r") as f:
                mbed_app = json.load(f)
                if "artifact_name" in mbed_app:
                    config["FILE"] = mbed_app["artifact_name"]

        if not "FILE" in config:
            config["FILE"] = pathlib.Path(pathlib.Path().absolute()).parts[-1]

        file_path = "BUILD/{}/{}/{}.bin".format(
            config["TARGET"], config["TOOLCHAIN"], config["FILE"]
        )

        if not pathlib.Path(file_path).exists():
            click.echo("  Binary file not found. Please provide a target and a path")
            return
        else:
            click.echo(f"  Found binary at {file_path}")

        if pathlib.Path("custom_targets.json").exists():
            with open("custom_targets.json", "r") as f:
                custom_target = json.load(f)
            if config["TARGET"] in custom_target:
                jlink_device = custom_target[config["TARGET"]]["device_name"]
            else:
                with open("mbed-os/targets/targets.json", "r") as f:
                    mbed_target = json.load(f)
                if config["TARGET"] in mbed_target:
                    jlink_device = mbed_target[config["TARGET"]]["device_name"]
                else:
                    click.echo("Target not found")
                    return
    else:
        click.echo("Mbed OS project not found")
        return

    click.echo("Flash: {}".format(file_path))

    if jlink_device.lower().startswith("stm32"):
        addr = "0x08000000"
    else:
        addr = "0x0"

    # Create the JLink command file
    # fmt: off
    command_file_content = (
        "r\n"
        "h\n"
        "loadfile \"{}\",{}\n"
        "r\n"
        "q\n"
    ).format(file_path, addr)
    # fmt: on

    command_dirname = os.path.dirname(os.path.abspath(file_path))
    command_path = os.path.join(command_dirname, "jlink_command_file.jlink").replace("\\", "/")
    command_file = open(command_path, "w")
    command_file.write(command_file_content)
    command_file.close()

    if jlink_server_ip:
        probe = f"-IP {jlink_server_ip}"
    elif jlink_probe:
        probe = f"-USB {jlink_probe}"
    else:
        probe = ""

    # Flash target
    if os.name == "nt":
        executable = "JLink.exe"
    else:
        executable = "JLinkExe"
    # fmt: off
    cmd = f"{executable} {probe} -if SWD -Speed 4000 -ExitOnError 1 -NoGui 1 -CommandFile \"{command_path}\" -Device {jlink_device}"
    # fmt: on
    ret = os.system(cmd)
    if ret != 0:
        if os.name == "nt":
            click.echo(
                "Error when running J-Link executable. Please verify that a J-Link probe is connected, and that JLink.exe has been added to the PATH"
            )
        elif os.name == "posix":
            click.echo(
                "Error when running J-Link executable. Please verify that a J-Link probe is connected, and that JLinkExe has been added to the PATH"
            )

    os.remove(command_path)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
