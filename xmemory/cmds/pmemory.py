# coding:utf-8

import os
from typing import Optional
from typing import Sequence

from psutil import Process
from xkits_command import ArgParser
from xkits_command import Command
from xkits_command import CommandArgument
from xkits_command import CommandExecutor

from xmemory.attribute import __description__
from xmemory.attribute import __project__
from xmemory.attribute import __urlhome__
from xmemory.attribute import __version__


@CommandArgument(__project__, description=__description__)
def add_cmd(_arg: ArgParser):  # pylint: disable=unused-argument
    pass


@CommandExecutor(add_cmd)
def run_cmd(cmds: Command) -> int:  # pylint: disable=unused-argument
    pid: int = os.getpid()
    cmds.stdout(f"Hello, PID {pid}")
    process: Process = Process(pid)
    memory_info = process.memory_info()
    cmds.stdout(f"VMS (Virtual Memory Size)\t{memory_info.vms / 1024 / 1024:.2f} MB\t{memory_info.vms}")  # noqa:E501
    cmds.stdout(f"RSS (Resident Set Size)  \t{memory_info.rss / 1024 / 1024:.2f} MB\t{memory_info.rss}")  # noqa:E501
    cmds.stdout("Goodbye!")
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    cmds = Command()
    cmds.version = __version__
    return cmds.run(root=add_cmd, argv=argv, epilog=f"For more, please visit {__urlhome__}.")  # noqa:E501
