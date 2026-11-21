# Front Matter Content for MedRadar Phase-I Project Report
# SCSVMV CSE Department Guidelines

FRONT_MATTER_DATA = {
    "project_title": "MEDRADAR: AI-DRIVEN REAL-TIME MEDICAL INTELLIGENCE AND GEOSPATIAL RESOURCE MAPPING PLATFORM",
    "course_code": "BCSF187Z50",
    "course_name": "PROJECT WORK PHASE – I",
    "degree": "B.E. (Computer Science and Engineering)",
    "batch": "Batch (2023-2027) (Semester VII)",
    "academic_year": "2026-2027",
    "submission_period": "Nov/Dec 2026",
    "students": [
        {"name": "G. TRIVIKRAM SIVAJI", "reg_no": "11239A029"},
        {"name": "Y. SESHU KUMAR", "reg_no": "11239A103"}
    ],
    "guide": {
        "name": "Dr. T. Sundar",
        "designation": "Assistant Professor",
        "department": "Department of Computer Science and Engineering"
    },
    "hod": {
        "name": "Dr. M. Senthil Kumar",
        "designation": "Head of the Department",
        "department": "Department of Computer Science and Engineering"
    },
    "institution": {
        "name": "SRI CHANDRASEKHARENDRA SARASWATHI VISWA MAHAVIDYALAYA",
        "short_name": "SCSVMV",
        "type": "(Deemed to be University u/s 3 of UGC Act 1956)",
        "address": "Enathur, Kanchipuram – 631 561, Tamil Nadu, India"
    },
    "abstract": (
        "In developing healthcare ecosystems across suburban and semi-urban Indian corridors, patient access to "
        "critical pharmaceutical supplies is severely undermined by fragmented retail inventory visibility, "
        "demand-forecasting blind spots, and catastrophic information asymmetry during acute medical crises. Patients "
        "managing chronic illnesses (e.g., insulin-dependent diabetes, cardiovascular dyslipidemia, bronchial asthma) "
        "frequently endure physical pharmacy hops, unregulated pricing markups, and delayed acute triage during stockout "
        "events. This project develops MedRadar: an AI-driven, real-time medical intelligence and geospatial "
        "resource mapping platform specifically architected for Kanchipuram district and its surrounding healthcare "
        "networks. MedRadar formulates a dual-stream computational architecture: (i) an empirical multi-day demand "
        "forecasting framework leveraging an enterprise-scale longitudinal pharmaceutical dataset (175,360 transactions "
        "spanning 2020–2025 across 10 critical molecules and 5 therapeutic categories) alongside auxiliary Anatomical "
        "Therapeutic Chemical (ATC) daily sales time series, benchmarked against Ordinary Least Squares (OLS), Ridge (L2), "
        "Lasso (L1), Random Forest, and Histogram Gradient Boosting Regression (LightGBM equivalent, attaining winning "
        "test R² = 0.8569, MAE = 66.216, RMSE = 104.096, and MAPE = 20.06%); and (ii) an Isotonic-Calibrated L2-regularized "
        "stockout risk classifier operating over rolling demand velocities, shelf inventory balances, and supplier delay "
        "coefficients, achieving ROC-AUC = 1.000, PR-AUC = 0.9941, precision = 95.56%, recall = 95.56%, and Brier score = 0.0001. "
        "At the operational tier, MedRadar integrates live Point-of-Sale (POS) telemetry across 18 regional pharmacies in "
        "Kanchipuram, featuring pharmacist cryptographic audit stamps, multi-channel restock push subscriptions, an "
        "interactive GIS radial shortage heatmap, a PMBJP Jan Aushadhi generic substitution engine delivering 50% to 85% "
        "direct household cost savings, and an emergency SOS triage protocol that computes Great-Circle Haversine geodesic "
        "travel matrices to dispatch 1-tap route navigation and 15-minute priority doorstep deliveries. The complete system "
        "is deployed with a dual MariaDB/SQLite backend and verified through comprehensive end-to-end test suites, "
        "establishing a scalable paradigm for regional healthcare supply chain resilience."
    ),
    "keywords": [
        "Artificial Intelligence",
        "Depletion Modeling",
        "Geospatial Resource Mapping",
        "Healthcare Supply Chain",
        "Machine Learning",
        "Point-of-Sale Synchronization"
    ]
}

TABLE_OF_CONTENTS_DATA = [
    {"level": 0, "num": "", "title": "BONAFIDE CERTIFICATE", "page": "II"},
    {"level": 0, "num": "", "title": "DECLARATION", "page": "III"},
    {"level": 0, "num": "", "title": "ABSTRACT", "page": "IV"},
    {"level": 0, "num": "", "title": "TABLE OF CONTENTS", "page": "V"},
    {"level": 0, "num": "", "title": "LIST OF TABLES", "page": "VII"},
    {"level": 0, "num": "", "title": "LIST OF FIGURES", "page": "VIII"},
    {"level": 0, "num": "", "title": "LIST OF ABBREVIATIONS", "page": "IX"},
    {"level": 1, "num": "1", "title": "INTRODUCTION", "page": "1"},
    {"level": 2, "num": "1.1", "title": "Problem Background & Real-World Motivation", "page": "1"},
    {"level": 2, "num": "1.2", "title": "Healthcare Vulnerabilities in Peri-Urban & Semi-Urban India", "page": "2"},
    {"level": 2, "num": "1.3", "title": "Regional Focus: Kanchipuram District Healthcare Geography", "page": "3"},
    {"level": 2, "num": "1.4", "title": "Objectives of the Project", "page": "4"},
    {"level": 2, "num": "1.5", "title": "Scope of the Project", "page": "4"},
    {"level": 2, "num": "1.6", "title": "About the Institution & Project Environment", "page": "5"},
    {"level": 2, "num": "1.7", "title": "Organization of the Report", "page": "5"},
    {"level": 1, "num": "2", "title": "LITERATURE SURVEY", "page": "6"},
    {"level": 2, "num": "2.1", "title": "Critical Review of Contemporary Literature (Post-Oct 2020 & 2024+)", "page": "6"},
    {"level": 2, "num": "2.2", "title": "Comparative Literature Matrix & Research Gap Analysis", "page": "9"},
    {"level": 2, "num": "2.3", "title": "Mathematical Problem Formulation", "page": "11"},
    {"level": 3, "num": "2.3.1", "title": "Inventory State Dynamics & Continuous Review Equations", "page": "11"},
    {"level": 3, "num": "2.3.2", "title": "Multi-Day Demand Forecasting Objective Function", "page": "12"},
    {"level": 3, "num": "2.3.3", "title": "Probabilistic Stockout Risk & Calibration Formulation", "page": "13"},
    {"level": 3, "num": "2.3.4", "title": "Geospatial Resource Allocation & Geodesic Routing Objective", "page": "14"},
    {"level": 1, "num": "3", "title": "SYSTEM ARCHITECTURE AND METHODOLOGY", "page": "15"},
    {"level": 2, "num": "3.1", "title": "High-Level System Architecture & Workflow Pipeline", "page": "15"},
    {"level": 2, "num": "3.2", "title": "Longitudinal Pharmaceutical Dataset Provenance & Ingestion Pipeline", "page": "18"},
    {"level": 2, "num": "3.3", "title": "Exploratory Data Diagnostics & Statistical Hypothesis Testing", "page": "20"},
    {"level": 3, "num": "3.3.1", "title": "Descriptive Statistics & Distributional Moments", "page": "20"},
    {"level": 3, "num": "3.3.2", "title": "Normality Verification & Distribution Testing", "page": "21"},
    {"level": 3, "num": "3.3.3", "title": "Hypothesis Testing: Category Variance & Pandemic Surge", "page": "22"},
    {"level": 3, "num": "3.3.4", "title": "Demographic Independence & Chi-Square Analysis", "page": "23"},
    {"level": 2, "num": "3.4", "title": "Signal Denoising, Outlier Filtering & Feature Engineering", "page": "24"},
    {"level": 3, "num": "3.4.1", "title": "Outlier Detection via IQR and MAD Fences", "page": "24"},
    {"level": 3, "num": "3.4.2", "title": "Signal Filtering: Savitzky-Golay vs EWMA vs Rolling Median", "page": "25"},
    {"level": 3, "num": "3.4.3", "title": "28 Engineered Temporal, Cyclical & Ratio Features", "page": "26"},
    {"level": 3, "num": "3.4.4", "title": "Multicollinearity Pruning & VIF Analysis", "page": "27"},
    {"level": 2, "num": "3.5", "title": "Multi-Day Demand Forecasting Framework (Regression Paradigms)", "page": "28"},
    {"level": 3, "num": "3.5.1", "title": "Ordinary Least Squares (OLS) Derivation", "page": "28"},
    {"level": 3, "num": "3.5.2", "title": "Ridge Regression (L2 Shrinkage)", "page": "29"},
    {"level": 3, "num": "3.5.3", "title": "Lasso Regression (L1 Sparsity)", "page": "30"},
    {"level": 3, "num": "3.5.4", "title": "Random Forest Ensemble Regressor", "page": "30"},
    {"level": 3, "num": "3.5.5", "title": "Histogram Gradient Boosting Regressor (LightGBM Equivalent)", "page": "31"},
    {"level": 2, "num": "3.6", "title": "Calibrated Stockout Risk & Forward Depletion Modeling", "page": "32"},
    {"level": 3, "num": "3.6.1", "title": "Binary Stockout Classification Formulation", "page": "32"},
    {"level": 3, "num": "3.6.2", "title": "Probability Calibration via Isotonic Regression (PAVA)", "page": "33"},
    {"level": 3, "num": "3.6.3", "title": "Multi-Horizon Forward Inventory Depletion Simulation", "page": "34"},
    {"level": 2, "num": "3.7", "title": "Geospatial Optimization & Emergency SOS Triage", "page": "35"},
    {"level": 3, "num": "3.7.1", "title": "Great-Circle Haversine Geodesic Distance Matrix", "page": "35"},
    {"level": 3, "num": "3.7.2", "title": "Spatial Clustering & Shortage Heat Density Mapping", "page": "36"},
    {"level": 3, "num": "3.7.3", "title": "Emergency SOS Triage Protocol & Doorstep Dispatch", "page": "36"},
    {"level": 2, "num": "3.8", "title": "Generic Medicine Economics & Jan Aushadhi Optimization", "page": "37"},
    {"level": 2, "num": "3.9", "title": "Multi-Tier Cloud POS Audit Architecture & Database Design", "page": "38"},
    {"level": 1, "num": "4", "title": "IMPLEMENTATION, RESULTS AND PERFORMANCE EVALUATION", "page": "39"},
    {"level": 2, "num": "4.1", "title": "System Implementation Stack & API Microservices", "page": "39"},
    {"level": 2, "num": "4.2", "title": "Machine Learning Regression Benchmark Results", "page": "41"},
    {"level": 3, "num": "4.2.1", "title": "Comparative Regression Metrics & Model Ranking", "page": "41"},
    {"level": 3, "num": "4.2.2", "title": "Relative Predictive Feature Weight Distribution (Gini Importance)", "page": "42"},
    {"level": 3, "num": "4.2.3", "title": "Residual Distribution, Q-Q Diagnostics & Autocorrelation", "page": "43"},
    {"level": 2, "num": "4.3", "title": "Classification Benchmarking, Calibration & ROC/PR Analysis", "page": "44"},
    {"level": 3, "num": "4.3.1", "title": "Calibrated Classifier Performance Benchmark", "page": "44"},
    {"level": 3, "num": "4.3.2", "title": "ROC and Precision-Recall Curve Characteristics", "page": "45"},
    {"level": 3, "num": "4.3.3", "title": "Reliability Diagrams & Brier Score Minimization", "page": "46"},
    {"level": 2, "num": "4.4", "title": "Geospatial Shortage Heatmap & Kanchipuram Regional Analysis", "page": "46"},
    {"level": 2, "num": "4.5", "title": "Economic Impact & Generic Jan Aushadhi Savings Results", "page": "47"},
    {"level": 2, "num": "4.6", "title": "Verification, Testing & System Validation", "page": "48"},
    {"level": 1, "num": "5", "title": "CONCLUSION AND FUTURE SCOPE", "page": "49"},
    {"level": 2, "num": "5.1", "title": "Project Summary & Synthesis of Contributions", "page": "49"},
    {"level": 2, "num": "5.2", "title": "Public Health & Societal Impact", "page": "50"},
    {"level": 2, "num": "5.3", "title": "Limitations of Current Work (Phase-I)", "page": "51"},
    {"level": 2, "num": "5.4", "title": "Future Work & Phase-II Roadmap", "page": "51"},
    {"level": 0, "num": "", "title": "PROJECT TIMELINES & REVIEW MILESTONES", "page": "53"},
    {"level": 0, "num": "", "title": "PUBLICATION DETAILS & MANUSCRIPTS", "page": "54"},
    {"level": 0, "num": "", "title": "REFERENCES", "page": "55"}
]

LIST_OF_TABLES_DATA = [
    {"num": "Table 2.1", "title": "Comparative Literature Matrix & Methodological Gap Analysis", "page": "10"},
    {"num": "Table 3.1", "title": "Longitudinal Dataset Schema & Data Dictionary (175,360 Records)", "page": "19"},
    {"num": "Table 3.2", "title": "Comprehensive Descriptive Statistics of Core Telemetry Variables", "page": "20"},
    {"num": "Table 3.3", "title": "Denoising Filter Performance Benchmark (Savitzky-Golay vs EWMA vs Median)", "page": "25"},
    {"num": "Table 3.4", "title": "Taxonomy of 28 Engineered Predictive Features Across Five Modalities", "page": "26"},
    {"num": "Table 3.5", "title": "Geographic Coordinates and Operational Attributes of 18 Kanchipuram Pharmacies", "page": "35"},
    {"num": "Table 3.6", "title": "Commercial Branded vs PMBJP Jan Aushadhi Generic Pricing & Savings", "page": "37"},
    {"num": "Table 3.7", "title": "MedRadar Relational Database Entity Specifications & Primary Keys", "page": "38"},
    {"num": "Table 4.1", "title": "Core REST API Microservices, HTTP Methods, and Payload Specifications", "page": "40"},
    {"num": "Table 4.2", "title": "Comparative Regression Model Benchmark Across 5 Architectures", "page": "41"},
    {"num": "Table 4.3", "title": "Classification Model Benchmark & Probability Calibration Diagnostics", "page": "44"},
    {"num": "Table 4.4", "title": "Regional Shortage Severity Distribution Across Five Kanchipuram Spatial Wards", "page": "47"},
    {"num": "Table 4.5", "title": "Annual Treatment Basket Cost Comparison for Chronic Illness Patients", "page": "47"},
    {"num": "Table 4.6", "title": "Comprehensive Verification & Integration Test Suite Execution Results", "page": "48"},
    {"num": "Table 5.1", "title": "Phase-II Engineering Roadmap & Technical Deliverables", "page": "52"}
]

LIST_OF_FIGURES_DATA = [
    {"num": "Figure 3.1", "title": "MedRadar v2 Multi-Tier Distributed Healthcare Intelligence Architecture", "page": "16"},
    {"num": "Figure 3.2", "title": "Time-Series Signal Smoothing & Noise Filtering Comparison", "page": "24"},
    {"num": "Figure 3.3", "title": "Pearson Correlation Heatmap & Feature Multicollinearity Matrix", "page": "26"},
    {"num": "Figure 3.4", "title": "Emergency SOS Triage & Rapid Doorstep Dispatch Workflow", "page": "35"},
    {"num": "Figure 3.5", "title": "PMBJP Jan Aushadhi Generic Medicine Optimization Engine", "page": "36"},
    {"num": "Figure 3.6", "title": "MedRadar v2 Relational Database Schema & Entity Relationships", "page": "37"},
    {"num": "Figure 4.1", "title": "Cryptographic Point-of-Sale (POS) Audit Telemetry Verification Workflow", "page": "40"},
    {"num": "Figure 4.2", "title": "Relative Predictive Feature Weight Distribution (Gini Importance)", "page": "42"},
    {"num": "Figure 4.3", "title": "Regression Residual Distribution & Q-Q Diagnostics for Winning Regressor", "page": "43"},
    {"num": "Figure 4.4", "title": "Receiver Operating Characteristic (ROC) & Precision-Recall (PR) Curves", "page": "45"},
    {"num": "Figure 4.5", "title": "MedRadar Geospatial Medicine Shortage Heatmap: Kanchipuram Regional Network", "page": "46"}
]

LIST_OF_ABBREVIATIONS_DATA = [
    {"abbrev": "ANOVA", "meaning": "Analysis of Variance"},
    {"abbrev": "API", "meaning": "Application Programming Interface"},
    {"abbrev": "ATC", "meaning": "Anatomical Therapeutic Chemical Classification System"},
    {"abbrev": "AUC", "meaning": "Area Under the Curve"},
    {"abbrev": "BP", "meaning": "Blood Pressure"},
    {"abbrev": "CDSCO", "meaning": "Central Drugs Standard Control Organisation (India)"},
    {"abbrev": "CI/CD", "meaning": "Continuous Integration / Continuous Deployment"},
    {"abbrev": "COD", "meaning": "Cash on Delivery"},
    {"abbrev": "CSV", "meaning": "Comma-Separated Values"},
    {"abbrev": "ERP", "meaning": "Enterprise Resource Planning"},
    {"abbrev": "EWMA", "meaning": "Exponentially Weighted Moving Average"},
    {"abbrev": "GIS", "meaning": "Geographic Information System"},
    {"abbrev": "GPS", "meaning": "Global Positioning System"},
    {"abbrev": "HGBR", "meaning": "Histogram Gradient Boosting Regressor"},
    {"abbrev": "IQR", "meaning": "Interquartile Range"},
    {"abbrev": "JSON", "meaning": "JavaScript Object Notation"},
    {"abbrev": "L1 / L2", "meaning": "Lasso (L1) / Ridge (L2) Regularization Norms"},
    {"abbrev": "MAD", "meaning": "Median Absolute Deviation"},
    {"abbrev": "MAE", "meaning": "Mean Absolute Error"},
    {"abbrev": "MAPE", "meaning": "Mean Absolute Percentage Error"},
    {"abbrev": "ML", "meaning": "Machine Learning"},
    {"abbrev": "OLS", "meaning": "Ordinary Least Squares"},
    {"abbrev": "OTP", "meaning": "One-Time Password"},
    {"abbrev": "PAVA", "meaning": "Pool Adjacent Violators Algorithm"},
    {"abbrev": "PHC", "meaning": "Primary Health Centre"},
    {"abbrev": "PMBJP", "meaning": "Pradhan Mantri Bhartiya Janaushadhi Pariyojana"},
    {"abbrev": "POS", "meaning": "Point of Sale"},
    {"abbrev": "PR-AUC", "meaning": "Precision-Recall Area Under the Curve"},
    {"abbrev": "PWA", "meaning": "Progressive Web Application"},
    {"abbrev": "REST", "meaning": "Representational State Transfer"},
    {"abbrev": "RFID", "meaning": "Radio-Frequency Identification"},
    {"abbrev": "RMSE", "meaning": "Root Mean Squared Error"},
    {"abbrev": "ROC-AUC", "meaning": "Receiver Operating Characteristic Area Under the Curve"},
    {"abbrev": "ROP", "meaning": "Reorder Point"},
    {"abbrev": "SCSVMV", "meaning": "Sri Chandrasekharendra Saraswathi Viswa Mahavidyalaya"},
    {"abbrev": "SHA-256", "meaning": "Secure Hash Algorithm 256-bit"},
    {"abbrev": "SMS", "meaning": "Short Message Service"},
    {"abbrev": "SOS", "meaning": "Save Our Souls (Emergency Distress Signal)"},
    {"abbrev": "SQL", "meaning": "Structured Query Language"},
    {"abbrev": "SQLite", "meaning": "Structured Query Language Lite Embedded Engine"},
    {"abbrev": "SS", "meaning": "Safety Stock"},
    {"abbrev": "TNMSC", "meaning": "Tamil Nadu Medical Services Corporation"},
    {"abbrev": "UI", "meaning": "User Interface"},
    {"abbrev": "UPI", "meaning": "Unified Payments Interface"},
    {"abbrev": "VIF", "meaning": "Variance Inflation Factor"},
    {"abbrev": "WGS-84", "meaning": "World Geodetic System 1984"},
    {"abbrev": "WHO-GMP", "meaning": "World Health Organization Good Manufacturing Practices"}
]
