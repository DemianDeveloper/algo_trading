import json
import threading
import time
import traceback
import websocket


class Socket_conn_Bybit(websocket.WebSocketApp):
    def __init__(self, url, on_message, params=None):
        super().__init__(
            url=url,
            on_open=self.on_open,
            on_message=on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        self.price = None
        self.params = params
        # self.run_forever()

    def send_heartbeat(self, ws):
        while True:
            ws.send(json.dumps({"req_id": "100001", "op": "ping"}))
            time.sleep(20)

    def on_open(self, ws):
        print(ws, 'Websocket was opened')

        # Start heartbeat
        # _thread.start_new_thread(self.send_heartbeat, (ws,))
        threading.Thread(target=self.send_heartbeat, args=(ws,)).start()

        # Subscription data:
        data = {"op": "subscribe", "args": self.params}
        ws.send(json.dumps(data))

    def on_error(self, ws, error):
        print('on_error', ws, error)
        print(traceback.format_exc())


    def on_close(self, ws, status, msg):
        print('on_close', ws, status, msg)

    def on_message(self, ws, msg):
        # print('on_message', ws, msg)
        data = json.loads(msg)
        # print(data)


    def return_price(self):
        return self.price
