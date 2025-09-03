import socket
import tkinter as tk
import tkinter.messagebox as messagebox
import sys

def connect_to_server(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        return client_socket
    except ConnectionRefusedError:
        raise ConnectionError("Failed to connect to the server. Check if the server is running and the port is correct.")
    except OSError as e:
        raise ConnectionError(f"Error: {e}")

def send_word(event=None):
    try:
        word = entry_word.get().strip()
        if word:
            client_socket.send(word.encode('utf-8'))
            meaning = client_socket.recv(1024).decode('utf-8')
            text_output.config(state=tk.NORMAL)
            text_output.delete(1.0, tk.END)
            text_output.insert(tk.END, meaning)
            text_output.config(state=tk.DISABLED)
        else:
            messagebox.showwarning("Input Error", "Please enter a word or phrase.")        
    except ConnectionResetError:
        messagebox.showerror("Connection Error", "Connection reset by the server.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def close_app():
    if client_socket:
        client_socket.close() 
    root.destroy()

def handle_keyboard_interrupt(event):
    messagebox.showwarning("Connection Warning", "The connection ended because you pressed <Control-c>")
    close_app()


root = tk.Tk()
root.title("Small Dictionary")
root.geometry("500x320")
root.configure(bg="pink")

frame = tk.Frame(root, padx=10, pady=10)
frame.grid(row=0, column=0)
frame.configure(bg="pink")

label_word = tk.Label(frame, text="Enter a word:", font=("Times New Roman", 12), bg="Deep Pink")
label_word.grid(row=0, column=0, padx=5, pady=5)

entry_word = tk.Entry(frame, width=30, font=("Arial", 12))
entry_word.grid(row=0, column=1, padx=5, pady=5)
entry_word.bind("<Return>", send_word) 

try:
    client_socket = connect_to_server('127.0.0.1', 8888)
except ConnectionError as e:
    messagebox.showerror("Connection Error", str(e))
    sys.exit()

button_search = tk.Button(frame, text="Search", command=send_word, font=("Times New Roman", 12), bg="Deep Pink", fg="black")
button_search.grid(row=0, column=2, padx=5, pady=5)

text_output = tk.Text(frame, width=50, height=10, state=tk.DISABLED, font=("Times New Roman", 12))
text_output.grid(row=1, columnspan=3, padx=5, pady=10)

button_close = tk.Button(frame, text="Close", command=close_app, font=("Times New Roman", 12), bg="Deep Pink", fg="black")
button_close.grid(row=2, columnspan=3, pady=5)

root.bind("<Control-c>", handle_keyboard_interrupt)
root.mainloop()
