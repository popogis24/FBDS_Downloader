import os
import shutil
import patoolib

class Converter:
    def __init__(self, file_path: str, output_dir: str):
        self.file_path = file_path
        self.output_dir = output_dir

    def unzip(self):
        if self.file_path.endswith('.tar'):
            patoolib.extract_archive(self.file_path, outdir=self.output_dir)
            print(f"Arquivo descompactado em: {self.output_dir}")
        else:
            print("Formato de arquivo não suportado para descompactação.")

if __name__ == "__main__":
    file_path = r'C:\FBDS_Downloader\FBDS_Downloader\tests\test_data\APP_PR_CURITIBA.tar'
    output_dir = r'C:\FBDS_Downloader\FBDS_Downloader\tests\test_data\APP_PR_CURITIBA'

    conversor = Converter(file_path, output_dir)
    conversor.unzip()
