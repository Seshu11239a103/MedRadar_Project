# DOCX Builder for MedRadar Phase-I Project Report
# Strictly conforming to SCSVMV CSE Department Project Guidelines
# High-Definition Typography, Proportional Table Layouts, and Publication-Grade Visuals

import os
import sys
import zipfile
import shutil
import re

# Add builder to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from front_matter import (
    FRONT_MATTER_DATA, TABLE_OF_CONTENTS_DATA, 
    LIST_OF_TABLES_DATA, LIST_OF_FIGURES_DATA, LIST_OF_ABBREVIATIONS_DATA
)
from chapter1 import CHAPTER1_CONTENT
from chapter2 import CHAPTER2_CONTENT
from chapter3 import CHAPTER3_CONTENT
from chapter4 import CHAPTER4_CONTENT
from chapter5 import CHAPTER5_CONTENT
from back_matter import TIMELINES_DATA, PUBLICATIONS_DATA, REFERENCES_DATA

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
WP_NS = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
PIC_NS = "http://schemas.openxmlformats.org/drawingml/2006/picture"

doc_pr_counter = 1000

def xml_escape(text):
    if not text:
        return ""
    return (str(text).replace("&", "&amp;")
                     .replace("<", "&lt;")
                     .replace(">", "&gt;")
                     .replace('"', "&quot;")
                     .replace("'", "&apos;"))

def make_para(text, align="both", bold=False, italic=False, size=24, space_before=0, space_after=120, line_spacing=360, first_indent=720, hanging_indent=0, keep_next=False, page_break_before=False, font="Times New Roman", color=None):
    esc_text = xml_escape(text)
    pb = '<w:pageBreakBefore/>' if page_break_before else ''
    kn = '<w:keepNext/>' if keep_next else ''
    jc = f'<w:jc w:val="{align}"/>' if align else ''
    
    if hanging_indent > 0:
        ind = f'<w:ind w:left="{first_indent}" w:hanging="{hanging_indent}"/>'
    elif first_indent > 0:
        ind = f'<w:ind w:firstLine="{first_indent}"/>'
    else:
        ind = '<w:ind w:left="0" w:firstLine="0"/>'
        
    sp = f'<w:spacing w:before="{space_before}" w:after="{space_after}" w:line="{line_spacing}" w:lineRule="auto"/>'
    b = '<w:b/>' if bold else ''
    i = '<w:i/>' if italic else ''
    col = f'<w:color w:val="{color}"/>' if color else ''
    
    # Handle multi-line text with w:br
    lines = esc_text.split("\n")
    runs_xml = []
    for idx, line in enumerate(lines):
        if idx > 0:
            runs_xml.append("<w:br/>")
        runs_xml.append(f'<w:t xml:space="preserve">{line}</w:t>')
    runs_str = "".join(runs_xml)
    
    return f"""<w:p>
        <w:pPr>
            {pb}
            {kn}
            {jc}
            {ind}
            {sp}
            <w:rPr>
                <w:rFonts w:ascii="{font}" w:hAnsi="{font}" w:cs="{font}"/>
                {b}
                {i}
                {col}
                <w:sz w:val="{size}"/>
            </w:rPr>
        </w:pPr>
        <w:r>
            <w:rPr>
                <w:rFonts w:ascii="{font}" w:hAnsi="{font}" w:cs="{font}"/>
                {b}
                {i}
                {col}
                <w:sz w:val="{size}"/>
            </w:rPr>
            {runs_str}
        </w:r>
    </w:p>"""

def make_heading(text, level=1, page_break=False):
    sizes = {1: 32, 2: 27, 3: 24}
    size = sizes.get(level, 24)
    align = "center" if level == 1 else "left"
    space_before = 320 if level == 1 else (240 if level == 2 else 180)
    space_after = 140 if level == 1 else (100 if level == 2 else 70)
    
    return make_para(text, align=align, bold=True, size=size, space_before=space_before, space_after=space_after, line_spacing=360, first_indent=0, keep_next=True, page_break_before=page_break)

def make_formula_block(formula_text, num_label=""):
    esc_formula = xml_escape(formula_text)
    num_xml = ""
    if num_label:
        num_xml = f'<w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="21"/></w:rPr><w:tab/><w:t xml:space="preserve">{xml_escape(num_label)}</w:t></w:r>'
        
    return f"""<w:p>
        <w:pPr>
            <w:jc w:val="center"/>
            <w:spacing w:before="140" w:after="140" w:line="300" w:lineRule="auto"/>
            <w:shd w:val="clear" w:color="auto" w:fill="F8FAFC"/>
            <w:pBdr>
                <w:top w:val="single" w:sz="4" w:space="4" w:color="E2E8F0"/>
                <w:left w:val="single" w:sz="12" w:space="8" w:color="3182CE"/>
                <w:bottom w:val="single" w:sz="4" w:space="4" w:color="E2E8F0"/>
                <w:right w:val="single" w:sz="4" w:space="4" w:color="E2E8F0"/>
            </w:pBdr>
            <w:tabs>
                <w:tab w:val="right" w:pos="8100"/>
            </w:tabs>
            <w:rPr>
                <w:rFonts w:ascii="Cambria Math" w:hAnsi="Times New Roman"/>
                <w:i/>
                <w:sz w:val="22"/>
            </w:rPr>
        </w:pPr>
        <w:r>
            <w:rPr>
                <w:rFonts w:ascii="Cambria Math" w:hAnsi="Times New Roman"/>
                <w:i/>
                <w:sz w:val="22"/>
            </w:rPr>
            <w:t xml:space="preserve">{esc_formula}</w:t>
        </w:r>
        {num_xml}
    </w:p>"""

def make_code_block(code_text):
    esc = xml_escape(code_text)
    lines = esc.split("\n")
    runs_xml = []
    for idx, line in enumerate(lines):
        if idx > 0:
            runs_xml.append("<w:br/>")
        runs_xml.append(f'<w:t xml:space="preserve">{line}</w:t>')
    runs_str = "".join(runs_xml)
    
    return f"""<w:p>
        <w:pPr>
            <w:spacing w:before="120" w:after="140" w:line="240" w:lineRule="auto"/>
            <w:shd w:val="clear" w:color="auto" w:fill="F8FAFC"/>
            <w:pBdr>
                <w:top w:val="single" w:sz="6" w:space="4" w:color="CBD5E0"/>
                <w:left w:val="single" w:sz="18" w:space="8" w:color="2B6CB0"/>
                <w:bottom w:val="single" w:sz="6" w:space="4" w:color="CBD5E0"/>
                <w:right w:val="single" w:sz="6" w:space="4" w:color="CBD5E0"/>
            </w:pBdr>
            <w:rPr>
                <w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>
                <w:sz w:val="19"/>
            </w:rPr>
        </w:pPr>
        <w:r>
            <w:rPr>
                <w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>
                <w:sz w:val="19"/>
            </w:rPr>
            {runs_str}
        </w:r>
    </w:p>"""

def make_signature_table(left_lines, right_lines, col_width=4150):
    left_p_runs = []
    for idx, l in enumerate(left_lines):
        if idx > 0:
            left_p_runs.append('<w:br/>')
        b = '<w:b/>' if (idx == 0 or 'Examiner' in l) else ''
        left_p_runs.append(f'<w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>{b}<w:sz w:val="22"/></w:rPr><w:t xml:space="preserve">{xml_escape(l)}</w:t></w:r>')
        
    right_p_runs = []
    for idx, l in enumerate(right_lines):
        if idx > 0:
            right_p_runs.append('<w:br/>')
        b = '<w:b/>' if (idx == 0 or 'Examiner' in l) else ''
        right_p_runs.append(f'<w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>{b}<w:sz w:val="22"/></w:rPr><w:t xml:space="preserve">{xml_escape(l)}</w:t></w:r>')

    return f"""<w:tbl>
        <w:tblPr>
            <w:tblW w:w="8300" w:type="dxa"/>
            <w:jc w:val="center"/>
            <w:tblBorders>
                <w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/><w:insideH w:val="none"/><w:insideV w:val="none"/>
            </w:tblBorders>
        </w:tblPr>
        <w:tr>
            <w:trPr><w:cantSplit/></w:trPr>
            <w:tc>
                <w:tcPr><w:tcW w:w="{col_width}" w:type="dxa"/><w:tcMar><w:top w:w="80" w:type="dxa"/><w:bottom w:w="80" w:type="dxa"/><w:left w:w="40" w:type="dxa"/><w:right w:w="80" w:type="dxa"/></w:tcMar></w:tcPr>
                <w:p><w:pPr><w:jc w:val="left"/><w:spacing w:line="280" w:lineRule="auto"/></w:pPr>{''.join(left_p_runs)}</w:p>
            </w:tc>
            <w:tc>
                <w:tcPr><w:tcW w:w="{col_width}" w:type="dxa"/><w:tcMar><w:top w:w="80" w:type="dxa"/><w:bottom w:w="80" w:type="dxa"/><w:left w:w="80" w:type="dxa"/><w:right w:w="40" w:type="dxa"/></w:tcMar></w:tcPr>
                <w:p><w:pPr><w:jc w:val="right"/><w:spacing w:line="280" w:lineRule="auto"/></w:pPr>{''.join(right_p_runs)}</w:p>
            </w:tc>
        </w:tr>
    </w:tbl>"""

def make_table(headers, rows, widths=None, aligns=None, total_width=8300):
    num_cols = len(headers)
    if not widths or len(widths) != num_cols:
        col_w = int(total_width / num_cols)
        widths = [col_w] * num_cols
        widths[-1] += (total_width - sum(widths))
        
    if not aligns or len(aligns) != num_cols:
        aligns = ["left"] * num_cols

    tbl = [f"""<w:tbl>
        <w:tblPr>
            <w:tblW w:w="{total_width}" w:type="dxa"/>
            <w:jc w:val="center"/>
            <w:tblBorders>
                <w:top w:val="single" w:sz="12" w:space="0" w:color="1A365D"/>
                <w:bottom w:val="single" w:sz="12" w:space="0" w:color="1A365D"/>
                <w:insideH w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
                <w:insideV w:val="none"/>
                <w:left w:val="none"/>
                <w:right w:val="none"/>
            </w:tblBorders>
        </w:tblPr>"""]
    
    # Header row
    tbl.append('<w:tr><w:trPr><w:tblHeader/><w:cantSplit/></w:trPr>')
    for idx, h in enumerate(headers):
        esc_h = xml_escape(str(h))
        w = widths[idx]
        al = aligns[idx]
        tbl.append(f"""<w:tc>
            <w:tcPr>
                <w:tcW w:w="{w}" w:type="dxa"/>
                <w:shd w:val="clear" w:color="auto" w:fill="1A365D"/>
                <w:tcMar><w:top w:w="120" w:type="dxa"/><w:bottom w:w="120" w:type="dxa"/><w:left w:w="120" w:type="dxa"/><w:right w:w="120" w:type="dxa"/></w:tcMar>
            </w:tcPr>
            <w:p>
                <w:pPr>
                    <w:jc w:val="{al}"/>
                    <w:spacing w:after="0" w:line="240" w:lineRule="auto"/>
                    <w:rPr>
                        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
                        <w:b/>
                        <w:color w:val="FFFFFF"/>
                        <w:sz w:val="20"/>
                    </w:rPr>
                </w:pPr>
                <w:r>
                    <w:rPr>
                        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
                        <w:b/>
                        <w:color w:val="FFFFFF"/>
                        <w:sz w:val="20"/>
                    </w:rPr>
                    <w:t>{esc_h}</w:t>
                </w:r>
            </w:p>
        </w:tc>""")
    tbl.append('</w:tr>')
    
    # Body rows with alternating zebra striping
    for row_idx, r in enumerate(rows):
        shd_color = "F8FAFC" if (row_idx % 2 == 1) else "FFFFFF"
        tbl.append('<w:tr><w:trPr><w:cantSplit/></w:trPr>')
        for idx, c in enumerate(r):
            esc_c = xml_escape(str(c))
            w = widths[idx]
            al = aligns[idx]
            b_tag = '<w:b/>' if (idx == 0 and len(r) > 2 and not esc_c.startswith(('1.', '2.', '3.'))) else ''
            
            tbl.append(f"""<w:tc>
                <w:tcPr>
                    <w:tcW w:w="{w}" w:type="dxa"/>
                    <w:shd w:val="clear" w:color="auto" w:fill="{shd_color}"/>
                    <w:tcMar><w:top w:w="90" w:type="dxa"/><w:bottom w:w="90" w:type="dxa"/><w:left w:w="120" w:type="dxa"/><w:right w:w="120" w:type="dxa"/></w:tcMar>
                </w:tcPr>
                <w:p>
                    <w:pPr>
                        <w:jc w:val="{al}"/>
                        <w:spacing w:after="0" w:line="240" w:lineRule="auto"/>
                        <w:rPr>
                            <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
                            {b_tag}
                            <w:sz w:val="20"/>
                        </w:rPr>
                    </w:pPr>
                    <w:r>
                        <w:rPr>
                            <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
                            {b_tag}
                            <w:sz w:val="20"/>
                        </w:rPr>
                        <w:t>{esc_c}</w:t>
                    </w:r>
                </w:p>
            </w:tc>""")
        tbl.append('</w:tr>')
        
    tbl.append('</w:tbl>')
    return "".join(tbl)

def make_drawing(rel_id, cx=5400000, cy=3200000, caption=""):
    global doc_pr_counter
    doc_pr_counter += 1
    doc_id = doc_pr_counter
    pic_id = doc_id
    
    cap_para = ""
    if caption:
        # Split caption into Figure No and title
        cap_parts = caption.split(":", 1)
        if len(cap_parts) == 2:
            fig_no = xml_escape(cap_parts[0].strip() + ":")
            fig_title = xml_escape(" " + cap_parts[1].strip())
            runs = f"""<w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="21"/></w:rPr><w:t xml:space="preserve">{fig_no}</w:t></w:r><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:i/><w:sz w:val="21"/></w:rPr><w:t xml:space="preserve">{fig_title}</w:t></w:r>"""
        else:
            runs = f"""<w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="21"/></w:rPr><w:t xml:space="preserve">{xml_escape(caption)}</w:t></w:r>"""
            
        cap_para = f"""<w:p>
            <w:pPr>
                <w:jc w:val="center"/>
                <w:spacing w:before="90" w:after="220" w:line="260" w:lineRule="auto"/>
                <w:rPr><w:sz w:val="21"/></w:rPr>
            </w:pPr>
            {runs}
        </w:p>"""
        
    drawing_xml = f"""<w:p>
        <w:pPr>
            <w:keepNext/>
            <w:jc w:val="center"/>
            <w:spacing w:before="160" w:after="60"/>
        </w:pPr>
        <w:r>
            <w:drawing>
                <wp:inline distT="0" distB="0" distL="0" distR="0">
                    <wp:extent cx="{cx}" cy="{cy}"/>
                    <wp:effectExtent l="0" t="0" r="0" b="0"/>
                    <wp:docPr id="{doc_id}" name="Picture{doc_id}"/>
                    <wp:cNvGraphicFramePr>
                        <a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>
                    </wp:cNvGraphicFramePr>
                    <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
                        <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
                            <pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
                                <pic:nvPicPr>
                                    <pic:cNvPr id="{pic_id}" name="Picture{pic_id}"/>
                                    <pic:cNvPicPr/>
                                </pic:nvPicPr>
                                <pic:blipFill>
                                    <a:blip r:embed="{rel_id}"/>
                                    <a:stretch><a:fillRect/></a:stretch>
                                </pic:blipFill>
                                <pic:spPr>
                                    <a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
                                    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
                                    <a:ln w="9525">
                                        <a:solidFill><a:srgbClr val="CBD5E0"/></a:solidFill>
                                    </a:ln>
                                </pic:spPr>
                            </pic:pic>
                        </a:graphicData>
                    </a:graphic>
                </wp:inline>
            </w:drawing>
        </w:r>
    </w:p>
    {cap_para}"""
    return drawing_xml

# Tables Data with Custom Widths & Alignments
TABLE_DATA = {
    "2.1": {
        "headers": ["Study & Year", "Forecasting", "Calibration", "POS Sync", "Spatial Triage", "Generic Engine", "Empirical Evaluation"],
        "rows": [
            ["Sharma et al. (2021)", "None", "None", "Annual Survey", "None", "None", "420 Retail Chemists (NCR)"],
            ["Patel & Rao (2022)", "1–7 Days ARIMA", "Uncalibrated", "Nightly Batch", "None", "None", "65 Secondary Hospitals"],
            ["Rajagopal (2023)", "None", "None", "Static Inventory", "Static 2SFCA", "None", "Suburban Tamil Nadu Wards"],
            ["Chen et al. (2024)", "Offline Batch", "Calibrated Platt", "Benchmark Logs", "None", "None", "Synthetic MIMIC-IV Subset"],
            ["Kumar & Nair (2024)", "None", "None", "Field Interviews", "None", "Manual Match", "14 Tamil Nadu Districts"],
            ["Aris & Gomez (2024)", "None", "None", "DLT Hyperledger", "None", "None", "12-Node Pilot IoT Network"],
            ["MedRadar v2 (Ours)", "1–30 Days HGBR", "Isotonic PAVA L2", "Light REST Webhooks", "Haversine Geodesic", "PMBJP Jan Aushadhi", "18 Kanchipuram Pharmacies (175k)"]
        ],
        "widths": [1400, 1100, 1100, 1100, 1100, 1100, 1400],
        "aligns": ["left", "center", "center", "center", "center", "center", "left"]
    },
    "3.1": {
        "headers": ["Attribute Name", "Data Type", "Constraints / Domain", "Operational Significance in MedRadar v2 Pipeline"],
        "rows": [
            ["date", "DATE", "2020-01-01 to 2025-12-31", "Primary temporal index; continuous daily calendar timestamp"],
            ["pharmacy_id", "INT", "1 to 18 (Unique FK)", "Spatial entity identifier across Kanchipuram retail pharmacy network"],
            ["medicine_name", "VARCHAR(100)", "10 Core Essential Molecules", "Standardized International Nonproprietary Name (INN)"],
            ["category", "VARCHAR(50)", "5 Pharmacological Classes", "Therapeutic classification (Antibiotic, Antidiabetic, Analgesic, etc.)"],
            ["units_sold", "INT", "0 to 10,640 units/day", "Daily consumer dispensing volume; primary target for ML regression"],
            ["stock_level", "INT", "0 to 5,124 units on shelf", "Real-time physical shelf inventory balance at close-of-business"],
            ["reorder_level", "INT", "Safety stock threshold", "Dynamic safety buffer triggering automated restocking alerts"],
            ["unit_price", "DECIMAL(8,2)", "₹5.00 to ₹100.00 / strip", "Commercial retail selling price per pharmaceutical dispensing unit"],
            ["expiry_days", "INT", "30 to 719 days remaining", "Batch expiration runway informing FIFO dispatch and waste minimization"],
            ["supplier_lead_time", "INT", "1 to 14 days", "Wholesale distributor fulfillment turnaround latency"],
            ["is_pandemic_surge", "TINYINT", "{0, 1} Binary Flag", "Epidemiological regime shift indicator for COVID-19 epidemic waves"]
        ],
        "widths": [1500, 900, 1900, 4000],
        "aligns": ["left", "center", "center", "left"]
    },
    "3.2": {
        "headers": ["Statistical Metric", "Units Sold (units)", "Stock Level (units)", "Unit Price (₹)", "Expiry Runway (days)", "Rolling 7d Velocity"],
        "rows": [
            ["Sample Count (N)", "175,360", "175,360", "175,360", "175,360", "175,360"],
            ["Arithmetic Mean (μ)", "454.63", "4,553.13", "₹52.55", "374.14", "455.92"],
            ["Standard Deviation (σ)", "350.96", "346.42", "₹27.42", "199.77", "199.79"],
            ["Median (Q2)", "390.00", "4,598.00", "₹52.61", "374.00", "417.86"],
            ["Interquartile Range (IQR)", "248.00", "292.00", "₹47.51", "346.00", "215.29"],
            ["Min / Max Range", "31 / 10,640", "0 / 5,124", "₹5.00 / ₹100.00", "30 / 719", "145 / 6,684"],
            ["Skewness Coefficient (γ₁)", "+7.73", "-5.53", "-0.00", "+0.00", "+2.22"],
            ["Excess Kurtosis (γ₂)", "+101.08", "+53.58", "-1.20", "-1.20", "+16.91"]
        ],
        "widths": [1800, 1300, 1300, 1300, 1300, 1300],
        "aligns": ["left", "right", "right", "right", "right", "right"]
    },
    "3.3": {
        "headers": ["Denoising Filter Architecture", "Output SNR (dB)", "Signal Power", "Residual Noise Power", "Variance Reduction", "Mean Absolute Error"],
        "rows": [
            ["Savitzky-Golay (w=7, p=2)", "23.06 dB", "1.48 × 10⁹", "7.34 × 10⁶", "4.44%", "1,984.76"],
            ["EWMA Filter (span=7, α=0.25)", "23.81 dB", "1.49 × 10⁹", "6.18 × 10⁶", "4.38%", "1,821.54"],
            ["Rolling Median Filter (window=7)", "22.68 dB", "1.46 × 10⁹", "7.86 × 10⁶", "6.52% (Winning)", "1,825.15"]
        ],
        "widths": [2300, 1200, 1200, 1200, 1200, 1200],
        "aligns": ["left", "right", "right", "right", "right", "right"]
    },
    "3.4": {
        "headers": ["Feature Modality", "Engineered Predictor Names", "Mathematical Formulation", "Logistical & Behavioral Significance"],
        "rows": [
            ["Temporal Demand Lags", "lag_1, lag_2, lag_3, lag_7, lag_14, lag_30", "D(t - k), k ∈ {1, 2, 3, 7, 14, 30}", "Captures short- and long-term autoregressive demand persistence"],
            ["Rolling Statistics", "rolling_3d_mean, 7d, 14d, rolling_7d_std", "(1/k) ∑ D(t - i); sample standard dev", "Measures instantaneous consumption momentum and demand volatility"],
            ["Trigonometric Calendar", "dow_sin, dow_cos, month_sin, month_cos", "sin/cos(2π · t / period)", "Encodes continuous weekly and seasonal disease cycle periodicities"],
            ["Inventory Depletion", "stock_cover_days, burn_rate, expiry_risk_index", "I(t)/MA_7d; D(t-1)/I(t); 100/(T_exp - t)", "Quantifies stockout countdown runway and batch expiration pressure"],
            ["Supply Chain Friction", "lead_time_stress_index, is_pandemic_surge", "lead_time × (1 + overdue_delay)", "Models distributor transit friction and macroeconomic shock waves"]
        ],
        "widths": [1600, 2200, 2000, 2500],
        "aligns": ["left", "left", "left", "left"]
    },
    "3.5": {
        "headers": ["Pharmacy Name & Facility", "Latitude", "Longitude", "Spatial Ward / Jurisdiction", "24x7 Casualty", "Cold Storage"],
        "rows": [
            ["1. Apollo Pharmacy Central", "12.8342° N", "79.7036° E", "Bus Stand Commercial Hub", "Yes", "Yes"],
            ["2. MedPlus Gandhi Road", "12.8315° N", "79.7078° E", "Gandhi Road Commercial Ward", "No", "Yes"],
            ["3. Jan Aushadhi Kendra (Kanchi)", "12.8351° N", "79.7042° E", "Moffusil Bus Stand North", "No", "No"],
            ["4. Sri Krishna Medicals", "12.8384° N", "79.7001° E", "Hospital Road Medical Corridor", "Yes", "Yes"],
            ["5. Kanchi HQ Hospital Chemist", "12.8390° N", "79.6995° E", "District Headquarters Campus", "Yes", "Yes"],
            ["6. Meenakshi Pharmacy Enathur", "12.8712° N", "79.7124° E", "Enathur University Belt", "Yes", "Yes"],
            ["7. SCSVMV Campus Dispensary", "12.8725° N", "79.7138° E", "SCSVMV University Campus", "No", "No"],
            ["8. Balaji Pharmacy Tollgate", "12.8510° N", "79.6845° E", "Bangalore Highway Tollgate", "Yes", "Yes"],
            ["9. Kumaran Pharmacy Walajabad", "12.7954° N", "79.8152° E", "Walajabad Highway Link", "No", "No"],
            ["10. Sriperumbudur Medicare", "12.9684° N", "79.9421° E", "Industrial Corridor Junction", "Yes", "Yes"]
        ],
        "widths": [2400, 1000, 1000, 1900, 1000, 1000],
        "aligns": ["left", "center", "center", "left", "center", "center"]
    },
    "3.6": {
        "headers": ["Generic Molecule & Strength", "Commercial Branded Equivalent", "Branded Retail MRP", "PMBJP Generic Price", "Direct Consumer Savings"],
        "rows": [
            ["Paracetamol 650mg", "Dolo-650 (Micro Labs)", "₹34.50 / 15 tabs", "₹7.20 / 10 tabs", "79.1% Savings"],
            ["Metformin 500mg SR", "Glycomet-500 (USV)", "₹48.00 / 20 tabs", "₹12.50 / 20 tabs", "74.0% Savings"],
            ["Amlodipine 5mg", "Amlopres-5 (Cipla)", "₹42.00 / 15 tabs", "₹6.80 / 10 tabs", "83.8% Savings"],
            ["Azithromycin 500mg", "Azithral-500 (Alembic)", "₹128.00 / 5 tabs", "₹38.00 / 5 tabs", "70.3% Savings"],
            ["Amoxicillin 500mg", "Mox-500 (Sun Pharma)", "₹85.00 / 10 caps", "₹24.00 / 10 caps", "71.8% Savings"],
            ["Atorvastatin 10mg", "Atorva-10 (Zydus)", "₹98.00 / 15 tabs", "₹16.50 / 10 tabs", "83.2% Savings"],
            ["Salbutamol Inhaler 100mcg", "Asthalin (Cipla)", "₹165.00 / canister", "₹62.00 / canister", "62.4% Savings"],
            ["Comprehensive Basket Mean", "10 Therapeutic Classes", "--", "--", "76.06% Direct Savings"]
        ],
        "widths": [2000, 1900, 1400, 1400, 1600],
        "aligns": ["left", "left", "right", "right", "right"]
    },
    "3.7": {
        "headers": ["Entity Table Name", "Primary Key", "Foreign Keys", "Core Relational Attributes", "Operational Function"],
        "rows": [
            ["users", "id (INT PK)", "pharmacy_id → pharmacies", "username, password_hash, role", "Role-based authentication (RBAC)"],
            ["pharmacies", "id (INT PK)", "None", "name, address, lat, lon, phone", "GIS coordinates & operational metadata"],
            ["medicines", "id (INT PK)", "None", "brand_name, generic_name, mrp", "Standardized ATC drug catalog & pricing"],
            ["inventory", "id (INT PK)", "pharmacy_id, medicine_id", "current_stock, batch_no, expiry_date", "Live on-shelf physical inventory balances"],
            ["transactions", "id (INT PK)", "pharmacy_id, medicine_id", "units_sold, sale_price, timestamp", "Immutable POS transactional dispensing logs"],
            ["stock_audits", "id (INT PK)", "pharmacy_id, medicine_id", "reported_stock, verified_by, hash", "Cryptographic SHA-256 physical audit trail"],
            ["prescriptions", "id (INT PK)", "user_id → users", "file_path, status, verified_at", "Citizen prescription OCR and digital verification"],
            ["delivery_orders", "id (INT PK)", "pharmacy_id, user_id", "delivery_address, total_amount, step", "Emergency doorstep dispatch and fulfillment"]
        ],
        "widths": [1300, 1100, 1600, 2300, 2000],
        "aligns": ["left", "center", "left", "left", "left"]
    },
    "4.1": {
        "headers": ["Endpoint URI", "HTTP Method", "Request Payload / Query Parameters", "Response Schema", "Operational Microservice Function"],
        "rows": [
            ["/api/predict", "GET", "medicine_id, horizon_days", "JSON {predictions: [...]}", "Multi-day demand regression forecasting"],
            ["/api/stock", "GET", "medicine_id, pharmacy_id", "JSON {stock: N, status: S}", "Real-time on-shelf physical inventory balance"],
            ["/api/heatmap", "GET", "medicine_id (optional)", "JSON {zones: [...], nodes: [...]}", "Geospatial shortage density cluster mapping"],
            ["/api/sos", "POST", "symptom, user_lat, user_lon", "JSON {dispatches: [...]}", "Haversine geodesic emergency triage routing"],
            ["/api/audit", "POST", "pharmacy_id, medicine_id, units", "JSON {status: 'ok', hash: H}", "Cryptographic POS physical audit verification"],
            ["/api/generic_savings", "GET", "brand_id or generic_id", "JSON {savings_pct: P, Kendras}", "PMBJP Jan Aushadhi price comparison"],
            ["/api/subscribe", "POST", "phone, medicine_id, channel", "JSON {subscription_id: ID}", "Restock notification and SMS push dispatcher"],
            ["/api/deliveries", "POST", "order_id, user_id, items, address", "JSON {tracking_step: S, eta: T}", "Doorstep order fulfillment and courier tracking"]
        ],
        "widths": [1500, 800, 2000, 1800, 2200],
        "aligns": ["left", "center", "left", "left", "left"]
    },
    "4.2": {
        "headers": ["Regression Architecture", "Mean Absolute Error", "Root Mean Sq Error", "R² Score", "Adjusted R²", "MAPE %", "Training Latency"],
        "rows": [
            ["Ordinary Least Squares (OLS)", "97.98 units", "128.01 units", "0.7836", "0.7834", "30.82%", "0.10 s"],
            ["Ridge Regression (L2, α=1.0)", "97.98 units", "128.01 units", "0.7836", "0.7834", "30.82%", "0.29 s"],
            ["Lasso Regression (L1, α=0.1)", "97.98 units", "128.00 units", "0.7836", "0.7834", "30.82%", "0.75 s"],
            ["Random Forest (Trees=100)", "74.85 units", "117.80 units", "0.8167", "0.8166", "23.41%", "2.63 s"],
            ["HistGradientBoosting (Winning)", "66.22 units", "104.10 units", "0.8569", "0.8568", "20.06%", "0.92 s"]
        ],
        "widths": [2300, 1000, 1000, 1000, 1000, 1000, 1000],
        "aligns": ["left", "right", "right", "right", "right", "right", "right"]
    },
    "4.3": {
        "headers": ["Classifier Architecture", "ROC-AUC", "PR-AUC", "Accuracy", "Precision", "Recall", "F1-Score", "Brier Score"],
        "rows": [
            ["Baseline Decision Tree", "0.9999", "0.9114", "99.97%", "90.91%", "88.89%", "0.8989", "0.0002"],
            ["L2 Logistic (Uncalibrated)", "1.0000", "0.9941", "99.99%", "95.56%", "95.56%", "0.9556", "0.0001"],
            ["Isotonic Calibrated L2 (Winning)", "1.0000", "0.9941", "99.99%", "95.56%", "95.56%", "0.9556", "0.0001"]
        ],
        "widths": [2000, 900, 900, 900, 900, 900, 900, 900],
        "aligns": ["left", "right", "right", "right", "right", "right", "right", "right"]
    },
    "4.4": {
        "headers": ["Spatial Ward / Cluster", "Mapped Pharmacies", "Shortage Risk %", "Risk Classification", "Actionable Logistical Mandate"],
        "rows": [
            ["1. Central Bus Stand Hub (Wards 1–8)", "4 Pharmacies", "38.5%", "CRITICAL SHORTAGE (>35%)", "Immediate priority warehouse replenishment"],
            ["2. Hospital Road Zone (Wards 9–16)", "3 Pharmacies", "26.2%", "ELEVATED RISK (22–35%)", "Lateral inventory rebalancing from Enathur"],
            ["3. Gandhi Road Core (Wards 17–28)", "4 Pharmacies", "14.8%", "MODERATE RISK (12–22%)", "Continuous monitoring of retail dispensing"],
            ["4. Enathur Corridor (Wards 29–36)", "3 Pharmacies", "6.5%", "NORMAL SUPPLY (<12%)", "Designated regional buffer supply donor depot"],
            ["5. Orikkai & Southern (Wards 37–45)", "4 Pharmacies", "11.2%", "NORMAL SUPPLY (<12%)", "Stable maintenance replenishment cycle"]
        ],
        "widths": [2300, 1100, 1100, 1800, 2000],
        "aligns": ["left", "center", "right", "left", "left"]
    },
    "4.5": {
        "headers": ["Chronic Therapy Component", "Commercial Brand Cost", "PMBJP Generic Cost", "Annual Net Savings", "Relief Ratio"],
        "rows": [
            ["Metformin 500mg SR (2 tabs/day)", "₹1,752.00 / year", "₹456.25 / year", "₹1,295.75", "73.96% Relief"],
            ["Amlodipine 5mg (1 tab/day)", "₹1,022.00 / year", "₹248.20 / year", "₹773.80", "75.71% Relief"],
            ["Atorvastatin 10mg (1 tab/day)", "₹2,384.00 / year", "₹602.25 / year", "₹1,781.75", "74.74% Relief"],
            ["Salbutamol Inhaler (6 cans/year)", "₹990.00 / year", "₹372.00 / year", "₹618.00", "62.42% Relief"],
            ["Seasonal Antibiotic & Antipyretic", "₹820.00 / year", "₹195.00 / year", "₹625.00", "76.22% Relief"],
            ["Single-Patient Maintenance Basket", "₹6,968.00 / year", "₹1,873.70 / year", "₹5,094.30", "73.11% Relief"],
            ["Two-Patient Multi-Gen Household", "₹13,936.00 / year", "₹3,747.40 / year", "₹10,188.60", "73.11% Relief"]
        ],
        "widths": [2300, 1500, 1500, 1500, 1500],
        "aligns": ["left", "right", "right", "right", "right"]
    },
    "4.6": {
        "headers": ["Test Suite Category", "Invocation Volume", "Target Microservice / Module", "Verification Criteria", "Execution Status"],
        "rows": [
            ["Database Schema & Tables", "8 Entity Tests", "db.py (SQLite/MySQL)", "8 tables schema verified", "100% PASS"],
            ["ML Model Snapshot Integrity", "5 Model Tests", "snapshot.pkl", "HGBR & Calibrated Logistic", "100% PASS"],
            ["Multi-Day Prediction API", "10 API Probes", "/api/predict", "1–30d forecasts & bounds", "100% PASS"],
            ["Emergency SOS Dispatch", "8 Routing Tests", "/api/sos", "Haversine 24x7 route logic", "100% PASS"],
            ["POS Audit Cryptographic Trail", "6 Tests", "/api/audit", "SHA-256 hash chaining", "100% PASS"],
            ["Generic Jan Aushadhi Engine", "5 Tests", "/api/generic_savings", "76% savings calculation", "100% PASS"],
            ["Dual-Database Failover", "4 Tests", "db.py connection pool", "Zero-latency SQLite fallback", "100% PASS"],
            ["End-to-End Test Suite Execution", "46 Assertions", "Complete System Integration", "All assertions validated", "100% PASS (0.42s)"]
        ],
        "widths": [2200, 1300, 1600, 1800, 1400],
        "aligns": ["left", "center", "left", "left", "center"]
    },
    "5.1": {
        "headers": ["Phase & Quarter", "Module / Capability", "Technical Specifications & Planned Deliverables"],
        "rows": [
            ["Q1 (Dec 2026–Jan 2027)", "IoT Smart Shelf Sensors", "Deploy ESP32 weight-sensor pads under high-velocity critical medicine trays for continuous telemetry."],
            ["Q1 (Jan–Feb 2027)", "Mobile PWA & Android App", "Native Kotlin Android client with offline SQLite caching, citizen SOS push, and restock notifications."],
            ["Q2 (Feb–Mar 2027)", "Deep Reinforcement Learning", "Proximal Policy Optimization (PPO) agents for autonomous multi-echelon inventory replenishment."],
            ["Q2 (Mar–Apr 2027)", "TNMSC State Integration", "Secure REST webhooks with Tamil Nadu Medical Services Corporation portal for regional warehouse sync."],
            ["Q3 (Apr–May 2027)", "Live Field Clinical Trial", "8-week prospective multi-pharmacy trial across Kanchipuram district to evaluate stockout reductions."]
        ],
        "widths": [1800, 2200, 4300],
        "aligns": ["left", "left", "left"]
    }
}

def render_section_blocks(sec_id, content, body_xml):
    """Parses section text into structured paragraphs, headings, code blocks, tables, and figures in exact sequence."""
    blocks = content.split("\n\n")
    
    for block in blocks:
        b_strip = block.strip()
        if not b_strip:
            continue
            
        # Code block handling
        if "```" in b_strip:
            parts = b_strip.split("```")
            before = parts[0].strip()
            code = parts[1].strip()
            if code.startswith("python"):
                code = code[6:].strip()
            if before:
                body_xml.append(make_para(before, first_indent=0))
            body_xml.append(make_code_block(code))
            continue
            
        # Handle Subsection Headings (e.g., "3.3.1", "3.4.2", "4.2.2")
        lines = b_strip.split("\n")
        first_line = lines[0].strip()
        
        if re.match(r'^\d\.\d\.\d(\s+|$)', first_line):
            body_xml.append(make_heading(first_line, level=3))
            if len(lines) > 1:
                rem_text = "\n".join(lines[1:]).strip()
            else:
                rem_text = ""
        else:
            rem_text = b_strip
            
        if not rem_text:
            continue
            
        # Check for Tables
        table_matched = False
        for t_key in TABLE_DATA:
            if rem_text.startswith(f"Table {t_key}:"):
                t_info = TABLE_DATA[t_key]
                first_row = rem_text.split("\n")[0].strip()
                body_xml.append(make_para(first_row, bold=True, size=21, space_before=180, space_after=60, first_indent=0, keep_next=True))
                body_xml.append(make_table(t_info["headers"], t_info["rows"], widths=t_info["widths"], aligns=t_info["aligns"]))
                table_matched = True
                break
        if table_matched:
            continue
            
        if rem_text.startswith("Table 5.1"):
            t_info = TABLE_DATA["5.1"]
            body_xml.append(make_para("Table 5.1: Phase-II Engineering Roadmap & Technical Deliverables", bold=True, size=21, space_before=180, space_after=60, first_indent=0, keep_next=True))
            body_xml.append(make_table(t_info["headers"], t_info["rows"], widths=t_info["widths"], aligns=t_info["aligns"]))
            continue

        # Check for standalone mathematical equations
        if rem_text.startswith(("VIF_j =", "d = 2R", "C_{commercial} =", "Audit_Hash =", "L(w) =", "P(y = 1")):
            body_xml.append(make_formula_block(rem_text))
            continue

        # Render normal paragraph or structured list
        if re.match(r'^(\d+\.|\-)\s', rem_text):
            body_xml.append(make_para(rem_text, first_indent=720, hanging_indent=360, space_after=80))
        elif rem_text.startswith(("Tier ", "Hypothesis ", "Algorithm ", "Listing ")):
            body_xml.append(make_para(rem_text, first_indent=0, bold=False, space_after=100))
        else:
            body_xml.append(make_para(rem_text, first_indent=720, space_after=110))

        # Check for Drawings immediately following the paragraph that references them
        if sec_id == "3.1" and "Figure 3.1" in rem_text:
            body_xml.append(make_drawing("rId21", cx=5400000, cy=3130000, caption="Figure 3.1: MedRadar v2 Multi-Tier Distributed Healthcare Intelligence Architecture"))
        if sec_id == "3.4" and "Figure 3.2" in rem_text:
            body_xml.append(make_drawing("rId22", cx=5400000, cy=3850000, caption="Figure 3.2: Time-Series Signal Smoothing & Noise Filtering Comparison"))
        if sec_id == "3.4" and "Figure 3.3" in rem_text:
            body_xml.append(make_drawing("rId23", cx=5200000, cy=4160000, caption="Figure 3.3: Pearson Correlation Heatmap & Feature Multicollinearity Matrix"))
        if sec_id == "3.7" and "Figure 3.4" in rem_text:
            body_xml.append(make_drawing("rId24", cx=5400000, cy=2920000, caption="Figure 3.4: Emergency SOS Triage & Rapid Doorstep Dispatch Workflow"))
        if sec_id == "3.8" and "Figure 3.5" in rem_text:
            body_xml.append(make_drawing("rId25", cx=5400000, cy=2870000, caption="Figure 3.5: PMBJP Jan Aushadhi Generic Medicine Optimization Engine"))
        if sec_id == "3.9" and "Figure 3.6" in rem_text:
            body_xml.append(make_drawing("rId26", cx=5400000, cy=3350000, caption="Figure 3.6: MedRadar v2 Relational Database Schema & Entity Relationships"))

        if sec_id == "4.1" and "Figure 4.1" in rem_text:
            body_xml.append(make_drawing("rId31", cx=5400000, cy=2670000, caption="Figure 4.1: Cryptographic Point-of-Sale (POS) Audit Telemetry Verification Workflow"))
        if sec_id == "4.2" and "Figure 4.2" in rem_text:
            body_xml.append(make_drawing("rId32", cx=5400000, cy=3240000, caption="Figure 4.2: Relative Predictive Feature Weight Distribution (Gini Importance)"))
        if sec_id == "4.2" and "Figure 4.3" in rem_text:
            body_xml.append(make_drawing("rId33", cx=5400000, cy=1680000, caption="Figure 4.3: Regression Residual Distribution & Q-Q Diagnostics for Winning Regressor"))
        if sec_id == "4.3" and "Figure 4.4" in rem_text:
            body_xml.append(make_drawing("rId34", cx=5400000, cy=2310000, caption="Figure 4.4: Receiver Operating Characteristic (ROC) & Precision-Recall (PR) Curves"))
        if sec_id == "4.4" and "Figure 4.5" in rem_text:
            body_xml.append(make_drawing("rId35", cx=5400000, cy=3500000, caption="Figure 4.5: MedRadar Geospatial Medicine Shortage Heatmap: Kanchipuram Regional Network"))

def build_docx_report():
    print("Building high-definition structured DOCX report strictly conforming to SCSVMV standards...")
    base_docx = "Report/SCVMV-CSE-Project Work Phase-I -Report Format.docx"
    fixed_docx = "Report/MedRadar_Phase_1_Project_Report_Final_Fixed.docx"
    final_docx = "Report/MedRadar_Phase_1_Project_Report_Final.docx"
    temp_dir = "Report/docx_workspace"
    
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)
    
    # Extract base docx
    with zipfile.ZipFile(base_docx, 'r') as z:
        z.extractall(temp_dir)
        
    media_dir = os.path.join(temp_dir, "word", "media")
    os.makedirs(media_dir, exist_ok=True)
    
    # Map all figures & images to proper IDs and target media filenames
    image_specs = [
        ("rId8",  "Report/assets/image1.jpeg", "word/media/image1.jpeg", "media/image1.jpeg"),
        ("rId9",  "Report/assets/image2.jpeg", "word/media/image2.jpeg", "media/image2.jpeg"),
        ("rId21", "Report/figures/figure_3_3_system_architecture.png", "word/media/figure_3_1.png", "media/figure_3_1.png"),
        ("rId22", "Report/assets/image5.png", "word/media/figure_3_2.png", "media/figure_3_2.png"),
        ("rId23", "Report/assets/image4.png", "word/media/figure_3_3.png", "media/figure_3_3.png"),
        ("rId24", "Report/figures/figure_3_5_sos_triage_flowchart.png", "word/media/figure_3_4.png", "media/figure_3_4.png"),
        ("rId25", "Report/figures/figure_3_6_generic_savings_flowchart.png", "word/media/figure_3_5.png", "media/figure_3_5.png"),
        ("rId26", "Report/figures/figure_3_4_database_er.png", "word/media/figure_3_6.png", "media/figure_3_6.png"),
        ("rId31", "Report/figures/figure_4_5_pos_audit_workflow.png", "word/media/figure_4_1.png", "media/figure_4_1.png"),
        ("rId32", "Report/assets/image6.png", "word/media/figure_4_2.png", "media/figure_4_2.png"),
        ("rId33", "Report/assets/image7.png", "word/media/figure_4_3.png", "media/figure_4_3.png"),
        ("rId34", "Report/assets/image8.png", "word/media/figure_4_4.png", "media/figure_4_4.png"),
        ("rId35", "Report/figures/figure_4_4_kanchipuram_heatmap.png", "word/media/figure_4_5.png", "media/figure_4_5.png")
    ]
    
    for rid, src_path, target_path, target_media in image_specs:
        if os.path.exists(src_path):
            shutil.copy(src_path, os.path.join(temp_dir, target_path))
        else:
            print(f"Warning: source image {src_path} not found!")
            
    # Update word/_rels/document.xml.rels
    rels_path = os.path.join(temp_dir, "word", "_rels", "document.xml.rels")
    with open(rels_path, "r", encoding="utf-8") as f:
        rels_content = f.read()
        
    for rid, src_path, target_path, target_media in image_specs:
        rel_entry = f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="{target_media}"/>'
        if rid in rels_content:
            rels_content = re.sub(rf'<Relationship[^>]*Id="{rid}"[^>]*/>', rel_entry, rels_content)
        else:
            rels_content = rels_content.replace('</Relationships>', f'{rel_entry}</Relationships>')
            
    with open(rels_path, "w", encoding="utf-8") as f:
        f.write(rels_content)
        
    # Ensure [Content_Types].xml includes png and jpeg
    ct_path = os.path.join(temp_dir, "[Content_Types].xml")
    with open(ct_path, "r", encoding="utf-8") as f:
        ct_content = f.read()
    if 'Extension="png"' not in ct_content:
        ct_content = ct_content.replace('<Types ', '<Types ><Default Extension="png" ContentType="image/png"/>')
    if 'Extension="jpeg"' not in ct_content:
        ct_content = ct_content.replace('<Types ', '<Types ><Default Extension="jpeg" ContentType="image/jpeg"/>')
    with open(ct_path, "w", encoding="utf-8") as f:
        f.write(ct_content)

    # Now construct the complete document.xml body elements in STRICT ORDER!
    body_xml = []
    
    # 1. Title Page (Exact SCSVMV format - Fits perfectly on Page 1)
    body_xml.append(make_drawing("rId8", cx=5100000, cy=1400000))
    body_xml.append(make_para("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING", align="center", bold=True, size=24, space_before=80, space_after=30, first_indent=0))
    body_xml.append(make_para("BCSF187Z50  PROJECT WORK PHASE – I", align="center", bold=True, size=22, space_after=20, first_indent=0))
    body_xml.append(make_para("B.E. (Computer Science and Engineering)", align="center", bold=False, size=20, space_after=100, first_indent=0))
    
    # University Crest
    body_xml.append(make_drawing("rId9", cx=1500000, cy=1350000))
    
    body_xml.append(make_para("MEDRADAR: AI-DRIVEN REAL-TIME MEDICAL INTELLIGENCE AND GEOSPATIAL RESOURCE MAPPING PLATFORM", align="center", bold=True, size=27, space_before=120, space_after=100, line_spacing=300, first_indent=0))
    body_xml.append(make_para("BCSF187Z50 - PROJECT WORK PHASE-I REPORT", align="center", bold=True, size=22, space_after=20, first_indent=0))
    body_xml.append(make_para("Batch (2023-2027) (Semester VII)", align="center", bold=False, size=20, space_after=140, first_indent=0))
    
    # Clean Side-by-Side Table for Submitted By & Guided By
    sub_lines = [
        "SUBMITTED BY:",
        "G. TRIVIKRAM SIVAJI (Reg. No. 11239A029)",
        "Y. SESHU KUMAR (Reg. No. 11239A103)"
    ]
    guide_lines = [
        "GUIDED BY:",
        "Dr. T. SUNDAR, M.E., Ph.D.",
        "Assistant Professor, Department of CSE"
    ]
    body_xml.append(make_signature_table(sub_lines, guide_lines, col_width=4150))
    
    body_xml.append(make_para("DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING\nSRI CHANDRASEKHARENDRA SARASWATHI VISWA MAHAVIDYALAYA\n(Deemed to be University u/s 3 of UGC Act 1956)\nEnathur, Kanchipuram – 631 561\nNOVEMBER / DECEMBER 2026", align="center", bold=True, size=20, space_before=120, space_after=0, line_spacing=260, first_indent=0))
    
    # 2. Bonafide Certificate (Page II)
    body_xml.append(make_heading("BONAFIDE CERTIFICATE", level=1, page_break=True))
    body_xml.append(make_para("This is to certify that the PROJECT WORK PHASE-I Report entitled “MEDRADAR: AI-DRIVEN REAL-TIME MEDICAL INTELLIGENCE AND GEOSPATIAL RESOURCE MAPPING PLATFORM” is the bonafide work carried out by Mr. G. TRIVIKRAM SIVAJI (Reg. No. 11239A029) and Mr. Y. SESHU KUMAR (Reg. No. 11239A103) under my direct guidance during the academic year 2026–2027 in partial fulfillment of the requirements for the award of the Degree of Bachelor of Engineering in Computer Science and Engineering of Sri Chandrasekharendra Saraswathi Viswa Mahavidyalaya, Enathur, Kanchipuram.", space_before=160, space_after=280, line_spacing=400, first_indent=720))
    
    # Signatures: Guide & HOD in professional borderless 2-column table
    guide_sig = [
        "Dr. T. SUNDAR, M.E., Ph.D.",
        "Internal Guide & Assistant Professor",
        "Department of CSE, SCSVMV"
    ]
    hod_sig = [
        "Dr. M. SENTHIL KUMAR, M.E., Ph.D.",
        "Head of the Department",
        "Department of CSE, SCSVMV"
    ]
    body_xml.append(make_signature_table(guide_sig, hod_sig, col_width=4150))
    
    body_xml.append(make_para("Submitted for the project work viva - voce examination held on: _____________________\nPlace: Kanchipuram.\nDate:  _____________________", align="left", bold=True, size=21, space_before=240, space_after=180, first_indent=0))
    
    examiner_left = ["Internal Examiner", "Signature: _______________________"]
    examiner_right = ["External Examiner", "Signature: _______________________"]
    body_xml.append(make_signature_table(examiner_left, examiner_right, col_width=4150))

    # 3. Declaration (Page III)
    body_xml.append(make_heading("DECLARATION", level=1, page_break=True))
    body_xml.append(make_para("We hereby declare that the PROJECT WORK PHASE-I work titled “MEDRADAR: AI-DRIVEN REAL-TIME MEDICAL INTELLIGENCE AND GEOSPATIAL RESOURCE MAPPING PLATFORM” is an authentic record of original research work implemented and compiled by us. No ideas, processes, mathematical formulations, software algorithms, or words of others have been presented as our own work without due scholarly acknowledgment and academic citation.", space_before=160, space_after=140, line_spacing=360, first_indent=720))
    
    dec_points = [
        "1. There is no fabrication of data, telemetry streams, or experimental benchmark results compiled or analyzed.",
        "2. There is no falsification by manipulating physical data, distorting models, or intentionally changing or omitting critical findings.",
        "3. All scientific literature reviewed adheres strictly to contemporary peer-reviewed journal articles published after October 2020 and 2024 onwards according to SCSVMV standards.",
        "4. We understand that the project is liable to be rejected at any stage if it is discovered that significant plagiarized material or unauthorized code was incorporated, rendering the Degree awarded invalid."
    ]
    for dp in dec_points:
        body_xml.append(make_para(dp, first_indent=720, hanging_indent=360, space_after=80))
        
    dec_left = [
        "Place: Kanchipuram",
        "Date:  20-11-2026"
    ]
    dec_right = [
        "1. G. TRIVIKRAM SIVAJI (11239A029)",
        "2. Y. SESHU KUMAR (11239A103)"
    ]
    body_xml.append(make_para("", space_before=160, space_after=0))
    body_xml.append(make_signature_table(dec_left, dec_right, col_width=4150))

    # 4. Abstract (Page IV)
    body_xml.append(make_heading("ABSTRACT", level=1, page_break=True))
    body_xml.append(make_para(FRONT_MATTER_DATA["abstract"], space_before=160, space_after=160, line_spacing=360, first_indent=720))
    body_xml.append(make_para(f"Keywords: {'; '.join(FRONT_MATTER_DATA['keywords'])}.", bold=True, size=22, space_before=100, space_after=100, first_indent=0))

    # 5. Table of Contents (Page V)
    body_xml.append(make_heading("TABLE OF CONTENTS", level=1, page_break=True))
    toc_headers = ["Chapter", "Title", "Page No."]
    toc_rows = []
    for item in TABLE_OF_CONTENTS_DATA:
        num = item["num"] if item["num"] else ""
        indent = "    " * item["level"]
        toc_rows.append([num, indent + item["title"], item["page"]])
    body_xml.append(make_table(toc_headers, toc_rows, widths=[1300, 5900, 1100], aligns=["left", "left", "right"]))

    # 6. List of Tables (Page VII)
    body_xml.append(make_heading("LIST OF TABLES", level=1, page_break=True))
    lot_headers = ["Table No.", "Table Description", "Page No."]
    lot_rows = [[t["num"], t["title"], t["page"]] for t in LIST_OF_TABLES_DATA]
    body_xml.append(make_table(lot_headers, lot_rows, widths=[1500, 5700, 1100], aligns=["left", "left", "right"]))

    # 7. List of Figures (Page VIII)
    body_xml.append(make_heading("LIST OF FIGURES", level=1, page_break=True))
    lof_headers = ["Figure No.", "Figure Caption", "Page No."]
    lof_rows = [[f["num"], f["title"], f["page"]] for f in LIST_OF_FIGURES_DATA]
    body_xml.append(make_table(lof_headers, lof_rows, widths=[1500, 5700, 1100], aligns=["left", "left", "right"]))

    # 8. List of Abbreviations (Page IX)
    body_xml.append(make_heading("LIST OF ABBREVIATIONS", level=1, page_break=True))
    ab_headers = ["Abbreviation", "Full Technical Nomenclature"]
    ab_rows = [[a["abbrev"], a["meaning"]] for a in LIST_OF_ABBREVIATIONS_DATA]
    body_xml.append(make_table(ab_headers, ab_rows, widths=[2000, 6300], aligns=["left", "left"]))

    # 9. Chapter 1: Introduction (Page 1)
    body_xml.append(make_heading("CHAPTER 1", level=1, page_break=True))
    body_xml.append(make_heading("INTRODUCTION", level=1, page_break=False))
    for sec in CHAPTER1_CONTENT["sections"]:
        body_xml.append(make_heading(f"{sec['id']} {sec['title']}", level=2))
        render_section_blocks(sec['id'], sec['content'], body_xml)

    # 10. Chapter 2: Literature Survey (Page 6)
    body_xml.append(make_heading("CHAPTER 2", level=1, page_break=True))
    body_xml.append(make_heading("LITERATURE SURVEY", level=1, page_break=False))
    for sec in CHAPTER2_CONTENT["sections"]:
        body_xml.append(make_heading(f"{sec['id']} {sec['title']}", level=2))
        render_section_blocks(sec['id'], sec['content'], body_xml)

    # 11. Chapter 3: System Architecture and Methodology (Page 15)
    body_xml.append(make_heading("CHAPTER 3", level=1, page_break=True))
    body_xml.append(make_heading("SYSTEM ARCHITECTURE AND METHODOLOGY", level=1, page_break=False))
    for sec in CHAPTER3_CONTENT["sections"]:
        body_xml.append(make_heading(f"{sec['id']} {sec['title']}", level=2))
        render_section_blocks(sec['id'], sec['content'], body_xml)

    # 12. Chapter 4: Implementation, Results & Performance Evaluation (Page 39)
    body_xml.append(make_heading("CHAPTER 4", level=1, page_break=True))
    body_xml.append(make_heading("IMPLEMENTATION, RESULTS AND PERFORMANCE EVALUATION", level=1, page_break=False))
    for sec in CHAPTER4_CONTENT["sections"]:
        body_xml.append(make_heading(f"{sec['id']} {sec['title']}", level=2))
        render_section_blocks(sec['id'], sec['content'], body_xml)

    # 13. Chapter 5: Conclusion and Future Scope (Page 49)
    body_xml.append(make_heading("CHAPTER 5", level=1, page_break=True))
    body_xml.append(make_heading("CONCLUSION AND FUTURE SCOPE", level=1, page_break=False))
    for sec in CHAPTER5_CONTENT["sections"]:
        body_xml.append(make_heading(f"{sec['id']} {sec['title']}", level=2))
        render_section_blocks(sec['id'], sec['content'], body_xml)

    # 14. Timelines & Review Milestones (Page 53)
    body_xml.append(make_heading("PROJECT TIMELINES & REVIEW MILESTONES", level=1, page_break=True))
    tl_headers = ["Phase", "Timeline", "Activities & Milestones", "Review", "Expected Outcomes"]
    tl_rows = [[t["phase"], t["timeline"], t["activities"], t["review"], t["outcomes"]] for t in TIMELINES_DATA]
    body_xml.append(make_table(tl_headers, tl_rows, widths=[1500, 1400, 2300, 1500, 1600], aligns=["left", "left", "left", "left", "left"]))

    # 15. Publication Details (Page 54)
    body_xml.append(make_heading("PUBLICATION DETAILS & MANUSCRIPTS", level=1, page_break=True))
    for pub in PUBLICATIONS_DATA:
        body_xml.append(make_para(pub["title"], bold=True, size=23, space_before=140, space_after=50, first_indent=0, keep_next=True))
        body_xml.append(make_para(f"Authors: {pub['authors']}\nTarget Journal: {pub['journal']}\nStatus: {pub['status']}", bold=True, size=21, space_after=80, first_indent=0, keep_next=True))
        body_xml.append(make_para(f"Manuscript Abstract: {pub['abstract']}", italic=True, size=21, space_after=180, first_indent=720))

    # 16. IEEE References (Page 55)
    body_xml.append(make_heading("REFERENCES", level=1, page_break=True))
    body_xml.append(make_para("(Compiled strictly according to IEEE Referencing Style. All references are peer-reviewed articles published in referred journals from January 2024 onwards; no web links).", italic=True, size=21, space_after=160, first_indent=0, keep_next=True))
    ref_headers = ["Ref No.", "IEEE Bibliographic Citation"]
    ref_rows = [[f"[{r['id']}]", r["citation"]] for r in REFERENCES_DATA]
    body_xml.append(make_table(ref_headers, ref_rows, widths=[1100, 7200], aligns=["center", "left"]))

    # Section Properties (Preserve SCSVMV university border, A4 dimensions, margins, and footers)
    sectPr_xml = """<w:sectPr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
        <w:footerReference w:type="even" r:id="rId16"/>
        <w:footerReference w:type="default" r:id="rId17"/>
        <w:pgSz w:w="11909" w:h="16834" w:code="9"/>
        <w:pgMar w:top="1440" w:right="1800" w:bottom="2070" w:left="1800" w:header="720" w:footer="720" w:gutter="0"/>
        <w:pgBorders>
            <w:top w:val="twistedLines1" w:sz="18" w:space="1" w:color="auto"/>
            <w:left w:val="twistedLines1" w:sz="18" w:space="4" w:color="auto"/>
            <w:bottom w:val="twistedLines1" w:sz="18" w:space="1" w:color="auto"/>
            <w:right w:val="twistedLines1" w:sz="18" w:space="4" w:color="auto"/>
        </w:pgBorders>
        <w:cols w:space="720"/>
    </w:sectPr>"""
    
    full_document_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" 
            xmlns:cx="http://schemas.microsoft.com/office/drawing/2014/chartex" 
            xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" 
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" 
            xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" 
            xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" 
            xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" 
            xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" 
            xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
    <w:body>
        {''.join(body_xml)}
        {sectPr_xml}
    </w:body>
</w:document>"""

    # Write document.xml
    doc_path = os.path.join(temp_dir, "word", "document.xml")
    with open(doc_path, "w", encoding="utf-8") as f:
        f.write(full_document_xml)
        
    # Re-zip into fixed docx
    with zipfile.ZipFile(fixed_docx, "w", zipfile.ZIP_DEFLATED) as zip_out:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                abs_f = os.path.join(root, file)
                rel_f = os.path.relpath(abs_f, temp_dir)
                zip_out.write(abs_f, rel_f)
                
    shutil.rmtree(temp_dir)
    print(f"Successfully generated high-definition DOCX report: {fixed_docx} ({os.path.getsize(fixed_docx):,} bytes)")

    # Attempt to copy to final docx
    try:
        shutil.copy(fixed_docx, final_docx)
        print(f"Successfully synchronized to primary report: {final_docx}")
    except Exception as e:
        print(f"Notice: {final_docx} is locked ({e}). Fixed version is saved as {fixed_docx}")

    # Also synchronize all destination copies
    for extra_dst in [
        "Report/MedRadar_Phase_1_Project_Report.docx",
        "Report/MedRadar_Phase_1_Project_Report_Final.docx",
        "Report/Sanjeevani_Phase_1_Project_Report_Final_Fixed.docx",
        "Report/Sanjeevani_Phase_1_Project_Report_Final.docx",
        "Report/Sanjeevani_Phase_1_Project_Report.docx"
    ]:
        try:
            shutil.copy(fixed_docx, extra_dst)
            print(f"Synchronized to: {extra_dst}")
        except Exception as e:
            print(f"Notice for {extra_dst}: {e}")

if __name__ == "__main__":
    build_docx_report()
