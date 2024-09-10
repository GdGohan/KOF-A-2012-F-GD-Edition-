def aumentar_imagem_fat32(arquivo_imagem, novo_tamanho_mb):
    # Converte o novo tamanho de MB para bytes
    novo_tamanho_bytes = novo_tamanho_mb * 1024 * 1024
    
    # Abre o arquivo da imagem FAT32
    with open(arquivo_imagem, "r+b") as img_file:
        # Calcula o tamanho atual do arquivo
        img_file.seek(0, 2)  # Move para o final do arquivo
        tamanho_atual_bytes = img_file.tell()
        
        # Verifica se o arquivo já é do tamanho desejado
        if tamanho_atual_bytes >= novo_tamanho_bytes:
            print(f"O arquivo já tem {tamanho_atual_bytes / (1024 * 1024)} MB, que é maior ou igual ao novo tamanho.")
            return
        
        # Localiza a posição onde "com" aparece no final do arquivo
        img_file.seek(0)
        conteudo = img_file.read()
        posicao_com = conteudo.rfind(b"com")
        
        if posicao_com == -1:
            print("String 'com' não encontrada no arquivo.")
            return
        
        print(f"Encontrada a string 'com' na posição {posicao_com}. Inserindo bytes antes.")
        
        # Insere os novos bytes antes da string "com"
        espaco_extra = novo_tamanho_bytes - tamanho_atual_bytes
        novos_bytes = b'\x00' * espaco_extra
        
        # Atualiza o arquivo, inserindo os novos bytes antes de "com"
        novo_conteudo = conteudo[:posicao_com] + novos_bytes + conteudo[posicao_com:]
        
        # Sobrescreve o arquivo com o novo conteúdo
        img_file.seek(0)
        img_file.write(novo_conteudo)
    
    # Modifica o setor de boot para refletir o novo tamanho
    modificar_boot_sector(arquivo_imagem, novo_tamanho_bytes)
    print(f"Tamanho da imagem FAT32 atualizado para {novo_tamanho_mb} MB.")

def modificar_boot_sector(arquivo_imagem, novo_tamanho_bytes):
    # Tamanho do setor em bytes (geralmente 512 para FAT32)
    tamanho_setor = 512
    
    # Calcula o novo número total de setores
    novo_total_setores = novo_tamanho_bytes // tamanho_setor
    
    # Posição do campo "Total Sectors" (32 bits) no setor de boot (offset 32)
    with open(arquivo_imagem, "r+b") as img_file:
        # Vai até o campo do total de setores no setor de boot
        img_file.seek(32)
        
        # Escreve o novo valor do número total de setores em formato little-endian
        img_file.write(novo_total_setores.to_bytes(4, byteorder='little'))
    
    print(f"Campo 'Total Sectors' atualizado no setor de boot para {novo_total_setores} setores.")

# Exemplo de uso
arquivo_imagem = "main.11.com.snkplaymore.kof2012a.obb"  # Nome do arquivo da imagem FAT32
novo_tamanho_mb = 1200  # Novo tamanho desejado (em MB)

aumentar_imagem_fat32(arquivo_imagem, novo_tamanho_mb)
