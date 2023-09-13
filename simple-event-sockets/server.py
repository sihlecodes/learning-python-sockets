from ses import ESServer

server = ESServer("localhost", 9898)

def _on_client_connection(client):
    server.emit_on(client, "message", "Hello, world!")

def _on_client_disconnect(client):
    server.emit_on(client, "message", "Goodbye, world!")

server.on("connection", _on_client_connection) # emitted internally
server.on("disconnect", _on_client_disconnect) # emitted internally

server.emit("do_the_thing") # user defined event signal