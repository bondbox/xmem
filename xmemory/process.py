# coding:utf-8

from typing import Optional
from typing import Tuple

from psutil import Process


class MemoryInfo():
    TITLE: str = "RSS (Resident Set Size)         VMS (Virtual Memory Size)"

    def __init__(self, rss: int, vms: int) -> None:
        self.__rss: int = rss
        self.__vms: int = vms

    def __str__(self) -> str:
        rss: str = f"{self.rss / 1048576:.02f} MB / {self.rss}"
        vms: str = f"{self.vms / 1048576:.02f} MB / {self.vms}"
        return f"{rss:<30}  {vms}"

    @property
    def rss(self) -> int:
        """Resident Set Size"""
        return self.__rss

    @property
    def vms(self) -> int:
        """Virtual Memory Size"""
        return self.__vms


class ProcessInfo():
    def __init__(self, pid: Optional[int] = None) -> None:
        self.__prev_memory_info: Optional[MemoryInfo] = None
        self.__curr_memory_info: Optional[MemoryInfo] = None
        self.__process: Process = Process(pid)

    @property
    def memory_info(self) -> MemoryInfo:
        memory_info = self.__process.memory_info()
        return MemoryInfo(memory_info.rss, memory_info.vms)

    @property
    def delta_memory_info(self) -> Tuple[MemoryInfo, MemoryInfo, MemoryInfo]:
        self.__prev_memory_info = self.__curr_memory_info or self.memory_info
        self.__curr_memory_info = self.memory_info
        return MemoryInfo(
            self.__curr_memory_info.rss - self.__prev_memory_info.rss,
            self.__curr_memory_info.vms - self.__prev_memory_info.vms
        ), self.__curr_memory_info, self.__prev_memory_info
