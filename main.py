import interface
import uvicorn
import os
from pyngrok import ngrok
app = interface.app
if __name__ == '__main__':
    port = 3000
    # Open a ngrok tunnel to the HTTP server
    ngrok.set_auth_token(os.getenv('ngrok_token'))
    public_url = ngrok.connect(port)
    print(public_url)
    uvicorn.run("main:app", reload=True, port=port)
