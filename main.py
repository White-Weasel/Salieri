import interface
import uvicorn
from pyngrok import ngrok
app = interface.app
if __name__ == '__main__':
    port = 3000
    # Open a ngrok tunnel to the HTTP server
    ngrok.set_auth_token(r"2L5VWLGxOLhsjQQeeEnnHPC6jAz_515XdsUJ2MMQ8Eivq8uJD")
    public_url = ngrok.connect(port)
    print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))
    uvicorn.run("main:app", reload=True, port=port)
