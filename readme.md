# 🌍 Global Water Use Dashboard

An interactive dashboard for visualizing global water consumption trends by country, year, and sector. Built using Dash, Plotly, and pandas.
The dashboard was developed as part of a university course in data visualization.

## 📊 Overview

This dashboard provides an intuitive way to explore water use across countries from 2000 to 2024. Users can interactively filter by country and year to visualize:

- Total water consumption and rainfall
- Sector-based water use (agriculture, industry, household)
- Per capita consumption change
- Rainfall vs groundwater depletion
- Long-term consumption trends and scarcity levels

## 📸 Screenshot

![Dashboard Screenshot](screenshots/screenshot1.png)
![Dashboard Screenshot](screenshots/screenshot2.png)

## 🛠️ Built With

- [Dash](https://dash.plotly.com/)  
- [Plotly](https://plotly.com/python/)  
- [pandas](https://pandas.pydata.org/)  
- [dash-bootstrap-components](https://dash-bootstrap-components.opensource.faculty.ai/)

## 📂 Folder Structure

```
.
├── app.py                 # Main Dash app
├── requirements.txt       # Python dependencies
├── .gitignore             # Exclude temp & system files
├── README.md              # This file
├── data/
│   └── global_water.csv   # Cleaned dataset
├── screenshots/
│   └── screenshot1.png      # Full-page screenshot
    └── screenshot2.png      # Full-page screenshot
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/wiederstrom/water_consumption.git
cd water_consumption
```

### 2. (Optional) Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python app.py
```

Then open your browser and visit:  
`http://127.0.0.1:8050`

## 🌐 Deployment

This app can be deployed using [Railway](https://railway.app/).

### Deploy to Railway

1. Push your code to GitHub
2. Sign up for a free account at [Railway](https://railway.app/)
3. Click "New Project" → "Deploy from GitHub repo"
4. Select this repository
5. Railway will automatically detect the configuration and deploy
6. Your app will be live at a Railway-provided URL

The repository includes:
- `Procfile` - Defines the web process
- `railway.json` - Railway configuration
- `requirements.txt` - Python dependencies (including gunicorn)

Railway will automatically redeploy whenever you push to your main branch.

## 📊 Dataset

The app uses a pre-cleaned dataset containing:

- Country and Year
- Agricultural / Industrial / Household Water Use (%)
- Total Water Consumption (Billion m³)
- Rainfall and Groundwater Depletion metrics
- Per Capita Water Use
- Water Scarcity Level

## ✍️ Author

**Erik Lunde Wiederstrøm**  
Bachelor in Applied Data Science, 2025  
[LinkedIn](https://linkedin.com/in/wiederstrom)
