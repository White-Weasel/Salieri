import interface
import uvicorn
from pyngrok import ngrok
app = interface.app
if __name__ == '__main__':
    port = 5000
    # Open a ngrok tunnel to the HTTP server
    ngrok.set_auth_token(r"2L5F22vHF8HA7VDq8WmEpDGCroQ_wxBar5S3o5cywLSBuGmt")
    public_url = ngrok.connect(port).public_url
    print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))
    uvicorn.run("main:app", reload=True, port=port)
