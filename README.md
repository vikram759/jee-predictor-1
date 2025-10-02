# JEE Admission Predictor Web Application

This project is a **predictive web application** that forecasts JEE admission outcomes based on cut-off ranks, integrating a **Next.js frontend** with a **Flask backend**.

---

## 📌 Project Overview
- Built a **predictive web app** combining Next.js (frontend) and Flask (backend) for real-time JEE admission predictions.
- Curated and pre-processed data from **120+ JoSAA colleges**, structured into a **CSV dataset**.
- Developed a **score-based model** to recommend the **top 5 colleges** based on user input.
- Built an **interactive front-end interface** for users to input rank and preferences and view predictions instantly.
- Achieved an **average API response time of 3–4 seconds**, optimizing performance and user experience.

---

## 📂 Dataset
- Data collected from **JoSAA 120+ colleges**.
- Pre-processed and structured into **CSV format** with columns such as:
  - College Name
  - Branch
  - Cut-off Rank
  - Category
  - Location

---

## ⚙️ Tech Stack
- **Frontend:** Next.js
- **Backend:** Flask
- **Data Processing:** Pandas, NumPy
- **Other Tools:** Axios / Fetch API for frontend-backend communication

---

## 🛠️ Features
- Input **JEE rank** and preferences.
- **Top 5 college predictions** displayed in real-time.
- Responsive and interactive UI.
- Fast API response time (~3–4 seconds).
- Score-based prediction model for accurate recommendations.

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/jee-admission-predictor.git
cd jee-admission-predictor

```
### 2. Backend Setup (Flask)
```bash
cd backend
pip install -r requirements.txt
python app.py
```
### 3. Frontend Setup(Next.js)
```bash
cd frontend
npm install
npm run dev
```
### 4.Open in Browser

Visit: **http://localhost:3000** to access the web application.

## 📊 Model & Prediction

-Score-based recommendation model:

-Takes rank and preferences as input.

-Outputs top 5 recommended colleges.

-Optimized for speed and accuracy.

## 📈 Performance

- Average API response: 3–4 seconds

- Real-time prediction updates for improved UX



