import logging
import traceback

from fastapi import FastAPI, Request, Response, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from brain import Brain

app = FastAPI()
app.mount("/static", StaticFiles(directory="assets"), name="static")
origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
templates = Jinja2Templates(directory="assets/template")
Salie = Brain()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/status")
async def get_satus(request: Request):
    return {"sleeping": Salie.sleeping}


@app.post("/conversation")
async def conversation(request: Request):
    req = await request.json()
    if 'question' not in req:
        return {'Error': 'Missing question.'}
    user = req.get('user')
    question = req['question']
    answer = Salie.languageProcessor.answer(question, user)
    logger.log(level=logging.DEBUG, msg=Salie.languageProcessor.model.conversation)
    return {
        "answer": answer,
    }


@app.post("/sleep")
async def salie_sleep(request: Request):
    Salie.sleep()
    logger.debug('Salie is sleeping')
    return {
        'success': True
    }


@app.post("/wake_up")
async def salie_wakeup(request: Request, response: Response):
    try:
        Salie.wake_up()
    except AssertionError:
        response.status_code = 400
        return {'success': False, 'message': 'Salie has already wake up'}
    except Exception as e:
        traceback_log = ''.join(traceback.format_exception(e))
        logger.error(traceback_log)
        return {
            'success': False,
            'error': e,
            'traceback': traceback_log
        }
    else:
        logger.debug('Salie is waking up')
        return {
            'success': True
        }


@app.post("/clear_memory")
async def clear_memory():
    try:
        Salie.memory.long_term_memory.clear_memory()
        return {
            'success': True
        }
    except Exception as e:
        traceback_log = ''.join(traceback.format_exception(e))
        logger.error(traceback_log)
        return {
            'success': False,
            'error': e,
            'traceback': traceback_log
        }

# TODO: clear previous prompts
