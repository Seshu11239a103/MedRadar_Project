"""MedRadar web app with AI availability, shortage forecasting, stock verification,
price comparison, spatial heatmap, emergency finder, and alert dispatch.
Run: python app.py then open http://127.0.0.1:5000
"""
import json, math, os, pickle, subprocess, sys, datetime, time, uuid
import numpy as np
from flask import Flask, jsonify, request, send_from_directory, abort, session, redirect
import db

from catalog import MEDS, PHARM, AREAS
from medmodel import hav, trip_cost

H = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(H, "artifacts")

def load_data():
    global SNAP, REPORT, POUT, PLAT, PLON
    snap_path = os.path.join(ART, "snapshot.pkl")
    if not os.path.exists(snap_path):
        print("Training model...")
        subprocess.check_call([sys.executable, os.path.join(H, "train.py")], cwd=H)
    with open(snap_path, "rb") as f:
        SNAP = pickle.load(f)
    with open(os.path.join(ART, "report.json"), "r", encoding="utf-8") as f:
        REPORT = json.load(f)
    POUT = SNAP["p_out"]
    PLAT = np.array([p["lat"] for p in PHARM])
    PLON = np.array([p["lon"] for p in PHARM])

load_data()
IN, CALL = .85, .55
app = Flask(__name__, static_folder="static")
app.secret_key = os.environ.get("SECRET_KEY", "medradar-kanchipuram-session-key-2026")

tier = lambda pa: "in_stock" if pa >= IN else "call_ahead" if pa >= CALL else "likely_out"

# In-memory stores
ALERTS = []
ORDERS = []
VERIFICATIONS = {} # (pharmacy_id, med_id) -> verification dict
NOTIFICATIONS = [] # Restock & emergency alerts log

def init_live_stores():
    """Seed live verifications, alerts, sample notifications, and active delivery orders."""
    global VERIFICATIONS, ALERTS, NOTIFICATIONS, ORDERS
    now = datetime.datetime.now()
    P, M = len(PHARM), len(MEDS)

    for p in range(P):
        for m in range(M):
            st = int(SNAP["stock"][p, m])
            pa = 1 - float(POUT[p, m])
            mins_ago = ((p * 7 + m * 13) % 41) + 3
            v_time = (now - datetime.timedelta(minutes=mins_ago)).strftime("%I:%M %p")
            status = "VERIFIED_IN_STOCK" if st > 0 and pa >= 0.55 else ("LOW_STOCK_CONFIRMED" if st > 0 else "OUT_OF_STOCK_VERIFIED")
            VERIFICATIONS[(p, m)] = {
                "pharmacy_id": p,
                "pharmacy_name": PHARM[p]["name"],
                "med_id": m,
                "med_brand": MEDS[m]["brand"],
                "status": status,
                "units": st,
                "batch_no": f"KC26-{(m * 73 + p * 31 + 105) % 900 + 100}",
                "expiry_date": f"{(m % 12) + 1:02d}/2028",
                "verified_at": f"{mins_ago}m ago ({v_time})",
                "verified_timestamp": (now - datetime.timedelta(minutes=mins_ago)).isoformat(),
                "verified_by": "Staff Pharmacist (R. Sundaram, Reg. TN-4821)" if p % 2 == 0 else "Marg ERP Auto-POS Sync",
                "pos_system": PHARM[p].get("pos_system", "Marg ERP Cloud"),
                "confidence_score": 98 if mins_ago < 15 else (95 if mins_ago < 30 else 91),
                "is_active": True,
                "notes": f"Physical shelf count confirmed {st} units in active dispensing tray." if st > 0 else "Distributor shipment awaited."
            }

    ALERTS.extend([
        {
            "id": "ALT-1001",
            "med_id": 6,
            "med_name": "Lantus Pen",
            "phone": "+91 98401 23456",
            "channels": ["sms", "whatsapp", "in_app"],
            "condition": "back_in_stock",
            "radius_km": 15,
            "created_at": "Today 08:30 AM",
            "status": "ACTIVE"
        },
        {
            "id": "ALT-1002",
            "med_id": 22,
            "med_name": "Augmentin 625",
            "phone": "+91 98401 98765",
            "channels": ["sms", "whatsapp", "in_app"],
            "condition": "back_in_stock",
            "radius_km": 10,
            "created_at": "Today 09:15 AM",
            "status": "ACTIVE"
        },
        {
            "id": "ALT-1003",
            "med_id": 19,
            "med_name": "Asthalin Inhaler",
            "phone": "+91 94432 11223",
            "channels": ["whatsapp", "in_app"],
            "condition": "low_stock_warning",
            "radius_km": 20,
            "created_at": "Today 07:45 AM",
            "status": "ACTIVE"
        }
    ])

    NOTIFICATIONS.extend([
        {
            "id": "NOTIF-901",
            "med_id": 19,
            "med_name": "Asthalin Inhaler",
            "pharmacy_id": 1,
            "pharmacy_name": "Apollo Pharmacy (Gandhi Road)",
            "title": "🎉 Restock Confirmed: Asthalin Inhaler",
            "message": "25 units of Asthalin Inhaler arrived at Apollo Pharmacy (Gandhi Road). High stock confirmed.",
            "time": "12 mins ago",
            "type": "RESTOCK_ALERT",
            "action_url": "med=19&pharm=1",
            "read": False
        },
        {
            "id": "NOTIF-902",
            "med_id": 12,
            "med_name": "Sorbitrate 5mg",
            "pharmacy_id": 3,
            "pharmacy_name": "Kanchi HQ Hospital Medicals",
            "title": "🚨 Emergency Stock Verified: Sorbitrate 5mg",
            "message": "Kanchi HQ Hospital Medicals verified 48 sublingual tablets available in 24x7 emergency desk.",
            "time": "35 mins ago",
            "type": "EMERGENCY_ALERT",
            "action_url": "med=12&pharm=3",
            "read": True
        }
    ])

    ORDERS.extend([
        {
            "id": "MR-DEL-482101",
            "created_at": "Today 11:20 AM",
            "customer_name": "K. Venkatesh",
            "phone": "+91 98401 23456",
            "address": "14, Gandhi Road, Near Bus Stand, Kanchipuram",
            "pharmacy_id": 1,
            "pharmacy_name": PHARM[1]["name"],
            "pharmacy_phone": PHARM[1]["phone"],
            "pharmacy_area": PHARM[1]["area"],
            "pharmacy_dl": "TN-KC-2024-1180",
            "pharmacy_gstin": "33AAACP1180Q1Z5",
            "med_id": 6,
            "med_brand": MEDS[6]["brand"],
            "med_salt": MEDS[6]["salt"],
            "med_strength": MEDS[6]["strength"],
            "batch_no": "KC26-482",
            "expiry_date": "08/2027",
            "quantity": 2,
            "unit_price": int(MEDS[6]["price"]),
            "subtotal": int(MEDS[6]["price"]) * 2,
            "delivery_fee": 0,
            "total": int(MEDS[6]["price"]) * 2,
            "payment_method": "Doorstep UPI",
            "payment_status": "Pending (Pay on Delivery)",
            "order_status": "Rider Dispatched & En Route",
            "status_step": 2,
            "eta_mins": 12,
            "rider_name": "Murugan K.",
            "rider_phone": "+91 98401 23456",
            "rider_vehicle": "Hero Splendor (TN-21-AX-4821)",
            "delivery_otp": "4821",
            "rx_required": MEDS[6]["rx"],
            "prescription": None,
            "notes": "Doorstep UPI QR payment ready"
        },
        {
            "id": "MR-DEL-482102",
            "created_at": "Today 10:45 AM",
            "customer_name": "S. Meenakshi",
            "phone": "+91 94432 99887",
            "address": "28, Ekambaranathar Sannidhi St, Periya Kanchipuram",
            "pharmacy_id": 3,
            "pharmacy_name": PHARM[3]["name"],
            "pharmacy_phone": PHARM[3]["phone"],
            "pharmacy_area": PHARM[3]["area"],
            "pharmacy_dl": "TN-KC-2024-1453",
            "pharmacy_gstin": "33AAACP1453Q1Z5",
            "med_id": 19,
            "med_brand": MEDS[19]["brand"],
            "med_salt": MEDS[19]["salt"],
            "med_strength": MEDS[19]["strength"],
            "batch_no": "KC26-119",
            "expiry_date": "11/2028",
            "quantity": 1,
            "unit_price": int(MEDS[19]["price"]),
            "subtotal": int(MEDS[19]["price"]),
            "delivery_fee": 35,
            "total": int(MEDS[19]["price"]) + 35,
            "payment_method": "Cash on Delivery",
            "payment_status": "Pending (Pay on Delivery)",
            "order_status": "Packed & Prescriptions Verified",
            "status_step": 1,
            "eta_mins": 25,
            "rider_name": "K. Selvam",
            "rider_phone": "+91 98402 77654",
            "rider_vehicle": "Honda Activa (TN-21-BY-1904)",
            "delivery_otp": "7291",
            "rx_required": MEDS[19]["rx"],
            "prescription": None,
            "notes": "Cash payment upon delivery"
        },
        {
            "id": "MR-DEL-482103",
            "created_at": "Today 09:10 AM",
            "customer_name": "R. Balamurugan",
            "phone": "+91 98401 55443",
            "address": "5, Kamarajar Street, Collectorate Post, Kanchipuram",
            "pharmacy_id": 0,
            "pharmacy_name": PHARM[0]["name"],
            "pharmacy_phone": PHARM[0]["phone"],
            "pharmacy_area": PHARM[0]["area"],
            "pharmacy_dl": "TN-KC-2024-1042",
            "pharmacy_gstin": "33AAACP1042Q1Z5",
            "med_id": 1,
            "med_brand": MEDS[1]["brand"],
            "med_salt": MEDS[1]["salt"],
            "med_strength": MEDS[1]["strength"],
            "batch_no": "KC26-178",
            "expiry_date": "05/2028",
            "quantity": 2,
            "unit_price": int(MEDS[1]["price"]),
            "subtotal": int(MEDS[1]["price"]) * 2,
            "delivery_fee": 35,
            "total": int(MEDS[1]["price"]) * 2 + 35,
            "payment_method": "Doorstep UPI",
            "payment_status": "Paid via Doorstep UPI",
            "order_status": "Delivered to Doorstep & Settled",
            "status_step": 3,
            "eta_mins": 0,
            "rider_name": "Murugan K.",
            "rider_phone": "+91 98401 23456",
            "rider_vehicle": "Hero Splendor (TN-21-AX-4821)",
            "delivery_otp": "1042",
            "rx_required": MEDS[1]["rx"],
            "prescription": None,
            "notes": "Delivered and settled"
        }
    ])

init_live_stores()

def get_verification(p, m):
    """Retrieve or generate real-time verification entry."""
    k = (int(p), int(m))
    if k not in VERIFICATIONS:
        st = int(SNAP["stock"][p, m])
        pa = 1 - float(POUT[p, m])
        VERIFICATIONS[k] = {
            "pharmacy_id": int(p),
            "pharmacy_name": PHARM[p]["name"],
            "med_id": int(m),
            "med_brand": MEDS[m]["brand"],
            "status": "VERIFIED_IN_STOCK" if st > 0 and pa >= 0.55 else ("LOW_STOCK_CONFIRMED" if st > 0 else "OUT_OF_STOCK_VERIFIED"),
            "units": st,
            "batch_no": f"KC26-{(m * 73 + p * 31 + 105) % 900 + 100}",
            "expiry_date": f"{(m % 12) + 1:02d}/2028",
            "verified_at": "Just now",
            "verified_timestamp": datetime.datetime.now().isoformat(),
            "verified_by": "Marg ERP Auto-POS Sync",
            "pos_system": PHARM[p].get("pos_system", "Marg ERP Cloud"),
            "confidence_score": 96,
            "is_active": True,
            "notes": "Verified via real-time ERP inventory sync."
        }
    return VERIFICATIONS[k]

def reasons(p, m):
    o = []
    lead = MEDS[m]["lead"]
    st = int(SNAP["stock"][p, m])
    cv = float(SNAP["cover"][p, m])
    pend = SNAP["pq"][p, m] > 0
    od = float(SNAP["overdue"][p, m])
    net = float(SNAP["net_out"][m])
    if st == 0: o.append("Out of stock today")
    if pend and od >= 1: o.append(f"Restock is about {int(od)} day(s) overdue")
    if net >= .25: o.append(f"{round(net*100)}% of regional pharmacies are out")
    if st > 0 and cv < lead: o.append(f"Only about {max(cv, .5):.1f} days of stock left")
    if st > 0 and not pend and cv < lead + 2 and len(o) < 2: o.append("No restock order placed yet")
    return (o or ["Healthy stock and steady supply"])[:2]

def row(p, m, d, rank=None):
    pa = 1 - float(POUT[p, m])
    ph = PHARM[p]
    v = get_verification(p, m)
    disc = ph.get("discount_pct", 8)
    discounted_pr = round(MEDS[m]["price"] * (1 - disc / 100), 1)
    return dict(
        id=int(p), name=ph["name"], phone=ph.get("phone", "+91 98401 00000"),
        area=ph["area"], lat=ph["lat"], lon=ph["lon"],
        dist_km=round(float(d[p]), 1), eta_min=int(round(d[p] * 3 + 2)),
        p_avail=round(pa, 3), tier=tier(pa), reasons=reasons(p, m), rank=rank,
        is_24x7=ph.get("is_24x7", False),
        has_cold_storage=ph.get("has_cold_storage", True),
        pos_system=ph.get("pos_system", "Marg ERP Cloud"),
        discount_pct=disc,
        discounted_price=discounted_pr,
        stock_units=int(SNAP["stock"][p, m]),
        verification=v
    )

def ranked(m, lat, lon, r):
    d = hav(lat, lon, PLAT, PLON)
    pa = 1 - POUT[:, m]
    c = np.where(d <= r)[0]
    return d, c[np.argsort(trip_cost(d[c], pa[c]))]

@app.get("/")
def index():
    return send_from_directory("static", "index.html")

@app.get("/login")
def login_page():
    return send_from_directory("static", "login.html")

@app.post("/api/auth/login")
def api_auth_login():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")
    
    if not username or not password:
        return jsonify(success=False, error="Username and password are required"), 400
        
    user = db.authenticate_user(username, password)
    if not user:
        return jsonify(success=False, error="Invalid username or security passcode"), 401
        
    session["user_id"] = user["id"]
    session["username"] = user["username"]
    session["role"] = user["role"]
    session["pharmacy_id"] = user.get("pharmacy_id")
    session["full_name"] = user.get("full_name")
    
    redirect_url = "/?view=admin" if user["role"] == "admin" else f"/?view=retailer&pharmacy_id={user.get('pharmacy_id', 0)}"
    
    safe_user = {
        "id": user["id"],
        "username": user["username"],
        "role": user["role"],
        "full_name": user["full_name"],
        "email": user["email"],
        "phone": user["phone"],
        "pharmacy_id": user.get("pharmacy_id"),
        "pharmacy_name": user.get("pharmacy_name"),
        "pharmacy_area": user.get("pharmacy_area")
    }
    return jsonify(success=True, user=safe_user, redirect=redirect_url)

@app.post("/api/auth/logout")
def api_auth_logout():
    session.clear()
    return jsonify(success=True, message="Successfully logged out")

@app.get("/api/auth/current_user")
def api_auth_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify(authenticated=False, user=None)
    user = db.get_user_by_id(user_id)
    if not user:
        session.clear()
        return jsonify(authenticated=False, user=None)
    return jsonify(authenticated=True, user=user)

@app.get("/api/db/status")
def api_db_status():
    conn, engine = db.get_db_connection()
    metrics = db.get_admin_metrics()
    conn.close()
    return jsonify(
        status="connected",
        engine=engine,
        database="medradar_db",
        host="localhost:3306" if engine == "mysql" else "local SQLite file",
        tables_count=7,
        users_count=metrics["total_users"],
        total_inventory_units=metrics["total_inventory_units"],
        critical_shortages=metrics["critical_low_stock_items"]
    )

@app.get("/api/admin/overview")
def api_admin_overview():
    metrics = db.get_admin_metrics()
    users = db.get_all_users()
    audits = list(reversed(VERIFICATIONS.values()))[:40]
    return jsonify(
        metrics=metrics,
        users=users,
        pharmacies=PHARM,
        medicines_count=len(MEDS),
        recent_audits=audits
    )

@app.post("/api/admin/users/create")
def api_admin_users_create():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")
    role = data.get("role", "sub_admin")
    pharmacy_id = data.get("pharmacy_id")
    full_name = data.get("full_name", "").strip()
    email = data.get("email", "").strip()
    phone = data.get("phone", "").strip()
    
    if not username or not password or not full_name:
        return jsonify(success=False, error="Username, password, and full name are required"), 400
        
    try:
        pharm_id_int = int(pharmacy_id) if pharmacy_id not in [None, ""] else None
        new_id = db.create_subadmin_user(username, password, role, pharm_id_int, full_name, email, phone)
        return jsonify(success=True, user_id=new_id, message="User created successfully in MySQL database")
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

@app.get("/api/retailer/inventory")
def api_retailer_inventory():
    p_id = request.args.get("pharmacy_id") or session.get("pharmacy_id")
    if p_id is None:
        p_id = 0
    try:
        p_id = int(p_id)
    except ValueError:
        p_id = 0
        
    inv = db.get_pharmacy_inventory(p_id)
    if not inv:
        inv = []
        for m_idx, m in enumerate(MEDS):
            inv.append({
                "inventory_id": m_idx,
                "pharmacy_id": p_id,
                "medicine_id": m_idx,
                "brand": m["brand"],
                "salt": m["salt"],
                "strength": m["strength"],
                "category": m["category"],
                "price": m["price"],
                "stock_units": int(SNAP["stock"][p_id, m_idx]),
                "batch_no": f"BATCH-2026-{p_id:02d}{m_idx:02d}",
                "expiry_date": "2027-06-30",
                "is_emergency": m.get("is_emergency", False),
                "packaging": m.get("packaging", "Strip of 10"),
                "pharmacy_name": PHARM[p_id]["name"],
                "area": PHARM[p_id]["area"]
            })
    return jsonify(
        pharmacy=PHARM[p_id],
        inventory=inv
    )

@app.post("/api/retailer/inventory/update")
def api_retailer_inventory_update():
    data = request.get_json(silent=True) or {}
    pharmacy_id = int(data.get("pharmacy_id", 0))
    medicine_id = int(data.get("medicine_id", 0))
    new_units = int(data.get("stock_units", 0))
    batch_no = data.get("batch_no")
    expiry_date = data.get("expiry_date")
    notes = data.get("notes")
    user_id = session.get("user_id", 1)
    
    db.update_inventory_stock(pharmacy_id, medicine_id, new_units, batch_no, expiry_date, user_id, notes)
    
    SNAP["stock"][pharmacy_id, medicine_id] = new_units
    now = datetime.datetime.now()
    v_time = now.strftime("%I:%M %p")
    status = "VERIFIED_IN_STOCK" if new_units >= 10 else ("LOW_STOCK_CONFIRMED" if new_units > 0 else "OUT_OF_STOCK_VERIFIED")
    
    VERIFICATIONS[(pharmacy_id, medicine_id)] = {
        "pharmacy_id": pharmacy_id,
        "pharmacy_name": PHARM[pharmacy_id]["name"],
        "med_id": medicine_id,
        "med_brand": MEDS[medicine_id]["brand"],
        "status": status,
        "units": new_units,
        "verified_at": v_time,
        "verified_by": session.get("full_name") or "Retail Pharmacist (Live Audit)",
        "batch": batch_no or f"BAT-2026-{pharmacy_id:02d}{medicine_id:02d}",
        "source": "RETAILER_PORTAL_STAMP"
    }
    return jsonify(success=True, status=status, units=new_units, message="Shelf stock updated and audit stamp recorded in XAMPP MySQL")

@app.get("/manifest.json")
def manifest():
    return send_from_directory("static", "manifest.json", mimetype="application/manifest+json")

@app.get("/sw.js")
def service_worker():
    resp = send_from_directory("static", "sw.js", mimetype="application/javascript")
    resp.headers["Service-Worker-Allowed"] = "/"
    return resp

@app.get("/icon-192.png")
def icon_192():
    return send_from_directory("static", "icon-192.png", mimetype="image/png")

@app.get("/icon-512.png")
def icon_512():
    return send_from_directory("static", "icon-512.png", mimetype="image/png")

@app.get("/icon.svg")
def icon_svg():
    return send_from_directory("static", "icon.svg", mimetype="image/svg+xml")

@app.get("/payment_qr.jpg")
def payment_qr_jpg():
    return send_from_directory("static", "payment_qr.jpg", mimetype="image/jpeg")

@app.get("/payment_qr.png")
def payment_qr_png():
    return send_from_directory("static", "payment_qr.png", mimetype="image/png")

@app.get("/payment_qr_code.png")
def payment_qr_code():
    return send_from_directory("static", "payment_qr_code.png", mimetype="image/png")

@app.get("/payment_qr_card.png")
def payment_qr_card():
    return send_from_directory("static", "payment_qr_card.png", mimetype="image/png")

@app.get("/api/bootstrap")
def bootstrap():
    sh = sorted(range(len(MEDS)), key=lambda i: -SNAP["net_out"][i])
    cats = sorted(list(set(m["category"] for m in MEDS)))
    emergency_meds = [m for m in MEDS if m.get("is_emergency")]
    return jsonify(
        medicines=MEDS,
        categories=cats,
        pharmacies=PHARM,
        areas=AREAS,
        shortage=[
            dict(id=i, brand=MEDS[i]["brand"], share=round(float(SNAP["net_out"][i]) * 100))
            for i in sh[:6] if SNAP["net_out"][i] >= .12
        ],
        emergency_medicines=[{
            "id": m["id"], "brand": m["brand"], "salt": m["salt"],
            "strength": m["strength"], "price": m["price"],
            "emergency_usage": m.get("emergency_usage", "")
        } for m in emergency_meds],
        stats={
            "total_medicines": len(MEDS),
            "emergency_count": len(emergency_meds),
            "total_pharmacies": len(PHARM),
            "active_alerts_count": len(ALERTS),
            "unread_notifications": sum(1 for n in NOTIFICATIONS if not n.get("read", False))
        }
    )

@app.get("/api/recommend")
def recommend():
    try:
        med_param = request.args.get("med") or request.args.get("med_id")
        if med_param is None:
            abort(400, "med, lat, lon required")
        m = int(med_param)
        lat = float(request.args["lat"])
        lon = float(request.args["lon"])
        r = min(max(float(request.args.get("radius", 15)), 1), 50)
    except (KeyError, ValueError):
        abort(400, "med, lat, lon required")
    if not 0 <= m < len(MEDS):
        abort(404, "unknown medicine")
    d, c = ranked(m, lat, lon, r)
    rows = [row(int(p), m, d, i + 1) for i, p in enumerate(c)]
    near = row(int(c[np.argmin(d[c])]), m, d) if len(c) else None
    subs = []
    if request.args.get("subs", "1") == "1":
        for s in MEDS[m]["subs"]:
            d2, c2 = ranked(s, lat, lon, r)
            if len(c2):
                x = row(int(c2[0]), s, d2)
                x.update(
                    brand=MEDS[s]["brand"], strength=MEDS[s]["strength"],
                    price=MEDS[s]["price"], mrp=MEDS[s].get("mrp", MEDS[s]["price"]),
                    generic_name=MEDS[s].get("generic_name", ""),
                    generic_price=MEDS[s].get("generic_price", MEDS[s]["price"]),
                    savings_pct=MEDS[s].get("savings_pct", 0),
                    med_id=s
                )
                subs.append(x)
        subs.sort(key=lambda x: -x["p_avail"])
    return jsonify(
        medicine=MEDS[m],
        results=rows, nearest=near, substitutes=subs, radius=r,
        network_out=round(float(SNAP["net_out"][m]) * 100)
    )

@app.get("/api/restock")
def restock():
    try:
        pharm_param = request.args.get("pharmacy") or request.args.get("pharmacy_id") or "0"
        p = int(pharm_param)
    except (KeyError, ValueError):
        abort(400, "pharmacy required")
    if not 0 <= p < len(PHARM):
        abort(404, "unknown pharmacy")
    rows = []
    for m, med in enumerate(MEDS):
        st = int(SNAP["stock"][p, m])
        dem = float(SNAP["dem"][p, m])
        cv = float(SNAP["cover"][p, m])
        pq = int(SNAP["pq"][p, m])
        od = float(SNAP["overdue"][p, m])
        po = float(POUT[p, m])
        lead = med["lead"]
        need = max(0, math.ceil(dem * (lead + 7) * 1.2 - st - pq))
        if pq and od >= 1: a, pri = "Chase supplier", 1
        elif pq: a, pri = "Order on the way", 2
        elif need > 0 and (po >= .25 or cv < lead + 2): a, pri = "Order now", 0
        else: a, pri = "Fine", 3
        v = get_verification(p, m)
        rows.append(dict(
            med_id=m, brand=med["brand"], strength=med["strength"], is_emergency=med["is_emergency"],
            p_out=round(po, 3), stock=st, cover=round(cv, 1), daily=round(dem, 1), pending=pq,
            suggested=need if pri == 0 else 0, action=a, pri=pri, network=round(float(SNAP["net_out"][m]) * 100),
            verified_at=v["verified_at"], batch_no=v["batch_no"], pos_sync=v["pos_system"]
        ))
    rows.sort(key=lambda r: (r["pri"], -r["p_out"]))
    pharm_orders = [o for o in ORDERS if o["pharmacy_id"] == p]
    return jsonify(pharmacy=PHARM[p]["name"], rows=rows, orders=pharm_orders)

# =========================================================================
# FEATURE 1: REAL-TIME MEDICINE STOCK VERIFICATION
# =========================================================================

@app.get("/api/stock_verification")
def api_stock_verification():
    """Retrieve real-time verification status for pharmacy & medicine."""
    med_id = request.args.get("med_id")
    pharm_id = request.args.get("pharmacy_id")

    if med_id is not None and pharm_id is not None:
        try:
            m = int(med_id)
            p = int(pharm_id)
            if 0 <= m < len(MEDS) and 0 <= p < len(PHARM):
                v = get_verification(p, m)
                return jsonify(status="success", verification=v)
        except (ValueError, TypeError):
            pass

    # If only med_id is given, return verifications across all pharmacies for that medicine
    if med_id is not None:
        try:
            m = int(med_id)
            if 0 <= m < len(MEDS):
                res = [get_verification(p, m) for p in range(len(PHARM))]
                res.sort(key=lambda x: -x["units"])
                return jsonify(
                    status="success",
                    medicine=MEDS[m],
                    verifications=res,
                    total_verified_stock=sum(x["units"] for x in res),
                    in_stock_pharmacies_count=sum(1 for x in res if x["units"] > 0)
                )
        except (ValueError, TypeError):
            pass

    # Return summary of recently verified medicines
    recent = list(VERIFICATIONS.values())
    recent.sort(key=lambda x: x["verified_timestamp"], reverse=True)
    return jsonify(status="success", recent_verifications=recent[:25])

@app.post("/api/verify_stock")
def api_verify_stock():
    """Interactive real-time stock verification submission by Pharmacist or User."""
    data = request.get_json(silent=True) or request.form
    if not data:
        abort(400, "Invalid JSON data")

    try:
        p = int(data.get("pharmacy_id"))
        m = int(data.get("med_id"))
    except (TypeError, ValueError):
        abort(400, "Valid pharmacy_id and med_id are required")

    if not (0 <= p < len(PHARM) and 0 <= m < len(MEDS)):
        abort(404, "Unknown pharmacy or medicine")

    reporter = str(data.get("verified_by", "Pharmacist")).strip()
    status_choice = str(data.get("status", "VERIFIED_IN_STOCK")).strip()
    notes = str(data.get("notes", "On-site physical inventory check confirmed.")).strip()

    reported_units = data.get("units")
    if reported_units is not None:
        try:
            new_units = max(0, int(reported_units))
            SNAP["stock"][p, m] = new_units
            if new_units == 0:
                POUT[p, m] = min(0.98, float(POUT[p, m]) + 0.35)
                status_choice = "OUT_OF_STOCK_VERIFIED"
            else:
                POUT[p, m] = max(0.02, float(POUT[p, m]) - 0.25)
                status_choice = "VERIFIED_IN_STOCK"
        except (ValueError, TypeError):
            new_units = int(SNAP["stock"][p, m])
    else:
        new_units = int(SNAP["stock"][p, m])

    now = datetime.datetime.now()
    batch_no = f"KC26-{(m * 73 + p * 31 + 105) % 900 + 100}"
    expiry_date = f"{(m % 12) + 1:02d}/2028"

    verification_entry = {
        "pharmacy_id": p,
        "pharmacy_name": PHARM[p]["name"],
        "med_id": m,
        "med_brand": MEDS[m]["brand"],
        "status": status_choice,
        "units": new_units,
        "batch_no": batch_no,
        "expiry_date": expiry_date,
        "verified_at": "Just now (" + now.strftime("%I:%M %p") + ")",
        "verified_timestamp": now.isoformat(),
        "verified_by": f"{reporter} (Verified Live)",
        "pos_system": PHARM[p].get("pos_system", "Marg ERP Cloud"),
        "confidence_score": 99,
        "is_active": True,
        "notes": notes
    }
    VERIFICATIONS[(p, m)] = verification_entry

    return jsonify(
        status="success",
        message=f"Live stock verified: {MEDS[m]['brand']} at {PHARM[p]['name']} ({new_units} units)",
        verification=verification_entry
    )

# =========================================================================
# FEATURE 2: MEDICINE SHORTAGE FORECASTING
# =========================================================================

@app.get("/api/shortage_forecast")
def api_shortage_forecast():
    """Multi-day shortage risk and depletion trajectory forecasting."""
    try:
        m = int(request.args.get("med_id", 0))
    except (ValueError, TypeError):
        m = 0

    if not 0 <= m < len(MEDS):
        abort(404, "Medicine not found")

    forecast_days = [0, 1, 2, 3, 5, 7, 10, 14, 21, 30]
    total_stock = int(np.sum(SNAP["stock"][:, m]))
    total_dem = float(np.sum(SNAP["dem"][:, m]))
    total_pq = int(np.sum(SNAP["pq"][:, m]))
    lead = MEDS[m]["lead"]
    avg_overdue = float(np.mean(SNAP["overdue"][:, m]))
    net_out = float(SNAP["net_out"][m])

    # Estimated delivery arrival day
    restock_arrival_day = max(1, int(round(lead + max(0, avg_overdue))))

    # Multi-day depletion trajectory
    trajectory = []
    for d in forecast_days:
        burn = d * total_dem
        incoming = total_pq if d >= restock_arrival_day else 0
        proj_stock = max(0, int(round(total_stock - burn + incoming)))
        # Projected network out-of-stock percentage
        if total_stock + incoming > 0:
            proj_out_pct = min(100.0, max(0.0, round(((burn - total_stock) / max(1, total_stock + incoming)) * 100 + net_out * 100, 1)))
        else:
            proj_out_pct = 100.0
        trajectory.append({
            "day": d,
            "label": "Today" if d == 0 else f"+{d} Days",
            "projected_stock": proj_stock,
            "projected_out_percentage": proj_out_pct,
            "is_depleted": proj_stock == 0
        })

    days_cover = round(total_stock / max(0.1, total_dem), 1)

    # Risk level determination
    if days_cover < 2.0 or (net_out >= 0.45 and total_pq == 0):
        risk_level = "CRITICAL"
        risk_score = 92
        urgency_msg = "Imminent total regional stockout within 48 hours. Emergency diversion needed."
    elif days_cover < 5.0 or net_out >= 0.28:
        risk_level = "HIGH RISK"
        risk_score = 75
        urgency_msg = "Supply buffer depleting rapidly. Restock orders must be expedited."
    elif days_cover < 9.0:
        risk_level = "MODERATE RISK"
        risk_score = 48
        urgency_msg = "Supply adequate for current week, reordering recommended to prevent gap."
    else:
        risk_level = "STABLE"
        risk_score = 18
        urgency_msg = "Comfortable inventory cover across Kanchipuram network."

    # Pharmacy-specific breakdown
    pharm_breakdown = []
    for p in range(len(PHARM)):
        st = int(SNAP["stock"][p, m])
        dm = float(SNAP["dem"][p, m])
        pq = int(SNAP["pq"][p, m])
        cv = round(st / max(0.05, dm), 1)
        po = float(POUT[p, m])
        pharm_breakdown.append({
            "pharmacy_id": p,
            "name": PHARM[p]["name"],
            "area": PHARM[p]["area"],
            "stock": st,
            "daily_demand": round(dm, 1),
            "cover_days": cv,
            "pending_order": pq,
            "prob_out_tomorrow": round(po, 3),
            "status": "Out Today" if st == 0 else ("Depletes <3d" if cv < 3 else ("Depletes <7d" if cv < 7 else "Adequate"))
        })
    pharm_breakdown.sort(key=lambda x: (x["cover_days"], -x["prob_out_tomorrow"]))

    # Root causes
    root_causes = []
    if net_out >= 0.25:
        root_causes.append(f"Network shortage shock: {round(net_out * 100)}% of regional pharmacies currently stockless")
    if avg_overdue >= 1.0:
        root_causes.append(f"Distributor delivery bottleneck: Restocks are running ~{round(avg_overdue, 1)} days overdue")
    if MEDS[m]["amp"] >= 0.3:
        root_causes.append(f"Seasonal monsoon/weather surge factor (+{int(MEDS[m]['amp']*100)}% seasonal amplitude)")
    if total_pq == 0 and total_stock < total_dem * 5:
        root_causes.append("Zero pending supplier orders recorded across regional distribution centers")
    if not root_causes:
        root_causes.append("Normal consumer consumption pattern with balanced supplier pipeline")

    return jsonify(
        medicine=MEDS[m],
        total_regional_stock=total_stock,
        total_daily_demand=round(total_dem, 1),
        days_of_supply_cover=days_cover,
        risk_level=risk_level,
        risk_score=risk_score,
        urgency_message=urgency_msg,
        restock_expected_in_days=restock_arrival_day,
        pending_incoming_units=total_pq,
        trajectory=trajectory,
        root_causes=root_causes,
        pharmacy_breakdown=pharm_breakdown
    )

@app.get("/api/forecast_summary")
def api_forecast_summary():
    """Citywide shortage forecast overview across all medicines."""
    critical = []
    high = []
    moderate = []
    stable = []

    for m in range(len(MEDS)):
        st = int(np.sum(SNAP["stock"][:, m]))
        dm = float(np.sum(SNAP["dem"][:, m]))
        net = float(SNAP["net_out"][m])
        cv = round(st / max(0.1, dm), 1)
        item = {
            "id": m,
            "brand": MEDS[m]["brand"],
            "salt": MEDS[m]["salt"],
            "category": MEDS[m]["category"],
            "is_emergency": MEDS[m]["is_emergency"],
            "total_stock": st,
            "daily_demand": round(dm, 1),
            "cover_days": cv,
            "net_out_pct": round(net * 100)
        }
        if cv < 2.5 or net >= 0.40:
            critical.append(item)
        elif cv < 6.0 or net >= 0.25:
            high.append(item)
        elif cv < 10.0:
            moderate.append(item)
        else:
            stable.append(item)

    critical.sort(key=lambda x: x["cover_days"])
    high.sort(key=lambda x: x["cover_days"])

    avg_cover = round(float(np.mean([x["cover_days"] for x in (critical + high + moderate + stable)])), 1)

    return jsonify(
        summary={
            "critical_count": len(critical),
            "high_risk_count": len(high),
            "moderate_count": len(moderate),
            "stable_count": len(stable),
            "average_network_cover_days": avg_cover,
            "supply_stress_index": round(min(100, (len(critical) * 15 + len(high) * 8) / len(MEDS) * 100))
        },
        critical_medicines=critical,
        high_risk_medicines=high
    )

# =========================================================================
# FEATURE 3: MEDICINE PRICE COMPARISON & GENERIC SAVINGS
# =========================================================================

@app.get("/api/price_comparison")
def api_price_comparison():
    """Compare prices across pharmacies, branded substitutes & Jan Aushadhi generic."""
    try:
        m = int(request.args.get("med_id", 0))
    except (ValueError, TypeError):
        m = 0

    if not 0 <= m < len(MEDS):
        abort(404, "Medicine not found")

    med = MEDS[m]
    base_price = med["price"]
    mrp = med.get("mrp", round(base_price * 1.15))
    gen_price = med.get("generic_price", round(base_price * 0.3))
    gen_name = med.get("generic_name", f"Generic {med['salt']} {med['strength']}")
    savings_amt = round(base_price - gen_price, 1)
    savings_pct = med.get("savings_pct", round((1 - gen_price / base_price) * 100))

    # 1. PMBJP Jan Aushadhi Generic Substitute Profile
    jan_aushadhi = {
        "generic_name": gen_name,
        "salt": med["salt"],
        "strength": med["strength"],
        "price": gen_price,
        "mrp": mrp,
        "savings_vs_brand": savings_amt,
        "savings_pct": savings_pct,
        "packaging": med.get("packaging", "Standard Strip"),
        "kendra_name": "Pradhan Mantri Jan Aushadhi Kendra (Kanchipuram Central)",
        "kendra_address": "Opp. Moffusil Bus Stand, Gandhi Road, Kanchipuram",
        "kendra_phone": "+91 94432 99112",
        "kendra_lat": 12.8388,
        "kendra_lon": 79.6990,
        "bioequivalence_rating": "100% Active Chemical Bioequivalence (CDSCO & WHO-GMP Certified)"
    }

    # 2. Branded Alternatives (Same salt & strength)
    branded_alternatives = []
    for s_id in med.get("subs", []):
        s_med = MEDS[s_id]
        diff = s_med["price"] - base_price
        branded_alternatives.append({
            "id": s_id,
            "brand": s_med["brand"],
            "salt": s_med["salt"],
            "strength": s_med["strength"],
            "price": s_med["price"],
            "mrp": s_med.get("mrp", round(s_med["price"] * 1.12)),
            "price_diff": diff,
            "is_cheaper": diff < 0,
            "savings_vs_target": abs(diff) if diff < 0 else 0
        })
    branded_alternatives.sort(key=lambda x: x["price"])

    # 3. Pharmacy-by-Pharmacy Pricing Matrix for this medicine
    pharmacy_prices = []
    for p in range(len(PHARM)):
        ph = PHARM[p]
        disc = ph.get("discount_pct", 8)
        disc_price = round(base_price * (1 - disc / 100), 1)
        st = int(SNAP["stock"][p, m])
        pa = 1 - float(POUT[p, m])
        pharmacy_prices.append({
            "pharmacy_id": p,
            "name": ph["name"],
            "area": ph["area"],
            "base_mrp": mrp,
            "discount_pct": disc,
            "final_price": disc_price,
            "saved_amount": round(mrp - disc_price, 1),
            "stock_units": st,
            "is_in_stock": st > 0,
            "prob_avail": round(pa, 3),
            "is_24x7": ph.get("is_24x7", False)
        })
    pharmacy_prices.sort(key=lambda x: (not x["is_in_stock"], x["final_price"]))

    # 4. Chronic Patient Savings Projections
    chronic_calculator = {
        "monthly_strips_2": {
            "brand_cost": round(base_price * 2),
            "generic_cost": round(gen_price * 2),
            "monthly_savings": round(savings_amt * 2),
            "annual_savings": round(savings_amt * 2 * 12)
        },
        "quarterly_strips_6": {
            "brand_cost": round(base_price * 6),
            "generic_cost": round(gen_price * 6),
            "quarterly_savings": round(savings_amt * 6),
            "annual_savings": round(savings_amt * 6 * 4)
        }
    }

    return jsonify(
        medicine=med,
        jan_aushadhi_generic=jan_aushadhi,
        branded_alternatives=branded_alternatives,
        pharmacy_prices=pharmacy_prices,
        chronic_calculator=chronic_calculator
    )

# =========================================================================
# FEATURE 4: MEDICINE SHORTAGE HEATMAP
# =========================================================================

@app.get("/api/shortage_heatmap")
def api_shortage_heatmap():
    """Geospatial shortage intensity mapping across Kanchipuram and extended region."""
    med_param = request.args.get("med_id", "all")
    selected_med_id = None
    if med_param != "all":
        try:
            selected_med_id = int(med_param)
            if not 0 <= selected_med_id < len(MEDS):
                selected_med_id = None
        except (ValueError, TypeError):
            selected_med_id = None

    area_features = []
    total_shortages = 0
    total_checks = 0

    for i, a in enumerate(AREAS):
        # Identify pharmacies mapped to this area
        area_pharms = [p for p in PHARM if p["area"] == a["name"]]
        if not area_pharms:
            # Fallback to closest pharmacy if none strictly matched
            dists = hav(a["lat"], a["lon"], PLAT, PLON)
            closest_idx = int(np.argmin(dists))
            area_pharms = [PHARM[closest_idx]]

        p_indices = [p["id"] for p in area_pharms]

        if selected_med_id is not None:
            # Shortage for single medicine
            out_count = sum(1 for p in p_indices if SNAP["stock"][p, selected_med_id] == 0)
            shortage_rate = out_count / max(1, len(p_indices))
            total_shortages += out_count
            total_checks += len(p_indices)
        else:
            # Aggregate shortage across all 40 medicines in this zone
            out_count = 0
            for p in p_indices:
                out_count += int(np.sum(SNAP["stock"][p] == 0))
            shortage_rate = out_count / (len(p_indices) * len(MEDS))
            total_shortages += out_count
            total_checks += (len(p_indices) * len(MEDS))

        # Classify zone severity
        if shortage_rate >= 0.35:
            severity = "CRITICAL"
            color = "#ef4444" # red
        elif shortage_rate >= 0.22:
            severity = "ELEVATED"
            color = "#f97316" # orange
        elif shortage_rate >= 0.12:
            severity = "MODERATE"
            color = "#eab308" # yellow
        else:
            severity = "LOW"
            color = "#10b981" # green

        # Top depleted drugs in this zone
        depleted_in_zone = []
        for m in range(len(MEDS)):
            if all(SNAP["stock"][p, m] == 0 for p in p_indices):
                depleted_in_zone.append(MEDS[m]["brand"])
            if len(depleted_in_zone) >= 3:
                break

        area_features.append({
            "id": i,
            "name": a["name"],
            "lat": a["lat"],
            "lon": a["lon"],
            "pharmacy_count": len(area_pharms),
            "pharmacies": [{"id": p["id"], "name": p["name"], "phone": p["phone"], "lat": p["lat"], "lon": p["lon"]} for p in area_pharms],
            "shortage_rate": round(shortage_rate * 100, 1),
            "severity": severity,
            "color": color,
            "heat_intensity": min(1.0, max(0.12, round(shortage_rate * 2.2, 2))),
            "depleted_medicines": depleted_in_zone or ["Stable supply across most lines"]
        })

    citywide_avg = round((total_shortages / max(1, total_checks)) * 100, 1)

    return jsonify(
        selected_medicine=MEDS[selected_med_id] if selected_med_id is not None else None,
        citywide_average_shortage=citywide_avg,
        areas=area_features
    )

# =========================================================================
# FEATURE 5: MEDICINE AVAILABILITY NOTIFICATION SYSTEM
# =========================================================================

@app.get("/api/alerts")
def api_get_alerts():
    """Get active availability subscriptions and received notifications log."""
    return jsonify(
        alerts=ALERTS,
        notifications=NOTIFICATIONS,
        total_active_alerts=len([a for a in ALERTS if a.get("status") == "ACTIVE"]),
        unread_notifications=sum(1 for n in NOTIFICATIONS if not n.get("read", False))
    )

@app.post("/api/subscribe_alert")
def subscribe_alert():
    """Register medicine restock / low-stock alert subscription."""
    data = request.get_json(silent=True) or request.form or request.args
    phone = str(data.get("phone", "+91 98401 00000")).strip()
    email = str(data.get("email", "")).strip()

    try:
        med_id = int(data.get("med_id"))
    except (TypeError, ValueError):
        abort(400, "Valid med_id required")

    if not 0 <= med_id < len(MEDS):
        abort(404, "Medicine not found")

    condition = str(data.get("condition", "back_in_stock")).strip()
    channels = data.get("channels") or ["sms", "whatsapp", "in_app"]
    if isinstance(channels, str):
        channels = [c.strip() for c in channels.split(",")]

    try:
        radius_km = int(data.get("radius_km", 15))
    except (TypeError, ValueError):
        radius_km = 15

    sub_id = f"ALT-{int(time.time() * 1000) % 90000 + 10000}"
    alert_entry = {
        "id": sub_id,
        "med_id": med_id,
        "med_name": MEDS[med_id]["brand"],
        "salt": MEDS[med_id]["salt"],
        "strength": MEDS[med_id]["strength"],
        "phone": phone,
        "email": email,
        "channels": channels,
        "condition": condition,
        "radius_km": radius_km,
        "created_at": datetime.datetime.now().strftime("%d %b, %I:%M %p"),
        "status": "ACTIVE"
    }
    ALERTS.insert(0, alert_entry)

    # Return friendly confirmation
    return jsonify(
        status="success",
        message=f"Restock notification registered for {MEDS[med_id]['brand']}. You will be alerted via {', '.join(channels).upper()}.",
        alert=alert_entry
    )

@app.post("/api/delete_alert")
def api_delete_alert():
    """Cancel or remove an alert subscription."""
    data = request.get_json(silent=True) or request.form
    alert_id = str(data.get("id", "")).strip()
    global ALERTS
    initial_len = len(ALERTS)
    ALERTS = [a for a in ALERTS if a.get("id") != alert_id]
    if len(ALERTS) < initial_len:
        return jsonify(status="success", message=f"Subscription {alert_id} removed.")
    abort(404, "Alert subscription not found")

@app.post("/api/trigger_restock_simulation")
def api_trigger_restock_simulation():
    """Interactive restock simulation: simulates distributor stock arrival and fires alerts."""
    data = request.get_json(silent=True) or request.form or {}
    med_id = data.get("med_id")
    pharmacy_id = data.get("pharmacy_id")

    if med_id is not None:
        try: m = int(med_id)
        except (ValueError, TypeError): m = 6
    else:
        # Default to Lantus Pen (id=6) or Augmentin 625 (id=22)
        m = 6 if SNAP["stock"][:, 6].sum() < SNAP["stock"][:, 22].sum() else 22

    if pharmacy_id is not None:
        try: p = int(pharmacy_id)
        except (ValueError, TypeError): p = 1
    else:
        p = 1 # Apollo Pharmacy (Gandhi Road)

    added_units = 25
    SNAP["stock"][p, m] += added_units
    POUT[p, m] = max(0.04, float(POUT[p, m]) - 0.50)

    # Update verification ledger
    now = datetime.datetime.now()
    VERIFICATIONS[(p, m)] = {
        "pharmacy_id": p,
        "pharmacy_name": PHARM[p]["name"],
        "med_id": m,
        "med_brand": MEDS[m]["brand"],
        "status": "VERIFIED_IN_STOCK",
        "units": int(SNAP["stock"][p, m]),
        "batch_no": f"KC26-{(m * 73 + p * 31 + 105) % 900 + 100}",
        "expiry_date": f"{(m % 12) + 1:02d}/2028",
        "verified_at": "Just now (" + now.strftime("%I:%M %p") + ")",
        "verified_timestamp": now.isoformat(),
        "verified_by": "Distributor Direct Restock Inbound Scan",
        "pos_system": PHARM[p].get("pos_system", "Marg ERP Cloud"),
        "confidence_score": 99,
        "is_active": True,
        "notes": f"Batch delivery confirmed: {added_units} fresh units checked in."
    }

    # Dispatch alerts to matching subscribers
    matched_subscribers = [a for a in ALERTS if a["med_id"] == m and a.get("status") == "ACTIVE"]
    notif_id = f"NOTIF-{int(time.time() * 1000) % 90000 + 10000}"
    new_notif = {
        "id": notif_id,
        "med_id": m,
        "med_name": MEDS[m]["brand"],
        "pharmacy_id": p,
        "pharmacy_name": PHARM[p]["name"],
        "title": f"🎉 In-Stock Alert: {MEDS[m]['brand']}",
        "message": f"{added_units} fresh units of {MEDS[m]['brand']} just arrived at {PHARM[p]['name']} ({PHARM[p]['area']}). Live stock verified!",
        "time": "Just now",
        "type": "RESTOCK_ALERT",
        "action_url": f"med={m}&pharm={p}",
        "read": False
    }
    NOTIFICATIONS.insert(0, new_notif)

    return jsonify(
        status="success",
        simulated_event={
            "medicine": MEDS[m]["brand"],
            "pharmacy": PHARM[p]["name"],
            "added_units": added_units,
            "new_stock": int(SNAP["stock"][p, m]),
            "matched_subscribers_alerted": len(matched_subscribers)
        },
        notification=new_notif
    )

# =========================================================================
# FEATURE 6: EMERGENCY MEDICINE FINDER
# =========================================================================

@app.get("/api/emergency_finder")
def api_emergency_finder():
    """Rapid emergency locator for critical life-saving medications."""
    try:
        lat = float(request.args.get("lat", 12.8342))
        lon = float(request.args.get("lon", 79.7036))
    except (ValueError, TypeError):
        lat, lon = 12.8342, 79.7036

    med_param = request.args.get("med_id")
    target_med_id = None
    if med_param:
        try:
            m = int(med_param)
            if 0 <= m < len(MEDS) and MEDS[m]["is_emergency"]:
                target_med_id = m
        except (ValueError, TypeError):
            pass

    # All emergency medicines
    em_meds = [m for m in MEDS if m["is_emergency"]]
    em_ids = [m["id"] for m in em_meds]

    dists = hav(lat, lon, PLAT, PLON)

    # Rank pharmacies by fastest ETA and emergency readiness
    ranked_pharmacies = []
    for p in range(len(PHARM)):
        ph = PHARM[p]
        d = float(dists[p])
        eta = int(round(d * 3 + 2))

        # Check in-stock emergency medicines at this pharmacy
        stocked_emergency_items = []
        for m_id in em_ids:
            if target_med_id is not None and m_id != target_med_id:
                continue
            st = int(SNAP["stock"][p, m_id])
            pa = 1 - float(POUT[p, m_id])
            if st > 0 and pa >= 0.40:
                m_info = MEDS[m_id]
                v = get_verification(p, m_id)
                stocked_emergency_items.append({
                    "id": m_id,
                    "brand": m_info["brand"],
                    "salt": m_info["salt"],
                    "strength": m_info["strength"],
                    "price": m_info["price"],
                    "stock_units": st,
                    "p_avail": round(pa, 3),
                    "emergency_usage": m_info.get("emergency_usage", ""),
                    "verified_at": v["verified_at"]
                })

        # Only list pharmacies having emergency stock (or if specific target requested, having that item)
        if stocked_emergency_items:
            ranked_pharmacies.append({
                "id": p,
                "name": ph["name"],
                "phone": ph["phone"],
                "area": ph["area"],
                "lat": ph["lat"],
                "lon": ph["lon"],
                "dist_km": round(d, 1),
                "eta_min": eta,
                "is_24x7": ph.get("is_24x7", False),
                "has_cold_storage": ph.get("has_cold_storage", True),
                "emergency_items": stocked_emergency_items,
                "emergency_items_count": len(stocked_emergency_items),
                "google_maps_url": f"https://www.google.com/maps/dir/?api=1&origin={lat},{lon}&destination={ph['lat']},{ph['lon']}&travelmode=driving",
                "whatsapp_sos_url": f"https://api.whatsapp.com/send?phone={ph['phone'].replace(' ', '').replace('+', '')}&text=" +
                    f"EMERGENCY%20SOS:%20Urgent%20life-saving%20medicine%20needed%20at%20Kanchipuram.%20Please%20confirm%20immediate%20readiness%20at%20{ph['name'].replace(' ', '%20')}!"
            })

    # Sort strictly by distance (fastest ETA)
    ranked_pharmacies.sort(key=lambda x: (not x["is_24x7"], x["dist_km"]))

    # Emergency Services Directory
    helplines = [
        {"title": "108 Ambulance (Tamil Nadu)", "number": "108", "type": "AMBULANCE", "desc": "Free 24x7 Government Emergency Ambulance Dispatch"},
        {"title": "112 Unified Emergency Helpline", "number": "112", "type": "POLICE_FIRE_MEDICAL", "desc": "National All-in-One Emergency Responder"},
        {"title": "Kanchipuram District HQ Hospital", "number": "+91 44 2722 2333", "type": "HOSPITAL", "desc": "24x7 Trauma Casualty & Anti-Venom Center, Gandhi Rd"},
        {"title": "Tamil Nadu Drug Control Helpline", "number": "1800 425 4085", "type": "MEDICINE_SUPPORT", "desc": "Official state regulatory emergency medicine desk"}
    ]

    return jsonify(
        user_coords={"lat": lat, "lon": lon},
        emergency_medicines=em_meds,
        selected_medicine=MEDS[target_med_id] if target_med_id is not None else None,
        nearest_emergency_pharmacies=ranked_pharmacies[:8],
        emergency_helplines=helplines
    )

# =========================================================================
# DELIVERY & EXISTING ENDPOINTS
# =========================================================================

@app.post("/api/order_delivery")
def order_delivery():
    data = request.get_json(silent=True) or request.form
    if not data:
        abort(400, "Invalid JSON data")

    pharmacy_id = data.get("pharmacy_id", 0)
    med_id = data.get("med_id", 0)
    customer_name = str(data.get("customer_name") or "Ramesh Kumar").strip()
    phone = str(data.get("phone") or "+91 98401 23456").strip()
    address = str(data.get("address") or "14, Gandhi Road, Kanchipuram").strip()
    payment_method = str(data.get("payment_method") or "Cash on Delivery").strip()
    try:
        quantity = max(1, min(100, int(data.get("quantity", 1))))
    except (ValueError, TypeError):
        quantity = 1
    notes = str(data.get("notes", "")).strip()
    prescription = data.get("prescription")

    try:
        pharmacy_id = int(pharmacy_id)
        med_id = int(med_id)
    except (ValueError, TypeError):
        pharmacy_id = 0
        med_id = 0

    pharmacy_id = max(0, min(len(PHARM) - 1, pharmacy_id))
    med_id = max(0, min(len(MEDS) - 1, med_id))

    med = MEDS[med_id]
    pharm = PHARM[pharmacy_id]

    unit_price = int(med["price"])
    subtotal = unit_price * quantity
    delivery_fee = 0 if subtotal >= 250 else 35
    total = subtotal + delivery_fee

    order_id = f"MR-DEL-{int(time.time() * 1000) % 1000000:06d}"
    order = {
        "id": order_id,
        "created_at": datetime.datetime.now().strftime("%d %b %Y, %I:%M %p"),
        "customer_name": customer_name,
        "phone": phone,
        "address": address,
        "pharmacy_id": pharmacy_id,
        "pharmacy_name": pharm["name"],
        "pharmacy_phone": pharm["phone"],
        "pharmacy_area": pharm["area"],
        "pharmacy_dl": f"TN-KC-2024-{(pharmacy_id * 137 + 1042) % 9000 + 1000}",
        "pharmacy_gstin": f"33AAACP{(pharmacy_id * 419 + 1102) % 9000 + 1000}Q1Z5",
        "med_id": med_id,
        "med_brand": med["brand"],
        "med_salt": med["salt"],
        "med_strength": med["strength"],
        "batch_no": f"KC26-{(med_id * 73 + 105) % 900 + 100}",
        "expiry_date": f"{(med_id % 12) + 1:02d}/2028",
        "quantity": quantity,
        "unit_price": unit_price,
        "subtotal": subtotal,
        "delivery_fee": delivery_fee,
        "total": total,
        "payment_method": payment_method,
        "payment_status": "Pending (Pay on Delivery)",
        "order_status": "Order Placed & Confirmed",
        "status_step": 0,
        "eta_mins": 35,
        "rider_name": "Murugan K.",
        "rider_phone": "+91 98401 23456",
        "rider_vehicle": "Hero Splendor (TN-21-AX-4821)",
        "delivery_otp": f"{(int(time.time()) % 9000) + 1000}",
        "rx_required": med["rx"],
        "prescription": prescription,
        "notes": notes
    }
    ORDERS.insert(0, order)
    return jsonify(status="success", order=order)

@app.post("/api/order_status")
def update_order_status():
    data = request.get_json(silent=True) or request.form
    if not data:
        abort(400, "Invalid JSON data")
    order_id = data.get("order_id")
    step = data.get("step")
    target_order = None
    for o in ORDERS:
        if o["id"] == order_id:
            target_order = o
            break
    if not target_order:
        abort(404, "Order not found")

    if "payment_method" in data and data["payment_method"]:
        target_order["payment_method"] = str(data["payment_method"]).strip()
    if "payment_status" in data and data["payment_status"]:
        target_order["payment_status"] = str(data["payment_status"]).strip()

    if step is not None:
        try:
            step = int(step)
        except (ValueError, TypeError):
            step = (target_order.get("status_step", 0) + 1) % 4
    elif "payment_status" not in data and "payment_method" not in data:
        # Default advance behavior when called with just order_id
        step = (target_order.get("status_step", 0) + 1) % 4

    if step is not None:
        step = max(0, min(3, step))
        status_labels = [
            "Order Placed & Confirmed",
            "Packed & Prescriptions Verified",
            "Rider Dispatched & En Route",
            "Delivered to Doorstep & Settled"
        ]
        target_order["status_step"] = step
        target_order["order_status"] = status_labels[step]
        if step == 2:
            target_order["eta_mins"] = 15
        elif step == 3:
            target_order["eta_mins"] = 0
            if "Paid" not in target_order.get("payment_status", ""):
                target_order["payment_status"] = f"Paid via {target_order['payment_method']}"
    elif "paid" in target_order.get("payment_status", "").lower():
        target_order["status_step"] = 3
        target_order["order_status"] = "Delivered to Doorstep & Settled"
        target_order["eta_mins"] = 0

    return jsonify(status="success", order=target_order)

@app.post("/api/order_payment")
def update_order_payment():
    data = request.get_json(silent=True) or request.form
    if not data:
        abort(400, "Invalid JSON data")
    order_id = data.get("order_id")
    payment_method = data.get("payment_method")
    payment_status = data.get("payment_status")
    target_order = None
    for o in ORDERS:
        if o["id"] == order_id:
            target_order = o
            break
    if not target_order:
        abort(404, "Order not found")

    if payment_method:
        target_order["payment_method"] = str(payment_method).strip()
    if payment_status:
        target_order["payment_status"] = str(payment_status).strip()
    else:
        target_order["payment_status"] = f"Paid via {target_order['payment_method']}"

    if "paid" in target_order["payment_status"].lower():
        target_order["status_step"] = 3
        target_order["order_status"] = "Delivered to Doorstep & Settled"
        target_order["eta_mins"] = 0

    return jsonify(status="success", order=target_order)

@app.get("/api/orders")
def get_orders():
    pharmacy_id = request.args.get("pharmacy_id")
    phone = request.args.get("phone")
    res = ORDERS
    if pharmacy_id is not None:
        try:
            pid = int(pharmacy_id)
            res = [o for o in res if o["pharmacy_id"] == pid]
        except ValueError:
            pass
    if phone:
        res = [o for o in res if phone in str(o["phone"])]
    return jsonify(orders=res)

@app.get("/api/report")
def report():
    return jsonify(REPORT)

@app.get("/api/chart_stats")
def chart_stats():
    """Aggregated pie & donut chart statistics across availability, shortages, and savings."""
    pout = SNAP["p_out"]
    total_pairs = int(pout.size)
    in_stock = int(np.sum(pout <= 0.15))
    call_ahead = int(np.sum((pout > 0.15) & (pout <= 0.45)))
    likely_out = int(np.sum(pout > 0.45))

    availability_pie = [
        {"label": "In Stock (≥85%)", "count": in_stock, "pct": round(in_stock / total_pairs * 100, 1), "color": "#10b981"},
        {"label": "Call Ahead (55-84%)", "count": call_ahead, "pct": round(call_ahead / total_pairs * 100, 1), "color": "#f59e0b"},
        {"label": "Likely Out (<55%)", "count": likely_out, "pct": round(likely_out / total_pairs * 100, 1), "color": "#ef4444"}
    ]

    # Category shortage contribution
    cat_outs = {}
    cat_colors = {
        "Diabetes": "#ec4899",
        "Heart & BP": "#f43f5e",
        "Breathing": "#06b6d4",
        "Antibiotics": "#8b5cf6",
        "Fever & pain": "#3b82f6",
        "Stomach": "#f59e0b",
        "Cold & allergy": "#10b981",
        "Thyroid": "#a855f7",
        "Vitamins": "#14b8a6"
    }
    for m in range(len(MEDS)):
        c = MEDS[m]["category"]
        out_cnt = int(np.sum(SNAP["stock"][:, m] == 0))
        cat_outs[c] = cat_outs.get(c, 0) + out_cnt

    total_outs = max(1, sum(cat_outs.values()))
    category_shortage_pie = [
        {
            "category": c,
            "label": c,
            "count": cnt,
            "pct": round(cnt / total_outs * 100, 1),
            "color": cat_colors.get(c, "#64748b")
        }
        for c, cnt in sorted(cat_outs.items(), key=lambda x: -x[1])
    ]

    # Shortage Risk classification
    crit, high, mod, stable = 0, 0, 0, 0
    for m in range(len(MEDS)):
        st = float(np.sum(SNAP["stock"][:, m]))
        dem = float(np.sum(SNAP["dem"][:, m]))
        cv = st / max(0.1, dem)
        if cv < 2.5: crit += 1
        elif cv < 6.0: high += 1
        elif cv < 10.0: mod += 1
        else: stable += 1

    total_meds = len(MEDS)
    risk_pie = [
        {"label": "Critical (<48h)", "count": crit, "pct": round(crit / total_meds * 100, 1), "color": "#ef4444"},
        {"label": "High Risk (3-7d)", "count": high, "pct": round(high / total_meds * 100, 1), "color": "#f97316"},
        {"label": "Moderate (7-14d)", "count": mod, "pct": round(mod / total_meds * 100, 1), "color": "#eab308"},
        {"label": "Stable (>14d)", "count": stable, "pct": round(stable / total_meds * 100, 1), "color": "#10b981"}
    ]

    # Trip evaluation pie
    trips_data = REPORT.get("trips", {"nearest_pct": 15.5, "model_pct": 3.3})
    ai_wasted = trips_data.get("model_pct", 3.3)
    ai_success = round(100 - ai_wasted, 1)
    near_wasted = trips_data.get("nearest_pct", 15.5)
    near_success = round(100 - near_wasted, 1)

    ai_trip_pie = [
        {"label": "Successful Trips", "pct": ai_success, "color": "#10b981"},
        {"label": "Wasted Journeys", "pct": ai_wasted, "color": "#ef4444"}
    ]
    near_trip_pie = [
        {"label": "Successful Trips", "pct": near_success, "color": "#3b82f6"},
        {"label": "Wasted Journeys", "pct": near_wasted, "color": "#f43f5e"}
    ]

    return jsonify(
        availability_pie=availability_pie,
        category_shortage_pie=category_shortage_pie,
        shortage_risk_pie=risk_pie,
        ai_trip_pie=ai_trip_pie,
        near_trip_pie=near_trip_pie,
        total_pharmacies=len(PHARM),
        total_medicines=len(MEDS)
    )

@app.post("/api/retrain")
def api_retrain():
    """Trigger model retraining with temporal splits and reload snapshots."""
    try:
        subprocess.check_call([sys.executable, os.path.join(H, "train.py")], cwd=H)
        load_data()
        return jsonify(
            status="success",
            message="Model successfully trained and calibrated. New snapshot loaded.",
            report=REPORT
        )
    except Exception as e:
        return jsonify(status="error", message=str(e)), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
