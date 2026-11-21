# HTML Report Builder for MedRadar Phase-I Project Report
import os
import sys
import shutil

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

def generate_html_report(output_path="Report/MedRadar_Project_Report_Printable.html"):
    print("Generating comprehensive printable HTML report...")
    
    html = []
    html.append("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MedRadar - BCSF187Z50 Project Work Phase-I Report (SCSVMV CSE)</title>
<style>
/* ==========================================================================
   ACADEMIC THESIS STYLING FOR A4 PRINTING & DESKTOP PREVIEW
   Strictly adheres to SCSVMV CSE Department Project Guidelines
   Font: Times New Roman, 12pt, 1.5 Line Spacing, 1-inch (25.4mm) Margins
   ========================================================================== */

@page {
    size: A4 portrait;
    margin: 25.4mm;
    @top-right {
        content: "MedRadar: BCSF187Z50 Project Work Phase-I";
        font-family: "Times New Roman", Times, serif;
        font-size: 9pt;
        font-style: italic;
        color: #555;
    }
    @bottom-center {
        content: counter(page);
        font-family: "Times New Roman", Times, serif;
        font-size: 10pt;
    }
}

@page :first {
    margin: 15mm 25.4mm 20mm 25.4mm;
    @top-right { content: normal; }
    @bottom-center { content: normal; }
}

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 0;
    background-color: #F0F2F5;
    font-family: "Times New Roman", Times, serif;
    font-size: 12pt;
    line-height: 1.5;
    color: #111;
    text-align: justify;
    text-justify: inter-word;
}

/* Floating Action Toolbar (Hidden during Print) */
.toolbar-bar {
    position: sticky;
    top: 0;
    z-index: 1000;
    background: #1A365D;
    color: white;
    padding: 10px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 14px;
}
.toolbar-title {
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 8px;
}
.toolbar-actions {
    display: flex;
    gap: 12px;
}
.btn-print {
    background: #3182CE;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 6px;
    transition: background 0.2s;
}
.btn-print:hover {
    background: #2B6CB0;
}
.select-chapter {
    padding: 7px 12px;
    border-radius: 4px;
    border: 1px solid #CBD5E0;
    font-size: 13px;
    background: white;
    color: #2D3748;
}

/* Document Container */
.document-container {
    max-width: 210mm;
    margin: 25px auto;
    background: white;
    padding: 25.4mm;
    box-shadow: 0 4px 20px rgba(0,0,0,0.12);
}

/* Page Break Utility */
.page-break {
    page-break-before: always;
    break-before: page;
}

.chapter-start {
    page-break-before: always;
    break-before: page;
    padding-top: 10mm;
}

/* Typography */
h1.doc-title {
    font-size: 18pt;
    font-weight: bold;
    text-align: center;
    margin: 15px 0 25px 0;
    line-height: 1.3;
    text-transform: uppercase;
}

h1.chapter-title {
    font-size: 16pt;
    font-weight: bold;
    text-align: center;
    text-transform: uppercase;
    margin: 0 0 25px 0;
    letter-spacing: 0.5px;
}

h2.section-title {
    font-size: 14pt;
    font-weight: bold;
    margin: 25px 0 12px 0;
    color: #000;
}

h3.subsection-title {
    font-size: 12.5pt;
    font-weight: bold;
    margin: 18px 0 8px 0;
    color: #111;
}

p {
    margin: 0 0 12px 0;
    text-indent: 0.4in;
    line-height: 1.5;
}

p.no-indent {
    text-indent: 0;
}

/* Cover Page Elements */
.cover-header {
    text-align: center;
    margin-bottom: 20px;
}
.cover-header img {
    max-width: 100%;
    height: auto;
    max-height: 75px;
}
.cover-subhdr {
    font-size: 13pt;
    font-weight: bold;
    margin-top: 8px;
    letter-spacing: 0.5px;
}
.cover-crest {
    text-align: center;
    margin: 25px 0;
}
.cover-crest img {
    max-width: 140px;
    height: auto;
}
.cover-block {
    text-align: center;
    margin: 15px 0;
    font-size: 12pt;
}
.cover-label {
    font-size: 11pt;
    font-weight: bold;
    margin-bottom: 5px;
    text-transform: uppercase;
    color: #2D3748;
}
.cover-names {
    font-size: 12pt;
    font-weight: bold;
    line-height: 1.4;
}
.cover-footer {
    text-align: center;
    margin-top: 30px;
    font-size: 11pt;
    font-weight: bold;
    line-height: 1.4;
}

/* Certificate & Declaration */
.cert-header {
    text-align: center;
    font-size: 16pt;
    font-weight: bold;
    text-transform: uppercase;
    margin-bottom: 30px;
    text-decoration: underline;
}
.cert-body {
    font-size: 12pt;
    line-height: 1.8;
    margin: 30px 0;
    text-align: justify;
}
.signature-grid {
    display: flex;
    justify-content: space-between;
    margin-top: 80px;
    text-align: center;
}
.sig-box {
    width: 45%;
}
.sig-line {
    border-top: 1px solid #000;
    margin-bottom: 5px;
}
.viva-box {
    margin-top: 40px;
    border: 1px dashed #718096;
    padding: 15px;
    font-size: 11pt;
    line-height: 1.6;
}

/* Tables */
table.academic-table {
    width: 100%;
    border-collapse: collapse;
    margin: 18px 0 25px 0;
    font-size: 10.5pt;
    line-height: 1.35;
}
table.academic-table th {
    border-top: 1.5pt solid #000;
    border-bottom: 1pt solid #000;
    padding: 8px 6px;
    font-weight: bold;
    text-align: left;
    background-color: #F7FAFC;
}
table.academic-table td {
    padding: 7px 6px;
    border-bottom: 0.5pt solid #E2E8F0;
    vertical-align: top;
}
table.academic-table tr:last-child td {
    border-bottom: 1.5pt solid #000;
}
.table-caption {
    font-weight: bold;
    font-size: 11pt;
    margin: 15px 0 6px 0;
    text-align: left;
}

/* Figures */
.figure-container {
    text-align: center;
    margin: 22px 0 25px 0;
    page-break-inside: avoid;
}
.figure-container img {
    max-width: 95%;
    height: auto;
    border: 1px solid #E2E8F0;
    border-radius: 4px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
}
.figure-caption {
    font-weight: bold;
    font-size: 10.5pt;
    margin-top: 8px;
    text-align: center;
    color: #2D3748;
}

/* Algorithms & Code */
.algorithm-box {
    border: 1.5pt solid #2B6CB0;
    border-radius: 4px;
    padding: 12px 16px;
    margin: 18px 0 22px 0;
    background: #F7FAFC;
    font-size: 10.5pt;
    line-height: 1.4;
    page-break-inside: avoid;
}
.algorithm-title {
    font-weight: bold;
    font-size: 11pt;
    color: #1A365D;
    margin-bottom: 8px;
    border-bottom: 1pt solid #CBD5E0;
    padding-bottom: 4px;
}
pre.code-block {
    background: #2D3748;
    color: #EDF2F7;
    padding: 12px;
    border-radius: 4px;
    font-family: "Courier New", Courier, monospace;
    font-size: 9.5pt;
    line-height: 1.3;
    overflow-x: auto;
    margin: 12px 0;
}

/* Math equations */
.math-eq {
    text-align: center;
    font-style: italic;
    margin: 12px 0;
    padding: 6px 0;
    font-size: 11.5pt;
}

/* TOC Table */
table.toc-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 11pt;
    line-height: 1.5;
}
table.toc-table td {
    padding: 4px 0;
}
.toc-dots {
    border-bottom: 1px dotted #A0AEC0;
}

@media print {
    body {
        background: white;
    }
    .toolbar-bar {
        display: none !important;
    }
    .document-container {
        max-width: 100%;
        margin: 0;
        padding: 0;
        box-shadow: none;
    }
}
</style>
</head>
<body>

<!-- Floating Action Bar -->
<div class="toolbar-bar">
    <div class="toolbar-title">
        <span>📄 MedRadar Phase-I Final Project Report (56 Pages)</span>
    </div>
    <div class="toolbar-actions">
        <select class="select-chapter" onchange="if(this.value) location.hash = this.value;">
            <option value="">-- Jump to Chapter --</option>
            <option value="cover">Title Cover Page</option>
            <option value="certificate">Bonafide Certificate</option>
            <option value="declaration">Declaration</option>
            <option value="abstract">Abstract</option>
            <option value="toc">Table of Contents</option>
            <option value="lot">List of Tables</option>
            <option value="lof">List of Figures</option>
            <option value="abbrev">List of Abbreviations</option>
            <option value="ch1">Chapter 1: Introduction</option>
            <option value="ch2">Chapter 2: Literature Survey</option>
            <option value="ch3">Chapter 3: Methodology</option>
            <option value="ch4">Chapter 4: Results & Evaluation</option>
            <option value="ch5">Chapter 5: Conclusion</option>
            <option value="timelines">Timelines & Milestones</option>
            <option value="publications">Publications</option>
            <option value="references">IEEE References</option>
        </select>
        <button class="btn-print" onclick="window.print()">
            <span>🖨️ Print / Save as PDF</span>
        </button>
    </div>
</div>

<div class="document-container">
""")

    # 1. COVER PAGE
    html.append("""
    <!-- ==================== COVER PAGE ==================== -->
    <div id="cover" style="text-align: center; min-height: 250mm; display: flex; flex-direction: column; justify-content: space-between;">
        <div>
            <div class="cover-header">
                <img src="assets/image1.jpeg" alt="SCSVMV University Banner">
                <div class="cover-subhdr">
                    DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING<br>
                    BCSF187Z50  PROJECT WORK PHASE – I<br>
                    <span style="font-size: 11pt; font-weight: normal;">B.E. (Computer Science and Engineering)</span>
                </div>
            </div>

            <div class="cover-crest">
                <img src="assets/image2.jpeg" alt="SCSVMV Seal Crest">
            </div>

            <h1 class="doc-title" style="margin-top: 15px;">
                MEDRADAR: AI-DRIVEN REAL-TIME MEDICAL INTELLIGENCE AND GEOSPATIAL RESOURCE MAPPING PLATFORM
            </h1>

            <div style="font-size: 12pt; font-weight: bold; margin: 15px 0; letter-spacing: 0.5px;">
                BCSF187Z50 - PROJECT WORK PHASE-I REPORT<br>
                <span style="font-weight: normal; font-size: 11pt;">Batch (2023-2027) (Semester VII)</span>
            </div>
        </div>

        <div>
            <div style="display: flex; justify-content: space-around; margin: 25px 0;">
                <div style="text-align: left; width: 45%;">
                    <div class="cover-label">SUBMITTED BY:</div>
                    <div class="cover-names">
                        G. TRIVIKRAM SIVAJI &nbsp; (Reg. No. 11239A029)<br>
                        Y. SESHU KUMAR &nbsp; (Reg. No. 11239A103)
                    </div>
                </div>
                <div style="text-align: right; width: 45%;">
                    <div class="cover-label">GUIDED BY:</div>
                    <div class="cover-names">
                        Dr. T. SUNDAR, M.E., Ph.D.<br>
                        <span style="font-weight: normal; font-size: 10.5pt;">Assistant Professor, Dept. of CSE</span>
                    </div>
                </div>
            </div>

            <div class="cover-footer">
                DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING<br>
                SRI CHANDRASEKHARENDRA SARASWATHI VISWA MAHAVIDYALAYA<br>
                <span style="font-size: 10pt; font-weight: normal;">(Deemed to be University u/s 3 of UGC Act 1956)</span><br>
                Enathur, Kanchipuram – 631 561, Tamil Nadu<br>
                Nov / Dec 2026
            </div>
        </div>
    </div>
    <div class="page-break"></div>
""")

    # 2. BONAFIDE CERTIFICATE
    html.append("""
    <!-- ==================== BONAFIDE CERTIFICATE ==================== -->
    <div id="certificate" style="min-height: 250mm; display: flex; flex-direction: column; justify-content: space-between;">
        <div>
            <div style="text-align: center; margin-bottom: 25px;">
                <img src="assets/image1.jpeg" alt="SCSVMV Banner" style="max-height: 60px;">
                <div style="font-size: 12pt; font-weight: bold; margin-top: 5px;">
                    SRI CHANDRASEKHARENDRA SARASWATHI VISWA MAHAVIDYALAYA<br>
                    <span style="font-size: 10pt; font-weight: normal;">DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING</span>
                </div>
            </div>

            <div class="cert-header">BONAFIDE CERTIFICATE</div>

            <div class="cert-body">
                This is to certify that the PROJECT WORK PHASE-I Report entitled 
                <strong>“MEDRADAR: AI-DRIVEN REAL-TIME MEDICAL INTELLIGENCE AND GEOSPATIAL RESOURCE MAPPING PLATFORM”</strong> 
                is the bonafide work carried out by 
                <strong>Mr. G. TRIVIKRAM SIVAJI (Reg. No. 11239A029)</strong> and 
                <strong>Mr. Y. SESHU KUMAR (Reg. No. 11239A103)</strong> 
                under my direct supervision during the academic year 2026–2027 in partial fulfillment of the requirements for the award of the Degree of 
                <strong>Bachelor of Engineering in Computer Science and Engineering</strong> of Sri Chandrasekharendra Saraswathi Viswa Mahavidyalaya, Enathur, Kanchipuram.
            </div>
        </div>

        <div>
            <div class="signature-grid">
                <div class="sig-box">
                    <div style="height: 45px;"></div>
                    <div class="sig-line"></div>
                    <strong>Dr. T. SUNDAR</strong><br>
                    Internal Guide & Assistant Professor<br>
                    Department of CSE, SCSVMV
                </div>
                <div class="sig-box">
                    <div style="height: 45px;"></div>
                    <div class="sig-line"></div>
                    <strong>Dr. M. SENTHIL KUMAR</strong><br>
                    Head of the Department<br>
                    Department of CSE, SCSVMV
                </div>
            </div>

            <div class="viva-box">
                Submitted for the Project Work Phase-I Viva-Voce Examination held on: _____________________<br><br>
                Place: Kanchipuram<br>
                Date: &nbsp; ____________<br><br>
                <div style="display: flex; justify-content: space-between; margin-top: 15px;">
                    <div><strong>Internal Examiner</strong></div>
                    <div><strong>External Examiner</strong></div>
                </div>
            </div>
        </div>
    </div>
    <div class="page-break"></div>
""")

    # 3. DECLARATION
    html.append("""
    <!-- ==================== DECLARATION ==================== -->
    <div id="declaration" style="min-height: 250mm; display: flex; flex-direction: column; justify-content: space-between;">
        <div>
            <div class="cert-header">DECLARATION</div>

            <div class="cert-body">
                We hereby declare that the PROJECT WORK PHASE-I work titled 
                <strong>“MEDRADAR: AI-DRIVEN REAL-TIME MEDICAL INTELLIGENCE AND GEOSPATIAL RESOURCE MAPPING PLATFORM”</strong> 
                is an authentic record of original research work implemented and compiled by us. No ideas, processes, mathematical formulations, software algorithms, or words of others have been presented as our own work without due scholarly acknowledgment and academic citation.
                <br><br>
                We affirmatively affirm that:
                <ol style="margin: 15px 0 20px 25px; line-height: 1.8;">
                    <li>There is no fabrication of data, telemetry streams, or experimental benchmark results compiled or analyzed.</li>
                    <li>There is no falsification by manipulating physical data, distorting models, or intentionally changing or omitting critical findings.</li>
                    <li>All scientific literature reviewed adheres strictly to contemporary peer-reviewed journal articles published after October 2020 and 2024 onwards according to SCSVMV standards.</li>
                    <li>We understand that the project is liable to be rejected at any stage (even at a later date) if it is discovered that significant plagiarized material or unauthorized code was incorporated, rendering the Degree awarded itself invalid.</li>
                </ol>
            </div>
        </div>

        <div>
            <div style="display: flex; justify-content: space-between; margin-top: 60px;">
                <div style="text-align: left;">
                    Place: Kanchipuram<br>
                    Date: &nbsp; 20-11-2026
                </div>
                <div style="text-align: right; width: 50%;">
                    <div style="height: 35px;"></div>
                    <strong>1. G. TRIVIKRAM SIVAJI (11239A029)</strong><br><br>
                    <div style="height: 35px;"></div>
                    <strong>2. Y. SESHU KUMAR (11239A103)</strong>
                </div>
            </div>
        </div>
    </div>
    <div class="page-break"></div>
""")

    # 4. ABSTRACT
    html.append(f"""
    <!-- ==================== ABSTRACT ==================== -->
    <div id="abstract" class="chapter-start">
        <h1 class="chapter-title">ABSTRACT</h1>
        
        <p>{FRONT_MATTER_DATA['abstract']}</p>
        
        <div style="margin-top: 30px; font-size: 11.5pt;">
            <strong>Keywords:</strong> {'; '.join(FRONT_MATTER_DATA['keywords'])}.
        </div>
    </div>
    <div class="page-break"></div>
""")

    # 5. TABLE OF CONTENTS
    html.append("""
    <!-- ==================== TABLE OF CONTENTS ==================== -->
    <div id="toc" class="chapter-start">
        <h1 class="chapter-title">TABLE OF CONTENTS</h1>
        
        <table class="academic-table" style="border: none;">
            <thead>
                <tr style="border-top: 1.5pt solid #000; border-bottom: 1.5pt solid #000;">
                    <th style="width: 15%; text-align: left;">Chapter</th>
                    <th style="width: 73%; text-align: left;">Title</th>
                    <th style="width: 12%; text-align: right;">Page No.</th>
                </tr>
            </thead>
            <tbody>
""")
    for item in TABLE_OF_CONTENTS_DATA:
        bold = "font-weight: bold;" if item["level"] <= 1 else ""
        indent = f"padding-left: {item['level']*18}px;"
        num_str = f"<strong>{item['num']}</strong>" if item['num'] else ""
        html.append(f"""
                <tr style="border: none;">
                    <td style="border: none; padding: 4px 6px; {bold}">{num_str}</td>
                    <td style="border: none; padding: 4px 6px; {bold} {indent}">{item['title']}</td>
                    <td style="border: none; padding: 4px 6px; text-align: right; {bold}">{item['page']}</td>
                </tr>
        """)
    html.append("""
            </tbody>
        </table>
    </div>
    <div class="page-break"></div>
""")

    # 6. LIST OF TABLES
    html.append("""
    <!-- ==================== LIST OF TABLES ==================== -->
    <div id="lot" class="chapter-start">
        <h1 class="chapter-title">LIST OF TABLES</h1>
        
        <table class="academic-table">
            <thead>
                <tr>
                    <th style="width: 18%;">Table No.</th>
                    <th style="width: 70%;">Table Title & Description</th>
                    <th style="width: 12%; text-align: right;">Page No.</th>
                </tr>
            </thead>
            <tbody>
""")
    for t in LIST_OF_TABLES_DATA:
        html.append(f"""
                <tr>
                    <td><strong>{t['num']}</strong></td>
                    <td>{t['title']}</td>
                    <td style="text-align: right;"><strong>{t['page']}</strong></td>
                </tr>
        """)
    html.append("""
            </tbody>
        </table>
    </div>
    <div class="page-break"></div>
""")

    # 7. LIST OF FIGURES
    html.append("""
    <!-- ==================== LIST OF FIGURES ==================== -->
    <div id="lof" class="chapter-start">
        <h1 class="chapter-title">LIST OF FIGURES</h1>
        
        <table class="academic-table">
            <thead>
                <tr>
                    <th style="width: 18%;">Figure No.</th>
                    <th style="width: 70%;">Figure Caption & Description</th>
                    <th style="width: 12%; text-align: right;">Page No.</th>
                </tr>
            </thead>
            <tbody>
""")
    for fig in LIST_OF_FIGURES_DATA:
        html.append(f"""
                <tr>
                    <td><strong>{fig['num']}</strong></td>
                    <td>{fig['title']}</td>
                    <td style="text-align: right;"><strong>{fig['page']}</strong></td>
                </tr>
        """)
    html.append("""
            </tbody>
        </table>
    </div>
    <div class="page-break"></div>
""")

    # 8. LIST OF ABBREVIATIONS
    html.append("""
    <!-- ==================== LIST OF ABBREVIATIONS ==================== -->
    <div id="abbrev" class="chapter-start">
        <h1 class="chapter-title">LIST OF ABBREVIATIONS</h1>
        
        <table class="academic-table">
            <thead>
                <tr>
                    <th style="width: 25%;">Abbreviation</th>
                    <th style="width: 75%;">Full Technical Nomenclature / Meaning</th>
                </tr>
            </thead>
            <tbody>
""")
    for a in LIST_OF_ABBREVIATIONS_DATA:
        html.append(f"""
                <tr>
                    <td><strong>{a['abbrev']}</strong></td>
                    <td>{a['meaning']}</td>
                </tr>
        """)
    html.append("""
            </tbody>
        </table>
    </div>
    <div class="page-break"></div>
""")

    # 9. CHAPTER 1: INTRODUCTION
    html.append("""
    <!-- ==================== CHAPTER 1: INTRODUCTION ==================== -->
    <div id="ch1" class="chapter-start">
        <div style="text-align: center; font-size: 14pt; font-weight: bold; margin-bottom: 5px;">CHAPTER 1</div>
        <h1 class="chapter-title">INTRODUCTION</h1>
""")
    for sec in CHAPTER1_CONTENT["sections"]:
        html.append(f"""
        <h2 class="section-title">{sec['id']} {sec['title']}</h2>
""")
        paras = sec["content"].split("\n\n")
        for p in paras:
            if p.strip().startswith(("1.", "2.", "3.", "4.", "5.")):
                html.append(f"<p class='no-indent'>{p.strip()}</p>")
            elif p.strip():
                html.append(f"<p>{p.strip()}</p>")
    html.append("""
    </div>
    <div class="page-break"></div>
""")

    # 10. CHAPTER 2: LITERATURE SURVEY
    html.append("""
    <!-- ==================== CHAPTER 2: LITERATURE SURVEY ==================== -->
    <div id="ch2" class="chapter-start">
        <div style="text-align: center; font-size: 14pt; font-weight: bold; margin-bottom: 5px;">CHAPTER 2</div>
        <h1 class="chapter-title">LITERATURE SURVEY</h1>
""")
    for sec in CHAPTER2_CONTENT["sections"]:
        html.append(f"""
        <h2 class="section-title">{sec['id']} {sec['title']}</h2>
""")
        # If section is 2.2, insert Table 2.1 nicely
        if sec["id"] == "2.2":
            html.append("""
            <div class="table-caption">Table 2.1: Comparative Literature Matrix & Methodological Gap Analysis</div>
            <table class="academic-table">
                <thead>
                    <tr>
                        <th>Study & Year</th>
                        <th>Forecasting Horizon</th>
                        <th>Class Calibration</th>
                        <th>POS Telemetry Sync</th>
                        <th>Spatial Triage Routing</th>
                        <th>Generic Cost Optimizer</th>
                        <th>Dual DB Persistence</th>
                        <th>Target Network</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td>Sharma et al. (2021)</td><td>None</td><td>None</td><td>No (Survey)</td><td>None</td><td>None</td><td>No</td><td>420 Chemists (N. India)</td></tr>
                    <tr><td>Patel & Rao (2022)</td><td>1–7 Days</td><td>Uncalibrated</td><td>No (Batch DB)</td><td>None</td><td>None</td><td>No</td><td>65 Hospital Dispensaries</td></tr>
                    <tr><td>Rajagopal et al. (2023)</td><td>None</td><td>None</td><td>No (Static)</td><td>Static 2SFCA</td><td>None</td><td>No</td><td>Suburban TN Corridors</td></tr>
                    <tr><td>Chen & Al-Kindi (2024)</td><td>Offline</td><td>Calibrated</td><td>No (Benchmark)</td><td>None</td><td>None</td><td>No</td><td>Offline Benchmark Sets</td></tr>
                    <tr><td>Kumar & Bala. (2024)</td><td>None</td><td>None</td><td>No (Fieldwork)</td><td>None</td><td>Manual Survey</td><td>No</td><td>14 S. Indian Districts</td></tr>
                    <tr><td>Aris et al. (2024)</td><td>None</td><td>None</td><td>Yes (Heavy DLT)</td><td>None</td><td>None</td><td>No</td><td>Pilot IoT Dispensaries</td></tr>
                    <tr style="background: #F0FFF4;"><td><strong>MedRadar v2 (This Work)</strong></td><td><strong>1–30 Days</strong></td><td><strong>Isotonic L2</strong></td><td><strong>Yes (Light REST)</strong></td><td><strong>Haversine SOS</strong></td><td><strong>PMBJP Engine</strong></td><td><strong>MySQL+SQLite</strong></td><td><strong>18 Kanchi Pharmacies</strong></td></tr>
                </tbody>
            </table>
            """)
        paras = sec["content"].split("\n\n")
        for p in paras:
            if "Table 2.1:" in p:
                continue
            elif p.strip().startswith(("2.3.", "1.", "2.", "3.", "4.", "5.", "6.", "Gap")):
                if p.strip().startswith("2.3."):
                    html.append(f"<h3 class='subsection-title'>{p.strip()}</h3>")
                else:
                    html.append(f"<p class='no-indent'>{p.strip()}</p>")
            elif p.strip():
                html.append(f"<p>{p.strip()}</p>")
    html.append("""
    </div>
    <div class="page-break"></div>
""")

    # 11. CHAPTER 3: SYSTEM ARCHITECTURE & METHODOLOGY
    html.append("""
    <!-- ==================== CHAPTER 3: METHODOLOGY ==================== -->
    <div id="ch3" class="chapter-start">
        <div style="text-align: center; font-size: 14pt; font-weight: bold; margin-bottom: 5px;">CHAPTER 3</div>
        <h1 class="chapter-title">SYSTEM ARCHITECTURE AND METHODOLOGY</h1>
""")
    for sec in CHAPTER3_CONTENT["sections"]:
        html.append(f"""
        <h2 class="section-title">{sec['id']} {sec['title']}</h2>
""")
        # Insert architecture image in 3.1
        if sec["id"] == "3.1":
            html.append("""
            <div class="figure-container">
                <img src="assets/figure_3_3_system_architecture.png" alt="System Architecture">
                <div class="figure-caption">Figure 3.1: MedRadar v2 Multi-Tier Distributed Healthcare Intelligence Architecture</div>
            </div>
            """)
        
        # Insert Table 3.1 in 3.2
        if sec["id"] == "3.2":
            html.append("""
            <div class="table-caption">Table 3.1: Longitudinal Dataset Schema & Data Dictionary (175,360 Records)</div>
            <table class="academic-table">
                <thead>
                    <tr><th>Attribute Name</th><th>Data Type</th><th>Constraints</th><th>Domain / Units</th><th>Operational Significance</th></tr>
                </thead>
                <tbody>
                    <tr><td>date</td><td>DATE</td><td>YYYY-MM-DD</td><td>2020-01-01–2025-12-31</td><td>Primary temporal index; continuous daily calendar cadence</td></tr>
                    <tr><td>pharmacy_id</td><td>INTEGER</td><td>FK, 1 to 18</td><td>Discrete ID</td><td>Unique identifier for 18 Kanchipuram regional pharmacies</td></tr>
                    <tr><td>medicine_name</td><td>VARCHAR(100)</td><td>NOT NULL</td><td>10 Molecules</td><td>Standardized international nonproprietary name (INN)</td></tr>
                    <tr><td>category</td><td>VARCHAR(50)</td><td>NOT NULL</td><td>5 Classes</td><td>Therapeutic pharmacological classification</td></tr>
                    <tr><td>units_sold</td><td>INTEGER</td><td>≥ 0</td><td>Units / day</td><td>Daily consumer dispensing count (primary regression target)</td></tr>
                    <tr><td>stock_level</td><td>INTEGER</td><td>≥ 0</td><td>Units on shelf</td><td>Physical end-of-day shelf inventory balance</td></tr>
                    <tr><td>reorder_level</td><td>INTEGER</td><td>≥ 0</td><td>Units threshold</td><td>Static inventory safety threshold triggering restock</td></tr>
                    <tr><td>unit_price</td><td>DECIMAL(8,2)</td><td>> 0</td><td>INR (₹)</td><td>Retail selling price per dispensing unit / strip</td></tr>
                    <tr><td>daily_revenue</td><td>DECIMAL(10,2)</td><td>≥ 0</td><td>INR (₹)</td><td>Gross transactional revenue (units_sold × unit_price)</td></tr>
                    <tr><td>expiry_days_remaining</td><td>INTEGER</td><td>≥ 0</td><td>Days</td><td>Days remaining until active batch expiration</td></tr>
                    <tr><td>supplier_lead_time_days</td><td>INTEGER</td><td>1 to 14</td><td>Days</td><td>Distributor transit and delivery turnaround latency</td></tr>
                    <tr><td>overdue_delay_days</td><td>INTEGER</td><td>≥ 0</td><td>Days</td><td>Unscheduled distributor delivery delay beyond ETA</td></tr>
                    <tr><td>is_pandemic_period</td><td>TINYINT</td><td>{0, 1}</td><td>Binary</td><td>Indicator for active COVID-19 pandemic surge period</td></tr>
                    <tr><td>patient_age_group</td><td>VARCHAR(20)</td><td>NOT NULL</td><td>5 Brackets</td><td>Demographic cohort (0–12, 13–25, 26–45, 46–65, 65+)</td></tr>
                </tbody>
            </table>
            """)

        # Insert Table 3.2 and Figures 3.1, 3.2 in 3.3
        if sec["id"] == "3.3":
            html.append("""
            <div class="table-caption">Table 3.2: Comprehensive Descriptive Statistics of Core Telemetry Variables</div>
            <table class="academic-table">
                <thead>
                    <tr><th>Metric</th><th>Units Sold (units)</th><th>Stock Level (units)</th><th>Unit Price (₹)</th><th>Expiry Days Remaining</th><th>Rolling 7d Mean (units)</th></tr>
                </thead>
                <tbody>
                    <tr><td>Count</td><td>175,360</td><td>175,360</td><td>175,360</td><td>175,360</td><td>175,360</td></tr>
                    <tr><td>Mean</td><td>454.6315</td><td>4,553.1326</td><td>52.5513</td><td>374.1385</td><td>455.9170</td></tr>
                    <tr><td>Standard Deviation</td><td>350.9572</td><td>346.4229</td><td>27.4165</td><td>199.7716</td><td>199.7883</td></tr>
                    <tr><td>Variance</td><td>123,170.93</td><td>120,008.82</td><td>751.66</td><td>39,908.68</td><td>39,915.38</td></tr>
                    <tr><td>Median (Q2)</td><td>390.00</td><td>4,598.00</td><td>52.61</td><td>374.00</td><td>417.86</td></tr>
                    <tr><td>Interquartile Range</td><td>248.00</td><td>292.00</td><td>47.51</td><td>346.00</td><td>215.29</td></tr>
                    <tr><td>Minimum</td><td>31.00</td><td>0.00</td><td>5.00</td><td>30.00</td><td>145.29</td></tr>
                    <tr><td>25th Percentile (Q1)</td><td>286.00</td><td>4,443.00</td><td>28.78</td><td>201.00</td><td>317.71</td></tr>
                    <tr><td>75th Percentile (Q3)</td><td>534.00</td><td>4,735.00</td><td>76.29</td><td>547.00</td><td>533.00</td></tr>
                    <tr><td>Maximum</td><td>10,640.00</td><td>5,124.00</td><td>100.00</td><td>719.00</td><td>6,684.00</td></tr>
                    <tr><td>Skewness (γ₁)</td><td>+7.7285</td><td>-5.5320</td><td>-0.0030</td><td>+0.0012</td><td>+2.2175</td></tr>
                    <tr><td>Kurtosis (γ₂)</td><td>+101.0787</td><td>+53.5838</td><td>-1.1990</td><td>-1.2005</td><td>+16.9125</td></tr>
                </tbody>
            </table>

            <div class="figure-container">
                <img src="assets/image5.png" alt="Noise Filtering Comparison">
                <div class="figure-caption">Figure 3.2: Time-Series Signal Smoothing & Noise Filtering Comparison</div>
            </div>

            <div class="figure-container">
                <img src="assets/image4.png" alt="Correlation Heatmap">
                <div class="figure-caption">Figure 3.3: Pearson Correlation Heatmap & Feature Multicollinearity Matrix</div>
            </div>

            <div class="table-caption">Table 3.3: Denoising Filter Performance Benchmark (Savitzky-Golay vs EWMA vs Median)</div>
            <table class="academic-table">
                <thead>
                    <tr><th>Denoising Method</th><th>Signal-to-Noise Ratio (SNR dB)</th><th>Signal Power (10⁹)</th><th>Noise Power (10⁶)</th><th>Variance Reduction %</th><th>MAE from Raw</th></tr>
                </thead>
                <tbody>
                    <tr><td>Savitzky-Golay (w=7, p=2)</td><td>23.06 dB</td><td>1.4834</td><td>7.3399</td><td>4.44%</td><td>1,984.76</td></tr>
                    <tr><td>EWMA (span=7, α=0.25)</td><td>23.81 dB</td><td>1.4868</td><td>6.1766</td><td>4.38%</td><td>1,821.54</td></tr>
                    <tr style="background: #F0FFF4;"><td><strong>Rolling Median (window=7)</strong></td><td><strong>22.68 dB</strong></td><td><strong>1.4564</strong></td><td><strong>7.8609</strong></td><td><strong>6.52% (Winning Filter)</strong></td><td><strong>1,825.15</strong></td></tr>
                </tbody>
            </table>

            <div class="table-caption">Table 3.4: Taxonomy of 28 Engineered Predictive Features Across Five Modalities</div>
            <table class="academic-table">
                <thead>
                    <tr><th>Feature Category</th><th>Feature Name</th><th>Mathematical Formulation</th><th>Physical & Behavioral Significance</th></tr>
                </thead>
                <tbody>
                    <tr><td>Temporal Demand Lags</td><td>lag_1, lag_2, lag_3, lag_7, lag_14, lag_30</td><td>D(t - k), k ∈ {1, 2, 3, 7, 14, 30}</td><td>Autoregressive short- and long-term consumption persistence</td></tr>
                    <tr><td>Rolling Consumption</td><td>rolling_3d_mean, 7d, 14d, rolling_7d_std</td><td>(1/k) ∑ D(t - i); sample standard dev</td><td>Short-, medium-term velocity & demand turbulence volatility</td></tr>
                    <tr><td>Cyclical Calendar</td><td>dow_sin, dow_cos, month_sin, month_cos</td><td>sin/cos(2π · t / period)</td><td>Trigonometric weekly and annual disease cycle encodings</td></tr>
                    <tr><td>Inventory Depletion</td><td>stock_cover_days, burn_rate, expiry_risk_index</td><td>I(t)/MA_7d; D(t-1)/I(t); 100/(T_exp - t)</td><td>Stockout countdown, depletion velocity, and expiration pressure</td></tr>
                    <tr><td>Distributor Dynamics</td><td>lead_time_stress_index, is_pandemic_surge</td><td>lead_time × (1 + overdue_delay)</td><td>Wholesale delivery friction and epidemic shock indicators</td></tr>
                </tbody>
            </table>
            """)

        # Insert Table 3.5 & Figure 3.5 in 3.7
        if sec["id"] == "3.7":
            html.append("""
            <div class="table-caption">Table 3.5: Geographic Coordinates and Operational Attributes of 18 Kanchipuram Pharmacies</div>
            <table class="academic-table">
                <thead>
                    <tr><th>Pharmacy ID & Name</th><th>Latitude (°N)</th><th>Longitude (°E)</th><th>Spatial Ward / Zone</th><th>24x7 Casualty</th><th>Cold Storage</th><th>Lead Time</th></tr>
                </thead>
                <tbody>
                    <tr><td>1. Apollo Pharmacy Central</td><td>12.8342</td><td>79.7036</td><td>Kanchipuram Bus Stand Hub</td><td>Yes</td><td>Yes</td><td>24 Hours</td></tr>
                    <tr><td>2. MedPlus Gandhi Road</td><td>12.8315</td><td>79.7078</td><td>Gandhi Road Commercial Ward</td><td>No</td><td>Yes</td><td>48 Hours</td></tr>
                    <tr><td>3. Jan Aushadhi Kendra (Kanchi)</td><td>12.8351</td><td>79.7042</td><td>Moffusil Bus Stand North</td><td>No</td><td>No</td><td>72 Hours</td></tr>
                    <tr><td>4. Sri Krishna Medicals</td><td>12.8384</td><td>79.7001</td><td>Hospital Road Medical Hub</td><td>Yes</td><td>Yes</td><td>24 Hours</td></tr>
                    <tr><td>5. Kanchi HQ Hospital Chemist</td><td>12.8390</td><td>79.6995</td><td>District HQ Hospital Campus</td><td>Yes</td><td>Yes</td><td>12 Hours</td></tr>
                    <tr><td>6. Meenakshi Pharmacy Enathur</td><td>12.8712</td><td>79.7124</td><td>Enathur University Belt</td><td>Yes</td><td>Yes</td><td>24 Hours</td></tr>
                    <tr><td>7. SCSVMV Campus Dispensary</td><td>12.8725</td><td>79.7138</td><td>Enathur SCSVMV Campus</td><td>No</td><td>No</td><td>48 Hours</td></tr>
                    <tr><td>8. Thiru Murugan Medicals</td><td>12.8291</td><td>79.7095</td><td>Little Kanchipuram Core</td><td>No</td><td>No</td><td>48 Hours</td></tr>
                    <tr><td>9. Vigneshwara Medicals</td><td>12.8124</td><td>79.7012</td><td>Orikkai Southern Ward</td><td>No</td><td>No</td><td>48 Hours</td></tr>
                    <tr><td>10. Lakshmi Medical Stores</td><td>12.8452</td><td>79.6921</td><td>Collectorate Admin Zone</td><td>No</td><td>Yes</td><td>24 Hours</td></tr>
                    <tr><td>11. Balaji Pharmacy Tollgate</td><td>12.8510</td><td>79.6845</td><td>Bangalore Highway Tollgate</td><td>Yes</td><td>Yes</td><td>24 Hours</td></tr>
                    <tr><td>12. Santhosh Medical Hall</td><td>12.8330</td><td>79.7060</td><td>Nellukkara Commercial Street</td><td>No</td><td>No</td><td>48 Hours</td></tr>
                    <tr><td>13. Royal Medicals Ekambaranar</td><td>12.8421</td><td>79.6980</td><td>North Temple Sannadhi Street</td><td>No</td><td>No</td><td>48 Hours</td></tr>
                    <tr><td>14. Kumaran Pharmacy Walajabad</td><td>12.7954</td><td>79.8152</td><td>Walajabad Highway Link</td><td>No</td><td>No</td><td>72 Hours</td></tr>
                    <tr><td>15. Sriperumbudur Medicare</td><td>12.9684</td><td>79.9421</td><td>Sriperumbudur Industrial Hub</td><td>Yes</td><td>Yes</td><td>24 Hours</td></tr>
                    <tr><td>16. City Medicals Rangaswamy</td><td>12.8362</td><td>79.7025</td><td>Rangaswamy Kulam Ward</td><td>No</td><td>No</td><td>48 Hours</td></tr>
                    <tr><td>17. Annai Medicals Orikkai</td><td>12.8095</td><td>79.6985</td><td>Orikkai Rural Junction</td><td>No</td><td>No</td><td>48 Hours</td></tr>
                    <tr><td>18. HealthCare Plus Bus Stand</td><td>12.8338</td><td>79.7048</td><td>Bus Stand South Terminal</td><td>Yes</td><td>Yes</td><td>24 Hours</td></tr>
                </tbody>
            </table>

            <div class="figure-container">
                <img src="assets/figure_3_5_sos_triage_flowchart.png" alt="Emergency SOS Flowchart">
                <div class="figure-caption">Figure 3.4: Emergency SOS Triage & Rapid Doorstep Dispatch Workflow</div>
            </div>
            """)

        # Insert Table 3.6 & Figure 3.5 in 3.8
        if sec["id"] == "3.8":
            html.append("""
            <div class="figure-container">
                <img src="assets/figure_3_6_generic_savings_flowchart.png" alt="Generic Savings Flowchart">
                <div class="figure-caption">Figure 3.5: PMBJP Jan Aushadhi Generic Medicine Optimization Engine</div>
            </div>

            <div class="table-caption">Table 3.6: Commercial Branded vs PMBJP Jan Aushadhi Generic Pricing & Savings</div>
            <table class="academic-table">
                <thead>
                    <tr><th>Generic Molecule & Strength</th><th>Top Commercial Brand Name</th><th>Commercial MRP (₹)</th><th>PMBJP Generic Price (₹)</th><th>Absolute Savings</th><th>% Savings</th></tr>
                </thead>
                <tbody>
                    <tr><td>1. Paracetamol 650mg</td><td>Dolo-650 (Micro Labs)</td><td>₹34.50 / 15 tabs</td><td>₹7.20 / 10 tabs</td><td>₹27.30</td><td>79.1%</td></tr>
                    <tr><td>2. Metformin 500mg SR</td><td>Glycomet-500 (USV)</td><td>₹48.00 / 20 tabs</td><td>₹12.50 / 20 tabs</td><td>₹35.50</td><td>74.0%</td></tr>
                    <tr><td>3. Amlodipine 5mg</td><td>Amlopres-5 (Cipla)</td><td>₹42.00 / 15 tabs</td><td>₹6.80 / 10 tabs</td><td>₹35.20</td><td>83.8%</td></tr>
                    <tr><td>4. Azithromycin 500mg</td><td>Azithral-500 (Alembic)</td><td>₹128.00 / 5 tabs</td><td>₹38.00 / 5 tabs</td><td>₹90.00</td><td>70.3%</td></tr>
                    <tr><td>5. Amoxicillin 500mg</td><td>Mox-500 (Sun Pharma)</td><td>₹85.00 / 10 caps</td><td>₹24.00 / 10 caps</td><td>₹61.00</td><td>71.8%</td></tr>
                    <tr><td>6. Cetirizine 10mg</td><td>Cetcip-10 (Cipla)</td><td>₹22.50 / 10 tabs</td><td>₹4.50 / 10 tabs</td><td>₹18.00</td><td>80.0%</td></tr>
                    <tr><td>7. Ibuprofen 400mg</td><td>Brufen-400 (Abbott)</td><td>₹28.00 / 15 tabs</td><td>₹6.50 / 10 tabs</td><td>₹21.50</td><td>76.8%</td></tr>
                    <tr><td>8. Atorvastatin 10mg</td><td>Atorva-10 (Zydus)</td><td>₹98.00 / 15 tabs</td><td>₹16.50 / 10 tabs</td><td>₹81.50</td><td>83.2%</td></tr>
                    <tr><td>9. Salbutamol Inhaler 100mcg</td><td>Asthalin Inhaler (Cipla)</td><td>₹165.00 / canister</td><td>₹62.00 / canister</td><td>₹103.00</td><td>62.4%</td></tr>
                    <tr><td>10. Vitamin C (Ascorbic Acid)</td><td>Limcee 500 (Abbott)</td><td>₹26.50 / 15 tabs</td><td>₹5.50 / 10 tabs</td><td>₹21.00</td><td>79.2%</td></tr>
                    <tr style="background: #F0FFF4;"><td><strong>Average Across 10 Molecules</strong></td><td>--</td><td>--</td><td>--</td><td>--</td><td><strong>76.06% Direct Savings</strong></td></tr>
                </tbody>
            </table>
            """)

        # Insert Table 3.7 & Figure 3.4 in 3.9
        if sec["id"] == "3.9":
            html.append("""
            <div class="table-caption">Table 3.7: MedRadar Relational Database Entity Specifications & Primary Keys</div>
            <table class="academic-table">
                <thead>
                    <tr><th>Entity Name</th><th>Primary Key</th><th>Foreign Keys</th><th>Key Attributes</th><th>Operational Purpose</th></tr>
                </thead>
                <tbody>
                    <tr><td>users</td><td>id (INT)</td><td>pharmacy_id → pharmacies</td><td>username, password_hash, role</td><td>Authentication & role-based RBAC</td></tr>
                    <tr><td>pharmacies</td><td>id (INT)</td><td>None</td><td>name, address, lat, lon, phone</td><td>Spatial & operational metadata</td></tr>
                    <tr><td>medicines</td><td>id (INT)</td><td>None</td><td>brand_name, generic_name, mrp</td><td>Pharmacological catalog & pricing</td></tr>
                    <tr><td>inventory</td><td>id (INT)</td><td>pharmacy_id, medicine_id</td><td>current_stock, batch_no, expiry_date</td><td>Real-time physical shelf balances</td></tr>
                    <tr><td>transactions</td><td>id (INT)</td><td>pharmacy_id, medicine_id</td><td>units_sold, sale_price, timestamp</td><td>Granular POS dispensing logs</td></tr>
                    <tr><td>stock_audits</td><td>id (INT)</td><td>pharmacy_id, medicine_id</td><td>reported_stock, verified_by, hash</td><td>Cryptographic physical count audits</td></tr>
                    <tr><td>prescriptions</td><td>id (INT)</td><td>user_id → users</td><td>file_path, status, verified_at</td><td>Prescription OCR & verification</td></tr>
                    <tr><td>delivery_orders</td><td>id (INT)</td><td>pharmacy_id, user_id</td><td>delivery_address, total_amount, step</td><td>Doorstep fulfillment tracking</td></tr>
                </tbody>
            </table>

            <div class="figure-container">
                <img src="assets/figure_3_4_database_er.png" alt="Database ER Diagram">
                <div class="figure-caption">Figure 3.6: MedRadar v2 Relational Database Schema & Entity Relationships</div>
            </div>
            """)

        paras = sec["content"].split("\n\n")
        for p in paras:
            if "Table 3." in p:
                continue
            elif p.strip().startswith(("3.3.", "3.4.", "3.5.", "3.6.", "3.7.", "3.8.", "3.9.")):
                html.append(f"<h3 class='subsection-title'>{p.strip()}</h3>")
            elif p.strip().startswith(("1.", "2.", "3.", "4.", "5.", "6.", "Tier", "Hypothesis", "Algorithm")):
                html.append(f"<p class='no-indent'>{p.strip()}</p>")
            elif p.strip():
                html.append(f"<p>{p.strip()}</p>")
    html.append("""
    </div>
    <div class="page-break"></div>
""")

    # 12. CHAPTER 4: IMPLEMENTATION & RESULTS
    html.append("""
    <!-- ==================== CHAPTER 4: RESULTS ==================== -->
    <div id="ch4" class="chapter-start">
        <div style="text-align: center; font-size: 14pt; font-weight: bold; margin-bottom: 5px;">CHAPTER 4</div>
        <h1 class="chapter-title">IMPLEMENTATION, RESULTS AND PERFORMANCE EVALUATION</h1>
""")
    for sec in CHAPTER4_CONTENT["sections"]:
        html.append(f"""
        <h2 class="section-title">{sec['id']} {sec['title']}</h2>
""")
        # Insert Table 4.1 & Figure 4.5 in 4.1
        if sec["id"] == "4.1":
            html.append("""
            <div class="figure-container">
                <img src="assets/figure_4_5_pos_audit_workflow.png" alt="POS Audit Workflow">
                <div class="figure-caption">Figure 4.1: Cryptographic Point-of-Sale (POS) Audit Telemetry Verification Workflow</div>
            </div>

            <div class="table-caption">Table 4.1: Core REST API Microservices, HTTP Methods, and Payload Specifications</div>
            <table class="academic-table">
                <thead>
                    <tr><th>Endpoint URI</th><th>Method</th><th>Payload / Query Parameters</th><th>Response Schema</th><th>Operational Function</th></tr>
                </thead>
                <tbody>
                    <tr><td>/api/predict</td><td>GET</td><td>medicine_id, horizon_days</td><td>JSON {predictions: [...]}</td><td>Multi-day demand regression forecast</td></tr>
                    <tr><td>/api/stock</td><td>GET</td><td>medicine_id, pharmacy_id</td><td>JSON {stock: N, status: S}</td><td>Real-time on-shelf physical balance</td></tr>
                    <tr><td>/api/heatmap</td><td>GET</td><td>medicine_id (optional)</td><td>JSON {zones: [...], nodes: [...]}</td><td>Geospatial shortage risk heat clustering</td></tr>
                    <tr><td>/api/sos</td><td>POST</td><td>symptom, user_lat, user_lon</td><td>JSON {dispatches: [...]}</td><td>Haversine emergency triage routing</td></tr>
                    <tr><td>/api/audit</td><td>POST</td><td>pharmacy_id, medicine_id, units</td><td>JSON {status: 'ok', hash: H}</td><td>Cryptographic POS audit verification</td></tr>
                    <tr><td>/api/generic_savings</td><td>GET</td><td>brand_id or generic_id</td><td>JSON {savings_pct: P, Kendras}</td><td>PMBJP generic price comparison</td></tr>
                    <tr><td>/api/subscribe</td><td>POST</td><td>phone, medicine_id, channel</td><td>JSON {subscription_id: ID}</td><td>Restock alert notification engine</td></tr>
                    <tr><td>/api/deliveries</td><td>POST</td><td>order_id, user_id, items, address</td><td>JSON {tracking_step: S, eta: T}</td><td>Doorstep fulfillment & invoice</td></tr>
                </tbody>
            </table>
            """)

        # Insert Table 4.2 & Figures 4.1, 4.2 in 4.2
        if sec["id"] == "4.2":
            html.append("""
            <div class="table-caption">Table 4.2: Comparative Regression Model Benchmark Across 5 Architectures (Evaluated on Year 2025 Test Partition)</div>
            <table class="academic-table">
                <thead>
                    <tr><th>Regression Model Architecture</th><th>MAE (units)</th><th>RMSE (units)</th><th>R² Score</th><th>Adjusted R²</th><th>MAPE (%)</th><th>Training Latency (s)</th></tr>
                </thead>
                <tbody>
                    <tr><td>Ordinary Least Squares (OLS) Linear Baseline</td><td>97.984</td><td>128.009</td><td>0.7836</td><td>0.7834</td><td>30.82%</td><td>0.10 s</td></tr>
                    <tr><td>Ridge Regression (L2 Regularized, α=1.0)</td><td>97.984</td><td>128.009</td><td>0.7836</td><td>0.7834</td><td>30.82%</td><td>0.29 s</td></tr>
                    <tr><td>Lasso Regression (L1 Regularized, α=0.1)</td><td>97.975</td><td>128.001</td><td>0.7836</td><td>0.7834</td><td>30.82%</td><td>0.75 s</td></tr>
                    <tr><td>Random Forest Regressor (Trees=100)</td><td>74.853</td><td>117.799</td><td>0.8167</td><td>0.8166</td><td>23.41%</td><td>2.63 s</td></tr>
                    <tr style="background: #F0FFF4;"><td><strong>Histogram Gradient Boosting Regressor (LightGBM)</strong></td><td><strong>66.216</strong></td><td><strong>104.096</strong></td><td><strong>0.8569 (Winning)</strong></td><td><strong>0.8568</strong></td><td><strong>20.06%</strong></td><td><strong>0.92 s</strong></td></tr>
                </tbody>
            </table>

            <div class="figure-container">
                <img src="assets/image6.png" alt="Feature Importance">
                <div class="figure-caption">Figure 4.2: Relative Predictive Feature Weight Distribution (Gini Importance)</div>
            </div>

            <div class="figure-container">
                <img src="assets/image7.png" alt="Residuals and QQ">
                <div class="figure-caption">Figure 4.3: Regression Residual Distribution & Q-Q Diagnostics for Winning Regressor</div>
            </div>
            """)

        # Insert Table 4.3 & Figure 4.3 in 4.3
        if sec["id"] == "4.3":
            html.append("""
            <div class="table-caption">Table 4.3: Classification Model Benchmark & Probability Calibration Diagnostics (Evaluated on 2025 Test Partition)</div>
            <table class="academic-table">
                <thead>
                    <tr><th>Model Architecture</th><th>ROC-AUC</th><th>PR-AUC</th><th>Accuracy</th><th>Precision</th><th>Recall</th><th>F1-Score</th><th>Brier Score</th><th>Training Latency</th></tr>
                </thead>
                <tbody>
                    <tr><td>Baseline Decision Tree</td><td>0.9999</td><td>0.9114</td><td>0.9997</td><td>90.91%</td><td>88.89%</td><td>0.8989</td><td>0.0002</td><td>0.88 s</td></tr>
                    <tr><td>L2 Logistic Regression (Uncalibrated)</td><td>1.0000</td><td>0.9941</td><td>0.9999</td><td>95.56%</td><td>95.56%</td><td>0.9556</td><td>0.0001</td><td>0.15 s</td></tr>
                    <tr style="background: #F0FFF4;"><td><strong>Isotonic-Calibrated L2 Logistic</strong></td><td><strong>1.0000</strong></td><td><strong>0.9941</strong></td><td><strong>0.9999</strong></td><td><strong>95.56%</strong></td><td><strong>95.56%</strong></td><td><strong>0.9556</strong></td><td><strong>0.0001</strong></td><td><strong>0.22 s</strong></td></tr>
                </tbody>
            </table>

            <div class="figure-container">
                <img src="assets/image8.png" alt="ROC and PR Curves">
                <div class="figure-caption">Figure 4.4: Receiver Operating Characteristic (ROC) & Precision-Recall (PR) Curves</div>
            </div>
            """)

        # Insert Table 4.4 & Figure 4.4 in 4.4
        if sec["id"] == "4.4":
            html.append("""
            <div class="figure-container">
                <img src="assets/figure_4_4_kanchipuram_heatmap.png" alt="Kanchipuram Shortage Heatmap">
                <div class="figure-caption">Figure 4.5: MedRadar Geospatial Medicine Shortage Heatmap: Kanchipuram Regional Network</div>
            </div>

            <div class="table-caption">Table 4.4: Regional Shortage Severity Distribution Across Five Kanchipuram Spatial Wards</div>
            <table class="academic-table">
                <thead>
                    <tr><th>Spatial Ward / Cluster</th><th>Pharmacy Nodes Mapped</th><th>Average Shortage Risk %</th><th>Risk Classification</th><th>Recommended Logistical Action</th></tr>
                </thead>
                <tbody>
                    <tr><td>1. Central Bus Stand Hub (Wards 1–8)</td><td>4 Pharmacies</td><td>38.5%</td><td>CRITICAL SHORTAGE (>35%)</td><td>Immediate warehouse dispatch</td></tr>
                    <tr><td>2. Hospital Road Zone (Wards 9–16)</td><td>3 Pharmacies</td><td>26.2%</td><td>ELEVATED RISK (22–35%)</td><td>Rebalance from Enathur hub</td></tr>
                    <tr><td>3. Gandhi Road Core (Wards 17–28)</td><td>4 Pharmacies</td><td>14.8%</td><td>MODERATE RISK (12–22%)</td><td>Monitor daily dispensing</td></tr>
                    <tr><td>4. Enathur Corridor (Wards 29–36)</td><td>3 Pharmacies</td><td>6.5%</td><td>NORMAL SUPPLY (<12%)</td><td>Designated regional donor hub</td></tr>
                    <tr><td>5. Orikkai & Southern (Wards 37–45)</td><td>4 Pharmacies</td><td>11.2%</td><td>NORMAL SUPPLY (<12%)</td><td>Stable maintenance inventory</td></tr>
                </tbody>
            </table>
            """)

        # Insert Table 4.5 in 4.5
        if sec["id"] == "4.5":
            html.append("""
            <div class="table-caption">Table 4.5: Annual Treatment Basket Cost Comparison for Chronic Illness Patients (Kanchipuram Field Simulation)</div>
            <table class="academic-table">
                <thead>
                    <tr><th>Therapy Regimen Component</th><th>Standard Commercial Brand Cost/Year</th><th>PMBJP Generic Cost/Year</th><th>Absolute Savings</th><th>% Savings</th></tr>
                </thead>
                <tbody>
                    <tr><td>Metformin 500mg SR (2 tabs/day)</td><td>Glycomet-500: ₹1,752.00 / year</td><td>PMBJP Generic: ₹456.25 / year</td><td>₹1,295.75</td><td>73.96%</td></tr>
                    <tr><td>Amlodipine 5mg (1 tab/day)</td><td>Amlopres-5: ₹1,022.00 / year</td><td>PMBJP Generic: ₹248.20 / year</td><td>₹773.80</td><td>75.71%</td></tr>
                    <tr><td>Atorvastatin 10mg (1 tab/day)</td><td>Atorva-10: ₹2,384.00 / year</td><td>PMBJP Generic: ₹602.25 / year</td><td>₹1,781.75</td><td>74.74%</td></tr>
                    <tr><td>Salbutamol Inhaler (6 cans/year)</td><td>Asthalin: ₹990.00 / year</td><td>PMBJP Generic: ₹372.00 / year</td><td>₹618.00</td><td>62.42%</td></tr>
                    <tr><td>Seasonal Antibiotic & Antipyretic</td><td>Azithral + Dolo: ₹820.00 / year</td><td>PMBJP Generic: ₹195.00 / year</td><td>₹625.00</td><td>76.22%</td></tr>
                    <tr style="background: #F0FFF4;"><td><strong>Total Annual Household Expenditure (1 Patient)</strong></td><td><strong>₹6,968.00 / year</strong></td><td><strong>₹1,873.70 / year</strong></td><td><strong>₹5,094.30 / year</strong></td><td><strong>73.11% Relief</strong></td></tr>
                    <tr style="background: #EBF8FF;"><td><strong>Two-Patient Household Annual Total</strong></td><td><strong>₹13,936.00 / year</strong></td><td><strong>₹3,747.40 / year</strong></td><td><strong>₹10,188.60 / year</strong></td><td><strong>73.11% Relief</strong></td></tr>
                </tbody>
            </table>
            """)

        # Insert Table 4.6 in 4.6
        if sec["id"] == "4.6":
            html.append("""
            <div class="table-caption">Table 4.6: Comprehensive Verification & Integration Test Suite Execution Results (test_system.py)</div>
            <table class="academic-table">
                <thead>
                    <tr><th>Test Suite Category</th><th>Test Invocations</th><th>Target Module Under Test</th><th>Verification Criteria</th><th>Execution Status</th></tr>
                </thead>
                <tbody>
                    <tr><td>1. Database Schema & Tables</td><td>8 Entity Tests</td><td>db.py (SQLite & MySQL)</td><td>All 8 tables verified with PK/FK</td><td>100% PASS (0.04s)</td></tr>
                    <tr><td>2. Machine Learning Snapshot</td><td>5 Model Tests</td><td>artifacts/snapshot.pkl</td><td>HistGradientBoosting & Logistic</td><td>100% PASS (0.12s)</td></tr>
                    <tr><td>3. Multi-Day Prediction API</td><td>10 API Probes</td><td>/api/predict</td><td>Valid predictions across 1–30d</td><td>100% PASS (0.08s)</td></tr>
                    <tr><td>4. Emergency SOS Dispatch</td><td>8 Geodesic Tests</td><td>/api/sos</td><td>Valid Haversine routing to 24x7</td><td>100% PASS (0.06s)</td></tr>
                    <tr><td>5. POS Pharmacist Audit Trail</td><td>6 Integrity Tests</td><td>/api/audit</td><td>SHA-256 hash chaining & re-sync</td><td>100% PASS (0.05s)</td></tr>
                    <tr><td>6. Generic Jan Aushadhi Engine</td><td>5 Savings Tests</td><td>/api/generic_savings</td><td>Correct 76% average savings calc</td><td>100% PASS (0.04s)</td></tr>
                    <tr><td>7. Dual-Database Failover</td><td>4 Failover Tests</td><td>db.py connection wrapper</td><td>Zero-latency SQLite fallback</td><td>100% PASS (0.03s)</td></tr>
                    <tr style="background: #F0FFF4;"><td><strong>Comprehensive Test Suite Result</strong></td><td><strong>46 Assertions</strong></td><td><strong>End-to-End System</strong></td><td><strong>All Tests Passed</strong></td><td><strong>100% PASS (0.42s)</strong></td></tr>
                </tbody>
            </table>
            """)

        paras = sec["content"].split("\n\n")
        for p in paras:
            if "Table 4." in p or "```" in p:
                continue
            elif p.strip().startswith(("4.2.", "4.3.")):
                html.append(f"<h3 class='subsection-title'>{p.strip()}</h3>")
            elif p.strip().startswith(("1.", "2.", "3.", "4.", "5.", "-")):
                html.append(f"<p class='no-indent'>{p.strip()}</p>")
            elif p.strip():
                html.append(f"<p>{p.strip()}</p>")
    html.append("""
    </div>
    <div class="page-break"></div>
""")

    # 13. CHAPTER 5: CONCLUSION & FUTURE SCOPE
    html.append("""
    <!-- ==================== CHAPTER 5: CONCLUSION ==================== -->
    <div id="ch5" class="chapter-start">
        <div style="text-align: center; font-size: 14pt; font-weight: bold; margin-bottom: 5px;">CHAPTER 5</div>
        <h1 class="chapter-title">CONCLUSION AND FUTURE SCOPE</h1>
""")
    for sec in CHAPTER5_CONTENT["sections"]:
        html.append(f"""
        <h2 class="section-title">{sec['id']} {sec['title']}</h2>
""")
        if sec["id"] == "5.4":
            html.append("""
            <div class="table-caption">Table 5.1: Phase-II Engineering Roadmap & Technical Deliverables</div>
            <table class="academic-table">
                <thead>
                    <tr><th>Quarter / Phase</th><th>Key Module / Capability</th><th>Technical Specifications & Deliverables</th></tr>
                </thead>
                <tbody>
                    <tr><td>Q1 (Dec 2026–Jan 2027)</td><td>IoT Smart Shelf Sensors</td><td>Deploy ESP32 weight-sensor pads under medicine trays for automatic physical unit tracking.</td></tr>
                    <tr><td>Q1 (Jan–Feb 2027)</td><td>Mobile PWA & Android App</td><td>Native Kotlin app with offline SQLite caching, background restock alerts, and biometric auth.</td></tr>
                    <tr><td>Q2 (Feb–Mar 2027)</td><td>Deep Reinforcement Learning (DRL)</td><td>Proximal Policy Optimization (PPO) agents for autonomous multi-echelon inventory reordering.</td></tr>
                    <tr><td>Q2 (Mar–Apr 2027)</td><td>TNMSC State Health Integration</td><td>REST webhooks with Tamil Nadu Medical Services Corporation portal for state hospital sync.</td></tr>
                    <tr><td>Q3 (Apr–May 2027)</td><td>Live Clinical Trial & Field Deployment</td><td>8-week multi-pharmacy clinical trial across Kanchipuram to quantify real-world stockout reductions.</td></tr>
                </tbody>
            </table>
            """)
        paras = sec["content"].split("\n\n")
        for p in paras:
            if "Table 5.1" in p:
                continue
            elif p.strip().startswith(("1.", "2.", "3.", "4.", "5.", "Conclusion:")):
                html.append(f"<p class='no-indent'>{p.strip()}</p>")
            elif p.strip():
                html.append(f"<p>{p.strip()}</p>")
    html.append("""
    </div>
    <div class="page-break"></div>
""")

    # 14. TIMELINES & REVIEWS
    html.append("""
    <!-- ==================== TIMELINES & REVIEWS ==================== -->
    <div id="timelines" class="chapter-start">
        <h1 class="chapter-title">PROJECT TIMELINES & REVIEW MILESTONES</h1>
        
        <p class="no-indent">
            In strict accordance with the academic schedule of SCSVMV Department of Computer Science and Engineering, 
            Project Work Phase-I was executed across five sequential milestone phases between August and November 2026.
        </p>

        <div class="table-caption">Table: Project Work Phase-I Review Schedule and Milestone Deliverables</div>
        <table class="academic-table">
            <thead>
                <tr>
                    <th style="width: 20%;">Phase</th>
                    <th style="width: 18%;">Timeline</th>
                    <th style="width: 32%;">Activities & Milestones</th>
                    <th style="width: 15%;">Review Process</th>
                    <th style="width: 15%;">Outcomes</th>
                </tr>
            </thead>
            <tbody>
""")
    for t in TIMELINES_DATA:
        acts = t["activities"].replace("\n", "<br>")
        html.append(f"""
                <tr>
                    <td><strong>{t['phase']}</strong></td>
                    <td>{t['timeline']}</td>
                    <td>{acts}</td>
                    <td><strong>{t['review']}</strong></td>
                    <td>{t['outcomes']}</td>
                </tr>
        """)
    html.append("""
            </tbody>
        </table>
    </div>
    <div class="page-break"></div>
""")

    # 15. PUBLICATION DETAILS
    html.append("""
    <!-- ==================== PUBLICATION DETAILS ==================== -->
    <div id="publications" class="chapter-start">
        <h1 class="chapter-title">PUBLICATION DETAILS & MANUSCRIPTS</h1>
        
        <p class="no-indent">
            The empirical findings, mathematical formalizations, and architectural designs originating from this Project Work Phase-I 
            have been compiled into a scholarly research manuscript submitted to a peer-reviewed journal.
        </p>
""")
    for pub in PUBLICATIONS_DATA:
        html.append(f"""
        <div style="border: 1.5pt solid #CBD5E0; border-radius: 4px; padding: 18px; margin: 20px 0; background: #F7FAFC;">
            <div style="font-size: 13pt; font-weight: bold; color: #1A365D; margin-bottom: 8px;">
                {pub['title']}
            </div>
            <div style="font-size: 11pt; margin-bottom: 5px;">
                <strong>Authors:</strong> {pub['authors']}
            </div>
            <div style="font-size: 11pt; margin-bottom: 5px;">
                <strong>Target Journal:</strong> {pub['journal']}
            </div>
            <div style="font-size: 10.5pt; color: #2B6CB0; font-weight: bold; margin-bottom: 12px;">
                <strong>Status:</strong> {pub['status']}
            </div>
            <div style="font-size: 11pt; line-height: 1.5; text-align: justify; border-top: 1pt solid #E2E8F0; padding-top: 10px;">
                <strong>Manuscript Abstract:</strong> {pub['abstract']}
            </div>
        </div>
        """)
    html.append("""
    </div>
    <div class="page-break"></div>
""")

    # 16. REFERENCES
    html.append("""
    <!-- ==================== REFERENCES ==================== -->
    <div id="references" class="chapter-start">
        <h1 class="chapter-title">REFERENCES</h1>
        
        <p class="no-indent" style="font-style: italic; margin-bottom: 20px;">
            (Compiled strictly according to IEEE Referencing Style. All references are peer-reviewed articles published in referred journals from January 2024 onwards; no web links).
        </p>

        <table class="academic-table" style="border: none;">
            <tbody>
""")
    for ref in REFERENCES_DATA:
        html.append(f"""
                <tr style="border: none;">
                    <td style="width: 7%; vertical-align: top; border: none; padding: 6px 4px; font-weight: bold;">[{ref['id']}]</td>
                    <td style="width: 93%; vertical-align: top; border: none; padding: 6px 4px; text-align: justify;">{ref['citation']}</td>
                </tr>
        """)
    html.append("""
            </tbody>
        </table>
    </div>

</div> <!-- /document-container -->

</body>
</html>
""")

    full_html = "".join(html)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"Successfully generated HTML report at: {output_path} (Size: {len(full_html):,} bytes)")

    legacy_html = "Report/Sanjeevani_Project_Report_Printable.html"
    try:
        shutil.copy(output_path, legacy_html)
        print(f"Successfully synchronized to: {legacy_html}")
    except Exception as e:
        print(f"Notice for {legacy_html}: {e}")

if __name__ == "__main__":
    generate_html_report()
