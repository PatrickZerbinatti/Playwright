from fastapi import FastAPI
from laptops_info import all_laptops_info

app = FastAPI()

@app.get("/")
async def get_all_laptop_info():
    teste = all_laptops_info()
    return teste