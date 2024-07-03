import os
import requests

class Downloader:
    def __init__(self, url:str, uf:str, county:list, file_to_download:str, output_dir:str):
        self.url = url
        self.uf = uf
        self.county = county
        self.file_to_download = file_to_download
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def download_tar(self):
        data = {
            'action': 'download',  # Include the 'action' parameter
            'as': f'{self.file_to_download}_{self.uf}_{self.county}.tar',
            'type': 'php-tar',
            'baseHref': f'/{self.uf}/{self.county}/',
            'hrefs': '',
            'hrefs[0]': f'/{self.uf}/{self.county}/{self.file_to_download}/'  # Make sure the 'hrefs[0]' parameter is correctly formatted
        }
        response = requests.post(f'https://geo.fbds.org.br/{self.uf}/{self.county}/?', data=data)
        if response.status_code == 200:
            output_path = os.path.join(self.output_dir, f'{self.file_to_download}_{self.uf}_{self.county}.tar')
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"Download completo. Arquivo salvo em: {output_path}")
        else:
            print(f"Falha ao baixar o arquivo. Código de status: {response.status_code}")
        
        return output_path
    
