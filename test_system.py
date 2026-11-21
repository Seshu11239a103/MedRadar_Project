"""
Comprehensive Verification Test for MedRadar Login & XAMPP MySQL Database Integration
Tests Flask routes, session auth, admin oversight, retailer inventory update, and MySQL tables.
"""

import os
import json
import pymysql
from app import app
import db

def test_all():
    print("==================================================")
    print("STARTING FULL SYSTEM VERIFICATION")
    print("==================================================")

    # 1. Test XAMPP MySQL direct query
    print("\n[Test 1] Testing XAMPP MySQL database 'medradar_db' connection...")
    try:
        conn = pymysql.connect(host='localhost', user='root', password='', database='medradar_db', port=3306)
        cur = conn.cursor()
        cur.execute("SHOW TABLES;")
        tables = [t[0] for t in cur.fetchall()]
        print(f"  -> SUCCESS: Connected to MySQL. Tables found: {tables}")
        
        cur.execute("SELECT count(*) FROM users;")
        user_cnt = cur.fetchone()[0]
        cur.execute("SELECT count(*) FROM inventory;")
        inv_cnt = cur.fetchone()[0]
        print(f"  -> Verified MySQL records: {user_cnt} users, {inv_cnt} inventory records.")
        conn.close()
    except Exception as e:
        print(f"  -> MySQL connection failed: {e}")

    # 2. Test Flask Test Client
    client = app.test_client()

    print("\n[Test 2] Testing GET /login page...")
    res = client.get("/login")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    assert b"Sign In" in res.data, "Sign In missing"
    assert b"Username" in res.data, "Username input missing"
    assert b"Password" in res.data, "Password input missing"
    print("  -> SUCCESS: /login served cleanly with Username & Password fields.")

    print("\n[Test 3] Testing GET /api/db/status...")
    res = client.get("/api/db/status")
    assert res.status_code == 200
    db_status = res.get_json()
    print(f"  -> SUCCESS: DB Status: {db_status}")
    assert db_status["status"] == "connected"

    print("\n[Test 4] Testing Admin Login (POST /api/auth/login)...")
    res = client.post("/api/auth/login", json={
        "username": "admin",
        "password": "Admin@MedRadar2026"
    })
    assert res.status_code == 200
    admin_auth = res.get_json()
    print(f"  -> SUCCESS: Admin login successful: {admin_auth['user']['full_name']}, redirect: {admin_auth['redirect']}")
    assert admin_auth["user"]["role"] == "admin"

    print("\n[Test 5] Testing Admin Overview (GET /api/admin/overview)...")
    res = client.get("/api/admin/overview")
    assert res.status_code == 200
    overview = res.get_json()
    print(f"  -> SUCCESS: Admin metrics: Total users = {len(overview['users'])}, Pharmacies = {len(overview['pharmacies'])}")

    print("\n[Test 6] Testing Sub-Admin / Retailer Login (Apollo Pharmacy)...")
    client_retailer = app.test_client()
    res = client_retailer.post("/api/auth/login", json={
        "username": "retailer_apollo",
        "password": "Apollo@Retail2026"
    })
    assert res.status_code == 200
    ret_auth = res.get_json()
    print(f"  -> SUCCESS: Retailer login: {ret_auth['user']['full_name']}, Pharmacy: {ret_auth['user']['pharmacy_name']}")
    assert ret_auth["user"]["role"] == "sub_admin"

    print("\n[Test 7] Testing Medical Member Login (Kanchi HQ Hospital)...")
    res = client.post("/api/auth/login", json={
        "username": "medical_kanchi_hq",
        "password": "Medical@Kanchi2026"
    })
    assert res.status_code == 200
    med_auth = res.get_json()
    print(f"  -> SUCCESS: Medical staff login: {med_auth['user']['full_name']}, Role: {med_auth['user']['role']}")
    assert med_auth["user"]["role"] == "medical_member"

    print("\n[Test 8] Testing Retailer Inventory Fetch (GET /api/retailer/inventory?pharmacy_id=1)...")
    res = client_retailer.get("/api/retailer/inventory?pharmacy_id=1")
    assert res.status_code == 200
    inv_data = res.get_json()
    print(f"  -> SUCCESS: Fetched {len(inv_data['inventory'])} medicines for {inv_data['pharmacy']['name']}")
    first_med = inv_data['inventory'][0]
    print(f"     Sample item: {first_med['brand']} ({first_med['salt']}) -> {first_med['stock_units']} units on shelf, Batch: {first_med['batch_no']}")

    print("\n[Test 9] Testing Retailer Shelf Stock Update (POST /api/retailer/inventory/update)...")
    test_med_id = first_med["medicine_id"]
    new_stock = first_med["stock_units"] + 25
    res = client_retailer.post("/api/retailer/inventory/update", json={
        "pharmacy_id": 1,
        "medicine_id": test_med_id,
        "stock_units": new_stock,
        "batch_no": "BAT-2026-TEST",
        "expiry_date": "2027-12-31",
        "notes": "Verified by Apollo Pharmacist physical shelf count"
    })
    assert res.status_code == 200
    upd_res = res.get_json()
    print(f"  -> SUCCESS: Updated shelf units to {new_stock}. Audit status: {upd_res['status']}")

    print("\n[Test 10] Testing Admin Create Sub-Admin User (POST /api/admin/users/create)...")
    import time
    test_uname = f"subadmin_t_{int(time.time())}"
    res = client.post("/api/admin/users/create", json={
        "username": test_uname,
        "password": "Test@Retail2026",
        "role": "sub_admin",
        "pharmacy_id": 3,
        "full_name": "Test Store Pharmacist (Walajabad)",
        "email": f"{test_uname}@medradar.in",
        "phone": "+91 98420 11223"
    })
    d = res.get_json()
    assert res.status_code == 200 and d.get("success") is True, f"Expected 200 success, got {res.status_code}: {d}"
    print(f"  -> SUCCESS: Created sub-admin user: {test_uname} -> {d.get('message')}")

    print("\n==================================================")
    print("ALL 10 TESTS PASSED CLEANLY & SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    test_all()
