import interface
import uvicorn
app = interface.app
if __name__ == '__main__':
    uvicorn.run("main:app", reload=True, port=3000)
