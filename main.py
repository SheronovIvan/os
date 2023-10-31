import os
import ctypes
from ctypes import wintypes


def get_drive_info():
    drive_info = []

    drives = ctypes.windll.kernel32.GetLogicalDrives()

    for drive_letter in range(1, 26):
        if drives & (1 << drive_letter):
            drive = chr(65 + drive_letter) + ":\\"
            free_bytes = wintypes.ULARGE_INTEGER()
            total_bytes = wintypes.ULARGE_INTEGER()
            available_bytes = wintypes.ULARGE_INTEGER()

            if ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                    drive,
                    ctypes.byref(free_bytes),
                    ctypes.byref(total_bytes),
                    ctypes.byref(available_bytes)):
                writable = os.access(drive, os.W_OK)
                drive_info.append({
                    "Диск": drive,
                    "Доступен для записи": writable,
                    "Общий объем": total_bytes.value,
                    "Свободное пространство": free_bytes.value
                })

    return drive_info


# Получить информацию о дисках
disk_info = get_drive_info()

# Вывести информацию о дисках
for info in disk_info:
    print("Диск:", info["Диск"])
    print("Общий объем:", info["Общий объем"] / (1024 ** 3), "GB")
    print("Свободное пространство:", info["Свободное пространство"] / (1024 ** 3), "GB")
    print("Доступен для записи:", "Да" if info["Доступен для записи"] else "Нет")
    print()
