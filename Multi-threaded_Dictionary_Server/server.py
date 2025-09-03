import socket
import threading
from concurrent.futures import ThreadPoolExecutor
import json
import sys

 
try:
    with open('database.json') as f:
        dictionary = json.load(f)
except FileNotFoundError:
    print("Sorry the dictionary file not found.")
    sys.exit()
except json.JSONDecodeError:
    print("Error : 'bad data' to decode the JSON file.")
    sys.exit()

def handle_client(client_socket):
    try:
        while True:
            word = client_socket.recv(1024).decode().strip()
            if not word:
                error_message = "Please enter a word or phrase."
                client_socket.send(error_message.encode())
                continue  # Continue listening for input
            if word in dictionary:
                meaning = dictionary[word]
                response = f"Meaning of the word '{word}': {meaning}"
            else:
                response = f"The word '{word}' was not found in the dictionary."
            client_socket.send(response.encode())
    except ConnectionAbortedError:
        print("Connection closed by the client ,as a result of pressing Close or <Control-c> or close the window.")   
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
    finally:
        client_socket.close()

def main():
    server_host = '127.0.0.1'
    server_port = 8888
    max_threads = 15  # Maximum number of threads in the thread pool

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_host, server_port))
    server_socket.listen(15)
    print(f"Server listening on {server_host}:{server_port}")

    # Create a thread pool
    with ThreadPoolExecutor(max_threads) as executor:
        try:
            while True:
                client_socket, client_address = server_socket.accept()
                client_add = client_address 
                print(f"Connection from {client_address} established.")
                # Submit the client handling task to the thread pool
                executor.submit(handle_client, client_socket)
        except KeyboardInterrupt:
            print("Server stopped by the user.")
        finally:
            server_socket.close()

if __name__ == "__main__":
    main()
