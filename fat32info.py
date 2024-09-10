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
    
    return info

def save_fat32_info_to_txt(file_path, output_txt_path):
    info = read_fat32_boot_sector(file_path)
    
    with open(output_txt_path, 'w') as f:
        for key, value in info.items():
            f.write(f"{key}: {value}\n")

# Exemplo de uso
fat32_image_path = 'main.11.com.snkplaymore.kof2012a.obb'
output_txt_path = 'fat32_info.txt'

save_fat32_info_to_txt(fat32_image_path, output_txt_path)
