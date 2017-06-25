
import mido
import mido.backends.rtmidi
from mido.ports import MultiPort
from mido.sockets import PortServer,connect


#keyboard_input  = mido.open_input('QX25 6')
clock = mido.open_input('5- TR-8 3')
#input = MultiPort([keyboard_input,clock])

input = MultiPort([clock])


with PortServer('localhost', 8080) as server:
	clients = []
	while True:
		# Handle connections.
		client = server.accept(block=False)
		if client:
			print('Connection from {}'.format(client.name))
			clients.append(client)

		if(len(clients) > 0):
			for i, client in enumerate(reversed(clients)):
				if client.closed:
					print('{} disconnected'.format(client.name))
					del clients[i]

			# Do other things
			for msg in input.iter_pending():
				for c in clients:
					c.send(msg)
