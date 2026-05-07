## 1 Missing file in data (raw)folder
Road data (OS Open Roads) is not included due to size.

Download from:
https://osdatahub.os.uk/downloads/open/OpenRoads

# 🚗 Intelligent Repairer Routing System

### AVIVA Case Study — Scalable Road-Network Based Repairer Selection

A scalable routing and optimisation system designed to improve insurance claim repairer allocation using real UK road network data.

This project replaces simplistic straight-line distance calculations with realistic road-network routing, enabling more accurate repairer recommendations and better operational efficiency.

---

## 📌 Project Overview

Insurance claim systems often assign repairers based on straight-line (“as-the-crow-flies”) distance. In reality, actual driving routes can significantly differ due to:

* road layouts
* motorways
* one-way systems
* geographic barriers
* traffic infrastructure

This project addresses that problem by building a routing engine using the **OS Open Roads dataset** and graph-based shortest-path algorithms.

---

## ✨ Key Features

✔ UK postcode-to-coordinate conversion
✔ Road network graph construction using OS Open Roads
✔ Repairer and postcode data cleaning pipeline
✔ Fast nearest-node lookup using KDTree
✔ Graph-ready architecture for Dijkstra / A* routing
✔ Modular and scalable system design
✔ Prepared for API integration and deployment

---

## 🏗️ System Architecture

```text
Raw Data
   ↓
Data Preparation Pipeline
   ↓
Road Network Graph
   ↓
Shortest Path Routing
   ↓
Repairer Recommendation API
```

---

## 🛠️ Technologies Used

* Python
* Pandas
* GeoPandas
* NetworkX
* SciPy KDTree
* Shapely
* OS Open Roads Dataset

---

## 📂 Project Structure

```text
AVIVA_PROJECT/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── src/
│   ├── data/
│   │   └── data_prep.py
│   │
│   └── utils/
│
├── scripts/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Data Pipeline

The preprocessing pipeline performs:

### 1. Data Cleaning

* removes invalid coordinates
* standardises postcode formatting
* removes duplicate records

### 2. Road Network Processing

* loads OS Open Roads shapefiles
* converts road segments into graph edges
* creates weighted network graph

### 3. Spatial Optimisation

* builds KDTree for fast nearest-node search
* snaps repairers to road network nodes

### 4. Persistence

Outputs reusable processed assets:

* cleaned datasets
* postcode lookup dictionary
* serialized road graph

---

## 🚀 Running the Project

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the data pipeline

```bash
python src/data/data_prep.py
```

---

## 📊 Scalability Considerations

The system was designed with scalability and maintainability in mind:

* preprocessing and runtime stages are separated
* expensive graph construction is cached
* modular architecture supports API deployment
* reusable graph persistence avoids repeated heavy computation

---

## 📍 Future Improvements

* A* shortest path optimisation
* Travel-time based routing
* Real-time traffic integration
* FastAPI deployment
* Cloud-hosted graph services
* Parallel graph processing

---

## 🧠 Engineering Focus

This project was built to demonstrate:

* spatial data engineering
* graph algorithms
* scalable system design
* data pipeline architecture
* real-world optimisation thinking

---

## 👨‍💻 Author

Developed as part of an AVIVA technical case study focused on intelligent repairer routing and operational optimisation.
