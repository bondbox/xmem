# coding:utf-8

from xmemory.process import MemoryInfo
from xmemory.process import ProcessInfo


def main():
    process: ProcessInfo = ProcessInfo()
    print("Memory usage:")
    print(MemoryInfo.TITLE)
    print(process.memory_info)
    print("Goodbye!")


if __name__ == "__main__":
    main()
