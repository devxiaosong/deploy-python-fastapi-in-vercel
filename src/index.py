from fastapi import FastAPI

from pywidevine.cdm import Cdm
from pywidevine.device import Device
from pywidevine.pssh import PSSH
from src.dtos.ISayHelloDto import ISayHelloDto

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/hello")
async def hello_message(dto: ISayHelloDto):
    return {"message": f"Hello {dto.message}"}


@app.get("/cdm/device")
async def cdm_device():
    Device(
        type_=Device.Types.ANDROID,
        security_level=3,
        flags={},
        client_id='123',
        private_key='456',
    )
    return {"message": "Device"}
