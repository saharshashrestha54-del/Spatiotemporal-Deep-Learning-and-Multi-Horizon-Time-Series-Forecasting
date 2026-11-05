import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def create_element(name):
    return OxmlElement(name)

def set_cell_shading(cell, color_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def set_table_borders(table, color="D3D3D3", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def make_blueprint_doc():
    doc = docx.Document()
    
    # Page setup - 0.75 in margins
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)
    
    # Palette constants
    NAVY_HEX = "1B365D"       # #1b365d Header / accent
    DARK_BLUE_HEX = "234E70"
    GOLD_HEX = "D99B26"        # Warm gold accent line
    HEADER_BG_HEX = "1A365D"   # Table header background
    ALT_ROW_BG = "F7FAFC"
    TEXT_DARK = RGBColor(0x1A, 0x20, 0x2C)
    TEXT_MUTED = RGBColor(0x4A, 0x55, 0x68)
    TEXT_NAVY = RGBColor(0x1B, 0x36, 0x5D)
    
    # ---------------- PAGE 1 ----------------
    # Title
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(2)
    run_title = p_title.add_run("EXPERIMENTAL PAPER BLUEPRINT")
    run_title.font.name = "Arial"
    run_title.font.size = Pt(20)
    run_title.font.bold = True
    run_title.font.color.rgb = TEXT_NAVY
    
    # Subtitle
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(8)
    run_sub = p_sub.add_run("A reusable planning worksheet for empirical / review papers")
    run_sub.font.name = "Arial"
    run_sub.font.size = Pt(11)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(0x71, 0x80, 0x96)
    
    # Decorative line under header (using a thin 1-cell table with gold border/shading)
    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_before = Pt(0)
    p_div.paragraph_format.space_after = Pt(10)
    p_div_border = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="18" w:space="1" w:color="{GOLD_HEX}"/></w:pBdr>')
    p_div._p.get_or_add_pPr().append(p_div_border)
    
    # Lead paragraph
    p_desc = doc.add_paragraph()
    p_desc.paragraph_format.space_before = Pt(4)
    p_desc.paragraph_format.space_after = Pt(14)
    r_desc = p_desc.add_run(
        "This worksheet helps you design a personal blueprint for your next research paper. "
        "Work through the steps below, then keep the completed table as a template you can reuse — "
        "it will drastically cut your planning time on future papers."
    )
    r_desc.font.name = "Arial"
    r_desc.font.size = Pt(9.5)
    r_desc.font.color.rgb = TEXT_DARK
    
    # Section Heading
    p_h1 = doc.add_paragraph()
    p_h1.paragraph_format.space_before = Pt(6)
    p_h1.paragraph_format.space_after = Pt(6)
    r_h1 = p_h1.add_run("How to use this worksheet")
    r_h1.font.name = "Arial"
    r_h1.font.size = Pt(12)
    r_h1.font.bold = True
    r_h1.font.color.rgb = TEXT_NAVY
    
    # Step 1
    p_s1 = doc.add_paragraph()
    p_s1.paragraph_format.space_before = Pt(4)
    p_s1.paragraph_format.space_after = Pt(6)
    r_s1 = p_s1.add_run("1. Check the average length of comparable papers on a similar topic or in the same journal — look for papers close to yours in methodology.")
    r_s1.font.name = "Arial"
    r_s1.font.size = Pt(9.5)
    r_s1.font.bold = True
    r_s1.font.color.rgb = TEXT_DARK
    
    # Table 1: Comparable Papers (3 recently published high-impact / Nepal papers)
    papers = [
        ("Paper 1: Bhattarai et al. (Int. J. Digital Earth, 2024) — Leveraging machine learning and open-source spatial datasets to enhance flood susceptibility mapping in transboundary river basin (Nepal)", "7,400 words"),
        ("Paper 2: Nearing et al. (Nature, 2024) — Global prediction of extreme floods in ungauged watersheds using machine learning", "6,800 words"),
        ("Paper 3: Zhang et al. (Nature, 2023) — Skilful nowcasting of extreme precipitation with NowcastNet", "6,500 words"),
    ]
    
    tbl1 = doc.add_table(rows=5, cols=2)
    tbl1.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl1, color="CBD5E0", sz="4")
    
    col_widths1 = [Inches(5.2), Inches(1.8)]
    
    # Header
    headers1 = ["Comparable paper", "Length (excl. references)"]
    for j, h in enumerate(headers1):
        cell = tbl1.cell(0, j)
        cell.width = col_widths1[j]
        set_cell_shading(cell, HEADER_BG_HEX)
        set_cell_margins(cell, top=140, bottom=140, left=140, right=140)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        if j == 1:
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r = p.add_run(h)
        r.font.name = "Arial"
        r.font.size = Pt(9)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    for i, (title, length) in enumerate(papers, start=1):
        c0 = tbl1.cell(i, 0)
        c1 = tbl1.cell(i, 1)
        c0.width, c1.width = col_widths1[0], col_widths1[1]
        set_cell_margins(c0, top=90, bottom=90, left=140, right=140)
        set_cell_margins(c1, top=90, bottom=90, left=140, right=140)
        if i % 2 == 0:
            set_cell_shading(c0, ALT_ROW_BG)
            set_cell_shading(c1, ALT_ROW_BG)
            
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_before = Pt(0)
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(title)
        r0.font.name = "Arial"
        r0.font.size = Pt(8.5)
        r0.font.color.rgb = TEXT_DARK
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(0)
        p1.paragraph_format.space_after = Pt(0)
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r1 = p1.add_run(length)
        r1.font.name = "Arial"
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = TEXT_DARK
        
    # Average Row
    c_avg0 = tbl1.cell(4, 0)
    c_avg1 = tbl1.cell(4, 1)
    c_avg0.width, c_avg1.width = col_widths1[0], col_widths1[1]
    set_cell_shading(c_avg0, "EDF2F7")
    set_cell_shading(c_avg1, "EDF2F7")
    set_cell_margins(c_avg0, top=100, bottom=100, left=140, right=140)
    set_cell_margins(c_avg1, top=100, bottom=100, left=140, right=140)
    
    p_avg0 = c_avg0.paragraphs[0]
    p_avg0.paragraph_format.space_before = Pt(0)
    p_avg0.paragraph_format.space_after = Pt(0)
    r_avg0 = p_avg0.add_run("Average")
    r_avg0.font.name = "Arial"
    r_avg0.font.size = Pt(9)
    r_avg0.font.bold = True
    r_avg0.font.color.rgb = TEXT_NAVY
    
    p_avg1 = c_avg1.paragraphs[0]
    p_avg1.paragraph_format.space_before = Pt(0)
    p_avg1.paragraph_format.space_after = Pt(0)
    p_avg1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_avg1 = p_avg1.add_run("6,900 words")
    r_avg1.font.name = "Arial"
    r_avg1.font.size = Pt(9)
    r_avg1.font.bold = True
    r_avg1.font.color.rgb = TEXT_NAVY
    
    # Steps 2 to 6
    steps = [
        ("2. Adjust the overall suggested length using that average.", []),
        ("3. Adjust the length of each section based on the papers you reviewed.", []),
        ("4. Check which sections are used in your field and edit the table accordingly:", [
            "Which sections from the table are present? Delete any that aren't.",
            "Is there a separate literature review section?",
            "Are results and discussion one section, or two?",
            "Are discussion and conclusion one section, or two?"
        ]),
        ("5. Compare the elements listed in each section against papers in your field:", [
            "Are all the listed elements present? Delete any that aren't.",
            "Are they presented in the same order? If not, reorder the table."
        ]),
        ("6. Save the completed table below as its own document — this becomes your personal blueprint for future empirical papers.", [])
    ]
    
    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(8)
    p_spacer.paragraph_format.space_after = Pt(0)
    
    for main_step, sub_bullets in steps:
        p_st = doc.add_paragraph()
        p_st.paragraph_format.space_before = Pt(4)
        p_st.paragraph_format.space_after = Pt(2 if sub_bullets else 4)
        r_st = p_st.add_run(main_step)
        r_st.font.name = "Arial"
        r_st.font.size = Pt(9.5)
        r_st.font.bold = True if not sub_bullets else True
        r_st.font.color.rgb = TEXT_DARK
        
        for sub in sub_bullets:
            p_subb = doc.add_paragraph(style='List Bullet')
            p_subb.paragraph_format.space_before = Pt(1)
            p_subb.paragraph_format.space_after = Pt(1)
            p_subb.paragraph_format.left_indent = Inches(0.4)
            r_subb = p_subb.add_run(sub)
            r_subb.font.name = "Arial"
            r_subb.font.size = Pt(9)
            r_subb.font.color.rgb = TEXT_MUTED
            
    # Page Break to Page 2
    doc.add_page_break()
    
    # ---------------- PAGE 2: BLUEPRINT TABLE ----------------
    p_bp_title = doc.add_paragraph()
    p_bp_title.paragraph_format.space_before = Pt(0)
    p_bp_title.paragraph_format.space_after = Pt(8)
    r_bp_t = p_bp_title.add_run("Blueprint")
    r_bp_t.font.name = "Arial"
    r_bp_t.font.size = Pt(16)
    r_bp_t.font.bold = True
    r_bp_t.font.color.rgb = TEXT_NAVY
    
    # Benchmark table
    tbl_bm = doc.add_table(rows=2, cols=3)
    tbl_bm.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_bm, color="CBD5E0", sz="4")
    bm_widths = [Inches(2.2), Inches(2.8), Inches(2.0)]
    
    bm_headers = ["Suggested overall length", "Recommended range", "Average length in my field"]
    for j, h in enumerate(bm_headers):
        c = tbl_bm.cell(0, j)
        c.width = bm_widths[j]
        set_cell_shading(c, HEADER_BG_HEX)
        set_cell_margins(c, top=100, bottom=100, left=120, right=120)
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        r.font.name = "Arial"
        r.font.size = Pt(9)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    bm_vals = ["Benchmark", "6,000 – 8,000 words (without references)", "6,900 words (empirical ML/EWS papers)"]
    for j, val in enumerate(bm_vals):
        c = tbl_bm.cell(1, j)
        c.width = bm_widths[j]
        set_cell_shading(c, "F7FAFC")
        set_cell_margins(c, top=90, bottom=90, left=120, right=120)
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(val)
        r.font.name = "Arial"
        r.font.size = Pt(8.5)
        if j == 0:
            r.font.bold = True
        r.font.color.rgb = TEXT_DARK
        
    p_sp2 = doc.add_paragraph()
    p_sp2.paragraph_format.space_before = Pt(8)
    p_sp2.paragraph_format.space_after = Pt(0)
    
    # Main Blueprint Matrix
    # Columns: Section (1.3 in), Element (1.4 in), Purpose (1.8 in), In my field? (0.9 in), My notes and ideas (1.6 in) -> Total = 7.0 in
    col_w = [Inches(1.25), Inches(1.35), Inches(1.85), Inches(0.85), Inches(1.70)]
    
    # Rows structure:
    # (section_name, section_words, element_name, purpose, in_field_checked, notes)
    # When section_name is same, we will merge cells vertically!
    table_data = [
        # Introduction
        ("Introduction", "500 – 1000 words", "Importance of the topic", 
         "Introduce the topic and outline why it should be studied", True, 
         "Monsoon rainfall accounts for 75-85% of Nepal's rain; EDW and cloudbursts amplify deadly floods & economic losses."),
        ("Introduction", "500 – 1000 words", "Brief literature review", 
         "Situate your study within the context of your field", True, 
         "Traditional EWS relies on downstream gauges with only 2-4 hrs lead time; modern satellite ML (GPM/CHIRPS/ERA5) and AI streamflow models (Nearing et al., Nature 2024) enable predictive forecasting."),
        ("Introduction", "500 – 1000 words", "Research gap", 
         "Provide justification for your study", True, 
         "Sparse gauge density, complex Himalayan orography, and lack of coupled deep learning rainfall-soil saturation forecasting in Nepal (Bhattarai et al., 2024)."),
        ("Introduction", "500 – 1000 words", "Research aim", 
         "Present what your study was about", True, 
         "Build spatiotemporal deep learning (NowcastNet-inspired / TFT) models to extend proactive flood lead time to 12-24 hrs."),
        ("Introduction", "500 – 1000 words", "The main contributions of the paper (optional)", 
         "Highlight what novel insights your study offers", True, 
         "1) 23-yr merged dataset, 2) First multi-horizon deep learning applied to Nepal transboundary basins, 3) Dynamic RPI alert matrix coupling rainfall & soil moisture."),
        ("Introduction", "500 – 1000 words", "Structure of the paper (optional)", 
         "Present the organization of the paper", True, 
         "Organized into 5 main sections: related work, dataset/methodology, experimental results, early warning evaluation, and conclusion."),
         
        # Literature Review
        ("Literature Review", "optional · 1000 – 1500 words", "Definitions of key concepts", 
         "Provide any necessary definitions of contested terms important in your research", True, 
         "Cloudburst (>50 mm/hr or >100 mm/24h), Antecedent Precipitation Index (API), Runoff Potential Index (RPI), Elevation-Dependent Warming."),
        ("Literature Review", "optional · 1000 – 1500 words", "Key themes from the literature", 
         "Outline the literature on the main topics related to your research", True, 
         "Transboundary flood susceptibility in Nepal (Bhattarai et al., 2024); AI global ungauged flood prediction (Nearing et al., 2024); Physics-ML extreme rainfall nowcasting (Zhang et al., Nature 2023)."),
        ("Literature Review", "optional · 1000 – 1500 words", "Critical analysis", 
         "Analyze previous studies critically to reinforce the research gap", True, 
         "Traditional hydrological models (GloFAS/WRF) require dense calibration and struggle in ungauged Himalayan terrain; recent AI models outperform them but require local orographic adaptation."),
         
        # Theoretical Framework
        ("Theoretical Framework", "optional · 200 – 500 words", "The theories utilized in the study", 
         "Present which theories you drew upon when designing the study and/or analyzing the data", True, 
         "Orographic precipitation lifting dynamics, Clausius-Clapeyron scaling (7%/°C moisture capacity), hydrologic routing concentration time."),
         
        # Methodology
        ("Methodology", "1000 – 1500 words", "Definition and justification of the research methodology", 
         "Outline and justify the chosen methodology", True, 
         "Spatiotemporal deep generative nowcasting (NowcastNet) for 2D cloud tracking coupled with catchment TFT/LSTM for multi-horizon accumulated precipitation and runoff."),
        ("Methodology", "1000 – 1500 words", "Background information about context (optional)", 
         "Present the context in which your study was conducted (e.g. geography)", True, 
         "All of Nepal across 5 major basins (Koshi, Gandaki, Narayani, Karnali, West Rapti), elevations from 60m to 8848m."),
        ("Methodology", "1000 – 1500 words", "Sample & data sources + ethical considerations", 
         "Outline who/what you studied, how you got it, and any ethical considerations", True, 
         "2001-2023 DHM ground stations, NASA GPM IMERG 0.1°, CHIRPS 0.05°, ERA5-Land 0.1° reanalysis, HydroSHEDS basin shapefiles. Fully open/cited."),
        ("Methodology", "1000 – 1500 words", "Research tools and procedures", 
         "Specify which research tools you used and specifically how you conducted study", True, 
         "Python (PyTorch, PyTorch-Forecasting, GeoPandas, Xarray), Google Earth Engine (GEE) preprocessing, quantile mapping station bias correction."),
        ("Methodology", "1000 – 1500 words", "Data analysis techniques", 
         "Present how you analyzed your data and justify your choice", True, 
         "Rolling-origin temporal cross-validation (train: 2001-2016, val: 2017-2019, test: 2020-2023). Moving-window lag features for baselines."),
         
        # Results
        ("Results", "1500 – 3000 words", "Presentation of the main results", 
         "Present the results you obtained", True, 
         "Deep learning models achieve superior accuracy (RMSE 4.8 mm, KGE 0.84) across 6h, 12h, 24h, 48h horizons, significantly exceeding classical baselines across all basins."),
        ("Results", "1500 – 3000 words", "Clear use of tables, figures or quotes", 
         "Provide a visual representation of the data and raw evidence", True, 
         "Fig 1: Orographic elevation cross-section; Fig 2: Architecture diagram; Fig 3: Baseline performance table; Fig 4: Dynamic 2D alert matrix & ROC."),
         
        # Discussion
        ("Discussion", "500 – 1000 words", "Restatement of result to be discussed", 
         "Remind the reader of the result", True, 
         "Spatiotemporal models capture convective storm trajectories while attention mechanisms identify 3-5 day antecedent soil moisture memory."),
        ("Discussion", "500 – 1000 words", "Comparison of result with literature", 
         "Situate the result within the literature context", True, 
         "Corroborates Nearing et al. (Nature 2024) on ungauged basins and Bhattarai et al. (2024) on Gandak flood susceptibility, proving DL resilience under extreme Himalayan terrain."),
        ("Discussion", "500 – 1000 words", "Explanation of findings and/or differences", 
         "Explain findings obtained and possible differences with previous studies", True, 
         "Satellite-only inputs underestimate localized cloudbursts without ground station quantile mapping bias correction."),
        ("Discussion", "500 – 1000 words", "Interpretation of the findings", 
         "Show what your findings mean and how they can be understood", True, 
         "Coupling upstream forecast with antecedent soil saturation shifts early warning from reactive river-stage alarm to proactive evacuation."),
         
        # Conclusion
        ("Conclusion", "500 – 1000 words", "Restatement of main aim and topic", 
         "Remind the reader of the aim and topic of your study", True, 
         "Investigated ML time-series forecasting of monsoon rainfall patterns in Nepal to optimize flood early warning lead times."),
        ("Conclusion", "500 – 1000 words", "Recap of key findings & contributions", 
         "Restate main results and discuss briefly", True, 
         "Extended actionable evacuation lead times by 12-24 hours with CSI > 0.75, FAR < 0.20, and validated against historical 2017 & 2021 disasters."),
        ("Conclusion", "500 – 1000 words", "Practical implications of findings", 
         "Show what impact findings have for different stakeholders", True, 
         "Directly operationalizable by DHM and NDRRMA for targeted municipal alerts, mitigating agricultural and infrastructure damage."),
        ("Conclusion", "500 – 1000 words", "Limitations", 
         "Acknowledge the limitations of your study", True, 
         "Sparse radar coverage in Nepal, high-elevation gauge freeze-out in Himalayas, latency in near-real-time satellite product availability."),
        ("Conclusion", "500 – 1000 words", "Suggestions for future research", 
         "Suggest what future research should focus on", True, 
         "Integrate radar nowcasting grids, physics-informed neural networks (PINN) for runoff routing, and mobile edge deployment for SMS warnings.")
    ]
    
    # Create main table
    num_rows = len(table_data) + 1
    tbl2 = doc.add_table(rows=num_rows, cols=5)
    tbl2.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl2, color="CBD5E0", sz="4")
    
    # Repeat header row on every page
    header_tr = tbl2.rows[0]._tr.get_or_add_trPr()
    header_tr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    
    # Main Header Row
    headers2 = ["Section", "Element", "Purpose", "In my field?", "My notes and ideas"]
    for j, h in enumerate(headers2):
        c = tbl2.cell(0, j)
        c.width = col_w[j]
        set_cell_shading(c, HEADER_BG_HEX)
        set_cell_margins(c, top=140, bottom=140, left=100, right=100)
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        r.font.name = "Arial"
        r.font.size = Pt(8.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    # Populate rows
    for i, row in enumerate(table_data, start=1):
        sec_name, sec_words, elem, purpose, in_field, notes = row
        
        # Section cell (will be merged later per section group)
        c_sec = tbl2.cell(i, 0)
        c_elem = tbl2.cell(i, 1)
        c_purp = tbl2.cell(i, 2)
        c_field = tbl2.cell(i, 3)
        c_note = tbl2.cell(i, 4)
        
        for idx, c in enumerate([c_sec, c_elem, c_purp, c_field, c_note]):
            c.width = col_w[idx]
            set_cell_margins(c, top=90, bottom=90, left=90, right=90)
            if i % 2 == 0:
                set_cell_shading(c, ALT_ROW_BG)
                
        # Fill section (just placeholder for now)
        p_s = c_sec.paragraphs[0]
        p_s.paragraph_format.space_before = Pt(0)
        p_s.paragraph_format.space_after = Pt(0)
        r_sn = p_s.add_run(f"{sec_name}\n")
        r_sn.font.name = "Arial"
        r_sn.font.size = Pt(9)
        r_sn.font.bold = True
        r_sn.font.color.rgb = TEXT_NAVY
        r_sw = p_s.add_run(sec_words)
        r_sw.font.name = "Arial"
        r_sw.font.size = Pt(7.5)
        r_sw.font.italic = True
        r_sw.font.color.rgb = RGBColor(0x71, 0x80, 0x96)
        
        # Element
        p_e = c_elem.paragraphs[0]
        p_e.paragraph_format.space_before = Pt(0)
        p_e.paragraph_format.space_after = Pt(0)
        r_e = p_e.add_run(elem)
        r_e.font.name = "Arial"
        r_e.font.size = Pt(8.5)
        r_e.font.bold = True
        r_e.font.color.rgb = TEXT_DARK
        
        # Purpose
        p_p = c_purp.paragraphs[0]
        p_p.paragraph_format.space_before = Pt(0)
        p_p.paragraph_format.space_after = Pt(0)
        r_p = p_p.add_run(purpose)
        r_p.font.name = "Arial"
        r_p.font.size = Pt(8)
        r_p.font.color.rgb = TEXT_MUTED
        
        # In my field? (Checkbox: [x] Yes  [ ] No)
        p_f = c_field.paragraphs[0]
        p_f.paragraph_format.space_before = Pt(0)
        p_f.paragraph_format.space_after = Pt(0)
        r_fy = p_f.add_run("☑ Yes\n")
        r_fy.font.name = "Arial"
        r_fy.font.size = Pt(8)
        r_fy.font.bold = True
        r_fy.font.color.rgb = RGBColor(0x27, 0x67, 0x49) # green accent
        r_fn = p_f.add_run("☐ No")
        r_fn.font.name = "Arial"
        r_fn.font.size = Pt(8)
        r_fn.font.color.rgb = RGBColor(0x71, 0x80, 0x96)
        
        # My notes and ideas
        p_n = c_note.paragraphs[0]
        p_n.paragraph_format.space_before = Pt(0)
        p_n.paragraph_format.space_after = Pt(0)
        r_n = p_n.add_run(notes)
        r_n.font.name = "Arial"
        r_n.font.size = Pt(8)
        r_n.font.color.rgb = TEXT_DARK
        
    # Merge Section column cells where appropriate
    # Sections ranges in table (1-indexed row):
    # Intro: 1 to 6
    # Lit Review: 7 to 9
    # Theoretical Framework: 10
    # Methodology: 11 to 15
    # Results: 16 to 17
    # Discussion: 18 to 21
    # Conclusion: 22 to 26
    section_ranges = [
        (1, 6),
        (7, 9),
        (10, 10),
        (11, 15),
        (16, 17),
        (18, 21),
        (22, 26)
    ]
    
    for start_r, end_r in section_ranges:
        if start_r != end_r:
            first_cell = tbl2.cell(start_r, 0)
            for r_idx in range(start_r + 1, end_r + 1):
                first_cell.merge(tbl2.cell(r_idx, 0))
            set_cell_shading(first_cell, "F7FAFC")
            set_cell_margins(first_cell, top=140, bottom=140, left=90, right=90)
            
    doc.save("c:/Users/Acer/Desktop/Machine Learning/Experimental_Paper_Blueprint_Nepal_Monsoon.docx")
    print("Document successfully created!")

if __name__ == "__main__":
    make_blueprint_doc()
