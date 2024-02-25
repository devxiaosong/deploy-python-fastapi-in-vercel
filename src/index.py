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

        cdm = Cdm.from_device(device)
        session_id = cdm.open()

        # raw_pssh = "AAACqnBzc2gAAAAAmgTweZhAQoarkuZb4IhflQAAAoqKAgAAAQABAIACPABXAFIATQBIAEUAQQBEAEUAUgAgAHgAbQBsAG4AcwA9ACIAaAB0AHQAcAA6AC8ALwBzAGMAaABlAG0AYQBzAC4AbQBpAGMAcgBvAHMAbwBmAHQALgBjAG8AbQAvAEQAUgBNAC8AMgAwADAANwAvADAAMwAvAFAAbABhAHkAUgBlAGEAZAB5AEgAZQBhAGQAZQByACIAIAB2AGUAcgBzAGkAbwBuAD0AIgA0AC4AMAAuADAALgAwACIAPgA8AEQAQQBUAEEAPgA8AFAAUgBPAFQARQBDAFQASQBOAEYATwA + ADwASwBFAFkATABFAE4APgAxADYAPAAvAEsARQBZAEwARQBOAD4APABBAEwARwBJAEQAPgBBAEUAUwBDAFQAUgA8AC8AQQBMAEcASQBEAD4APAAvAFAAUgBPAFQARQBDAFQASQBOAEYATwA + ADwASwBJAEQAPgA5AHoAQQBHAHQAMwBPAEYARABPAE4AUwBrAE8AbQBuADIAagBLAG8AOQBBAD0APQA8AC8ASwBJAEQAPgA8AEMASABFAEMASwBTAFUATQA + AEcAegBsAFEAaABOAE0AagA0AHYAbwA9ADwALwBDAEgARQBDAEsAUwBVAE0APgA8AEwAQQBfAFUAUgBMAD4AaAB0AHQAcABzADoALwAvAGwAaQBjAGUAbgBzAGUALgBwAGEAbABsAHkAYwBvAG4ALgBjAG8AbQAvAHIAaQAvAGwAaQBjAGUAbgBzAGUATQBhAG4AYQBnAGUAcgAuAGQAbwA8AC8ATABBAF8AVQBSAEwAPgA8AC8ARABBAFQAQQA+ADwALwBXAFIATQBIAEUAQQBEAEUAUgA+AA=="
        raw_pssh = "AAAAUnBzc2gAAAAA7e+LqXnWSs6jyCfc1R0h7QAAADIIARIQtwYw94Vz4wxSkOmn2jKo9BoMaW5rYWVudHdvcmtzIgozMTc0MTAxNjg4KgJIRA=="
        pssh = PSSH(raw_pssh)
        challenge = cdm.get_license_challenge(session_id, pssh)
        return {"message": challenge}
    except Exception as e:
        return {"message": str(e)}

    return {"message": "Device"}
