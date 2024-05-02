import tomli as toml

class Config:
    def __init__(self, filepath=r"/Users/andersonstolfi/Documents/coding/FBDS_Downloader/FBDS_Downloader/settings.toml"):
        with open(filepath, "rb") as file:  # Open the file in binary mode
            self.settings = toml.load(file)

    def __getattr__(self, name):
        return self.settings.get(name, None)
    
# Usage:
# from configs import Config
# settings = Config()
# settings.EMAIL['email_receiver']