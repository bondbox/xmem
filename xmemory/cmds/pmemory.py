# coding:utf-8

import os
from typing import Optional
from typing import Sequence

from psutil import Process
from xkits_command import ArgParser
from xkits_command import Command
from xkits_command import CommandArgument
from xkits_command import CommandExecutor

from xmemory.attribute import __urlhome__
from xmemory.attribute import __version__


@CommandArgument("pmemory", description="View memory usage of a process")
def add_cmd(_arg: ArgParser):  # pylint: disable=unused-argument
    pass


@CommandExecutor(add_cmd)
def run_cmd(cmds: Command) -> int:  # pylint: disable=unused-argument
    pid: int = os.getpid()
    process: Process = Process(pid)
    memory_info = process.memory_info()
    cmds.stdout(f"PID {pid} memory usage:")
    cmds.stdout("RSS (Resident Set Size)         VMS (Virtual Memory Size)")
    rss: str = f"{memory_info.rss / 1048576:.02f} MB / {memory_info.rss}"
    vms: str = f"{memory_info.vms / 1048576:.02f} MB / {memory_info.vms}"
    cmds.stdout(f"{rss:<30}  {vms}")
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    cmds = Command()
    cmds.version = __version__
    return cmds.run(root=add_cmd, argv=argv, epilog=f"For more, please visit {__urlhome__}.")  # noqa:E501
