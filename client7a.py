import tkinter as tk
import socket
import ssl
import threading

class ChatWindow:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("----------------Chat Room--------------------")
        
        self.chat_box = tk.Text(self.parent, height=40, width=80)
        self.chat_box.pack()
        
        self.entry_box = tk.Entry(self.parent)
        self.entry_box.pack()
        
        self.send_button = tk.Button(self.parent, text="Send", command=self.send_message)
        self.send_button.pack()
        
        # Load SSL/TLS certificate and key
        certfile = "server.crt"
        ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        ssl_context.load_verify_locations(certfile)

        # Connect to the server
        server_address = ('localhost', 8080)
        self.client_socket = ssl_context.wrap_socket(socket.socket(socket.AF_INET), server_hostname='localhost')
        self.client_socket.connect(server_address)

        # Start thread for receiving messages
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

        send_thread = threading.Thread(target=self.send_message)
        send_thread.start()
        
    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                self.chat_box.insert(tk.END, message + "\n")
                print(message)
            except:
                break

    def send_message(self):
        message = self.entry_box.get()
        try:
            self.client_socket.send(message.encode())
            self.chat_box.insert(tk.END, "You: " + message + "\n")
            self.entry_box.delete(0, tk.END)
        except:
            self.chat_box.insert(tk.END, "Error sending message\n")



if __name__ == "__main__":
    root = tk.Tk()
    app = ChatWindow(root)
    root.mainloop()
