from struct import unpack, pack
from win32con import PROCESS_VM_READ, PROCESS_QUERY_INFORMATION
from win32api import OpenProcess, CloseHandle
from win32process import EnumProcesses, GetModuleFileNameEx, EnumProcessModules
from ctypes import byref, sizeof, c_uint, windll
from ReadWriteMemory import ReadWriteMemory
from pymem import *
from pymem.process import *

def Get_Process(process_name):
    global processt
    global mem
    mem = Pymem(process_name)
    rwm = ReadWriteMemory()
    processt = rwm.get_process_by_name(process_name)
    processt.open()
    p_id, base_address = get_process_by_name(process_name)
    return p_id, base_address


def Find_Pointer(base_address, address, offsets):
    pointer = processt.get_pointer(base_address + address, offsets)
    return pointer

def Read_Int(address) -> int:
    val = processt.read(address)
    return val

def Read_Float(address) -> float:
    val = To_Float(processt.read(address))
    return val

def Read_String(address) -> str:
    val = mem.read_string(address)
    return val

def Read_Bool(address) -> bool:
    val = mem.read_bool(address)
    return val



def read_process_memory(p_id, address, offsets=[]):
    h_process = windll.kernel32.OpenProcess(PROCESS_VM_READ, False, p_id)
    data = c_uint(0)
    bytesRead = c_uint(0)
    current_address = address

    if offsets:
        offsets.append(None)
        for offset in offsets:
            windll.kernel32.ReadProcessMemory(h_process, current_address, byref(data), sizeof(data), byref(bytesRead))
            if not offset:
                return data.value
            else:
                current_address = data.value + offset
    else:
        windll.kernel32.ReadProcessMemory(h_process, current_address, byref(data), sizeof(data), byref(bytesRead))

    windll.kernel32.CloseHandle(h_process)
    return data.value

# 0 - int, 1 - float
def Write_Mem(address, New_Value, float_or_int) -> None:
    if float_or_int == 1:
        processt.write(address, To_Int(New_Value))
    else:
        processt.write(address, New_Value)

def To_Float(x) -> float:
    y = unpack("@f", pack("@I", x))[0]
    return y

def To_Int(x) -> int:
    y = unpack("@I", pack("@f", x))[0]
    return y

def get_process_by_name(process_name):
    process_name = process_name.lower()
    processes = EnumProcesses()
    for process_id in processes:
        if process_id == -1:
            continue
        try:
            h_process = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, True, process_id)
            try:
                modules = EnumProcessModules(h_process)
                for base_address in modules:
                    name = str(GetModuleFileNameEx(h_process, base_address))
                    if name.lower().find(process_name) != -1:
                        return process_id, base_address
            finally:
                CloseHandle(h_process)
        except:
            pass