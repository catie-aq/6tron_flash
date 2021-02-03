# -*- coding: utf-8 -*-

"""Console script for sixtron_flash."""
import sys
import click
import os


@click.command()
@click.argument('device', nargs=1)
@click.argument('elf_file', type=click.Path(exists=True))
@click.option('-p', '--probe', default="j-link", type=click.Choice(['j-link', 'st-link']))
def main(device, elf_file, probe):
    """Console script for sixtron_flash."""
    click.echo("6TRON Flash Tool")
    
    script_dirname = os.path.dirname(os.path.abspath(__file__))

    if probe == "j-link":

        if device.lower().startswith("stm32"):
            addr = "0x08000000"
        else:
            addr = "0x0"

        print(elf_file)

        elf_path = os.path.abspath(elf_file).replace("\\","/").replace(".elf",".bin")

        # Create the JLink command file
        command_file_content = ("si 1\n"
                                "speed 4000\n"
                                "r\n"
                                "h\n"
                                "loadfile {},{}\n"
                                "r\n"
                                "q\n").format(elf_path, addr)
        command_file = open(os.path.join(script_dirname, "jlink_command_file.jlink").replace("\\", "/"), 'w')
        command_file.write(command_file_content)
        command_file.close()

        command_path = os.path.join(script_dirname, "jlink_command_file.jlink").replace("\\", "/")

        # Flash target
        if os.name == 'nt':
            executable = 'JLink.exe'
        else:
            executable = 'JLinkExe'
        cmd = executable + ' -Device {} -if JTAG -CommanderScript {} '.format(device, command_path)
        ret = os.system(cmd)
        if ret != 0:
            if os.name == 'nt':
                print("Error when calling J-Link executable. Please verify that JLink.exe has been added to the PATH")
            elif os.name == 'posix':
                print("Error when calling J-Link executable. Please verify that JLinkEXE has been added to the PATH")

        os.remove(command_path)

    if probe == "st-link":
        elf_path = os.path.abspath(elf_file).replace("\\","/")

        if "STM32L4" in device:
            openocd_cli_args = " -f interface/stlink-v2-1.cfg -c \"transport select hla_swd\"\
                    -f target/stm32l4x.cfg -c \"reset_config srst_only srst_nogate\""

            # Flash target
            cmd = "openocd" + openocd_cli_args + ' -c "program {} verify reset exit"'.format(elf_path)
            ret = os.system(cmd)
            if ret != 0:
                if os.name == 'nt':
                    print("Error when calling OpenOCD executable. Please verify that openocd.exe has been added to the PATH")
                elif os.name == 'posix':
                    print("Error when calling OpenOCD executable. Please verify that openocd has been added to the PATH")

        else:  # use the config file of the project
            print("Unknown device, using openocd.cfg configuration file of the project")

            # Flash target
            cmd = 'openocd -f openocd.cfg -c "program {} verify reset exit"'.format(elf_path)
            ret = os.system(cmd)
            if ret != 0:
                if os.name == 'nt':
                    print("Error when calling OpenOCD executable. Please verify that openocd.exe has been added to the PATH")
                elif os.name == 'posix':
                    print("Error when calling OpenOCD executable. Please verify that openocd has been added to the PATH")
            print()
        
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
