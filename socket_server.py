import socketio
import json
import datetime

sio = socketio.Server(cors_allowed_origins="*", always_connect=True)
app = socketio.WSGIApp(sio)

reset = 0

stop = None

sending_flag = False


def send_infinitely():
    global sending_flag
    global reset
    while sending_flag:
        data = {
            "data": [
                {
                    "independent": "test1",
                    "dependent": reset,
                },
                {"independant": "test2", "dependant": datetime.datetime.now()},
            ]
        }
        data = json.dumps(data, default=str)
        sio.emit(
            "test_channel",
            data,
        )
        print("sent data")
        reset += 1
        reset %= 100
        sio.sleep(5)


@sio.event
def connect(sid, environ):
    print("connect ", sid)
    global sending_flag
    global stop
    sending_flag = True
    stop = sio.start_background_task(send_infinitely)


@sio.event
def disconnect(sid):
    print("disconnect ", sid)
    global sending_flag
    sending_flag = False
    global stop
    stop.join()


print("starting server")
