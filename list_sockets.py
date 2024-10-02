import psutil

def list_connections():
	counter = 0
	for conn in psutil.net_connections(kind='inet'):
		counter = counter + 1
		print(conn)
	print('Number of connections: ', counter)

if __name__ == "__main__":
	list_connections()
