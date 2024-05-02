import requests
import uvicorn
from fastapi import FastAPI
from pipeline import Pipeline
from configs import Config

settings = Config()

app = FastAPI()

@app.get("/")
async def root():
    return "Hello World!"


@app.get("/run_pipeline")
def run_pipeline(dict_of_files: dict):
    url = settings.BASIC['url']
    output_dir = settings.BASIC['output_dir']

    pipeline = Pipeline(url=url,
                        dict_of_files=dict_of_files,
                        output_dir=output_dir)
    
    list_of_files = pipeline.get_list_of_files()
    pipeline.get_merged_shapefiles(list_of_files)
    
    return {"message": "Pipeline run successfully!"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)