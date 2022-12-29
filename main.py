# -*- coding: utf-8 -*-
"""
Created on Thu May  5 17:17:51 2022

Idea's correlation / cointegration table. Use for prediction. 
- portolio optimizer. 

@author: Gebruiker
- fix that stocks update only till last friday., make sure strat updaters only use that data.
- fix, only first 1000 tickers are added. 
^ Only run script on Ipython terminal. Mabey split the Server and update script seperated. 


"""

from typing import Optional
from fastapi import BackgroundTasks, FastAPI, Response, HTTPException
from core_service_layer.data_service import get_system_info
import database_querys_main
import startup_script
import service_layer_data_service
import json
import constants
import uvicorn
from mangum import Mangum

app = FastAPI()

# startup_script.start_update_scedule()


def onstart_function():

    startup_script.start_update_scedule()


@app.on_event("startup")
async def startup_event():

    onstart_function()


@app.get("/")
def read_root():

    return {"Welcome to the flowimpact core.. I Love you Leo, LIKE ELMO"}


handler = Mangum(app)

if __name__ == "__main__":

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, debug=True,
                workers=4, limit_concurrency=1000)
