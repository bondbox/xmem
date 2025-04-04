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
from xmemory.process import DeltaMemoryInfo
from xmemory.process import ProcessInfo


@CommandArgument("pmemory", description="View memory usage of a process")
def add_cmd(_arg: ArgParser):  # pylint: disable=unused-argument
    _arg.add_argument("-i", type=int, dest="interval", help="Interval seconds",
                      default=1, metavar="SECONDS")
    _arg.add_argument(dest="pid", type=int, help="PID of the process",
                      nargs="?", metavar="PID")


@CommandExecutor(add_cmd)
def run_cmd(cmds: Command) -> int:  # pylint: disable=unused-argument
    delta_memory_info: DeltaMemoryInfo
    pid: int = cmds.args.pid or getpid()
    process: ProcessInfo = ProcessInfo(pid)
    interval: int = max(cmds.args.interval, 1)
    delta_memory_info = process.delta_memory_info
    cmds.stdout(f"PID {pid} memory usage:")
    cmds.stdout(DeltaMemoryInfo.TITLE)
    while True:
        delta_memory_info = process.delta_memory_info
        cmds.stdout(delta_memory_info)
        sleep(interval)
    return ENOTRECOVERABLE


def main(argv: Optional[Sequence[str]] = None) -> int:
    cmds = Command()
    cmds.version = __version__
    return cmds.run(root=add_cmd, argv=argv, epilog=f"For more, please visit {__urlhome__}.")  # noqa:E501
