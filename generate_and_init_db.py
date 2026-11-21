"""
MedRadar Database Generator & XAMPP MySQL Initializer
Generates medradar_database.sql and initializes medradar_db in XAMPP MySQL / phpMyAdmin.
"""

import os
import sys
import json
import datetime
import pymysql
from werkzeug.security import generate_password_hash
from catalog import MEDS, PHARM

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQL_FILE = os.path.join(BASE_DIR, "medradar_database.sql")

# Seed Users configuration
DEFAULT_USERS = [
    {
        "username": "admin",
        "password": "Admin@MedRadar2026",
        "role": "admin",
        "pharmacy_id": None,
        "full_name": "Kanchipuram Health Administrator (App Owner)",
        "email": "admin@medradar-kanchi.gov.in",
        "phone": "+91 94440 12345"
    },
    {
        "username": "retailer_sriram",
        "password": "SriRam@Retail2026",
        "role": "sub_admin",
        "pharmacy_id": 0,
        "full_name": "Kanchi Sri Ram Medicals Store Manager",
        "email": "sriram.gandhi@medradar-retail.in",
        "phone": "+91 98421 87654"
    },
    {
        "username": "retailer_apollo",
        "password": "Apollo@Retail2026",
        "role": "sub_admin",
        "pharmacy_id": 1,
        "full_name": "Apollo Pharmacy Gandhi Road Supervisor",
        "email": "apollo.gandhird@medradar-retail.in",
        "phone": "+91 98422 98765"
    },
    {
        "username": "retailer_medplus",
        "password": "MedPlus@Retail2026",
        "role": "sub_admin",
        "pharmacy_id": 2,
        "full_name": "MedPlus Bus Stand Retail Pharmacist",
        "email": "medplus.busstand@medradar-retail.in",
        "phone": "+91 98423 09876"
    },
    {
        "username": "medical_kanchi_hq",
        "password": "Medical@Kanchi2026",
        "role": "medical_member",
        "pharmacy_id": 4,
        "full_name": "Dr. S. Sundararajan (Chief Pharmacist, Kanchi HQ Hospital)",
        "email": "casualty.pharmacy@kanchidistrict.gov.in",
        "phone": "+91 98425 21098"
    },
    {
        "username": "retailer_janaushadhi",
        "password": "Generic@PMBJP2026",
        "role": "sub_admin",
        "pharmacy_id": 13,
        "full_name": "PMBJP Jan Aushadhi Kendra Central Manager",
        "email": "pmbjp.kanchi@medradar-generic.gov.in",
        "phone": "+91 98434 10987"
    }
]

def generate_sql():
    lines = []
    lines.append("-- ============================================================")
    lines.append("-- MedRadar v2 Kanchipuram: Comprehensive Database Schema")
    lines.append("-- Optimized for XAMPP MySQL / MariaDB and phpMyAdmin")
    lines.append(f"-- Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("-- ============================================================\n")
    
    lines.append("CREATE DATABASE IF NOT EXISTS `medradar_db` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    lines.append("USE `medradar_db`;\n")
    lines.append("SET FOREIGN_KEY_CHECKS = 0;\n")

    # Table: users
    lines.append("-- ------------------------------------------------------------")
    lines.append("-- Table structure for table `users`")
    lines.append("-- ------------------------------------------------------------")
    lines.append("DROP TABLE IF EXISTS `users`;")
    lines.append("""CREATE TABLE `users` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(50) NOT NULL UNIQUE,
  `password_hash` VARCHAR(255) NOT NULL,
  `role` ENUM('admin', 'sub_admin', 'pharmacist', 'medical_member') NOT NULL DEFAULT 'sub_admin',
  `pharmacy_id` INT NULL,
  `full_name` VARCHAR(120) NOT NULL,
  `email` VARCHAR(120) NOT NULL,
  `phone` VARCHAR(30) NOT NULL,
  `status` ENUM('active', 'inactive', 'suspended') DEFAULT 'active',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `last_login` DATETIME NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;\n""")

    # Table: pharmacies
    lines.append("-- ------------------------------------------------------------")
    lines.append("-- Table structure for table `pharmacies`")
    lines.append("-- ------------------------------------------------------------")
    lines.append("DROP TABLE IF EXISTS `pharmacies`;")
    lines.append("""CREATE TABLE `pharmacies` (
  `id` INT PRIMARY KEY,
  `name` VARCHAR(120) NOT NULL,
  `phone` VARCHAR(30) NOT NULL,
  `area` VARCHAR(100) NOT NULL,
  `lat` DOUBLE NOT NULL,
  `lon` DOUBLE NOT NULL,
  `size` DOUBLE DEFAULT 1.0,
  `is_24x7` TINYINT(1) DEFAULT 0,
  `has_cold_storage` TINYINT(1) DEFAULT 1,
  `pos_system` VARCHAR(60) DEFAULT 'Marg ERP Cloud',
  `discount_pct` INT DEFAULT 10,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;\n""")

    # Table: medicines
    lines.append("-- ------------------------------------------------------------")
    lines.append("-- Table structure for table `medicines`")
    lines.append("-- ------------------------------------------------------------")
    lines.append("DROP TABLE IF EXISTS `medicines`;")
    lines.append("""CREATE TABLE `medicines` (
  `id` INT PRIMARY KEY,
  `brand` VARCHAR(120) NOT NULL,
  `salt` VARCHAR(160) NOT NULL,
  `strength` VARCHAR(60) NOT NULL,
  `category` VARCHAR(60) NOT NULL,
  `lead_days` INT DEFAULT 2,
  `daily_level` DOUBLE DEFAULT 5.0,
  `seasonal_amp` DOUBLE DEFAULT 0.2,
  `price` DOUBLE NOT NULL,
  `rx_required` TINYINT(1) DEFAULT 0,
  `is_emergency` TINYINT(1) DEFAULT 0,
  `mrp` DOUBLE NOT NULL,
  `generic_name` VARCHAR(160) NOT NULL,
  `generic_price` DOUBLE NOT NULL,
  `packaging` VARCHAR(60) DEFAULT 'Strip of 10',
  `emergency_usage` VARCHAR(255) NULL,
  `savings_pct` INT DEFAULT 50
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;\n""")

    # Table: inventory
    lines.append("-- ------------------------------------------------------------")
    lines.append("-- Table structure for table `inventory`")
    lines.append("-- ------------------------------------------------------------")
    lines.append("DROP TABLE IF EXISTS `inventory`;")
    lines.append("""CREATE TABLE `inventory` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `pharmacy_id` INT NOT NULL,
  `medicine_id` INT NOT NULL,
  `stock_units` INT NOT NULL DEFAULT 0,
  `batch_no` VARCHAR(50) DEFAULT 'BATCH-2026-A1',
  `expiry_date` DATE NOT NULL,
  `reorder_threshold` INT DEFAULT 15,
  `last_restock_date` DATETIME NULL,
  `last_audited_by` INT NULL,
  `last_audited_at` DATETIME NULL,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY `unique_pharm_med` (`pharmacy_id`, `medicine_id`),
  FOREIGN KEY (`pharmacy_id`) REFERENCES `pharmacies`(`id`) ON DELETE CASCADE,
  FOREIGN KEY (`medicine_id`) REFERENCES `medicines`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;\n""")

    # Table: stock_audits
    lines.append("-- ------------------------------------------------------------")
    lines.append("-- Table structure for table `stock_audits`")
    lines.append("-- ------------------------------------------------------------")
    lines.append("DROP TABLE IF EXISTS `stock_audits`;")
    lines.append("""CREATE TABLE `stock_audits` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `pharmacy_id` INT NOT NULL,
  `medicine_id` INT NOT NULL,
  `user_id` INT NULL,
  `auditor_name` VARCHAR(100) NOT NULL,
  `status` ENUM('VERIFIED_IN_STOCK', 'LOW_STOCK_CONFIRMED', 'OUT_OF_STOCK_VERIFIED') NOT NULL,
  `units_verified` INT NOT NULL,
  `notes` TEXT NULL,
  `verified_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;\n""")

    # Table: restock_alerts
    lines.append("-- ------------------------------------------------------------")
    lines.append("-- Table structure for table `restock_alerts`")
    lines.append("-- ------------------------------------------------------------")
    lines.append("DROP TABLE IF EXISTS `restock_alerts`;")
    lines.append("""CREATE TABLE `restock_alerts` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NULL,
  `pharmacy_id` INT NULL,
  `medicine_id` INT NOT NULL,
  `trigger_type` VARCHAR(50) NOT NULL,
  `contact_channel` VARCHAR(30) NOT NULL,
  `contact_value` VARCHAR(100) NOT NULL,
  `is_active` TINYINT(1) DEFAULT 1,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;\n""")

    # Table: delivery_orders
    lines.append("-- ------------------------------------------------------------")
    lines.append("-- Table structure for table `delivery_orders`")
    lines.append("-- ------------------------------------------------------------")
    lines.append("DROP TABLE IF EXISTS `delivery_orders`;")
    lines.append("""CREATE TABLE `delivery_orders` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `order_ref` VARCHAR(50) NOT NULL UNIQUE,
  `pharmacy_id` INT NOT NULL,
  `customer_name` VARCHAR(100) NOT NULL,
  `customer_phone` VARCHAR(30) NOT NULL,
  `delivery_address` TEXT NOT NULL,
  `items_json` LONGTEXT NOT NULL,
  `total_inr` DOUBLE NOT NULL,
  `payment_mode` VARCHAR(50) DEFAULT 'COD',
  `order_status` VARCHAR(50) DEFAULT 'PENDING',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;\n""")

    # Insert Pharmacies
    lines.append("-- ------------------------------------------------------------")
    lines.append("-- Dumping data for table `pharmacies`")
    lines.append("-- ------------------------------------------------------------")
    lines.append("INSERT INTO `pharmacies` (`id`, `name`, `phone`, `area`, `lat`, `lon`, `size`, `is_24x7`, `has_cold_storage`, `pos_system`, `discount_pct`) VALUES")
    pharm_vals = []
    for p in PHARM:
        p_name = p['name'].replace("'", "''")
        p_area = p['area'].replace("'", "''")
        p_pos = p['pos_system'].replace("'", "''")
        val = f"({p['id']}, '{p_name}', '{p['phone']}', '{p_area}', {p['lat']}, {p['lon']}, {p['size']:.4f}, {1 if p['is_24x7'] else 0}, {1 if p['has_cold_storage'] else 0}, '{p_pos}', {p['discount_pct']})"
        pharm_vals.append(val)
    lines.append(",\n".join(pharm_vals) + ";\n")

    # Insert Medicines
    lines.append("-- ------------------------------------------------------------")
    lines.append("-- Dumping data for table `medicines`")
    lines.append("-- ------------------------------------------------------------")
    lines.append("INSERT INTO `medicines` (`id`, `brand`, `salt`, `strength`, `category`, `lead_days`, `daily_level`, `seasonal_amp`, `price`, `rx_required`, `is_emergency`, `mrp`, `generic_name`, `generic_price`, `packaging`, `emergency_usage`, `savings_pct`) VALUES")
    med_vals = []
    for m in MEDS:
        m_brand = m['brand'].replace("'", "''")
        m_salt = m['salt'].replace("'", "''")
        m_gen = m['generic_name'].replace("'", "''")
        em_usage = (m.get('emergency_usage', '') or '').replace("'", "''")
        val = f"({m['id']}, '{m_brand}', '{m_salt}', '{m['strength']}', '{m['category']}', {m['lead']}, {m['level']}, {m['amp']}, {m['price']}, {1 if m['rx'] else 0}, {1 if m['is_emergency'] else 0}, {m['mrp']}, '{m_gen}', {m['generic_price']}, '{m['packaging']}', '{em_usage}', {m['savings_pct']})"
        med_vals.append(val)
    lines.append(",\n".join(med_vals) + ";\n")

    # Insert Users
    lines.append("-- ------------------------------------------------------------")
    lines.append("-- Dumping data for table `users`")
    lines.append("-- ------------------------------------------------------------")
    lines.append("INSERT INTO `users` (`username`, `password_hash`, `role`, `pharmacy_id`, `full_name`, `email`, `phone`, `status`) VALUES")
    user_vals = []
    for u in DEFAULT_USERS:
        h = generate_password_hash(u["password"])
        p_id_str = str(u["pharmacy_id"]) if u["pharmacy_id"] is not None else "NULL"
        val = f"('{u['username']}', '{h}', '{u['role']}', {p_id_str}, '{u['full_name']}', '{u['email']}', '{u['phone']}', 'active')"
        user_vals.append(val)
    lines.append(",\n".join(user_vals) + ";\n")

    # Seed Inventory using realistic shelf numbers
    lines.append("-- ------------------------------------------------------------")
    lines.append("-- Dumping initial inventory data for table `inventory`")
    lines.append("-- ------------------------------------------------------------")
    lines.append("INSERT INTO `inventory` (`pharmacy_id`, `medicine_id`, `stock_units`, `batch_no`, `expiry_date`, `reorder_threshold`) VALUES")
    inv_vals = []
    import random
    random.seed(42)
    for p in PHARM:
        for m in MEDS:
            base = int(m['level'] * p['size'] * 7) + random.randint(5, 45)
            # A few items intentionally near stockout for realistic risk alerts
            if (p['id'] + m['id']) % 17 == 0:
                base = random.randint(0, 3)
            batch = f"BAT-2026-{p['id']:02d}{m['id']:02d}"
            exp_days = random.randint(120, 680)
            exp_date = (datetime.date.today() + datetime.timedelta(days=exp_days)).strftime("%Y-%m-%d")
            inv_vals.append(f"({p['id']}, {m['id']}, {base}, '{batch}', '{exp_date}', 15)")
    lines.append(",\n".join(inv_vals) + ";\n")

    lines.append("SET FOREIGN_KEY_CHECKS = 1;\n")
    lines.append("-- ============================================================")
    lines.append("-- End of MedRadar Database Script")
    lines.append("-- ============================================================")

    sql_content = "\n".join(lines)
    with open(SQL_FILE, "w", encoding="utf-8") as f:
        f.write(sql_content)
    print(f"Generated SQL schema file at: {SQL_FILE} ({len(sql_content):,} bytes)")
    return SQL_FILE

def init_xampp_mysql():
    print("Connecting to XAMPP MySQL server at localhost:3306...")
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            port=3306,
            autocommit=True
        )
        cursor = conn.cursor()
        print("Connected to MySQL server successfully!")
        
        # Explicitly create database first
        cursor.execute("CREATE DATABASE IF NOT EXISTS `medradar_db` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        cursor.execute("USE `medradar_db`;")
        print("Database 'medradar_db' selected successfully.")

        # Read SQL script
        with open(SQL_FILE, "r", encoding="utf-8") as f:
            sql_script = f.read()
        
        # Execute each statement
        statements = sql_script.split(";\n")
        executed_count = 0
        for stmt in statements:
            stmt = stmt.strip()
            # Skip empty lines or pure comments
            lines = [l for l in stmt.split("\n") if not l.strip().startswith("--") and l.strip()]
            cleaned_stmt = "\n".join(lines).strip()
            if cleaned_stmt:
                try:
                    cursor.execute(cleaned_stmt)
                    executed_count += 1
                except Exception as ex:
                    print(f"Warning on stmt execution: {ex}")
        
        print(f"Executed {executed_count} SQL statements into XAMPP MySQL database 'medradar_db'!")
        
        # Verify tables
        cursor.execute("SHOW TABLES;")
        tables = [t[0] for t in cursor.fetchall()]
        print("Verified tables in 'medradar_db':", tables)
        
        cursor.execute("SELECT username, role, full_name FROM users;")
        users = cursor.fetchall()
        print("\nVerified pre-seeded users in XAMPP MySQL:")
        for u in users:
            print(f"  - [{u[1]}] {u[0]} -> {u[2]}")
            
        cursor.execute("SELECT count(*) FROM inventory;")
        inv_count = cursor.fetchone()[0]
        print(f"Total inventory items seeded: {inv_count}")
        
        conn.close()
        return True
    except Exception as e:
        print(f"Failed to connect to XAMPP MySQL: {e}")
        return False

if __name__ == "__main__":
    generate_sql()
    success = init_xampp_mysql()
    if success:
        print("\nXAMPP MySQL database 'medradar_db' is fully initialized and ready in phpMyAdmin!")
    else:
        print("\nNotice: SQL schema file is ready for manual import in phpMyAdmin if MySQL is not currently running.")
