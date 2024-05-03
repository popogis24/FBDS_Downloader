from nicegui import ui
import uuid
from typing import Dict
 
from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
import json
from nicegui import app
from fbds_client.counties import County_List
import requests
import os
app.add_middleware(SessionMiddleware, secret_key="some_random_string")  # use your own secret key here

# in reality users and session_info would be persistent (e.g. database, file, ...) and passwords obviously hashed
county_list = County_List.county_list()
users = [("user1", "pass1"), ("taesa", "taesa"), ("", "")]
session_info: Dict[str, Dict] = {}
 
 
def is_authenticated(request: Request) -> bool:
    return session_info.get(request.session.get("id"), {}).get("authenticated", False)
 
class MainApplication:
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        self.api_table_gui = {}
        self.report_gui = {}        
        self.dropfields = {}
        self.gui = {}

    def download_shapefiles(self, selected_counties_value) -> None:
        url = f'http://{self.host}:{self.port}/download_shapefiles'
        response = requests.post(url, json=selected_counties_value)
        if response.status_code == 200:
            ui.notify('Download realizado com sucesso! 🎉')
        else:
            ui.notify('Erro ao realizar o download. Por favor, tente novamente.')
        

@ui.page("/")
def main_page(request: Request) -> None:
    #get from this file the url funtions D:\Caruso\geoapi_downloader_windows\TGAD_Server\teste\gado_server\gado_server\src\gado_server\database\configs_db.py
    ui.label("Bem vindo ao FBDS Downloader")
    # if not is_authenticated(request):
    #     return RedirectResponse("/login")
   
    #session_info[request.session["id"]]
 
    #mapp = MainApplication(host=app.storage.user['host_server'], port=app.storage.user['host_port'])
    mapp = MainApplication()
    ui.label(text='Selecione os municípios de interesse: ',
                )
    counties = county_list

    selected_counties = ui.select(counties, multiple=True, value=None, label='with chips') \
                            .classes('w-200').props('use-chips')


    def on_download_click():
        selected_counties_value = {'selected_counties': selected_counties.value}
        mapp.download_shapefiles(selected_counties_value)

    ui.button('Download', on_click=on_download_click)

@ui.page("/login")
def login(request: Request) -> None:
    def try_login() -> None:  # local function to avoid passing username and password as arguments
        if (username.value, password.value) in users:
            session_info[request.session["id"]] = {"username": username.value, "authenticated": True}
            app.storage.user['host_server'] = host_server.value
            app.storage.user['host_port'] = host_port.value
            ui.open("/")
        else:
            ui.notify("Wrong username or password", color="negative")
 
    if is_authenticated(request):
        return RedirectResponse("/")
    request.session["id"] = str(uuid.uuid4())  # NOTE this stores a new session ID in the cookie of the client
    with ui.card().classes("absolute-center"):
        username = ui.input("Username").on("keydown.enter", try_login)
        password = ui.input("Password").props("type=password").on("keydown.enter", try_login)
        host_server = ui.input("IP",value='127.0.0.1').on("keydown.enter", try_login)
        host_port = ui.input("Port", value='8000').on("keydown.enter", try_login)
        ui.button("Log in", on_click=try_login)
       

@ui.page("/logout")
def logout(request: Request) -> None:
    if is_authenticated(request):
        session_info.pop(request.session["id"])
        request.session["id"] = None
        return RedirectResponse("/login")
    return RedirectResponse("/")
ui.run()
