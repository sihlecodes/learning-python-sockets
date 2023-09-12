from ses import ESClient

with ESClient("localhost", 9898) as client:
    client.on("connected", lambda *args: print("client connected!")) # emited internally
    client.on("disconnected", lambda *args: print("client disconnected!")) # emited internally
    client.on("do_the_thing", lambda: print("client did the thing!"))
    client.on("message", lambda message: print(message))

    # should print "client connected!" and then "client disconnected!"

# client.close() # disconnect should be emitted after .close() is called.