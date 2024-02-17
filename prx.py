import socket
from threading import Thread

image_filter = 0
image_extentions = {'.jpg', '.png', '.jpeg', '.gif', 'apng', 'avif', 'svg', 'webp'}
	
def extract_header(http_message):
	splited_message = http_message.split('\r\n\r\n', maxsplit=1)
	header = splited_message[0]
	
	header_lines = header.split('\r\n')

	target = ['Host', 'User-Agent', 'Content-Type', 'Content-Length']
	headers = {'head':None, 'Host': None, 'User-Agent':None, 'Content-Type':None, 'Content-Length':None, 'redirect':0, 'filter':0}

	headers['head'] = header_lines[0]	

	if "korea" in headers['head']:
		headers['redirect'] = "[O] Redirected"
	else:
		headers['redirect'] = "[X] Redirected"

	global image_filter
	if "?image_off" in headers['head']:
		image_filter = 1
	if "?image_on" in headers['head']:
		image_filter = 0
	if image_filter:
		headers['filter'] = "[O] Image Filter"
	else:
		headers['filter'] = "[X] Image Filter"
	
	for line in header_lines:
		if ':' not in line: continue
		key, value = line.split(':', 1)
		if key.strip() in target:
			headers[key.strip()] = value.strip()
	return headers
		

def handle_client(client_socket, address, request_order):
	log = ""

	request_data = client_socket.recv(4096)
	headers = extract_header(request_data.decode('utf-8', errors='ignore'))
	
	log += f"{request_order} {headers['redirect']} {headers['filter']}\n"	
	log += f"[CLI connected from {address}\n[CLI ==> PRX --- SRV]\n"
	log += f" > {headers['head']}\n > {headers['User-Agent']}\n"

	destination_host, destination_port = headers['Host'], 80

	if "korea" in headers['head']:
		destination_host = "mnet.yonsei.ac.kr"
		request_data = f"GET http://mnet.yonsei.ac.kr HTTP/1.1\r\nHost: mnet.yonsei.ac.kr\r\nUser-Agent: {headers['User-Agent']}\r\n\r\n".encode('utf-8')
	
	global image_filter
	if image_filter:
		for extention in image_extentions:
			if extention in headers['head']:
				response = "HTTP/1.1 404 Not Found\r\n"
				client_socket.send(response.encode())
				client_socket.close()
				log += f"[CLI <== PRX --- SRV]\n > 404 Not Found\n[CLI disconnected]\n"
				print(log)
				return
	
	destination_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	destination_socket.connect((destination_host, destination_port))

	headers = extract_header(request_data.decode('utf-8', errors='ignore'))
	log += f"[SVR connected to {destination_host}:{destination_port}]\n[CLI --- PRX ==> SVR]\n > {headers['head']}\n > {headers['User-Agent']}\n"

	destination_socket.send(request_data)
	response_data = destination_socket.recv(4096)

	headers = extract_header(response_data.decode('utf-8', errors='ignore'))
	log += f"[CLI --- PRX <== SVR]\n > {headers['head']}\n > {headers['Content-Type']} {headers['Content-Length']}\n" 
	
	while response_data:	
		#response_data = modify_header(response_data.decode())
		client_socket.send(response_data)
		response_data = destination_socket.recv(4096)
	log += f"[CLI <== PRX --- SVR]\n > {headers['head']}\n > {headers['Content-Type']} {headers['Content-Length']}\n" 

	client_socket.close()
	destination_socket.close()

	log += "[CLI disconnected]\n[SVR disconnected]\n"
	print(log)

def start_proxy(client_ip, client_port):
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind((client_ip, client_port))
	server_socket.listen()

	print(f"Starting proxy server on port 9001")
	
	request_order = 0
	try:
		while True:
			client_socket, address = server_socket.accept()
			request_order += 1	
			proxy_thread = Thread(target = handle_client, args = (client_socket, address, request_order))
			proxy_thread.start()
	except KeyboardInterrupt:
		server_socket.close()
		print("\n[Ctrl+c received Closing the proxy server]")

if __name__ == "__main__":
	
	host = '127.0.0.1'
	port = 9001 
	start_proxy(host, port)
