import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
import matplotlib.patheffects as pe

def create_16_9_system_architecture():
    # 16:9 exact aspect ratio: 16.0 inches by 9.0 inches at 240 DPI -> 3840 x 2160 pixels
    fig_w, fig_h = 16.0, 9.0
    fig = plt.figure(figsize=(fig_w, fig_h), dpi=240)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1600)
    ax.set_ylim(0, 900)
    ax.axis('off')

    # Color Palette - Professional Healthcare Intelligence Theme
    BG_COLOR = '#F8FAFC'           # Slate 50
    HEADER_BG = '#090E1F'          # Deep Navy Slate
    CARD_BG = '#FFFFFF'            # Pure White
    TEXT_MAIN = '#0F172A'          # Slate 900
    TEXT_MUTED = '#334155'         # Slate 700
    BORDER_LIGHT = '#E2E8F0'       # Slate 200
    
    TIER_COLORS = [
        {'primary': '#1D4ED8', 'tint': '#F0F7FF', 'badge': '#DBEAFE', 'text': '#1E40AF', 'sub_text': '#E0E7FF'}, # Tier 1 Navy
        {'primary': '#0D9488', 'tint': '#F0FDFA', 'badge': '#CCFBF1', 'text': '#115E59', 'sub_text': '#CCFBF1'}, # Tier 2 Teal
        {'primary': '#7C3AED', 'tint': '#F5F3FF', 'badge': '#EDE9FE', 'text': '#5B21B6', 'sub_text': '#EDE9FE'}, # Tier 3 Purple
        {'primary': '#059669', 'tint': '#ECFDF5', 'badge': '#D1FAE5', 'text': '#065F46', 'sub_text': '#D1FAE5'}, # Tier 4 Emerald
        {'primary': '#D97706', 'tint': '#FFFBEB', 'badge': '#FEF3C7', 'text': '#92400E', 'sub_text': '#FEF3C7'}, # Tier 5 Amber
        {'primary': '#E11D48', 'tint': '#FFF1F2', 'badge': '#FFE4E6', 'text': '#9F1239', 'sub_text': '#FFE4E6'}  # Tier 6 Rose
    ]

    # Background canvas
    ax.add_patch(Rectangle((0, 0), 1600, 900, facecolor=BG_COLOR, edgecolor='none', zorder=0))

    # Top Header Banner (Deep Navy)
    ax.add_patch(Rectangle((0, 810), 1600, 90, facecolor=HEADER_BG, edgecolor='none', zorder=1))
    
    # Top accent cyan glow bar
    ax.add_patch(Rectangle((0, 896), 1600, 4, facecolor='#06B6D4', edgecolor='none', zorder=2))

    # Title & Subtitle
    ax.text(35, 860, "MEDRADAR v2: SYSTEM ARCHITECTURE", 
            fontsize=17.5, fontweight='bold', color='#FFFFFF', family='sans-serif', zorder=3)
    ax.text(35, 832, "Multi-Tier Distributed Healthcare Intelligence, Real-Time POS Audit Telemetry & Geospatial Resource Allocation", 
            fontsize=10.2, color='#94A3B8', family='sans-serif', zorder=3)

    # Badges on Top Right
    badges = [
        ("ASPECT RATIO 16:9", "#38BDF8", "#0369A1"),
        ("KANCHIPURAM DISTRICT", "#34D399", "#065F46"),
        ("ENTERPRISE AI PIPELINE", "#C084FC", "#5B21B6"),
        ("4K UHD (3840 x 2160)", "#FBBF24", "#92400E")
    ]
    bx = 1565
    for text, text_col, border_col in reversed(badges):
        bw = len(text) * 6.5 + 16
        bx -= bw
        badge_box = FancyBboxPatch((bx, 840), bw, 22, boxstyle="round,pad=3,rounding_size=4",
                                   facecolor='#1E293B', edgecolor=border_col, linewidth=1.2, zorder=3)
        ax.add_patch(badge_box)
        ax.text(bx + bw/2, 851, text, fontsize=7.5, fontweight='bold', color=text_col, 
                ha='center', va='center', family='sans-serif', zorder=4)
        bx -= 8

    # Pipeline Workflow Stepper Ribbon (Y: 768 to 800)
    ax.add_patch(Rectangle((20, 768), 1560, 32, facecolor='#FFFFFF', edgecolor=BORDER_LIGHT, linewidth=1, zorder=1))
    ax.text(32, 784, "PIPELINE FLOW:", fontsize=8.0, fontweight='bold', color='#1E293B', va='center', family='sans-serif', zorder=3)
    
    pipeline_steps = [
        "1. POS Ingestion",
        "2. Cleansing & Denoising",
        "3. AI Regressor & Classifier",
        "4. Haversine SOS & Savings",
        "5. Dual-Failover DB",
        "6. Bilingual PWA & Triage"
    ]
    # Fixed slot spacing to guarantee no collisions
    ribbon_start = 140
    slot_width = (1560 - ribbon_start) / 6.0
    for i, step_text in enumerate(pipeline_steps):
        center_x = ribbon_start + i * slot_width + (slot_width / 2.0)
        ax.text(center_x, 784, step_text, fontsize=7.6, fontweight='bold', 
                color=TIER_COLORS[i]['primary'], ha='center', va='center', family='sans-serif', zorder=3)
        if i < 5:
            arr_pos = ribbon_start + (i + 1) * slot_width
            ax.text(arr_pos, 784, "➔", fontsize=8.5, fontweight='bold', color='#94A3B8', ha='center', va='center', family='sans-serif', zorder=3)

    # 6 Columns Layout
    col_w = 246
    gap_x = 14
    start_x = 25
    col_top = 750
    col_bottom = 66
    col_h = col_top - col_bottom # 684

    tier_data = [
        {
            "tier_num": "TIER 1",
            "tier_title": "DISTRIBUTED POS & TELEMETRY",
            "tier_sub": "Edge Ingestion & Shift Auditing",
            "cards": [
                {
                    "title": "Cloud POS Adapters",
                    "tag": "Non-Invasive Webhooks",
                    "items": [
                        "Marg ERP 9+ Enterprise Sync",
                        "ApolloLive Cloud Telemetry",
                        "MedPlus OmniPOS Connector",
                        "Custom Local Billing REST API"
                    ]
                },
                {
                    "title": "Cryptographic Shelf Audit",
                    "tag": "SHA-256 Tamper-Proof",
                    "items": [
                        "Dual-Shift Physical Ledger Verification",
                        "Pharmacist Identity Signature",
                        "Cryptographic Hash Chaining",
                        "Stale Stock & Fraud Mitigation"
                    ]
                },
                {
                    "title": "Regional Node Coverage",
                    "tag": "Kanchipuram District",
                    "items": [
                        "18 Geocoded Community Pharmacies",
                        "Bus Stand, Hospital Rd, Enathur",
                        "Real-time Dispense Decrements",
                        "Batch Expiry & Restock Inbound"
                    ]
                }
            ]
        },
        {
            "tier_num": "TIER 2",
            "tier_title": "SIGNAL PROCESSING & FEATURES",
            "tier_sub": "Data Cleansing & Synthesis",
            "cards": [
                {
                    "title": "Outlier Suppression",
                    "tag": "Robust Statistical Fences",
                    "items": [
                        "Dual IQR & MAD Screening",
                        "Clamping Dispense Reversals (≥ 0)",
                        "Null Date-Pharmacy Forward Impute",
                        "Extreme Spike Normalization"
                    ]
                },
                {
                    "title": "Signal Denoising Engine",
                    "tag": "Triple Algorithm Benchmark",
                    "items": [
                        "Savitzky-Golay Polynomial Filter",
                        "Exponential Weighted Moving Avg",
                        "Rolling Median (Window = 7d)",
                        "Noise Reduction Ratio: 71.4%"
                    ]
                },
                {
                    "title": "28-D Feature Matrix",
                    "tag": "Dynamic Feature Pipeline",
                    "items": [
                        "Temporal Lags: t-1, t-2, t-7, t-14",
                        "Rolling Velocity & Momentum",
                        "Cyclic Fourier Sine/Cosine Signals",
                        "Depletion Rate & Supplier Delay Ratios"
                    ]
                }
            ]
        },
        {
            "tier_num": "TIER 3",
            "tier_title": "AI / ML PREDICTIVE CORE",
            "tier_sub": "Forecasting & Calibration Engines",
            "cards": [
                {
                    "title": "Multi-Day Demand Regressor",
                    "tag": "R² = 0.8569 | MAE = 66.21",
                    "items": [
                        "HistGradientBoosting Regressor",
                        "Multi-Horizon: +1d, +3d, +7d, +14d, +30d",
                        "Benchmarked vs OLS, Ridge, Lasso, RF",
                        "Sub-Second Training & Inference"
                    ]
                },
                {
                    "title": "Calibrated Stockout Classifier",
                    "tag": "ROC-AUC: 1.000 | Brier: 0.0001",
                    "items": [
                        "Isotonic-Calibrated L2 Logistic",
                        "PR-AUC = 0.9941, Precision = 95.56%",
                        "Brier Reliability Loss: 0.0001",
                        "Eliminates Alarm Fatigue"
                    ]
                },
                {
                    "title": "Stress & Depletion Engine",
                    "tag": "Dynamic Simulation",
                    "items": [
                        "Forward-Looking Depletion Simulator",
                        "What-If Surge Sliders (+10% to +100%)",
                        "Supplier Delay Stress Testing",
                        "Multi-Echelon Buffer Health Score"
                    ]
                }
            ]
        },
        {
            "tier_num": "TIER 4",
            "tier_title": "SPATIAL & ECONOMIC ENGINE",
            "tier_sub": "Geospatial Triage & Affordability",
            "cards": [
                {
                    "title": "GIS Shortage Heatmap",
                    "tag": "Radial Heat Density",
                    "items": [
                        "Leaflet GIS Ward Shortage Clustering",
                        "Multi-Level Glowing Radial Heat Nodes",
                        "Critical Red (>35%), Elevated Orange",
                        "Cross-Ward Spillover Analysis"
                    ]
                },
                {
                    "title": "Emergency SOS Triage",
                    "tag": "Haversine Distance Routing",
                    "items": [
                        "Great-Circle Geodesic Distance Matrix",
                        "Verified 24x7 Casualty Pharmacy Filter",
                        "Cold-Storage Readiness Verification",
                        "1-Tap GPS Turn-by-Turn Navigation"
                    ]
                },
                {
                    "title": "Generic Jan Aushadhi (PMBJP)",
                    "tag": "73.1% Direct Cost Savings",
                    "items": [
                        "Bioequivalent Molecule Substitution",
                        "WHO-GMP & CDSCO Verified Formulations",
                        "Chronic Disease Savings Calculator",
                        "Kanchipuram PMBJP Kendra Routing"
                    ]
                }
            ]
        },
        {
            "tier_num": "TIER 5",
            "tier_title": "RESILIENT PERSISTENCE",
            "tier_sub": "High-Availability Dual-Engine",
            "cards": [
                {
                    "title": "Primary Enterprise DB",
                    "tag": "XAMPP MariaDB / MySQL",
                    "items": [
                        "Relational 3NF Normalized Schema",
                        "PyMySQL Threaded Connection Pools",
                        "ACID Transactional Guarantees",
                        "Port 3306 Dedicated Service"
                    ]
                },
                {
                    "title": "Embedded Failover DB",
                    "tag": "Local SQLite3 (Zero-Downtime)",
                    "items": [
                        "Mirrored Standalone `medradar.db`",
                        "Instantaneous Failover Trigger",
                        "Offline Disaster Resilience",
                        "Zero-Latency Interruption Recovery"
                    ]
                },
                {
                    "title": "Audit & Sync Management",
                    "tag": "Bidirectional State Sync",
                    "items": [
                        "Ledger Reconciliation Daemon",
                        "Tamper-Proof Audit Archive Table",
                        "Automated Database Seeding Scripts",
                        "175,360 Historical Ingestion Rows"
                    ]
                }
            ]
        },
        {
            "tier_num": "TIER 6",
            "tier_title": "PRESENTATION & CITIZEN PWA",
            "tier_sub": "Mobile-First Glassmorphism Client",
            "cards": [
                {
                    "title": "Progressive Web App (PWA)",
                    "tag": "Modern ES6+ UI",
                    "items": [
                        "Glassmorphism Responsive Dashboard",
                        "Pure Vector SVG Charts & Badges",
                        "Offline Service Worker Caching",
                        "Web Speech Voice Search Recognition"
                    ]
                },
                {
                    "title": "Bilingual Localization",
                    "tag": "Tamil & English Dual-Locale",
                    "items": [
                        "Full English & Tamil Toggle",
                        "Localized Medicine & Symptom Terms",
                        "Prescription Verification Stepper",
                        "Tamil Voice Query Translation"
                    ]
                },
                {
                    "title": "Triage, Alerts & Delivery",
                    "tag": "Multi-Channel Restock",
                    "items": [
                        "SMS, WhatsApp & In-App Notifications",
                        "15-Minute Priority Courier Dispatch",
                        "Doorstep UPI QR / Cash on Delivery",
                        "Direct Emergency 108 / 112 Speed Dials"
                    ]
                }
            ]
        }
    ]

    # Draw each Column / Tier
    for i, tier in enumerate(tier_data):
        cx = start_x + i * (col_w + gap_x)
        tc = TIER_COLORS[i]

        # Column background container
        col_box = FancyBboxPatch((cx, col_bottom), col_w, col_h, boxstyle="round,pad=0,rounding_size=8",
                                 facecolor=tc['tint'], edgecolor=tc['primary'], linewidth=1.5, zorder=2)
        ax.add_patch(col_box)

        # Tier Header Box
        header_h = 62
        hdr_box = FancyBboxPatch((cx, col_top - header_h), col_w, header_h, boxstyle="round,pad=0,rounding_size=8",
                                 facecolor=tc['primary'], edgecolor='none', zorder=3)
        ax.add_patch(hdr_box)
        ax.add_patch(Rectangle((cx, col_top - header_h), col_w, 10, facecolor=tc['primary'], edgecolor='none', zorder=3))

        # Two-line header for clean breathing room
        ax.text(cx + col_w/2, col_top - 16, tier['tier_num'], 
                fontsize=9.5, fontweight='bold', color='#FFFFFF', ha='center', va='center', family='sans-serif', zorder=4)
        ax.text(cx + col_w/2, col_top - 32, tier['tier_title'], 
                fontsize=7.3, fontweight='bold', color='#FFFFFF', ha='center', va='center', family='sans-serif', zorder=4)
        ax.text(cx + col_w/2, col_top - 48, tier['tier_sub'], 
                fontsize=6.8, color=tc['sub_text'], ha='center', va='center', family='sans-serif', zorder=4)

        # 3 Sub-Cards inside each Tier
        card_start_y = col_top - header_h - 12
        card_h = 188
        card_gap = 9
        card_w = col_w - 16
        card_x = cx + 8

        for c_idx, card in enumerate(tier['cards']):
            cy = card_start_y - (c_idx + 1) * card_h - c_idx * card_gap + card_gap

            # Sub-card background
            c_box = FancyBboxPatch((card_x, cy), card_w, card_h, boxstyle="round,pad=0,rounding_size=6",
                                   facecolor=CARD_BG, edgecolor=BORDER_LIGHT, linewidth=1.2, zorder=3)
            ax.add_patch(c_box)

            # Left accent pill line
            ax.add_patch(FancyBboxPatch((card_x, cy + 6), 3.5, card_h - 12, boxstyle="round,pad=0,rounding_size=2",
                                       facecolor=tc['primary'], edgecolor='none', zorder=4))

            # Card Title
            ax.text(card_x + 12, cy + card_h - 16, card['title'], 
                    fontsize=8.5, fontweight='bold', color=TEXT_MAIN, va='center', family='sans-serif', zorder=4)

            # Card Tag / Badge
            tag_box = FancyBboxPatch((card_x + 12, cy + card_h - 36), card_w - 24, 16, boxstyle="round,pad=1,rounding_size=3",
                                     facecolor=tc['badge'], edgecolor='none', zorder=4)
            ax.add_patch(tag_box)
            ax.text(card_x + card_w/2, cy + card_h - 28, card['tag'], 
                    fontsize=6.8, fontweight='bold', color=tc['text'], ha='center', va='center', family='sans-serif', zorder=5)

            # Bullet items
            bullet_y = cy + card_h - 52
            for item in card['items']:
                # Bullet icon dot
                ax.plot(card_x + 15, bullet_y, marker='o', markersize=3, color=tc['primary'], zorder=4)
                # Bullet text
                ax.text(card_x + 23, bullet_y, item, 
                        fontsize=7.0, color=TEXT_MUTED, va='center', family='sans-serif', zorder=4)
                bullet_y -= 18.5

        # Refined inter-column flow indicator badges
        if i < 5:
            arr_x = cx + col_w + 1
            for arr_y in [col_top - header_h - 95, col_top - header_h - 295, col_top - header_h - 495]:
                ax.add_patch(Circle((arr_x + gap_x/2, arr_y), 5.5, facecolor='#FFFFFF', edgecolor=BORDER_LIGHT, linewidth=1, zorder=5))
                ax.text(arr_x + gap_x/2, arr_y, "➔", fontsize=7.5, fontweight='bold', color=tc['primary'], 
                        ha='center', va='center', zorder=6)

    # Bottom Technical Summary & Performance Ledger (Footer bar)
    ax.add_patch(Rectangle((0, 0), 1600, 56, facecolor=HEADER_BG, edgecolor='none', zorder=1))
    ax.add_patch(Rectangle((0, 54), 1600, 2, facecolor='#334155', edgecolor='none', zorder=2))

    footer_cards = [
        {"slot_x": 30,  "label": "DEMAND REGRESSOR", "val": "HistGradientBoosting", "detail": "R² = 0.8569 | MAE = 66.21 | RMSE = 104.10", "color": "#38BDF8"},
        {"slot_x": 425, "label": "STOCKOUT CLASSIFIER", "val": "Isotonic L2 Logistic", "detail": "ROC-AUC = 1.000 | PR-AUC = 0.9941 | Brier = 0.0001", "color": "#34D399"},
        {"slot_x": 820, "label": "DISTRICT TELEMETRY", "val": "18 Regional Pharmacies", "detail": "175,360 Transactions | SHA-256 Audit Chaining", "color": "#FBBF24"},
        {"slot_x": 1215, "label": "PERSISTENCE & SOS", "val": "MariaDB ➔ SQLite3", "detail": "Zero-Latency Failover | Haversine Geodesic Routing", "color": "#F472B6"}
    ]
    
    for fc in footer_cards:
        fx = fc['slot_x']
        # Line 1: Label in gray, Value in bright color
        ax.text(fx, 38, fc['label'], fontsize=7.0, fontweight='bold', color='#94A3B8', family='sans-serif', zorder=3)
        ax.text(fx, 24, fc['val'], fontsize=8.2, fontweight='bold', color=fc['color'], family='sans-serif', zorder=3)
        # Line 2: Technical detail in crisp light text
        ax.text(fx, 10, fc['detail'], fontsize=6.8, color='#CBD5E1', family='sans-serif', zorder=3)

    # Output paths
    out_dir_fig = os.path.join("Report", "figures")
    out_dir_asset = os.path.join("Report", "assets")
    os.makedirs(out_dir_fig, exist_ok=True)
    os.makedirs(out_dir_asset, exist_ok=True)

    # 1. 16:9 dedicated files
    p1 = os.path.join(out_dir_fig, "system_architecture_16_9.png")
    p2 = os.path.join(out_dir_asset, "system_architecture_16_9.png")
    p3 = os.path.join(out_dir_fig, "system_architecture_16_9.svg")
    p4 = os.path.join(out_dir_asset, "system_architecture_16_9.svg")
    
    # 2. Update existing figure_3_3 files with the clean 16:9 version
    p5 = os.path.join(out_dir_fig, "figure_3_3_system_architecture.png")
    p6 = os.path.join(out_dir_asset, "figure_3_3_system_architecture.png")

    fig.savefig(p1, dpi=240, facecolor=BG_COLOR, edgecolor='none')
    fig.savefig(p2, dpi=240, facecolor=BG_COLOR, edgecolor='none')
    fig.savefig(p3, format='svg', facecolor=BG_COLOR, edgecolor='none')
    fig.savefig(p4, format='svg', facecolor=BG_COLOR, edgecolor='none')
    fig.savefig(p5, dpi=240, facecolor=BG_COLOR, edgecolor='none')
    fig.savefig(p6, dpi=240, facecolor=BG_COLOR, edgecolor='none')

    plt.close(fig)
    print("SUCCESS: 16:9 System Architecture diagram successfully rendered and saved to all target directories!")

if __name__ == '__main__':
    create_16_9_system_architecture()
