from fastapi import FastAPI

from pywidevine.cdm import Cdm
from pywidevine.device import Device
from pywidevine.pssh import PSSH
from src.dtos.ISayHelloDto import ISayHelloDto

app = FastAPI()

client_id_file = "client_id.bin"
private_key_file = "private_key.pem"

# 从文件中读取内容
with open(client_id_file, "rb") as f:
    client_id = f.read()

with open(private_key_file, "r") as f:
    private_key = f.read()


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
    try:
        device = Device(
            type_=Device.Types.ANDROID,
            security_level=3,
            flags={},
            client_id=client_id,
            private_key=private_key,
        )
    except Exception as e:
        return {"message": str(e)}

    return {"message": "Device"}
