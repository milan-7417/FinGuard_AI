# 🛡️ FinGuard AI

> **AI-Powered Financial Fraud Detection System using CNN + BiLSTM with Explainable AI**

FinGuard AI is an end-to-end deep learning application designed to detect fraudulent financial transactions in real time. The system combines a **CNN + BiLSTM neural network** with **Explainable AI (XAI)** to provide accurate predictions along with human-readable explanations and an interactive analytics dashboard.

---

## 🚀 Features

### 🔍 Fraud Detection

* Real-time fraud prediction
* CNN + BiLSTM deep learning model
* Probability-based classification
* Configurable fraud threshold

### 🧠 Explainable AI

* Human-readable prediction explanations
* Risk-level assessment (Low, Medium, High)
* Fraud confidence score
* Fraud probability & Genuine probability

### 📊 Analytics Dashboard

* Manual transaction prediction
* Batch CSV prediction
* Fraud vs Genuine visualization
* Risk Distribution chart
* Interactive dashboard
* CSV report download

### 🌐 Modern Web Interface

* Professional landing page
* Responsive dashboard
* FastAPI backend
* Interactive charts using Chart.js

---

# 📸 Project Preview

## Landing Page

![alt text](screenshots/Screenshot%20(217).png)

![alt text](screenshots/Screenshot%20(218).png)

## Dashboard

![alt text](screenshots/Screenshot%20(219)-1.png)

![alt text](screenshots/Screenshot%20(220).png)

## Prediction & Analytics Dashboard

![alt text](screenshots/Screenshot%20(221).png)

![alt text](screenshots/Screenshot%20(222).png)

---

# 🏗️ Project Architecture

```
                Transaction Data
                       │
                       ▼
               Data Preprocessing
                       │
                       ▼
            Feature Engineering
                       │
                       ▼
                CNN + BiLSTM Model
                       │
         ┌─────────────┴─────────────┐
         ▼                           ▼
 Fraud Probability             Genuine Probability
         │
         ▼
 Risk Assessment + Explainable AI
         │
         ▼
 Dashboard & Analytics
```

---

# 📂 Project Structure

```
FinGuard_AI/
│
├── app/
│   ├── model/
│   ├── services/
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── assets/
│   └── app.py
│
├── dataset/
├── screenshots/
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 🧠 Deep Learning Model

Architecture:

```
Input Layer
      │
      ▼
1D Convolution Layer
      │
      ▼
MaxPooling
      │
      ▼
Bidirectional LSTM
      │
      ▼
Dense Layer
      │
      ▼
Sigmoid Output
```

---

# 📈 Model Performance

| Metric   |        Score |
| -------- | -----------: |
| Accuracy |   **97.58%** |
| ROC-AUC  |   **99.59%** |
| Model    | CNN + BiLSTM |

---

# 📊 Dashboard Features

* Manual Prediction
* CSV Batch Prediction
* Fraud Probability
* Confidence Score
* Explainable AI
* Fraud vs Genuine Chart
* Risk Distribution Chart
* Download CSV Report

---

# 🛠️ Technology Stack

### Backend

* FastAPI
* Python

### Machine Learning

* TensorFlow / Keras
* Scikit-learn
* NumPy
* Pandas

### Frontend

* HTML5
* CSS3
* JavaScript
* Chart.js

### Deployment

* Render

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/milan-7417/FinGuard_AI.git
```

Move into the project

```bash
cd FinGuard_AI
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
uvicorn app.app:app --reload
```

Open your browser

```
http://127.0.0.1:8000
```

---

# 📋 Input Features

| Feature                 |
| ----------------------- |
| Step                    |
| Transaction Type        |
| Amount                  |
| Old Origin Balance      |
| New Origin Balance      |
| Old Destination Balance |
| New Destination Balance |

---

# 📊 Output

The model returns:

* Fraud / Genuine Prediction
* Fraud Probability
* Genuine Probability
* Confidence Score
* Risk Level
* Explainable AI Reasons

---

# 🔮 Future Improvements

* PDF Report Generation
* Prediction History
* User Authentication
* Real-Time Streaming Detection
* REST API Integration
* Cloud Deployment
* Admin Dashboard

---

# 👨‍💻 Author

**Milan Kumar**

AI & Machine Learning Enthusiast


---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

It helps others discover the project and supports future improvements.
