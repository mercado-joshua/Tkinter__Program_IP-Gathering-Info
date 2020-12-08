#===========================
# Imports
#===========================
import tkinter as tk
from tkinter import ttk, colorchooser as cc, Menu, Spinbox as sb, scrolledtext as st, messagebox as mb, filedialog as fd, simpledialog as sd

import requests
import socket
import ipaddress

#===========================
# Main App
#===========================
class App(tk.Tk):
    """Main Application."""
    #------------------------------------------
    # Initializer
    #------------------------------------------
    def __init__(self):
        super().__init__()
        self.init_config()
        self.init_vars()
        self.init_widgets()

    #------------------------------------------
    # Instance Variables
    #------------------------------------------
    def init_vars(self):
        self.ip_api = 'http://ip-api.com/json/'
        self.static_ip = socket.gethostbyname(socket.gethostname())
        self.public_ip = requests.get('http://httpbin.org/ip').json()['origin']

    #-------------------------------------------
    # Window Settings
    #-------------------------------------------
    def init_config(self):
        self.resizable(True, True)
        self.title('IP Gathering Tool Version 1.0')
        self.iconbitmap('python.ico')
        self.style = ttk.Style(self)
        self.style.theme_use('clam')

    #-------------------------------------------
    # Widgets / Components
    #-------------------------------------------
    def init_widgets(self):
        frame1 = ttk.Frame(self)
        frame1.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.frame2 = ttk.Frame(self)
        self.frame2.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # ------------------------------------------
        label = ttk.Label(frame1, text='IP Address')
        label.pack(side=tk.TOP, fill=tk.X, anchor=tk.NW, padx=10, pady=(10, 0))

        self.ip = tk.StringVar()
        self.ip.set(self.static_ip)
        entry = ttk.Entry(frame1, width=50, textvariable=self.ip)
        entry.pack(side=tk.TOP, fill=tk.X, anchor=tk.NW, padx=10, ipady=5)
        entry.focus()

        self.button = ttk.Button(frame1, text='Gather Info', command=self.gather_info)
        self.button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.textarea = st.ScrolledText(self.frame2, wrap=tk.WORD)
        self.textarea.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.textarea.pack_forget()

    # ------------------------------------------
    def ip_valid(self, ip):
        try:
            ipaddress.ip_address(ip)
            return True
        except:
            return False

    def gather_info(self):
        self.button.config(state=tk.DISABLED)
        self.textarea.delete('1.0', tk.END)
        try:
            target_ip = self.ip.get()
            if not self.ip_valid(target_ip):
                target_ip = socket.gethostbyname(target_ip)
        except IndexError:
            target_ip = self.public_ip

        data = requests.get(f'{self.ip_api}/{target_ip}').json()

        for item in data:
            self.textarea.insert(tk.END, f'{item} : {data[item]}\n')
        self.textarea.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.button.config(state=tk.NORMAL)


#===========================
# Start GUI
#===========================
def main():
    app = App()
    app.mainloop()

if __name__ == '__main__':
    main()