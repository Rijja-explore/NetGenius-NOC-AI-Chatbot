# 🚀 NetGenius-NOC-AI-Chatbot

NetGenius-NOC-AI-Chatbot is a web-based application that provides **real-time network status** and **system performance metrics**. It integrates with **Zabbix** for network monitoring and uses **FastAPI** as the backend, supporting **PDF report generation**, **AI chatbot integration**, and **CORS-enabled frontend communication**.

---

## 🌟 Features

- 🔄 **Real-Time Network Status** – Fetch and display live network metrics from Zabbix.
- 📊 **System Metrics** – Monitor CPU, memory, disk usage, and more via `psutil`.
- 📄 **PDF Reports** – Generate and download detailed PDF reports using `ReportLab`.
- 🤖 **NOC Chatbot** – AI-powered assistant for NOC-related queries and automation.
- 🌐 **CORS Support** – Seamlessly integrate with frontend apps through cross-origin access.
- 🌓 **Dark Mode** – Toggle between light and dark UI themes for a better experience.

---

## 🧰 Technologies Used

- **Backend**: FastAPI
- **Frontend**: HTML, CSS, JavaScript
- **PDF Generation**: ReportLab
- **System Metrics**: psutil
- **Network Monitoring**: Zabbix API
- **HTTP Requests**: requests

---

## ScreenShot 
---
![image](https://github.com/user-attachments/assets/241e229b-f5f2-41f6-a7fc-f41bc46ab121)
![image](https://github.com/user-attachments/assets/6ea15fc3-3645-4696-bca3-821a2742f486)
![image](https://github.com/user-attachments/assets/9e1f86f1-ac69-4234-8921-d357ac9fc92d)





## 📦 Installation Guide

### 🔁 Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/noc-ai-chatbot.git
cd noc-ai-chatbot 
```

📦 Step 2: Install Required Dependencies
Make sure you have Python 3.7+ installed. Then run:

```bash
pip install -r requirements.txt
```
🔧 Step 3: Configure Zabbix Connection
Open the file zabbix_connector.py and update it with your Zabbix server credentials:

```bash
ZABBIX_API_URL = "http://your_zabbix_server/api_jsonrpc.php"
ZABBIX_USER = "your_username"
ZABBIX_PASSWORD = "your_password"
```

### ▶️ Step 4: Run the Application
Start the FastAPI server using Uvicorn:

```bash
uvicorn main:app --reload
```
Once the server starts, open your browser and go to:

```bash
http://127.0.0.1:8000
```
You will see the API documentation powered by Swagger UI. You can also integrate this with your frontend application.

🧭 How to Use the Application
🤖 Chatbot Section
Navigate to the Chatbot tab in the frontend to interact with the AI assistant for help with network operations.

📡 Network Status
Visit the Network Status section to fetch real-time metrics from Zabbix like latency, packet loss, and bandwidth usage.

📄 Generate Report
Click on Generate Report to create a downloadable PDF of the current network and system status.

## **Contributing**

1. Fork the repository and create a new branch.
2. Make your changes and commit them.
3. Push to your fork and create a pull request.

## **License**

This project is licensed under the  **MIT License** .

⚙️ System Metrics
Access detailed server performance data such as CPU load, memory usage, and disk I/O in real time.




