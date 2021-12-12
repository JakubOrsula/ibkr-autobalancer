import ib_insync as ib_lib


class IBBrokerage:
    _instance = None

    @staticmethod
    def connect(port, readonly, host='127.0.0.1', clientId=0):
        ib_lib.util.startLoop()
        ib = ib_lib.IB()

        # ensure that we connect just once
        if not ib.isConnected():
            print('connecting')
            ib.connect(host, port, clientId=clientId, readonly=readonly)
            if ib.isConnected():
                ib.reqMarketDataType(1)
                print('connected')
            else:
                print('Error, try again or smthing')
        else:
            print('already connected')

        IBBrokerage._instance = ib

    @staticmethod
    def get_client():
        if IBBrokerage._instance is None:
            raise ValueError("Brokerage not connected")
        return IBBrokerage._instance

    @staticmethod
    def disconnect():
        IBBrokerage._instance.disconnect()
