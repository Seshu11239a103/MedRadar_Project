# MedRadar: Smart Medicine Availability Predictor
Run: `pip install -r requirements.txt` then `python app.py` and open http://127.0.0.1:5000
(first run trains the model in ~30 s; `python train.py` retrains).
All data is SIMULATED. Replace `simulate()` in medmodel.py with a loader returning the same arrays (days x pharmacies x medicines).

## Key Features in MedRadar v2 Kanchipuram

1. **Real-Time Medicine Stock Verification**:
   - Live physical shelf count synchronization with pharmacy cloud POS systems (Marg ERP, ApolloLive, MedPlus OmniPOS).
   - Real-time audit stamps (e.g., "Verified 6m ago by Pharmacist", exact shelf units available, batch numbers, and expiry dates).
   - Interactive on-site audit modal allowing pharmacists and customers to confirm in-stock items or report discrepancies live.

2. **Medicine Shortage Forecasting & Depletion Modeling**:
   - Multi-day forward-looking predictive trajectory (Today, +1d, +2d, +3d, +5d, +7d, +14d, +30d) based on consumption velocity, supplier lead times, and overdue delay factors.
   - Shortage Risk Index classification: Critical (<48h), High Risk (3-7d), Moderate Risk, and Stable Supply.
   - Interactive "What-If Supply Stress Simulator" with sensitivity sliders for demand surges and distributor delays.
   - Root cause analysis and pharmacy stockout countdown.

3. **Medicine Price Comparison & Generic Jan Aushadhi Savings**:
   - Direct side-by-side comparison between commercial branded formulations and Pradhan Mantri Bhartiya Janaushadhi Pariyojana (PMBJP) generic equivalents (50% to 85% cost savings).
   - Jan Aushadhi Kendra details at Kanchipuram Central (Near Moffusil Bus Stand) with CDSCO & WHO-GMP bioequivalence certification.
   - Interactive Chronic Disease Savings Calculator (e.g. annual savings for diabetes and hypertension patients).
   - Pharmacy Price Leaderboard ranking all regional pharmacies from lowest to highest discounted price.

4. **Geospatial Medicine Shortage Heatmap**:
   - Interactive GIS spatial heat map across Kanchipuram district and regional corridors (Temple City, Bus Stand, Enathur, Hospital Rd, Orikkai, Tollgate, Walajabad, Sriperumbudur, Chengalpattu, Chennai).
   - Glowing multi-level radial heat nodes (Critical Red >35%, Elevated Orange 22-35%, Moderate Yellow 12-22%, Normal Green <12%).
   - Interactive Zone Inspector displaying local pharmacy counts, depleted medicines, and nearest stocked alternative zone routing.
   - Filterable by citywide aggregate or specific medicine.

5. **Medicine Availability Notification System**:
   - Multi-channel restock subscription engine supporting SMS, WhatsApp, and In-App Push notifications.
   - Configurable trigger criteria (Back in Stock, Low Stock Warning, Price Drop).
   - Notification Center with active subscription management and delivered alerts feed.
   - Interactive 1-click "Simulate Restock Event" demo to test live distributor inbound scans and animated toast alerts.

6. **Emergency Medicine Finder & Rapid SOS Dispatch**:
   - High-visibility emergency mode with 1-click GPS nearest emergency pharmacy locator.
   - Symptom-based triage (Cardiac Angina/Chest Pain, Asthma Attack, Diabetic Crisis, Severe Colic, Dehydration).
   - Verified 24x7 casualty pharmacy indicators and cold-storage readiness.
   - 1-Tap Emergency Phone Calls, pre-formatted WhatsApp SOS messages, and turn-by-turn Google Maps GPS navigation.
   - 24x7 Government Helplines (108 Tamil Nadu Ambulance, 112 National Emergency, Kanchi HQ District Hospital).
   - Priority 15-minute emergency doorstep courier option.

7. **Pay on Delivery & Doorstep Settlement**:
   - Doorstep Delivery with Cash on Delivery (COD) or UPI on Delivery (Scan & Pay at doorstep).
   - Prescription verification, 4-stage delivery tracking stepper, and printable compliant pharmacy tax invoice.

8. **Bilingual Localization (தமிழ் / English)**:
   - Full bilingual interface tailored for Kanchipuram and extended Tamil Nadu region.

## Recommendations for enhancement
1. Connect real data: pharmacy POS/inventory exports, distributor feeds, or a crowd "confirm stock" button.
2. Live map tiles (Leaflet / Mapbox) with live animated rider GPS navigation.
3. Weekly drift monitoring + scheduled retraining; log predictions vs outcomes.
4. SMS/WhatsApp alerts when a watched medicine returns to stock (chronic patients, insulin).
5. Move from Flask dev server to gunicorn + Docker; add CI/CD tests.
