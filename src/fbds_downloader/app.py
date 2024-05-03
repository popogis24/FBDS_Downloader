import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pipeline import Pipeline
from configs import Config

app = FastAPI()
settings = Config()

class FileStructure(BaseModel):
    selected_counties: list[str]

@app.get("/")
async def root():
    return "Hello World!"
    
@app.post("/download_shapefiles")
async def download_shapefiles(file_structure: FileStructure):
    selected_counties = file_structure.selected_counties
    
    dict_of_files = {}
    for county in selected_counties:
        county_data = county.split('-')
        if len(county_data) != 2:
            raise HTTPException(status_code=400, detail="Invalid county format")
        city_name, state_code = county_data
        dict_of_files.setdefault(state_code, {})[city_name] = ['APP', 'HIDROGRAFIA']
    
    print(f'Parsed data: {dict_of_files}')
    
    url = settings.BASIC['url']
    output_dir = settings.BASIC['output_dir']

    pipeline = Pipeline(url=url,
                        dict_of_files=dict_of_files,
                        output_dir=output_dir)

    list_of_files = pipeline.get_list_of_files()
    pipeline.get_merged_shapefiles(list_of_files)

    return {"message": "Pipeline run successfully!"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8000, workers=1, log_level="info")
