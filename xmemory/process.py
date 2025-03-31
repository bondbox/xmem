# coding:utf-8

from typing import Optional
from typing import Union

from psutil import Process
from xkits_lib.unit import DataUnit
from xkits_logger.colorful import Color


class MemoryInfo():
    TITLE: str = "RSS (Resident Set Size)         VMS (Virtual Memory Size)"

    def __init__(self, rss: Union[DataUnit, int], vms: Union[DataUnit, int]) -> None:  # noqa:E501
        self.__rss: DataUnit = rss if isinstance(rss, DataUnit) else DataUnit(rss)  # noqa:E501
        self.__vms: DataUnit = vms if isinstance(vms, DataUnit) else DataUnit(vms)  # noqa:E501

    def __str__(self) -> str:
        rss: str = f"{self.rss.bytes} / {self.__rss.human}".ljust(30)
        vms: str = f"{self.vms.bytes} / {self.__vms.human}"
        return f"{rss}  {vms}"

    @property
    def rss(self) -> DataUnit:
        """Resident Set Size"""
        return self.__rss

    @property
    def vms(self) -> DataUnit:
        """Virtual Memory Size"""
        return self.__vms


class DeltaMemoryInfo(MemoryInfo):
    TITLE: str = "RSS (Resident Set Size)           VMS (Virtual Memory Size)"

    def __init__(self, prev: MemoryInfo, curr: MemoryInfo) -> None:
        super().__init__(curr.rss.bytes - prev.rss.bytes,
                         curr.vms.bytes - prev.vms.bytes)
        self.__prev: MemoryInfo = prev
        self.__curr: MemoryInfo = curr

    def __str__(self) -> str:
        def color(s: str, v: DataUnit) -> str:
            return f"{s} {Color.red('+'+v.human)}" if v.bytes > 0 else f"{s} {Color.green(v.human)}" if v.bytes < 0 else s  # noqa:E501

        rss: str = f"{self.current.rss.bytes} / {self.current.rss.human}"
        vms: str = f"{self.current.vms.bytes} / {self.current.vms.human}"
        return f"{color(rss, self.rss).ljust(42 if self.rss.bytes != 0 else 32)}  {color(vms, self.vms)}"  # noqa:E501

    @property
    def previous(self) -> MemoryInfo:
        return self.__prev

    @property
    def current(self) -> MemoryInfo:
        return self.__curr


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
    def delta_memory_info(self) -> DeltaMemoryInfo:
        self.__prev_memory_info = self.__curr_memory_info or self.memory_info
        self.__curr_memory_info = self.memory_info
        return DeltaMemoryInfo(self.__prev_memory_info, self.__curr_memory_info)  # noqa:E501
