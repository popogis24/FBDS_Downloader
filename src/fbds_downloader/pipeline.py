import os
from configs import Config
from downloader import Downloader
from converter import Converter

class Pipeline:
    def __init__(self, url:str, dict_of_files:dict, output_dir:str):
        self.url = url
        self.dict_of_files = dict_of_files
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
   
    def get_list_of_files(self):
        file_list = []
        for uf, counties in self.dict_of_files.items():
            for county in counties:
                for file in counties[county]:
                    downloader = Downloader(url=self.url, 
                                            uf=uf, 
                                            county=county, 
                                            file_to_download=file, 
                                            output_dir=self.output_dir)
                    downloader.download_tar()
                    file_path = downloader.download_tar()
                    output_dir = os.path.join(self.output_dir, f'{file}_{uf}_{county}')
                    converter = Converter(file_path, output_dir)
                    converter.unzip()
                    file_list.extend(converter.iterate_and_append())
        print(file_list)
        return file_list
    
    def get_merged_shapefiles(self, list_of_files):
        for file in list_of_files:
            print(f"Processando arquivo: {file}")
            output_dir = os.path.join(self.output_dir, 'merged_shapefiles')
            converter = Converter(file, output_dir)
        converter.merge_shapefiles(list_of_files)
        zipped_files = converter.zipfiles()
        return zipped_files

    def run(self):
        list_of_files = self.get_list_of_files()
        output = self.get_merged_shapefiles(list_of_files)
        return output
        
