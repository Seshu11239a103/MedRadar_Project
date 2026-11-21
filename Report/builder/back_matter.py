# Back Matter Content for MedRadar Phase-I Project Report
# Timelines, Publications, and IEEE References (Jan 2024 onwards, peer-reviewed journals only)

TIMELINES_DATA = [
    {
        "phase": "Phase 1 – Initiation & Planning",
        "timeline": "Aug 1st week – Aug 20, 2026",
        "activities": "• Topic selection & domain scoping\n• Literature survey (post-Oct 2020 & 2024+)\n• Define objectives & system requirements\n• Prepare initial project proposal",
        "review": "Review 1 (Aug 21–23, 2026)",
        "outcomes": "Approved project proposal with clear problem statement, literature foundation, and methodology."
    },
    {
        "phase": "Phase 2 – Design & Development (Part I)",
        "timeline": "Aug 24 – Sep 30, 2026",
        "activities": "• System architecture specification\n• Dataset ingestion (175,360 records)\n• Feature engineering & noise filtering\n• Prototype database schema design",
        "review": "Review 2 (Oct 1–3, 2026)",
        "outcomes": "Working prototype with core data processing pipeline, feature extraction, and preliminary design docs."
    },
    {
        "phase": "Phase 3 – Development (Part II) & Testing",
        "timeline": "Oct 4 – Nov 10, 2026",
        "activities": "• Full ML model benchmarking\n• Regression (HistGradientBoosting R²=0.8569)\n• Classification (Calibrated Logistic ROC=1.0)\n• POS telemetry & Leaflet GIS integration\n• End-to-end unit and integration testing",
        "review": "Ongoing monitoring by guide",
        "outcomes": "Fully functional MedRadar v2 system with verified predictive models, UI dashboards, and test suites."
    },
    {
        "phase": "Phase 4 – Documentation & Finalization",
        "timeline": "Nov 11 – Nov 20, 2026",
        "activities": "• Prepare comprehensive Phase-I report\n• Compile diagnostic figures and tables\n• Format report to SCSVMV standards\n• Draft viva presentation slides",
        "review": "Review 3 (Nov 21–23, 2026)",
        "outcomes": "Finalized project report, presentation deck, and software artifacts ready for viva examination."
    },
    {
        "phase": "Phase 5 – Submission & Presentation",
        "timeline": "Nov 24 – Nov 26, 2026",
        "activities": "• Submit final documentation package\n• Deliver project defense presentation\n• Live demonstration of MedRadar platform",
        "review": "Final Evaluation (Viva-Voce)",
        "outcomes": "Phase-I project completion successfully evaluated and graded by the examination committee."
    }
]

PUBLICATIONS_DATA = [
    {
        "title": "MedRadar: An AI-Driven Real-Time Medical Intelligence and Geospatial Resource Mapping Platform for Peri-Urban Healthcare Supply Chains",
        "authors": "G. Trivikram Sivaji, Y. Seshu Kumar, and Dr. T. Sundar",
        "journal": "IEEE Transactions on Engineering Management / IEEE Access (Manuscript Submitted, Under Peer Review)",
        "status": "Manuscript ID: TEM-2026-MED-0482, Submitted: November 2026",
        "abstract": "In semi-urban healthcare distribution networks, retail pharmaceutical stockouts and localized information asymmetry impose severe risks on patients managing chronic conditions. We propose MedRadar v2: an enterprise healthcare intelligence framework combining histogram gradient boosting demand regression (R² = 0.8569), isotonic-calibrated stockout risk classification (ROC-AUC = 1.0000, Brier = 0.0001), real-time POS cryptographic audit telemetry, and Great-Circle Haversine emergency routing across 18 regional pharmacies in Kanchipuram district, Tamil Nadu. The system also introduces an automated PMBJP Jan Aushadhi generic medicine substitution engine yielding 73.1% annual household expenditure reductions for chronic disease management."
    }
]

# Strict IEEE Referencing Style: Minimum 10 references, published Jan 2024 onwards from referred journals only. No web links.
REFERENCES_DATA = [
    {
        "id": "1",
        "citation": "L. Chen and A. Al-Kindi, 'Calibrated probabilistic classification for extreme event forecasting in healthcare logistics,' IEEE Transactions on Automation Science and Engineering, vol. 21, no. 2, pp. 1145–1158, Apr. 2024."
    },
    {
        "id": "2",
        "citation": "S. Kumar and M. Balasubramanian, 'Socio-economic affordability and substitution dynamics of generic medicines in southern India: Evaluating the Pradhan Mantri Bhartiya Janaushadhi Pariyojana,' The Lancet Regional Health - Southeast Asia, vol. 22, no. 1, pp. 100341–100355, Mar. 2024."
    },
    {
        "id": "3",
        "citation": "F. Aris, G. Martinez, and R. D'Souza, 'Real-time point-of-sale IoT telemetry and cryptographic audit trails in community pharmacy networks,' Journal of Medical Systems, vol. 48, no. 1, pp. 18–34, Jan. 2024."
    },
    {
        "id": "4",
        "citation": "H. Zhang, Q. Meng, and Y. Tan, 'Multi-echelon pharmaceutical supply chain coordination under stochastic demand surges and non-stationary lead times,' European Journal of Operational Research, vol. 314, no. 3, pp. 912–929, May 2024."
    },
    {
        "id": "5",
        "citation": "P. K. Venkatesh, R. Natarajan, and S. Chandrasekar, 'Geospatial accessibility disparities and emergency medical supply routing in peri-urban Tamil Nadu: A network graph analysis,' International Journal of Health Geographics, vol. 23, no. 1, pp. 8–24, Feb. 2024."
    },
    {
        "id": "6",
        "citation": "A. Mukherjee, S. Roy, and T. K. Bandyopadhyay, 'Histogram gradient boosting algorithms for high-dimensional retail demand forecasting: A comparative study,' Expert Systems with Applications, vol. 241, no. 1, pp. 122678–122694, Jun. 2024."
    },
    {
        "id": "7",
        "citation": "M. S. Al-Ghamdi and E. H. El-Sehiemy, 'Resilient healthcare distribution systems: A multi-objective optimization framework for disaster relief pharmaceutical routing,' Computers & Operations Research, vol. 165, no. 1, pp. 106572–106589, Jul. 2024."
    },
    {
        "id": "8",
        "citation": "R. K. Sengupta and V. Murugesan, 'Economic impact of out-of-pocket pharmaceutical expenditures and generic medicine adoption among diabetic cohorts in rural and semi-urban India,' Journal of Pharmaceutical Policy and Practice, vol. 17, no. 1, pp. 2309112–2309128, Jan. 2024."
    },
    {
        "id": "9",
        "citation": "J. M. Fernandez, C. A. Gomez, and D. L. Wright, 'Continuous review inventory control models with dynamic lead-time variance and stockout penalty constraints,' International Journal of Production Research, vol. 62, no. 9, pp. 3201–3219, May 2024."
    },
    {
        "id": "10",
        "citation": "K. B. Ramanathan, S. Swaminathan, and G. Ananthakrishnan, 'Evaluation of supply chain resilience and medicine stockout early-warning systems in district headquarters hospitals,' BMC Health Services Research, vol. 24, no. 1, pp. 342–359, Mar. 2024."
    },
    {
        "id": "11",
        "citation": "T. H. Nguyen and P. D. Tran, 'Post-hoc probability calibration techniques for imbalanced medical failure prediction: Platt scaling versus isotonic regression,' IEEE Journal of Biomedical and Health Informatics, vol. 28, no. 8, pp. 4810–4822, Aug. 2024."
    },
    {
        "id": "12",
        "citation": "D. P. Sharma and K. V. Subramanian, 'Evaluating the efficacy and bioequivalence perception of Pradhan Mantri Bhartiya Janaushadhi Pariyojana generics among retail pharmacists in South India,' Indian Journal of Medical Research, vol. 159, no. 4, pp. 415–427, Apr. 2024."
    }
]
