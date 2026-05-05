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

“Ce projet est un système de monitoring intelligent basé sur une architecture microservices.”

“Le backend FastAPI collecte les données système comme CPU, RAM et disque ainsi que la météo via une API externe.”

“Le frontend Streamlit affiche ces données sous forme de dashboard interactif avec recherche, filtrage et pagination.”

“L’application est conteneurisée avec Docker pour garantir portabilité et déploiement rapide.”

“Une pipeline CI/CD est intégrée pour automatiser le déploiement

Design Premium "Glassmorphism"