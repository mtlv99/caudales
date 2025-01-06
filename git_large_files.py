import os
import sys
import zipfile
import shutil
from pathlib import Path

class GitLargeFiles:
    def __init__(self, chunk_size=95*1024*1024):  # 95MB por chunk para estar seguro
        self.chunk_size = chunk_size
        self.large_files = [
            'datos/SHP/COMUNAS_v1.shp',
            'datos/datos.txt'
        ]
        self.chunks_dir = 'git_chunks'

    def split_file(self, file_path):
        """Divide un archivo en chunks más pequeños."""
        if not os.path.exists(file_path):
            print(f"Error: No se encuentra el archivo {file_path}")
            return False

        # Crear directorio para los chunks si no existe
        os.makedirs(self.chunks_dir, exist_ok=True)
        
        # Obtener el nombre base del archivo para los chunks
        base_name = os.path.join(self.chunks_dir, Path(file_path).name)
        
        # Leer y dividir el archivo
        chunk_number = 0
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(self.chunk_size)
                if not chunk:
                    break
                chunk_name = f"{base_name}.{chunk_number:03d}"
                with open(chunk_name, 'wb') as chunk_file:
                    chunk_file.write(chunk)
                chunk_number += 1
        return True

    def merge_file(self, original_path):
        """Reconstruye un archivo a partir de sus chunks."""
        base_name = os.path.join(self.chunks_dir, Path(original_path).name)
        
        # Asegurarse que el directorio destino existe
        os.makedirs(os.path.dirname(original_path), exist_ok=True)
        
        # Encontrar todos los chunks
        chunks = sorted([f for f in os.listdir(self.chunks_dir) 
                       if f.startswith(Path(original_path).name + ".")])
        
        if not chunks:
            print(f"Error: No se encontraron chunks para {original_path}")
            return False

        # Reconstruir el archivo
        with open(original_path, 'wb') as output:
            for chunk_name in chunks:
                chunk_path = os.path.join(self.chunks_dir, chunk_name)
                with open(chunk_path, 'rb') as chunk:
                    output.write(chunk.read())
        return True

    def process_files(self, should_split=True):
        """Procesa todos los archivos grandes."""
        success = True
        for file_path in self.large_files:
            if should_split:
                print(f"Dividiendo {file_path}...")
                if not self.split_file(file_path):
                    success = False
            else:
                print(f"Reconstruyendo {file_path}...")
                if not self.merge_file(file_path):
                    success = False
        return success

def main():
    if len(sys.argv) != 2 or sys.argv[1].lower() not in ['-s', '-m']:
        print("Uso: python git_large_files.py [-s|-m]")
        print("  -s: Dividir archivos en chunks")
        print("  -m: Reconstruir archivos desde chunks")
        sys.exit(1)

    should_split = sys.argv[1].lower() == '-s'
    handler = GitLargeFiles()
    
    if handler.process_files(should_split):
        print("Operación completada exitosamente!")
    else:
        print("Se encontraron errores durante el proceso.")
        sys.exit(1)

if __name__ == "__main__":
    main()