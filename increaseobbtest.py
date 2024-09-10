def read_fat32_boot_sector(file_path):
    with open(file_path, 'rb') as f:
        boot_sector = bytearray(f.read(512))  # Ler o setor de inicialização (512 bytes)

    info = {
        "Jump Instruction": boot_sector[0:3],
        "OEM Name": boot_sector[3:11].decode('ascii').strip(),
        "Bytes per Sector": int.from_bytes(boot_sector[11:13], 'little'),
        "Sectors per Cluster": boot_sector[13],
        "Reserved Sectors": int.from_bytes(boot_sector[14:16], 'little'),
        "Number of FATs": boot_sector[16],
        "Root Entries": int.from_bytes(boot_sector[17:19], 'little'),
        "Total Sectors (16-bit)": int.from_bytes(boot_sector[19:21], 'little'),
        "Media Descriptor": boot_sector[21],
        "Sectors per FAT (16-bit)": int.from_bytes(boot_sector[22:24], 'little'),
        "Sectors per Track": int.from_bytes(boot_sector[24:26], 'little'),
        "Number of Heads": int.from_bytes(boot_sector[26:28], 'little'),
        "Hidden Sectors": int.from_bytes(boot_sector[28:32], 'little'),
        "Total Sectors (32-bit)": int.from_bytes(boot_sector[32:36], 'little'),
        "Sectors per FAT (32-bit)": int.from_bytes(boot_sector[36:40], 'little'),
        "Flags": int.from_bytes(boot_sector[40:42], 'little'),
        "Version": int.from_bytes(boot_sector[42:44], 'little'),
        "Root Cluster": int.from_bytes(boot_sector[44:48], 'little'),
        "FSInfo Sector": int.from_bytes(boot_sector[48:50], 'little'),
        "Backup Boot Sector": int.from_bytes(boot_sector[50:52], 'little'),
        "Reserved": boot_sector[52:64].decode('ascii').strip(),
        "Drive Number": boot_sector[64],
        "Reserved1": boot_sector[65],
        "Boot Signature": boot_sector[66],
        "Volume ID": int.from_bytes(boot_sector[67:71], 'little'),
        "Volume Label": boot_sector[71:81].decode('ascii').strip(),
        "File System Type": boot_sector[82:90].decode('ascii').strip(),
    }

    return boot_sector, info

def update_fat32_boot_sector(file_path, updates):
    # Read the current boot sector
    boot_sector, info = read_fat32_boot_sector(file_path)

    # Apply updates
    for key, value in updates.items():
        if key == "Bytes per Sector":
            boot_sector[11:13] = value.to_bytes(2, 'little')
        elif key == "Sectors per Cluster":
            boot_sector[13] = value
        elif key == "Reserved Sectors":
            boot_sector[14:16] = value.to_bytes(2, 'little')
        elif key == "Number of FATs":
            boot_sector[16] = value
        elif key == "Root Entries":
            boot_sector[17:19] = value.to_bytes(2, 'little')
        elif key == "Total Sectors (16-bit)":
            boot_sector[19:21] = value.to_bytes(2, 'little')
        elif key == "Media Descriptor":
            boot_sector[21] = value
        elif key == "Sectors per FAT (16-bit)":
            boot_sector[22:24] = value.to_bytes(2, 'little')
        elif key == "Sectors per Track":
            boot_sector[24:26] = value.to_bytes(2, 'little')
        elif key == "Number of Heads":
            boot_sector[26:28] = value.to_bytes(2, 'little')
        elif key == "Hidden Sectors":
            boot_sector[28:32] = value.to_bytes(4, 'little')
        elif key == "Total Sectors (32-bit)":
            boot_sector[32:36] = value.to_bytes(4, 'little')
        elif key == "Sectors per FAT (32-bit)":
            boot_sector[36:40] = value.to_bytes(4, 'little')
        elif key == "Flags":
            boot_sector[40:42] = value.to_bytes(2, 'little')
        elif key == "Version":
            boot_sector[42:44] = value.to_bytes(2, 'little')
        elif key == "Root Cluster":
            boot_sector[44:48] = value.to_bytes(4, 'little')
        elif key == "FSInfo Sector":
            boot_sector[48:50] = value.to_bytes(2, 'little')
        elif key == "Backup Boot Sector":
            boot_sector[50:52] = value.to_bytes(2, 'little')
        elif key == "Drive Number":
            boot_sector[64] = value
        elif key == "Reserved1":
            boot_sector[65] = value
        elif key == "Boot Signature":
            boot_sector[66] = value
        elif key == "Volume ID":
            boot_sector[67:71] = value.to_bytes(4, 'little')
        elif key == "Volume Label":
            boot_sector[71:81] = value.ljust(10).encode('ascii')
        elif key == "File System Type":
            boot_sector[82:90] = value.ljust(8).encode('ascii')

    # Write the updated boot sector back to the file
    with open(file_path, 'rb+') as f:
        f.write(boot_sector)

# Exemplo de uso
fat32_image_path = 'main.11.com.snkplaymore.kof2012a.obb'

# Atualize os valores desejados
updates = {
    "Bytes per Sector": 512,
    "Sectors per Cluster": 8,
    "Reserved Sectors": 32,
    "Number of FATs": 2,
    "Root Entries": 0,
    "Total Sectors (16-bit)": 0,
    "Media Descriptor": 248,
    "Sectors per FAT (16-bit)": 0,
    "Sectors per Track": 32,
    "Number of Heads": 64,
    "Hidden Sectors": 0,
    "Total Sectors (32-bit)": 2457600,
    "Sectors per FAT (32-bit)": 2288,
    "Flags": 0,
    "Version": 0,
    "Root Cluster": 2,
    "FSInfo Sector": 1,
    "Backup Boot Sector": 6,
    "Drive Number": 0,
    "Reserved1": 0,
    "Boot Signature": 41,
    "Volume ID": 3267004188
}

update_fat32_boot_sector(fat32_image_path, updates)