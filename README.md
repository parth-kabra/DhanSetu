# 📈 DhanSetu - Automated Stock Trading Bot  

DhanSetu is an automated stock trading bot that utilizes **Exponential Moving Average (EMA) crossover strategy** to identify potential buy opportunities in the **NSE (National Stock Exchange)**. It integrates with **Angel One SmartAPI** to fetch real-time stock data, analyze trends, and place orders accordingly.

---

## 🚀 Features  

✅ **Real-time Stock Data**: Fetches 15-minute candle data from NSE.  
✅ **EMA Crossover Detection**: Implements **EMA(9) & EMA(20) strategy** for automated stock selection.  
✅ **Automated Order Placement**: Places buy orders when a valid crossover is detected.  
✅ **Login System**: Secured authentication for accessing the application.  
✅ **Graphical Interface**: User-friendly **Tkinter-based GUI** to monitor stocks in real time.  
✅ **Multi-threaded Execution**: Ensures smooth UI interaction while fetching stock data.  

---

## 📂 Project Structure  

```
DhanSetu/
│── api.py               # Handles API authentication, data fetching & order placement
│── constants.py         # Stores stock symbols, tokens, and user credentials
│── main.py              # GUI-based application for stock monitoring and trading
│── README.md            # Documentation
│── requirements.txt     # Dependencies for the project
```

---

## 🛠 Setup & Installation  

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/parth-kabra/DhanSetu.git
cd DhanSetu
```

### 2️⃣ Install Dependencies  
Ensure you have **Python 3.7+** installed. Install required packages:  
```bash
pip install -r requirements.txt
```

### 3️⃣ Configure API Keys & Credentials  
- **SmartAPI**: Replace `api_key`, `username`, and `password` in `api.py`.  
- **TOTP Token**: Obtain from Angel One and update in `api.py`.  
- **User Credentials**: Modify `USERS` dictionary in `constants.py` for login authentication.  

### 4️⃣ Run the Application  
```bash
python main.py
```

---

## 📊 Trading Strategy  

DhanSetu follows a **9-20 EMA crossover strategy**:  
- **Buy Signal**: When **EMA(9) crosses above EMA(20)** with an increasing trend.  
- **No Trade**: If crossover conditions are not met or stock is already bought.  

---

## 🖥 User Interface  

The GUI allows:  
- 📌 Selecting stock symbols from a dropdown menu  
- 📈 Viewing **real-time stock data** in a tabular format  
- 🔄 **Auto-refreshing** stock prices and EMA values  
- 🛒 Automatic **order execution** upon valid crossover detection  

---

## ⚠️ Disclaimer  

This project is **for educational purposes only** and does not provide financial advice. Trade at your own risk!  

---

## 🏆 Contributions  

Contributions are welcome! Feel free to fork the repository and submit a PR.  

---

## 📞 Support  

For issues & queries, open an **issue** on GitHub. 🚀  

---
🔗 **Happy Trading!** 🚀