import tkinter as tk
from tkinter import ttk, messagebox
from api import getData, placeOrder, check_ema_crossover  # Importing required functions from API module
from constants import tokens, symbol_to_company, USERS  # Importing token and user data
import threading
import time
from datetime import datetime

# Function to validate user login
def check_login():
    username = username_entry.get()
    password = password_entry.get()

    if username in USERS and USERS[username] == password:
        login_window.destroy()  # Close login window on successful login
        open_main_application()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")  # Show error message

# Dictionary to track if a stock has been bought already
bought = {symbol: False for symbol in tokens.keys()}

# Function to open the main application window
def open_main_application():
    root = tk.Tk()
    root.title("DhanSetu")
    root.state('zoomed')  # Maximize the window

    selected_symbol = None  # Variable to track the selected stock

    # Function to update stock data in the UI
    def update_stock_data():
        nonlocal selected_symbol
        while True:
            if selected_symbol:
                symboltoken = tokens.get(selected_symbol)
                if symboltoken:
                    df = getData(symboltoken)
                    root.after(0, lambda: update_table(df))  # Ensure UI updates from main thread
            time.sleep(2)  # Update every 2 seconds

    # Start stock data update thread
    def start_stock_update_thread():
        thread = threading.Thread(target=update_stock_data, daemon=True)
        thread.start()

    # Function to update selected stock symbol
    def on_symbol_select(event):
        nonlocal selected_symbol
        selected_symbol = symbol_var.get()

    # Function to monitor stock conditions and place orders
    def getStatus():
        global bought
        while True:
            for symbol, token in tokens.items():
                df = getData(token)
                check = check_ema_crossover(df)
                if check and not bought[symbol]:
                    add_status(f"(Pending) Placing order - {symbol_to_company[symbol]}...")
                    order_id, order_status = placeOrder(symbol, token)
                    if order_status:
                        add_status(f'(Done) {symbol} - Order placed (ORDER ID = {order_id})')
                        bought[symbol] = True
                    else:
                        add_status(f'(Error) {symbol} - Order placement failed.')
                else:
                    add_status(f"(Pending) Checking for {symbol_to_company[symbol]}...")
                    add_status(f'(Done) Skipped..')
                time.sleep(2)  # Small delay between checks
            time.sleep(65)  # Wait before checking again

    # Start stock monitoring thread
    def start_getStatus_thread():
        thread = threading.Thread(target=getStatus, daemon=True)
        thread.start()

    # Dropdown for selecting stock symbols
    symbol_var = tk.StringVar()
    symbol_dropdown = ttk.Combobox(root, width=100, textvariable=symbol_var, values=list(tokens.keys()), state="readonly", font=("Arial", 12))
    symbol_dropdown.set("Select a symbol")
    symbol_dropdown.bind("<<ComboboxSelected>>", on_symbol_select)
    symbol_dropdown.pack(pady=10)

    # Table frame for displaying stock data
    table_frame = ttk.Frame(root)
    table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    columns = ['datetime', 'open', 'high', 'low', 'close', 'volume', 'EMA9', 'EMA20']
    tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=20)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    for col in columns:
        tree.heading(col, text=col, anchor='center')
        tree.column(col, anchor='center', width=100)

    scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Function to add status messages to the UI
    def add_status(message):
        timestamp = time.strftime('%H:%M:%S')
        status_text.insert(tk.END, f"[{timestamp}] {message}\n")
        status_text.see(tk.END)

    # Status text box for logging messages
    status_text = tk.Text(root, bg="black", fg="white", font=("Arial", 11), wrap=tk.WORD, height=6)
    status_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Function to update the table with new stock data
    def update_table(df):
        for row in tree.get_children():
            tree.delete(row)
        for _, row in df.iterrows():
            tree.insert("", tk.END, values=list(row))

    # Start background threads
    start_getStatus_thread()
    start_stock_update_thread()

    root.mainloop()

# Function to toggle password visibility
def toggle_password():
    if password_entry.cget('show') == "*":
        password_entry.config(show="")
        toggle_button.config(text="Hide")
    else:
        password_entry.config(show="*")
        toggle_button.config(text="Show")

# Create login window
login_window = tk.Tk()
login_window.title("DhanSetu | Login")
login_window.geometry("400x420")
login_window.resizable(False, False)
login_window.configure(bg="#f0f0f0")

# Frame for login widgets
frame = ttk.Frame(login_window, padding=30)
frame.pack(expand=True)

# Username input
username_label = ttk.Label(frame, text="Username:", font=("Arial", 12))
username_label.grid(row=0, column=0, sticky="w", pady=8)
username_entry = ttk.Entry(frame, font=("Arial", 12), width=20)
username_entry.grid(row=0, column=1, pady=8)

# Password input
password_label = ttk.Label(frame, text="Password:", font=("Arial", 12))
password_label.grid(row=1, column=0, sticky="w", pady=8)
password_entry = ttk.Entry(frame, show="*", font=("Arial", 12), width=20)
password_entry.grid(row=1, column=1, pady=8)

# Toggle password visibility button
toggle_button = ttk.Button(frame, text="Show", command=toggle_password)
toggle_button.grid(row=1, column=2, padx=5)

# Login button
login_button = ttk.Button(frame, text="Login", command=check_login)
login_button.grid(row=2, columnspan=3, pady=15)

# Run the login window
login_window.mainloop()
