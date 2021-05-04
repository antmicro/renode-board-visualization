import clr
clr.AddReference("Renode-peripherals")
clr.AddReference("IronPython.StdLib")

import os
import SimpleHTTPServer
import SocketServer
from threading import Thread

from Antmicro.Renode.Peripherals.Miscellaneous import LED
from Antmicro.Renode.Peripherals.UART import IUART
# get current path, 0 is for Renode directory, 1 for cwd
cwd = monitor.CurrentPathPrefixes[1]
sys.path.append(cwd)
# fix compat issues
#sys.version_info = [2,7,1]

os.chdir(cwd)

from websocket_server import WebsocketServer

def send_message(message):
    if websocket_server is not None and len(websocket_server.clients) > 0:
        for client in websocket_server.clients:
            try:
                websocket_server.send_message(client, message)
            except Exception as e:
                # in case something got disconnected
                pass

# called when a client sends a message
def message_received(client, server, message):
    if len(message) > 200:
        message = message[:200]+'..'
    print "Client(%d) said: %s" % (client['id'], message)


def blink_led(led, state):
    send_message("|".join(["LED", machine.GetLocalName(led), str(state)]))


def send_uart_chars(char):
    send_message("|".join(["UART", "uart0", chr(char)]))

main_server = None
server_thread = None
websocket_server = None
websocket_thread = None

machine = None

print "Adding serveVisualization command."
def mc_serveVisualization(port):
    global main_server
    global server_thread
    global websocket_server
    global websocket_thread
    global machine

    # get emulation
    emulation = Antmicro.Renode.Core.EmulationManager.Instance.CurrentEmulation

    # Assume a single machine for now.
    machine = emulation.Machines[0]

    leds = machine.GetPeripheralsOfType[LED]()
    for led in leds:
        led.StateChanged += blink_led
    
    uarts = machine.GetPeripheralsOfType[IUART]()
    for uart in uarts:
        uart.CharReceived += send_uart_chars
        #break on uart0
        break

    # setting up server threads
    websocket_server = WebsocketServer(9001)
    websocket_server.set_fn_message_received(message_received)
    websocket_thread = Thread(target=websocket_server.serve_forever)
    websocket_thread.deamon = True
    websocket_thread.start()

    try:
        main_server = SocketServer.TCPServer(("", port), SimpleHTTPServer.SimpleHTTPRequestHandler)
        server_thread = Thread(target = main_server.serve_forever)
        server_thread.deamon = True

        print "Serving interactive visualization at port", port
        server_thread.start()
    except:
        import traceback
        traceback.print_exc()



def mc_stopVisualization():
    global main_server
    global server_thread
    global websocket_server
    global websocket_thread

    if main_server is None:
        print "Start visualization with `serveVisualization {port}` first"
        return

    main_server.shutdown()
    main_server.server_close()
    websocket_server.close_server()
    server_thread.join()
    websocket_thread.join()
    main_server = None
    server_thread = None
    websocket_server = None
    websocket_thread = None

