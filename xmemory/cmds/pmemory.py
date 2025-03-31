# coding:utf-8

from errno import ENOTRECOVERABLE
from os import getpid
from time import sleep
from typing import Optional
from typing import Sequence

from xkits_command import ArgParser
from xkits_command import Command
from xkits_command import CommandArgument
from xkits_command import CommandExecutor

from xmemory.attribute import __urlhome__
from xmemory.attribute import __version__
from xmemory.process import MemoryInfo
from xmemory.process import ProcessInfo


@CommandArgument("pmemory", description="View memory usage of a process")
def add_cmd(_arg: ArgParser):  # pylint: disable=unused-argument
    pass


@CommandExecutor(add_cmd)
def run_cmd(cmds: Command) -> int:  # pylint: disable=unused-argument
    pid: int = getpid()
    memory_info: MemoryInfo
    delta_memory_info: MemoryInfo
    process: ProcessInfo = ProcessInfo(pid)
    _, memory_info, _ = process.delta_memory_info
    cmds.stdout(f"PID {pid} memory usage:")
    cmds.stdout(MemoryInfo.TITLE)
    while True:
        delta_memory_info, memory_info, _ = process.delta_memory_info
        cmds.stdout(memory_info)
        sleep(1)
    return ENOTRECOVERABLE


def main(argv: Optional[Sequence[str]] = None) -> int:
    cmds = Command()
    cmds.version = __version__
    return cmds.run(root=add_cmd, argv=argv, epilog=f"For more, please visit {__urlhome__}.")  # noqa:E501
