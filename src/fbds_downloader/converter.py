import os
import shutil
import patoolib
import geopandas as gpd


class Converter:
    def __init__(self, file_path: str, output_dir: str):
        self.file_path = file_path
        self.output_dir = output_dir
        
    def unzip(self):
        try:
            patoolib.extract_archive(self.file_path, outdir=self.output_dir, verbosity=-1)
            print(f"Arquivo descompactado em: {self.output_dir}")
        except patoolib.util.PatoolError as e:
            print(f"Erro ao descompactar o arquivo: {e}")
        finally:
            os.remove(self.file_path)
            print(f"Arquivo removido: {self.file_path}")
    
    def iterate_and_append(self):
        shp_file_paths = []  # Lista para armazenar os endereços completos dos arquivos .shp encontrados
        for root, dirs, files in os.walk(self.output_dir):
            for file in files:
                if file.endswith('.shp'):
                    shp_file_paths.append(os.path.join(root, file))
        print(f"Arquivos .shp encontrados: {shp_file_paths}")
        return shp_file_paths

    def merge_shapefiles(self, list_of_files):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
        APP = [file for file in list_of_files if file.endswith('APP.shp')], "APP"
        APP_USO = [file for file in list_of_files if file.endswith('APP_USO.shp')], "APP_USO"
        MASSAS_DAGUA = [file for file in list_of_files if file.endswith('MASSAS_DAGUA.shp')], "MASSAS_DAGUA"
        NASCENTES = [file for file in list_of_files if file.endswith('NASCENTES.shp')], "NASCENTES"
        RIOS_DUPLOS = [file for file in list_of_files if file.endswith('RIOS_DUPLOS.shp')], "RIOS_DUPLOS"
        RIOS_SIMPLES = [file for file in list_of_files if file.endswith('RIOS_SIMPLES.shp')], "RIOS_SIMPLES"
        
        list_of_lists = [APP, APP_USO, MASSAS_DAGUA, NASCENTES, RIOS_DUPLOS, RIOS_SIMPLES]
        for i in list_of_lists:
            if len(i[0])>1:
                read_file = [gpd.read_file(file).to_crs(4674) for file in i[0]]
                
                gpd.pd.concat(read_file, ignore_index=True).to_file(os.path.join(self.output_dir, i[1] + ".shp"))

    def zipfiles(self):
        try:
            zipped_file = shutil.make_archive(self.output_dir, 'zip', self.output_dir)
            return zipped_file
        except Exception as e:
            print(f"Erro ao compactar o arquivo: {e}")
        