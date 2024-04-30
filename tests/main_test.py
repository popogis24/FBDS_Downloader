import os
import pytest
from src.fbds_downloader.downloader import Downloader

@pytest.fixture
def downloader():
    return Downloader(url='https://geo.fbds.org.br/', 
                      uf='PR', county='CURITIBA', 
                      file_to_download='APP', 
                      output_dir=r'C:\FBDS_Downloader\FBDS_Downloader\tests\test_data')

def test_download_tar(downloader, tmp_path):
    downloader.output_dir = tmp_path
    downloader.download_tar()
    expected_file = tmp_path / 'APP_PR_CURITIBA.tar'
    assert expected_file.is_file(), "Arquivo não foi baixado corretamente"
