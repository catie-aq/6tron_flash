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
@click.option(
    "-p",
    "--probe",
    default="j-link",
    type=click.Choice(["j-link", "st-link"]),
    show_default=True,
)
def main(jlink_device, file_path, probe):
    """Console tool to flash 6TRON boards."""
    click.echo("6TRON Flash Tool")

    script_dirname = os.path.dirname(os.path.abspath(__file__))

    config = {}

    if file_path is not None:
        file_path = os.path.abspath(file_path).replace("\\", "/")
    elif pathlib.Path(".mbed").exists():
        with open(".mbed", "r") as f:
            for key, value in [line.split("=") for line in f]:
                config[key] = value.strip().upper()

        if pathlib.Path("mbed_app.json"):
            with open("mbed_app.json", "r") as f:
                mbed_app = json.load(f)
                if "artifact_name" in mbed_app:
                    config["FILE"] = mbed_app["artifact_name"]

        if not "FILE" in config:
            config["FILE"] = pathlib.Path(pathlib.Path().absolute()).parts[-1]

        file_path = "BUILD/{}/{}/{}.bin".format(
            config["TARGET"], config["TOOLCHAIN"], config["FILE"]
        )

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

    if probe == "j-link":

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
        command_file = open(
            os.path.join(script_dirname, "jlink_command_file.jlink").replace("\\", "/"),
            "w",
        )
        command_file.write(command_file_content)
        command_file.close()

        command_path = os.path.join(script_dirname, "jlink_command_file.jlink").replace(
            "\\", "/"
        )

        # Flash target
        if os.name == "nt":
            executable = "JLink.exe"
        else:
            executable = "JLinkExe"
        # fmt: off
        cmd = "{} -Device {} -if SWD -Speed 4000 -ExitOnError 1 -NoGui 1 -CommandFile \"{}\" ".format(
            executable, jlink_device, command_path
        )
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

    if probe == "st-link":

        if "STM32L4" in jlink_device:
            openocd_cli_args = ' -f interface/stlink-v2-1.cfg -c "transport select hla_swd"\
                    -f target/stm32l4x.cfg -c "reset_config srst_only srst_nogate"'

            # Flash target
            cmd = (
                "openocd"
                + openocd_cli_args
                + ' -c "program {} verify reset exit"'.format(file_path)
            )
            ret = os.system(cmd)
            if ret != 0:
                if os.name == "nt":
                    click.echo(
                        "Error when calling OpenOCD executable. Please verify that openocd.exe has been added to the PATH"
                    )
                elif os.name == "posix":
                    click.echo(
                        "Error when calling OpenOCD executable. Please verify that openocd has been added to the PATH"
                    )

        else:  # use the config file of the project
            click.echo(
                "Unknown device, using openocd.cfg configuration file of the project"
            )

            # Flash target
            cmd = 'openocd -f openocd.cfg -c "program {} verify reset exit"'.format(
                file_path
            )
            ret = os.system(cmd)
            if ret != 0:
                if os.name == "nt":
                    click.echo(
                        "Error when calling OpenOCD executable. Please verify that openocd.exe has been added to the PATH"
                    )
                elif os.name == "posix":
                    click.echo(
                        "Error when calling OpenOCD executable. Please verify that openocd has been added to the PATH"
                    )
            click.echo()

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
