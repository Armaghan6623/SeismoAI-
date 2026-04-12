# SeismoAI-

SeismoAI – Seismic Data Processing Pipeline
📌 Overview

SeismoAI is a modular Python-based project designed to process, analyze, and interpret seismic data using machine learning. The system is built as a collaborative pipeline where each module performs a specific task, contributing to a complete AI-driven seismic analysis workflow.

This project works with real SEG-Y (.sgy) seismic data and covers everything from data loading to explainable AI.

🧠 Project Structure

The system is divided into 5 independent but connected modules:

seismoai/
│
├── seismoai_io/       # Load and preprocess SGY files
├── seismoai_viz/      # Visualization of seismic data
├── seismoai_qc/       # Quality control (noise & bad trace detection)
├── seismoai_model/    # Machine learning model
├── seismoai_xai/      # Explainable AI (SHAP analysis)


Author Muhammad Armaghan 
