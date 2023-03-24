from fastapi import FastAPI, Request
from brain import Brain
import logging

app = FastAPI()
Salie = Brain()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


@app.get("/")
async def root():
    return {"question": "Hello World"}


@app.post("/conversation")
async def conversation(request: Request):
    req = await request.json()
    question = req['question']
    answer = Salie.languageProcessor.answer(question)
    logger.log(level=logging.DEBUG, msg=Salie.languageProcessor.model.conversation)
    return {
        "answer": answer,
    }


@app.post("/sleep")
async def salie_sleep(request: Request):
    Salie.sleep()
    logger.debug('Salie is sleeping')
    return {
        'status': 'Successful'
    }


@app.post("/wake_up")
async def salie_wakeup(request: Request):
    Salie.wake_up()
    logger.debug('Salie is waking up')
    return {
        'status': 'Successful'
    }
