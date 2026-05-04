# 🧠 DevNet Dashboard - Intelligent Monitoring System

## 📌 Description
DevNet Dashboard is a DevOps project that monitors system performance in real-time using:
- FastAPI backend
- Streamlit frontend
- Docker containerization
- External API integration (Weather)

---

## 🚀 Features
✔ CPU Usage Monitoring (psutil)  
✔ RAM Usage Monitoring  
✔ Disk Usage Monitoring  
✔ Weather API Integration  
✔ Real-time Dashboard  
✔ Dockerized Microservices Architecture  

---

## 🏗 Architecture

Frontend (Streamlit) → Backend (FastAPI) → System APIs + External APIs

---

## ⚙️ Tech Stack
- Python
- FastAPI
- Streamlit
- Docker
- psutil
- requests

---

## 🚀 Run Project

```bash
docker compose up --build

devnet-dashboard/
│
├── backend/              # API FastAPI
├── frontend/             # Dashboard Streamlit
├── docker/               # Dockerfiles
├── docker-compose.yml    # Orchestration
├── Jenkinsfile (option)  # CI/CD alternatif
├── .github/workflows/    # GitHub Actions CI/CD
└── README.md




## 🗣️ Présentation simple :

> “Ce projet est un système de monitoring intelligent développé avec une architecture microservices.”

> “Le backend FastAPI collecte les données système comme CPU, RAM et disque.”

> “Le frontend Streamlit affiche ces données en temps réel sous forme de dashboard.”

> “Le système est containerisé avec Docker pour assurer portabilité et déploiement rapide.”

> “Une API externe météo est intégrée pour simuler un système DevOps réel connecté.”