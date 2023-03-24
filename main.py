import brain
# import interface
# import uvicorn
# import threading

# app = interface.app

if __name__ == '__main__':
    # port = 3000
    # Open a ngrok tunnel to the HTTP server
    # ngrok.set_auth_token(os.getenv('ngrok_token'))
    # public_url = ngrok.connect(port)
    # print(public_url)
    # nest_asyncio.apply()=
    # uvicorn.run(app, port=port)
    Salie = brain.Brain()
    try:
        Salie.wake_up()
    except KeyboardInterrupt:
        Salie.sleep()
