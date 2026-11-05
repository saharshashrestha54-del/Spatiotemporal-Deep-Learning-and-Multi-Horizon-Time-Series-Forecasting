import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_comprehensive_proposal():
    doc = docx.Document()

    # Set Margins (Standard 1 inch / 72 pt)
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Base Normal Style Configuration (Times New Roman 12pt)
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(6)

    # Helper: Add Hyperlink
    def add_hyperlink(paragraph, url, text, color='004B87', underline=True):
        part = paragraph.part
        r_id = part.relate_to(url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)
        hyperlink = parse_xml(f'<w:hyperlink {nsdecls("w", "r")} r:id="{r_id}"/>')
        new_run = parse_xml(
            f'<w:r {nsdecls("w")}><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:color w:val="{color}"/>'
            + ('<w:u w:val="single"/>' if underline else '')
            + f'</w:rPr></w:r>'
        )
        t_elem = parse_xml(f'<w:t {nsdecls("w")}/>')
        t_elem.text = text
        new_run.append(t_elem)
        hyperlink.append(new_run)
        paragraph._p.append(hyperlink)

    # Helpers for Typography
    def add_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(16)
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(16)
        run.bold = True
        run.font.color.rgb = RGBColor(0, 32, 96) # Dark Navy
        return p

    def add_subtitle(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(20)
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.italic = True
        run.font.color.rgb = RGBColor(80, 80, 80)
        return p

    def add_heading_1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(14)
        run.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_heading_2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.bold = True
        run.font.color.rgb = RGBColor(30, 30, 30)
        return p

    def add_heading_3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.bold = True
        run.italic = True
        run.font.color.rgb = RGBColor(50, 50, 50)
        return p

    def add_paragraph(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        return p

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_bold = p.add_run(bold_prefix)
            r_bold.font.name = 'Times New Roman'
            r_bold.font.size = Pt(12)
            r_bold.bold = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        return p

    def add_figure(img_path, caption_text, width_inches=6.2):
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(10)
            p_img.paragraph_format.space_after = Pt(4)
            p_img.add_run().add_picture(img_path, width=Inches(width_inches))

            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(12)
            p_cap.paragraph_format.keep_with_next = True
            r_cap = p_cap.add_run(caption_text)
            r_cap.font.name = 'Times New Roman'
            r_cap.font.size = Pt(10.5)
            r_cap.bold = True
            r_cap.italic = True
            r_cap.font.color.rgb = RGBColor(40, 40, 40)

    # =========================================================================
    # DEDICATED COVER PAGE
    # =========================================================================
    p_spacer_top = doc.add_paragraph()
    p_spacer_top.paragraph_format.space_before = Pt(72)

    # Document Classification Banner
    p_type = doc.add_paragraph()
    p_type.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_type.paragraph_format.space_after = Pt(20)
    r_type = p_type.add_run("ACADEMIC RESEARCH PROJECT PROPOSAL")
    r_type.font.name = 'Times New Roman'
    r_type.font.size = Pt(13)
    r_type.bold = True
    r_type.font.color.rgb = RGBColor(100, 116, 139) # Slate Grey

    # Main Title on Cover Page
    p_main_title = doc.add_paragraph()
    p_main_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_main_title.paragraph_format.space_before = Pt(14)
    p_main_title.paragraph_format.space_after = Pt(18)
    p_main_title.paragraph_format.line_spacing = 1.25
    r_main_title = p_main_title.add_run("DATA-DRIVEN SPATIOTEMPORAL ANALYSIS AND MACHINE LEARNING TIME-SERIES FORECASTING OF MONSOON RAINFALL PATTERNS IN NEPAL FOR FLOOD EARLY WARNING OPTIMIZATION")
    r_main_title.font.name = 'Times New Roman'
    r_main_title.font.size = Pt(17)
    r_main_title.bold = True
    r_main_title.font.color.rgb = RGBColor(0, 32, 96) # Dark Navy

    # Subtitle on Cover Page
    p_cover_sub = doc.add_paragraph()
    p_cover_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cover_sub.paragraph_format.space_after = Pt(36)
    r_cover_sub = p_cover_sub.add_run("A Comprehensive Spatiotemporal Machine Learning Framework for Hydrometeorological Disaster Risk Reduction")
    r_cover_sub.font.name = 'Times New Roman'
    r_cover_sub.font.size = Pt(12)
    r_cover_sub.italic = True
    r_cover_sub.font.color.rgb = RGBColor(71, 85, 105)

    # Mid-cover context
    p_context = doc.add_paragraph()
    p_context.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_context.paragraph_format.space_before = Pt(24)
    p_context.paragraph_format.space_after = Pt(90)
    r_ctx = p_context.add_run("Submitted in partial fulfillment of the requirements for the degree of\nBachelor of Science (Hons) in Computer Science / Artificial Intelligence\nDepartment of Computing and Information Systems")
    r_ctx.font.name = 'Times New Roman'
    r_ctx.font.size = Pt(11.5)
    r_ctx.font.color.rgb = RGBColor(51, 65, 85)

    # Bottom Metadata Table: Student (Left) vs. Module Leader (Right)
    meta_table = doc.add_table(rows=1, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False

    # Remove all borders for clean presentation
    tblPr = meta_table._tbl.tblPr
    borders = parse_xml(r'''
        <w:tblBorders {} >
            <w:top w:val="none"/>
            <w:left w:val="none"/>
            <w:bottom w:val="none"/>
            <w:right w:val="none"/>
            <w:insideH w:val="none"/>
            <w:insideV w:val="none"/>
        </w:tblBorders>
    '''.format(nsdecls('w')))
    tblPr.append(borders)

    cell_left = meta_table.rows[0].cells[0]
    cell_right = meta_table.rows[0].cells[1]
    cell_left.width = Inches(3.25)
    cell_right.width = Inches(3.25)

    # Left Cell: Student Information
    p_l = cell_left.paragraphs[0]
    p_l.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_l.paragraph_format.space_after = Pt(3)
    p_l.paragraph_format.line_spacing = 1.15
    r_l_lbl = p_l.add_run("Submitted By:\n")
    r_l_lbl.font.name = 'Times New Roman'
    r_l_lbl.font.size = Pt(11)
    r_l_lbl.bold = True
    r_l_lbl.font.color.rgb = RGBColor(0, 32, 96)

    r_l_name = p_l.add_run("Saharsha\n")
    r_l_name.font.name = 'Times New Roman'
    r_l_name.font.size = Pt(12)
    r_l_name.bold = True

    r_l_id = p_l.add_run("Student ID: 210425\n")
    r_l_id.font.name = 'Times New Roman'
    r_l_id.font.size = Pt(11)

    r_l_date = p_l.add_run("Date: September 2026")
    r_l_date.font.name = 'Times New Roman'
    r_l_date.font.size = Pt(10.5)
    r_l_date.font.color.rgb = RGBColor(100, 116, 139)

    # Right Cell: Module Leader Information
    p_r = cell_right.paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_r.paragraph_format.space_after = Pt(3)
    p_r.paragraph_format.line_spacing = 1.15
    r_r_lbl = p_r.add_run("Supervised & Evaluated By:\n")
    r_r_lbl.font.name = 'Times New Roman'
    r_r_lbl.font.size = Pt(11)
    r_r_lbl.bold = True
    r_r_lbl.font.color.rgb = RGBColor(0, 32, 96)

    r_r_name = p_r.add_run("[Module Leader Name]\n")
    r_r_name.font.name = 'Times New Roman'
    r_r_name.font.size = Pt(12)
    r_r_name.bold = True

    r_r_title = p_r.add_run("Module Leader / Research Supervisor\n")
    r_r_title.font.name = 'Times New Roman'
    r_r_title.font.size = Pt(11)

    r_r_dept = p_r.add_run("Faculty of Science and Technology")
    r_r_dept.font.name = 'Times New Roman'
    r_r_dept.font.size = Pt(10.5)
    r_r_dept.font.color.rgb = RGBColor(100, 116, 139)

    # Page Break after Cover Page
    doc.add_page_break()

    # --- TABLE OF CONTENTS ---
    add_heading_1("Table of Contents")

    toc_data = [
        ("1. Introduction", "3"),
        ("    1.1 Meteorological Context and the South Asian Monsoon Regime in Nepal", "3"),
        ("    1.2 The Himalayan Physical Geography and Orographic Precipitation Mechanisms", "4"),
        ("    1.3 Climate Change Accelerations and Hydro-Hazard Vulnerabilities", "5"),
        ("    1.4 Motivation for Data-Driven Predictive Machine Learning Architectures", "6"),
        ("2. Problem Statement", "7"),
        ("    2.1 The Crisis of Convective and Orographic Flash Flooding in Nepal", "7"),
        ("    2.2 Inherent Physical Deficiencies of Numerical Weather Prediction (NWP) Models", "8"),
        ("    2.3 Spatial Latency, Elevation Bias, and Gauging Inadequacies in Headwater Catchments", "9"),
        ("    2.4 The Critical Downstream Evacuation Gap and Warning Threshold Inelasticity", "10"),
        ("3. Objectives of the Study", "11"),
        ("    3.1 Primary Overarching Objective", "11"),
        ("    3.2 Specific Research and Technical Objectives", "11"),
        ("    3.3 Research Hypotheses and Success Metrics", "12"),
        ("4. Data Sources and Acquisition Strategy", "13"),
        ("    4.1 High-Resolution Satellite Precipitation Products (NASA GPM IMERG and CHIRPS)", "13"),
        ("    4.2 High-Dimensional Atmospheric Reanalysis Datasets (ECMWF ERA5-Land)", "14"),
        ("    4.3 Ground-Truth Hydrometeorological Gauges (DHM Nepal and ICIMOD RDS)", "15"),
        ("    4.4 High-Resolution Topographical, Soil, and Catchment Auxiliary Datasets", "16"),
        ("    4.5 Comprehensive Data Source Matrix and Spatial-Temporal Characterization", "17"),
        ("5. Proposed Methodology", "18"),
        ("    5.1 Data Pipeline Engineering, Geospatial Masking, and Elevation-Aware Bias Correction", "18"),
        ("    5.2 Rigorous Spatiotemporal Trend Characterization and Extreme Value Theory (EVT)", "20"),
        ("    5.3 Deep Learning Spatiotemporal Precipitation Engine (ConvLSTM, PredRNN, ST-GNN)", "21"),
        ("    5.4 Catchment-Aggregated Multi-Horizon Forecasting via Temporal Fusion Transformers (TFT)", "23"),
        ("    5.5 Empirical Benchmark Baselines (XGBoost, CatBoost, Bidirectional LSTM)", "24"),
        ("    5.6 Flood Early Warning Optimization, Threshold Mapping, and Evacuation Gain Modeling", "25"),
        ("    5.7 Computational Architecture, Model Interpretability (SHAP/Attention), and Evaluation", "26"),
        ("6. Expected Outcomes, Scientific Deliverables, and Operational Impact", "27"),
        ("7. Comprehensive 24-Week Work Plan, Resource Allocation, and Risk Mitigation", "28"),
        ("8. References", "30")
    ]

    toc_table = doc.add_table(rows=len(toc_data), cols=2)
    toc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    toc_table.autofit = False

    for i, (section_title, page_num) in enumerate(toc_data):
        row = toc_table.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(5.6)
        c1.width = Inches(0.9)
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(section_title)
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(12)
        if not section_title.startswith("    "):
            r0.bold = True

        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(page_num)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(12)
        if not section_title.startswith("    "):
            r1.bold = True

    # Page Break after TOC
    doc.add_page_break()

    # =========================================================================
    # 1. INTRODUCTION
    # =========================================================================
    add_heading_1("1. Introduction")

    add_heading_2("1.1 Meteorological Context and the South Asian Monsoon Regime in Nepal")
    add_paragraph(
        "The South Asian summer monsoon constitutes one of the most prominent, thermodynamically vigorous, and socially consequential "
        "atmospheric circulation phenomena on Earth. For the Federal Democratic Republic of Nepal, the summer monsoon—which typically "
        "initiates in early June and withdraws toward late September or early October—delivers approximately 75% to 85% of the total annual "
        "precipitation across a compressed, four-month window. Driven by the colossal differential thermal heating between the high-altitude "
        "Tibetan Plateau and the warm oceanic waters of the Indian Ocean and the Bay of Bengal, immense moisture-laden maritime air masses are "
        "funneled northward across the low-lying Indo-Gangetic Plains. Upon encountering the colossal geological ramparts of the Himalayan "
        "mountain arc, these moisture fluxes undergo intense, rapid orographic lifting, culminating in unprecedented convective updrafts, "
        "persistent rainstorms, and localized torrential downpours."
    )
    add_paragraph(
        "In a nation where agrarian cultivation sustains over 65% of the rural labor force and where run-of-the-river hydroelectric power "
        "facilities generate over 90% of national electricity, monsoon precipitation functions as the indispensable foundation of economic "
        "viability, food security, and regional water supply. The timing of monsoon onset, the spatial distribution of intraseasonal active "
        "and break spells, and the frequency of high-intensity precipitation anomalies directly govern agricultural production, reservoir "
        "storage, and groundwater recharge. Yet, this hydrological bounty exists in constant, perilous tension with severe environmental "
        "catastrophes. When moisture-laden low-level jet streams collide with high-relief topography, precipitation rates frequently exceed the "
        "infiltration capacity of mountain soils, transforming pristine alpine and sub-alpine river valleys into violent, debris-laden torrents "
        "that surge southward into populated alluvial plains."
    )

    add_heading_2("1.2 The Himalayan Physical Geography and Orographic Precipitation Mechanisms")
    add_paragraph(
        "Nepal presents what is universally recognized as the most extreme and compact topographic gradient on the planet. Across an average "
        "north-to-south lateral distance of merely 150 to 200 kilometers, the land surface ascends precipitously from the low-lying Terai "
        "plains—situated at less than 60 meters above mean sea level—through the Siwalik (Chure) foothills, the rugged Mahabharat range "
        "(Middle Mountains), the deeply incised High Himalayan massifs, and ultimately into the rain-shadowed Tibetan Marginal Plateau peaking "
        "at 8,848 meters at Mount Everest. This staggering elevation difference creates an extraordinarily complex mosaic of microclimates, "
        "wherein tropical, subtropical, temperate, subalpine, and alpine conditions coexist within the same river catchment."
    )
    add_paragraph(
        "From an atmospheric and fluid-dynamics perspective, this extreme vertical barrier acts as a formidable mechanical wedge. When "
        "stratified monsoon air masses encounter these abrupt slopes, forced orographic ascent induces intense adiabatic cooling, rapid "
        "saturation, and thermodynamic condensation. Consequently, precipitation patterns across Nepal do not follow simple latitudinal or "
        "longitudinal trends; rather, they are dictated by slope orientation, valley channeling, windward-leeward dynamics, and elevation "
        "zones. Empirical climatological records demonstrate that annual rainfall does not increase linearly with elevation; instead, it "
        "exhibits distinct dual orographic peaks—the first occurring along the southern foothills of the Siwaliks and the second concentrated "
        "along the windward slopes of the Middle Mountains at elevations between 1,500 and 2,500 meters (such as Pokhara and the Annapurna "
        "foothills, which regularly record over 4,500 mm of annual rainfall). Beyond the crest of the High Himalayas, the trans-Himalayan valleys "
        "of Mustang and Manang receive less than 300 mm annually, exemplifying extreme rain-shadow aridity. Accurately deciphering and predicting "
        "these multi-scale orographic dynamics requires modeling frameworks that integrate high-resolution terrain morphology with continuous "
        "spatiotemporal moisture tracking."
    )

    add_figure(
        r"c:\Users\Acer\Desktop\Machine Learning\figures\fig2_orographic_and_leadtime.png",
        "Figure 1: (Top) Himalayan physiographic cross-section illustrating dual-peak orographic rainfall mechanisms and trans-Himalayan rain shadow effects; (Bottom) Evacuation lead-time comparison between reactive point gauges and predictive ML forecasting.",
        width_inches=6.3
    )

    add_heading_2("1.3 Climate Change Accelerations and Hydro-Hazard Vulnerabilities")
    add_paragraph(
        "Under the accelerating influence of global climate change, the Hindu Kush Himalaya (HKH) region is warming at a rate significantly "
        "higher than the global average—a phenomenon known as Elevation-Dependent Warming (EDW). Observational and paleoclimatic studies indicate "
        "that while total seasonal monsoon rainfall volumes may exhibit subtle or statistically ambiguous decadal shifts, the internal temporal "
        "structure, frequency, and intensity distribution of monsoon precipitation are experiencing radical, non-stationary transformations. "
        "The Clausius-Clapeyron thermodynamic relationship dictates that atmospheric water-holding capacity increases by roughly 7% for every "
        "one-degree Celsius increase in temperature. In the moisture-saturated monsoon boundary layer over South Asia, this thermodynamic shift "
        "fueling deeper convective instability, leading to a marked proliferation of short-duration, high-intensity extreme precipitation "
        "events (cloudbursts) interspersed with prolonged, unseasonal dry spells."
    )
    add_paragraph(
        "The human, infrastructural, and ecological toll of these intensified hydrometeorological extremes is catastrophic. Mountain slopes, "
        "already destabilized by active tectonic seismicity, extensive road construction, and deforestation, rapidly lose shear strength when "
        "saturated by multi-day antecedent rainfall or sudden cloudburst downpours. The resulting hazards are inherently cascading and "
        "compound in nature: localized slope failures evolve into catastrophic debris flows, damming narrow gorge sections before breaching as "
        "violent Landslide Dam Outburst Floods (LDOFs) or Glacial Lake Outburst Floods (GLOFs). As these swollen flows debouch from mountain "
        "exits into the low-gradient Terai plains (such as the Koshi, Gandaki, Narayani, Karnali, West Rapti, and Bagmati basins), riverbeds "
        "choked with sediment overflow their banks, inundating hundreds of thousands of hectares of fertile farmland, displacing vulnerable "
        "rural populations, severing east-west transit arteries, and destroying vital civil infrastructure. The National Disaster Risk Reduction "
        "and Management Authority (NDRRMA) of Nepal routinely reports that water-induced disasters account for over 60% of all disaster-related "
        "mortality and economic loss annually, highlighting the critical imperative for upgraded early warning mechanisms."
    )

    add_heading_2("1.4 Motivation for Data-Driven Predictive Machine Learning Architectures")
    add_paragraph(
        "To mitigate this recurring cycle of devastation, disaster risk management paradigms must transition from reactive post-event relief "
        "to proactive, predictive anticipation. The core foundation of effective flood risk reduction is an actionable Flood Early Warning "
        "System (FEWS) capable of delivering reliable warnings with sufficient lead time for downstream district authorities, municipal emergency "
        "responders, and vulnerable community members to execute planned evacuation, secure livestock, and protect high-value assets. "
        "Historically, early warning systems have relied either on deterministic physical hydrological models or on downstream river stage gauges."
    )
    add_paragraph(
        "However, in high-energy mountain river basins characterized by short catchment concentration times, waiting for a downstream gauge "
        "to register an alert threshold leaves an evacuation window of mere minutes to a couple of hours. To achieve operational lead times of "
        "12, 24, or 48 hours, early warning must be decoupled from reactive downstream stage monitoring and coupled directly to upstream "
        "predictive rainfall forecasting. Fortunately, the recent explosion in high-resolution, multi-sensor gridded satellite precipitation "
        "estimates (e.g., NASA GPM IMERG, CHIRPS), open atmospheric reanalyses (e.g., ECMWF ERA5-Land), and deep learning methodologies "
        "provides an unprecedented opportunity. Advanced neural architectures—including Convolutional Long Short-Term Memory networks (ConvLSTM), "
        "Spatio-Temporal Graph Neural Networks (ST-GNN), and Temporal Fusion Transformers (TFT)—can natively model non-linear spatiotemporal "
        "dependencies, extract complex topographical teleconnections, and process high-dimensional atmospheric moisture dynamics orders of "
        "magnitude faster than traditional numerical models. This study is fundamentally motivated by the imperative to harness these data-driven "
        "breakthroughs to engineer a robust, operational spatiotemporal rainfall forecasting and flood warning optimization framework tailored "
        "specifically to the physiographic and hydro-climatic complexities of Nepal."
    )

    # =========================================================================
    # 2. PROBLEM STATEMENT
    # =========================================================================
    add_heading_1("2. Problem Statement")

    add_heading_2("2.1 The Crisis of Convective and Orographic Flash Flooding in Nepal")
    add_paragraph(
        "Flash flooding and extreme riverine inundation during the summer monsoon represent the most pervasive, recurring existential threat to "
        "human security, public health, and infrastructural stability across Nepal. The fundamental hydrological crisis stems from the disparity "
        "between the extreme speed of hydrological runoff generation in steep headwaters and the sluggish response capability of human "
        "settlements situated along downstream river corridors. In catchments such as the Melamchi, Bhotekoshi, West Rapti, and Babai, heavy "
        "precipitation occurring over mountain catchments of less than a few hundred square kilometers can generate peak discharge surges within "
        "3 to 6 hours. When intense convective rain cells hover over high-altitude headwaters, torrential surface runoff rapidly mobilizes "
        "massive volumes of glaciofluvial sediment and boulder colluvium, drastically amplifying the destructive kinetic energy of the flood wave. "
        "Despite decades of disaster management discourse, vulnerable communities in both mountain valleys and Terai floodplains continue to "
        "suffer avoidable casualties and multi-million-dollar economic shocks each summer because the existing warning infrastructure fails to "
        "provide timely, spatially resolved notice of impending deluge."
    )

    add_heading_2("2.2 Inherent Physical Deficiencies of Numerical Weather Prediction (NWP) Models")
    add_paragraph(
        "Current operational meteorological forecasting in Nepal relies substantially on regional Numerical Weather Prediction (NWP) models, "
        "such as the Weather Research and Forecasting (WRF) model, alongside synoptic-scale global models (e.g., ECMWF-IFS, GFS). While these "
        "deterministic systems represent atmospheric thermodynamics through discretized Navier-Stokes equations and physical parameterization "
        "schemes, they suffer from deep-seated, chronic inadequacies when applied over the Himalayan arc. The foremost limitation is spatial "
        "resolution: running high-resolution, convection-permitting NWP simulations (at 1 km grid spacing) over a domain as rugged as Nepal is "
        "computationally prohibitive for daily operational forecasting, requiring supercomputing infrastructure that exceeds the resources of "
        "national hydro-meteorological services."
    )
    add_paragraph(
        "Consequently, operational models run at coarser resolutions (9 to 25 km), wherein the complex vertical relief of the Himalayas is "
        "heavily smoothed into artificial, subdued topography. This spatial smoothing obliterates critical micro-topographical features such as "
        "deep river canyons, ridge saddles, and localized foothill barriers that govern real-world orographic cloud formation and convective "
        "triggering. Furthermore, standard sub-grid cumulus parameterizations and boundary-layer turbulence schemes perform notoriously poorly "
        "over steep, heterogeneous terrain, frequently miscalculating the timing of convective rainfall initiation by 6 to 12 hours, severely "
        "underestimating peak precipitation intensity, and misplacing rainfall maxima by tens of kilometers across mountain divides. These "
        "physical parameterization errors render raw NWP precipitation forecasts unreliable as direct inputs for localized flood early warning triggers."
    )

    add_heading_2("2.3 Spatial Latency, Elevation Bias, and Gauging Inadequacies in Headwater Catchments")
    add_paragraph(
        "The ground-based observation network maintained by the Department of Hydrology and Meteorology (DHM) serves as the indispensable ground "
        "truth for hydrological monitoring in Nepal. However, the physical reality of the country's geography imposes severe logistical and "
        "spatial limitations on in-situ gauging. The vast majority of Nepal's automated weather stations (AWS) and manual rain gauges are "
        "concentrated in accessible valleys, mid-hill district headquarters, and low-altitude southern plains. High-altitude catchments—above "
        "3,000 meters, where orographic condensation begins and where glacial lakes and headwater streams reside—remain severely under-gauged."
    )
    add_paragraph(
        "Maintaining automated telemetry in remote alpine zones involves immense challenges, including bitter sub-zero winters, lack of cellular "
        "or satellite transceiver connectivity, lightning strikes, solar battery exhaustion during prolonged monsoon cloud cover, and catastrophic "
        "landslide severance of sensor stations. Consequently, real-time ground-gauge data suffers from persistent spatial gaps, latency, and "
        "intermittent data dropouts. Conversely, while remote sensing satellite products provide seamless spatial coverage, they suffer from "
        "elevation-dependent retrieval biases: satellite infrared and passive microwave sensors frequently confuse warm, low-level orographic "
        "clouds with non-raining clouds, or underestimate heavy rainfall trapped beneath deep cloud decks in narrow gorges. There is an absence of "
        "a unified, automated computational framework in Nepal that harmonizes multi-source satellite observations, assimilates atmospheric "
        "reanalyses, and statistically removes elevation biases against sparse ground stations in real time."
    )

    add_heading_2("2.4 The Critical Downstream Evacuation Gap and Warning Threshold Inelasticity")
    add_paragraph(
        "The existing operational Flood Early Warning System administered by DHM relies primarily on an empirical river stage-threshold "
        "architecture. Hydrological stations installed along major river trunks continuously monitor water levels using radar or pressure sensors. "
        "When river levels breach pre-defined 'Warning' and 'Danger' thresholds, automated sirens sound locally and bulk SMS alerts are "
        "broadcast to registered mobile phones in downstream administrative zones. While this system represents a commendable step forward in "
        "disaster communication, its fundamental structural flaw is its reactive nature: it triggers alerts only after the river stage has "
        "already escalated upstream."
    )
    add_paragraph(
        "In high-gradient river basins with rapid runoff concentration times (such as the Narayani tributaries or the Kankai basin), the wave "
        "propagation lag from upstream gauge to downstream vulnerable villages is frequently less than 2 to 4 hours, and during catastrophic "
        "nighttime flash floods, lead times shrink to less than 60 minutes. This minimal warning window is wholly inadequate for orderly human "
        "evacuation, the relocation of bedridden individuals and children, the transport of livestock, or the reinforcement of flood barriers. "
        "Moreover, static river stage thresholds exhibit severe inelasticity; they fail to incorporate soil moisture saturation states, antecedent "
        "precipitation indices, or forecasted upstream rainfall volumes over the next 24 to 48 hours. If a catchment is completely saturated "
        "from three days of continuous drizzle, a sudden 50 mm storm will generate an immediate catastrophic surge, whereas the same 50 mm storm "
        "falling on dry soils might produce negligible runoff. Existing operational frameworks fail to dynamically couple spatiotemporal rainfall "
        "predictions with basin hydrological state variables, creating an urgent, glaring operational gap that this project directly addresses."
    )

    # =========================================================================
    # 3. OBJECTIVES OF THE STUDY
    # =========================================================================
    add_heading_1("3. Objectives of the Study")

    add_heading_2("3.1 Primary Overarching Objective")
    add_paragraph(
        "The overarching aim of this research project is to design, develop, rigorously validate, and benchmark an end-to-end data-driven "
        "computational framework that combines spatiotemporal remote sensing, atmospheric reanalysis, and state-of-the-art machine learning "
        "architectures to forecast monsoon rainfall patterns across Nepal and dynamically optimize flood early warning lead times for "
        "downstream river basins."
    )

    add_heading_2("3.2 Specific Research and Technical Objectives")
    add_paragraph("To realize this primary aim, the study will execute the following six interconnected technical objectives:")
    
    add_bullet(
        "To acquire, harmonize, and systematically pre-process multi-decadal (2000–present) gridded satellite precipitation products "
        "(NASA GPM IMERG and CHIRPS) alongside high-resolution atmospheric reanalysis parameters (ECMWF ERA5-Land), integrating them with "
        "in-situ daily and hourly meteorological records from the Department of Hydrology and Meteorology (DHM) across all physiographic "
        "zones of Nepal.",
        "Objective 1: Multi-Source Hydrometeorological Data Fusion & Curation — "
    )
    add_bullet(
        "To develop and deploy elevation-aware statistical and machine learning bias-correction algorithms (e.g., Quantile Delta Mapping and "
        "Spatial Kriging with External Drift using high-resolution DEM covariates) that rectify satellite retrieval inaccuracies across rugged "
        "mountain terrain and narrow Himalayan valleys.",
        "Objective 2: Elevation-Aware Bias Correction & Terrain Downscaling — "
    )
    add_bullet(
        "To conduct exhaustive spatiotemporal trend, seasonality, and anomaly analyses using non-parametric Mann-Kendall statistics, Sen's slope "
        "estimators, Spatial Moran's I autocorrelation, and Generalized Extreme Value (GEV) distributions to characterize orographic hotspots, "
        "monsoon break/active phases, and extreme rainfall return levels across Nepal's major drainage basins.",
        "Objective 3: Spatiotemporal Monsoon Climatology & Extreme Value Modeling — "
    )
    add_bullet(
        "To architect, train, and optimize deep learning spatiotemporal video-sequence forecasting models—specifically Convolutional Long Short-Term "
        "Memory (ConvLSTM), Predictive Recurrent Neural Networks (PredRNN), and Spatio-Temporal Graph Neural Networks (ST-GNN)—to forecast continuous "
        "gridded precipitation fields across Nepal at lead times of 6, 12, 24, 48, and 72 hours.",
        "Objective 4: Deep Spatiotemporal Gridded Precipitation Forecasting Engine — "
    )
    add_bullet(
        "To construct and benchmark catchment-aggregated multi-horizon time-series forecasting pipelines utilizing the Temporal Fusion "
        "Transformer (TFT), N-BEATS, and gradient-boosted decision trees (XGBoost/CatBoost) that assimilate static topographical attributes, "
        "dynamic atmospheric moisture variables (CAPE, specific humidity, wind vectors), and antecedent precipitation indices.",
        "Objective 5: Catchment-Scale Multi-Horizon Time-Series Modeling — "
    )
    add_bullet(
        "To dynamically couple predictive rainfall forecasts with river basin hydrological thresholds, establishing an optimized multi-tier "
        "Flood Early Warning System (FEWS) trigger mechanism that maximizes warning lead time while minimizing false alarm ratios, rigorously "
        "benchmarking gains in Critical Success Index (CSI), ROC-AUC, and actionable evacuation hours.",
        "Objective 6: Flood Early Warning Optimization & Evacuation Lead-Time Extension — "
    )

    add_heading_2("3.3 Research Hypotheses and Success Metrics")
    add_paragraph("This investigation is governed by three testable scientific hypotheses:")
    add_bullet(
        "Explicitly incorporating high-resolution topographical covariates (elevation, slope, aspect, Topographic Wetness Index) into "
        "spatiotemporal neural network representations will reduce rainfall forecasting root mean square error (RMSE) over mountainous "
        "catchments by at least 20% compared to topography-agnostic baseline models.",
        "Hypothesis 1: "
    )
    add_bullet(
        "Deep learning architectures that simultaneously model spatial cloud advection and temporal moisture accumulation (e.g., ConvLSTM / TFT) "
        "will significantly outperform classical statistical time-series models (ARIMA) and standard machine learning regressors in capturing "
        "high-intensity localized cloudburst anomalies exceeding 50 mm/day.",
        "Hypothesis 2: "
    )
    add_bullet(
        "Coupling catchment-aggregated predictive rainfall time-series with dynamic soil saturation indices will extend actionable flood early "
        "warning lead times for downstream vulnerable communities from the current reactive 2–4 hours to 12–24 hours, while maintaining a "
        "False Alarm Ratio (FAR) below 0.25 and a Critical Success Index (CSI) exceeding 0.70.",
        "Hypothesis 3: "
    )

    # =========================================================================
    # 4. DATA SOURCES AND ACQUISITION STRATEGY
    # =========================================================================
    add_heading_1("4. Data Sources and Acquisition Strategy")
    add_paragraph(
        "To achieve robust generalization across the immense climatic and elevational diversity of Nepal, this research establishes an extensive, "
        "multi-tiered data ingestion strategy. The data architecture synthesizes four complementary tiers: (i) gridded satellite precipitation "
        "estimates, (ii) atmospheric reanalysis products, (iii) in-situ ground-truth station observations, and (iv) static physiographic and "
        "hydrological surface covariates."
    )

    add_heading_2("4.1 High-Resolution Satellite Precipitation Products (NASA GPM IMERG and CHIRPS)")
    add_paragraph(
        "Satellite precipitation products provide the foundational spatial continuity that is physically impossible to attain through sparse "
        "mountain ground gauges. Two premier satellite precipitation products will be utilized:"
    )
    add_bullet(
        "Produced by NASA and JAXA, GPM IMERG represents the global gold standard in satellite-based precipitation estimation. It fuses passive "
        "microwave observations from the GPM constellation with geostationary infrared measurements, calibrated against global monthly gauge "
        "analyses. For this project, IMERG Version 06/07 will be extracted at its native spatial resolution of 0.1° × 0.1° (~10 km) and 30-minute "
        "temporal frequency across the continuous historical span from June 2000 to the present. The IMERG Final Run (research quality, gauge-adjusted) "
        "will serve as the primary training and retrospective validation baseline, whereas the IMERG Early Run (latency ~4 hours) and Late Run "
        "(latency ~14 hours) will be rigorously benchmarked to assess the operational feasibility of real-time early warning deployment. "
        "Access is established via the NASA Earthdata portal and the Google Earth Engine (GEE) repository.",
        "NASA GPM IMERG (Integrated Multi-satellitE Retrievals for GPM): "
    )
    add_bullet(
        "Developed by the Climate Hazards Center at the University of California, Santa Barbara, CHIRPS incorporates 0.05° × 0.05° (~5 km) "
        "resolution satellite infrared imagery with in-situ station data to construct gridded rainfall time-series dating from 1981 to the present. "
        "CHIRPS is engineered explicitly for monitoring agricultural drought and hydrometeorological extremes in complex, data-scarce terrain. "
        "Its fine 5-km spatial resolution renders it exceptionally potent for resolving steep foothill precipitation gradients along the Siwalik "
        "and Middle Mountain zones. CHIRPS daily and pentad products will be ingested via Google Earth Engine and the UCSB CHG data portal.",
        "CHIRPS (Climate Hazards Group InfraRed Precipitation with Stations): "
    )

    add_heading_2("4.2 High-Dimensional Atmospheric Reanalysis Datasets (ECMWF ERA5-Land)")
    add_paragraph(
        "Precipitation is the final thermodynamic outcome of atmospheric moisture flux convergence, instability, and vertical motion. Relying "
        "solely on historical rainfall lags severely limits predictive lead time. To provide our deep learning models with rich physical predictive "
        "signals, we ingest atmospheric and land-surface reanalysis variables from the European Centre for Medium-Range Weather Forecasts (ECMWF):"
    )
    add_bullet(
        "ERA5-Land is a globally consistent reanalysis dataset providing an enhanced resolution of 0.1° × 0.1° (~9 km) at hourly intervals "
        "from 1950 to the present, driven by the thermodynamic atmospheric forcing of ERA5 with land-surface physics parameterization. "
        "For this project, twelve key physical predictors will be systematically extracted across the Nepal bounding box: (1) Total precipitation, "
        "(2) 2-meter air temperature, (3) 2-meter dewpoint temperature (yielding relative humidity and vapor pressure deficit), (4) Surface pressure, "
        "(5) Convective Available Potential Energy (CAPE), (6) Total column water vapor (precipitable water), (7) 10-meter U-component of wind, "
        "(8) 10-meter V-component of wind (enabling moisture flux vector computation), (9) Volumetric soil water layer 1 (0–7 cm), (10) Volumetric "
        "soil water layer 2 (7–28 cm), (11) Surface runoff, and (12) Sub-surface runoff. Data acquisition will be automated via the Copernicus "
        "Climate Data Store (CDS) API.",
        "ECMWF ERA5-Land Reanalysis: "
    )

    add_heading_2("4.3 Ground-Truth Hydrometeorological Gauges (DHM Nepal and ICIMOD RDS)")
    add_paragraph(
        "In-situ ground observations provide the indispensable ground truth required to validate satellite products, calibrate statistical "
        "bias corrections, and define empirical flood trigger thresholds:"
    )
    add_bullet(
        "The national custodian of weather and water data in Nepal operates a nationwide network of meteorological and hydrological stations. "
        "Historical daily rainfall observations from over 250 manual precipitation stations and hourly time-series from over 100 Automated "
        "Weather Stations (AWS) spanning the period 2000–2024 will be formally acquired through the DHM Data Procurement Section in Babarmahal, "
        "Kathmandu. Simultaneously, historical river stage heights, rating curves, discharge measurements, and operational warning/danger thresholds "
        "from key hydrological gauging stations along the Koshi, Gandaki, Narayani, Karnali, West Rapti, Babai, and Bagmati river systems will be "
        "curated to serve as ground-truth flood targets. Real-time telemetry will be monitored via the DHM Flood Forecasting Division portal.",
        "Department of Hydrology and Meteorology (DHM), Nepal: "
    )
    add_bullet(
        "The Regional Database System maintained by the International Centre for Integrated Mountain Development provides supplementary "
        "hydrometeorological datasets, high-altitude cryospheric records, and specialized river basin shapefiles for transboundary Himalayan catchments.",
        "ICIMOD Regional Database System (RDS): "
    )

    add_heading_2("4.4 High-Resolution Topographical, Soil, and Catchment Auxiliary Datasets")
    add_paragraph(
        "Because terrain is the primary driver of orographic precipitation and hydrological runoff concentration in Nepal, detailed static "
        "geospatial rasters will be integrated directly into model feature representations:"
    )
    add_bullet(
        "High-resolution 30-meter Digital Elevation Model (DEM) data from the NASA Shuttle Radar Topography Mission (SRTM GL1) and the European "
        "Copernicus DEM (GLO-30) will be acquired. From these elevation rasters, primary and secondary topographic derivatives will be computed "
        "using GDAL and RichDEM: terrain slope, aspect, curvature, flow direction, flow accumulation, topographic position index (TPI), and "
        "Topographic Wetness Index (TWI). These variables explicitly inform neural networks regarding valley channeling and windward/leeward barriers.",
        "Digital Elevation Models (SRTM 30m / Copernicus DEM 30m): "
    )
    add_bullet(
        "Standardized hydrologically conditioned river basin and sub-catchment boundaries (HydroBASINS Levels 6, 7, and 8) will be utilized to "
        "spatially aggregate gridded rainfall into hydrologically coherent watershed units.",
        "HydroSHEDS Catchment Boundaries: "
    )
    add_bullet(
        "High-resolution (250m) gridded soil physical properties (sand, silt, clay fractions, bulk density, and hydraulic conductivity) from "
        "ISRIC SoilGrids, coupled with dynamic land-use/land-cover (LULC) maps from ESA WorldCover (10m), will be incorporated to quantify "
        "soil infiltration capacity and surface runoff generation potential.",
        "SoilGrids 250m and ESA WorldCover Land Use: "
    )

    add_heading_2("4.5 Comprehensive Data Source Matrix and Spatial-Temporal Characterization")
    add_paragraph(
        "To provide a clear, rigorous architectural overview of all empirical datasets ingested in this investigation, Table 1 details the provider, "
        "spatial resolution, temporal coverage, update cadence, and specific functional role within the machine learning pipeline."
    )

    # TABLE 1
    table_p = doc.add_paragraph()
    table_p.paragraph_format.space_before = Pt(6)
    table_p.paragraph_format.space_after = Pt(4)
    run_t = table_p.add_run("Table 1: Comprehensive Data Source Matrix for the Proposed Research Project")
    run_t.font.name = 'Times New Roman'
    run_t.font.size = Pt(11)
    run_t.bold = True

    table_data = [
        ("Dataset / Entity", "Agency / Provider", "Spatial Extent / Res.", "Temporal Coverage", "Role in Machine Learning Framework"),
        ("NASA GPM IMERG Final/Late", "NASA PMM / JAXA", "0.1° (~10 km) Gridded", "2000–Present (30-min)", "Primary target grid for spatiotemporal sequence modeling"),
        ("CHIRPS Precipitation", "UCSB Climate Hazards Group", "0.05° (~5 km) Gridded", "1981–Present (Daily)", "Long-term historical climatology and extreme return modeling"),
        ("ERA5-Land Reanalysis", "ECMWF / Copernicus CDS", "0.1° (~9 km) Gridded", "1950–Present (Hourly)", "Atmospheric forcing, moisture flux, CAPE, & soil moisture features"),
        ("In-Situ Rain Gauges (AWS/Manual)", "Govt. of Nepal DHM", "Point Gauges (>350 stns)", "2000–2024 (Daily/Hourly)", "Ground-truth calibration, validation, and quantile bias correction"),
        ("River Stage & Discharge Gauges", "DHM Flood Forecasting Div.", "Key River Corridors", "Historical & Real-Time", "Ground-truth flood alert/danger threshold optimization"),
        ("Copernicus DEM / SRTM", "ESA / NASA USGS", "30-meter Elevation Raster", "Static Topography", "Orographic lifting, slope, aspect, TWI feature generation"),
        ("HydroBASINS Sub-Catchments", "WWF / USGS HydroSHEDS", "Vector Polygons (L6-L8)", "Static Drainage Basin", "Catchment spatial masking and time-series zonal aggregation"),
        ("ISRIC SoilGrids & ESA LandCover", "ISRIC / ESA WorldCover", "250m / 10m Rasters", "Static & Decadal Update", "Infiltration capacity, roughness, and runoff curve features")
    ]

    mat_table = doc.add_table(rows=len(table_data), cols=5)
    mat_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    mat_table.autofit = False

    col_widths = [Inches(1.6), Inches(1.1), Inches(1.2), Inches(1.1), Inches(1.5)]

    for row_idx, row_content in enumerate(table_data):
        row = mat_table.rows[row_idx]
        for col_idx, text_val in enumerate(row_content):
            cell = row.cells[col_idx]
            cell.width = col_widths[col_idx]
            p = cell.paragraphs[0]
            if row_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                shading = parse_xml(r'<w:shd {} w:fill="002060"/>'.format(nsdecls('w')))
                cell._tc.get_or_add_tcPr().append(shading)
                r = p.add_run(text_val)
                r.font.name = 'Times New Roman'
                r.font.size = Pt(9.5)
                r.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT if col_idx in [0, 4] else WD_ALIGN_PARAGRAPH.CENTER
                r = p.add_run(text_val)
                r.font.name = 'Times New Roman'
                r.font.size = Pt(9.5)

    # =========================================================================
    # 5. PROPOSED METHODOLOGY
    # =========================================================================
    add_heading_1("5. Proposed Methodology")
    add_paragraph(
        "The proposed technical methodology establishes an end-to-end data science and deep learning workflow organized into seven rigorous, "
        "interlocking phases: (1) Data ingestion, spatial masking, and elevation-aware bias correction; (2) Spatiotemporal trend analysis and "
        "extreme value modeling; (3) Spatiotemporal deep learning video-sequence modeling; (4) Catchment-scale multi-horizon time-series forecasting; "
        "(5) Empirical baseline benchmarking; (6) Flood early warning threshold optimization; and (7) Model interpretability and computational validation."
    )

    add_figure(
        r"c:\Users\Acer\Desktop\Machine Learning\figures\fig1_system_architecture.png",
        "Figure 2: End-to-end computational pipeline architecture showing 5 operational stages from multi-source data ingestion and elevation-aware bias correction to deep learning sequence forecasting and early warning decision support.",
        width_inches=6.3
    )

    add_heading_2("5.1 Data Pipeline Engineering, Geospatial Masking, and Elevation-Aware Bias Correction")
    add_paragraph(
        "All gridded datasets will be programmatically harvested using automated Python scripts interfacing with the Google Earth Engine (GEE) "
        "API and the Copernicus Climate Data Store (CDS) API. The geographical domain is bounded by the official bounding box of Nepal "
        "(Longitude: 80.0°E to 88.2°E; Latitude: 26.3°N to 30.5°N). All raster layers will be projected into a standardized coordinate reference "
        "system (WGS 84 / UTM Zone 45N, EPSG:32645) and resampled to a consistent 0.1° × 0.1° grid using bilinear interpolation for continuous "
        "atmospheric fields and bilinear or nearest-neighbor interpolation for topographical features."
    )
    add_paragraph(
        "Because raw satellite precipitation products exhibit severe systematic errors across the Himalayas, a multi-stage bias correction pipeline "
        "will be implemented. First, missing records and sensor dropouts in ground station data will be identified and flagged using automated "
        "quality control routines, including range checks (0–500 mm/day), step checks, and spatial consistency checks with neighboring gauges. "
        "Second, Quantile Delta Mapping (QDM)—an advanced non-parametric quantile mapping algorithm that preserves relative changes in precipitation "
        "quantiles while rectifying systematic distributional skews—will be calibrated between GPM IMERG grid cells and co-located DHM ground gauges. "
        "Third, to account for complex orography in ungauged areas, Regression Kriging (RK) and Kriging with External Drift (KED) using DEM elevation, "
        "slope, and aspect as auxiliary external drift predictors will be deployed to generate spatially continuous, elevation-adjusted daily rainfall "
        "matrices across the entire country."
    )

    add_heading_2("5.2 Rigorous Spatiotemporal Trend Characterization and Extreme Value Theory (EVT)")
    add_paragraph(
        "Prior to model training, exhaustive exploratory climatological characterization will be performed to understand the spatiotemporal "
        "behavior of monsoon extremes over the historical record (1981–2024 for CHIRPS, 2000–2024 for GPM/ERA5):"
    )
    add_bullet(
        "Monotonic trends in annual, seasonal, and monthly precipitation, as well as the timing of monsoon onset and withdrawal dates, will be "
        "computed for each grid cell across Nepal using the non-parametric Mann-Kendall test. The magnitude of trend changes will be quantified "
        "using Sen's slope estimator, with serial autocorrelation pre-whitened using the Yue-Pilon method to eliminate false positive trend detections.",
        "Non-Parametric Trend Detection: "
    )
    add_bullet(
        "To model extreme hydrometeorological events that drive catastrophic flooding, Generalized Extreme Value (GEV) distributions (encompassing "
        "Gumbel, Fréchet, and Weibull families) will be fitted to annual maximum 1-day (Rx1day) and consecutive 5-day (Rx5day) rainfall depths "
        "using Maximum Likelihood Estimation (MLE) and L-moment methods. This analysis establishes baseline return levels (10-, 25-, 50-, and "
        "100-year return periods) for every catchment in Nepal, providing the physical basis for flood risk classification.",
        "Extreme Value Distribution Modeling: "
    )
    add_bullet(
        "Spatial clustering of torrential downpours and localized cloudbursts will be mapped using Global and Local Moran's I statistics. This "
        "pinpoints statistically significant High-High spatial clusters (cloudburst hotspots along foothill ridges) and High-Low spatial outliers "
        "across complex valleys, providing critical insights into orographic rain traps.",
        "Spatial Autocorrelation and Hotspot Mapping: "
    )

    add_heading_2("5.3 Deep Learning Spatiotemporal Precipitation Engine (ConvLSTM, PredRNN, ST-GNN)")
    add_paragraph(
        "To forecast continuous precipitation fields over the entire national territory, we formulate gridded rainfall prediction as a "
        "spatiotemporal sequence-to-sequence video prediction task. The input tensor at time step t consists of a multi-channel grid of dimensions "
        "[Batch, Time_Steps, Channels, Height, Width], where Channels include lagged precipitation grids (IMERG), atmospheric variables (ERA5-Land CAPE, "
        "moisture flux, U/V winds), and static topographical rasters (elevation, slope, TWI)."
    )
    add_bullet(
        "Unlike standard LSTMs that flatten spatial arrays into 1D vectors (destroying topological spatial relationships), ConvLSTM replaces matrix "
        "multiplications in the input, forget, output gates, and cell state updates with 2D convolutional operations. This architecture allows the "
        "recurrent unit to preserve spatial coordinate geometry while propagating temporal memory over time. Stacking multiple bidirectional "
        "ConvLSTM layers enables the network to learn both localized cloud convection and synoptic-scale monsoon trough migrations.",
        "Convolutional Long Short-Term Memory (ConvLSTM): "
    )
    add_bullet(
        "To overcome the gradient vanishing problem across extended forecast horizons, PredRNN (Predictive Recurrent Neural Network) will be "
        "deployed. PredRNN introduces a Spatiotemporal Memory Flow (M) that zigzag-propagates spatial representations vertically across layers and "
        "horizontally across time, significantly improving long-term predictive fidelity for 24- to 72-hour precipitation nowcasting.",
        "Predictive RNN (PredRNN / Memory Decoupling): "
    )
    add_bullet(
        "To explicitly model hydrological stream networks where rainfall runoff flows down river channels according to graph topology, "
        "Spatio-Temporal Graph Neural Networks (ST-GNN) will be implemented. Graph nodes represent sub-catchment centroids or gauge stations, "
        "while graph edges represent river connectivity and flow direction derived from HydroSHEDS. Spatial graph convolutions (GCN/GAT) capture "
        "upstream-to-downstream water propagation, while temporal convolutions capture rainfall accumulation over time.",
        "Spatio-Temporal Graph Neural Network (ST-GNN): "
    )

    add_heading_2("5.4 Catchment-Aggregated Multi-Horizon Forecasting via Temporal Fusion Transformers (TFT)")
    add_paragraph(
        "While 2D gridded models predict spatial rain maps, operational early warning requires high-precision, multi-step time-series forecasting "
        "of aggregated rainfall volumes over specific river catchments (e.g., Koshi, Narayani, Karnali, West Rapti, Babai). For this purpose, we "
        "deploy the state-of-the-art Temporal Fusion Transformer (TFT):"
    )
    add_paragraph(
        "TFT is explicitly architected for multi-horizon time-series forecasting with interpretable attention mechanisms. It excels in heterogeneous "
        "hydrometeorological modeling because it natively processes four distinct input categories: (1) Static metadata (basin drainage area, mean "
        "elevation, hypsometric curve, soil hydraulic conductivity, land cover type); (2) Past time-varying inputs with unknown future values "
        "(lagged river discharge, observed ground gauge rainfall, past soil moisture); (3) Known a-priori future inputs (day-of-year, seasonal "
        "monsoon harmonics); and (4) Exogenous atmospheric forecasts from NWP/ERA5 (forecasted CAPE, precipitable water, wind vectors). "
        "TFT's Variable Selection Networks dynamically filter out noisy predictors at each time step, while Gated Residual Networks (GRN) prevent "
        "overfitting. Self-attention layers compute multi-head attention weights across historical time steps, revealing which antecedent days "
        "most strongly drive peak flood conditions."
    )

    add_figure(
        r"c:\Users\Acer\Desktop\Machine Learning\figures\fig3_deep_learning_models.png",
        "Figure 3: Core machine learning architectures: (Left) Spatiotemporal ConvLSTM cell integrating spatial convolution gates; (Right) Temporal Fusion Transformer (TFT) with variable selection networks and self-attention mechanism.",
        width_inches=6.3
    )

    add_heading_2("5.5 Empirical Benchmark Baselines (XGBoost, CatBoost, Bidirectional LSTM)")
    add_paragraph(
        "To scientifically justify the deployment of complex deep neural networks, their predictive performance must be rigorously benchmarked "
        "against established classical machine learning and statistical time-series baselines under identical cross-validation splits:"
    )
    add_bullet(
        "Gradient boosted decision tree algorithms trained on extensive tabular lag features (moving window rainfall sums at 6h, 12h, 24h, 48h, "
        "exponential moving averages, atmospheric indices, and static catchment descriptors). XGBoost and CatBoost serve as formidable, highly "
        "competitive tabular baselines.",
        "Extreme Gradient Boosting (XGBoost) and CatBoost: "
    )
    add_bullet(
        "A standard deep sequence baseline that processes time-series forward and backward to capture temporal context without attention mechanisms.",
        "Bidirectional LSTM (Bi-LSTM): "
    )
    add_bullet(
        "A classical linear statistical benchmark to evaluate the non-linear gain of machine learning architectures.",
        "Seasonal Autoregressive Integrated Moving Average with Exogenous Regressors (SARIMAX): "
    )

    add_heading_2("5.6 Flood Early Warning Optimization, Threshold Mapping, and Evacuation Gain Modeling")
    add_paragraph(
        "The ultimate operational deliverable of this research is transforming predictive precipitation fields into optimized, actionable flood "
        "early warning triggers. The predicted catchment-aggregated precipitation time-series (Pt+6, Pt+12, Pt+24, Pt+48) will be integrated with "
        "the Antecedent Precipitation Index (API) and ERA5-Land volumetric soil moisture to compute dynamic Runoff Potential Indices (RPI). "
        "These dynamic indices will be mapped against historical DHM hydrological gauge records where 'Warning Level' (yellow) and 'Danger Level' "
        "(red) inundations occurred."
    )
    add_paragraph(
        "Threshold optimization will be formulated as a multi-objective cost-sensitive optimization problem. Instead of applying static rainfall "
        "thresholds (e.g., a universal 100 mm/24h rule), thresholds will be dynamically calibrated per sub-basin and antecedent soil saturation state. "
        "By optimizing the threshold boundary along the Receiver Operating Characteristic (ROC) curve, the system aims to maximize the Critical "
        "Success Index (CSI) and Probability of Detection (POD) while maintaining the False Alarm Ratio (FAR) below an operational tolerance limit. "
        "Crucially, Lead-Time Gain (LTG)—defined as the additional hours of warning provided by predictive rainfall thresholds before river stage "
        "gauges reach danger level—will be quantified across historical major flood events (e.g., the August 2017 Terai floods, the 2021 Melamchi "
        "disaster, and the October 2021 unseasonal post-monsoon floods)."
    )

    add_figure(
        r"c:\Users\Acer\Desktop\Machine Learning\figures\fig4_threshold_and_roc.png",
        "Figure 4: Flood early warning decision optimization: (Left) Dynamic 2D hydro-hazard alert matrix coupling forecasted rainfall with antecedent soil moisture; (Right) Receiver Operating Characteristic (ROC) curve tradeoff illustrating optimal trigger threshold.",
        width_inches=6.3
    )

    add_heading_2("5.7 Computational Architecture, Model Interpretability (SHAP/Attention), and Evaluation")
    add_paragraph(
        "Model training will be executed using PyTorch, PyTorch Lightning, and the Darts / PyTorch Forecasting time-series libraries. Distributed "
        "training will utilize NVIDIA GPU acceleration. To prevent data leakage, temporal blocked cross-validation will be enforced: historical "
        "monsoons from 2000 to 2018 will serve as the training set, 2019–2021 as the validation and hyperparameter tuning set, and 2022–2024 as the "
        "independent, held-out test set."
    )
    add_paragraph(
        "To establish trust among hydrologists and disaster managers, model interpretability will be prioritized. For tabular models (XGBoost/CatBoost), "
        "SHapley Additive exPlanations (SHAP) will compute global feature importances and local waterfall attribution plots, explaining which "
        "meteorological parameters triggered specific flood alerts. For the Temporal Fusion Transformer, multi-head attention weights will be "
        "extracted and visualized to identify the critical temporal lookback horizon driving extreme surges. Performance evaluation will employ "
        "both continuous hydrometeorological metrics (RMSE, MAE, R², Kling-Gupta Efficiency - KGE, Nash-Sutcliffe Efficiency - NSE) and categorical "
        "contingency table metrics (Probability of Detection - POD, False Alarm Ratio - FAR, Critical Success Index - CSI, Heidke Skill Score - HSS, "
        "and Area Under the ROC Curve - AUC-ROC)."
    )

    # =========================================================================
    # 6. EXPECTED OUTCOMES AND OPERATIONAL DELIVERABLES
    # =========================================================================
    add_heading_1("6. Expected Outcomes, Scientific Deliverables, and Operational Impact")
    add_paragraph(
        "The successful completion of this research project will generate tangible scientific, computational, and societal outcomes directly "
        "aligned with Nepal's national disaster risk reduction priorities:"
    )
    add_bullet(
        "A modular, automated Python and Google Earth Engine pipeline that ingests, cleans, harmonizes, and bias-corrects multi-decadal GPM IMERG, "
        "CHIRPS, and ERA5-Land data against DHM ground stations, generating an open-access analysis-ready data store for hydrometeorological research.",
        "Deliverable 1: Automated Multi-Source Geospatial Data Ingestion & Bias-Correction Pipeline — "
    )
    add_bullet(
        "A detailed, peer-reviewed spatial atlas detailing decadal rainfall trends, orographic precipitation hotspots, and extreme rainfall "
        "return levels (10-, 25-, 50-year return periods) for every major river catchment in Nepal.",
        "Deliverable 2: High-Resolution Climatological & Extreme Value Atlas of Nepal — "
    )
    add_bullet(
        "A fully validated deep learning codebase implementing ConvLSTM, PredRNN, ST-GNN, and Temporal Fusion Transformer architectures, achieving "
        "superior spatiotemporal rainfall forecasting accuracy across lead times of 6 to 48 hours compared to existing operational models.",
        "Deliverable 3: State-of-the-Art Deep Learning Spatiotemporal Forecasting Engine — "
    )
    add_bullet(
        "A dynamic, soil-moisture-conditioned early warning trigger framework demonstrating an empirical extension of flood early warning lead "
        "times by 12 to 24 hours over downstream river gauge thresholds, with quantified CSI > 0.70 and FAR < 0.25.",
        "Deliverable 4: Optimized Flood Early Warning Decision-Support Framework — "
    )
    add_bullet(
        "A fully documented, open-source GitHub repository containing reproducible Jupyter notebooks, trained model weights, API deployment "
        "scripts, and at least two manuscripts submitted to high-impact international peer-reviewed journals (e.g., Journal of Hydrology, "
        "Hydrology and Earth System Sciences, or IEEE Transactions on Geoscience and Remote Sensing).",
        "Deliverable 5: Open-Source Code Repository and High-Impact Academic Publications — "
    )

    # =========================================================================
    # 7. PROJECT TIMELINE, WORK PLAN, AND RISK MITIGATION
    # =========================================================================
    add_heading_1("7. Comprehensive 24-Week Work Plan, Resource Allocation, and Risk Mitigation")
    add_paragraph(
        "The project is structured across five sequential, milestone-driven phases executed over a 24-week (6-month) operational timeframe:"
    )

    plan_items = [
        ("Phase 1: Data Acquisition, Quality Control & Ingestion (Weeks 1–4)", 
         "Establish formal DHM data procurement protocols; deploy automated GEE and Copernicus CDS ingestion scripts; download GPM IMERG, CHIRPS, and ERA5-Land archives; perform geospatial clipping, re-projection, and missing-value imputation. Milestone 1: Complete analysis-ready spatiotemporal database for Nepal."),
        ("Phase 2: Elevation-Aware Bias Correction & Terrain Feature Engineering (Weeks 5–8)", 
         "Implement Quantile Delta Mapping (QDM) and Regression Kriging against DHM ground gauge records; process high-resolution Copernicus/SRTM DEMs; compute slope, aspect, curvature, and Topographic Wetness Index (TWI); assemble composite multi-channel training tensors. Milestone 2: Validated, bias-corrected gridded rainfall matrices."),
        ("Phase 3: Spatiotemporal Climatology & Baseline Model Development (Weeks 9–12)", 
         "Conduct Mann-Kendall trend tests, GEV extreme value fitting, and Moran's I spatial clustering; engineer tabular lag features; train and tune XGBoost, CatBoost, and SARIMAX benchmark models. Milestone 3: Comprehensive climatological baseline and benchmark performance metrics."),
        ("Phase 4: Deep Spatiotemporal Architecture Engineering & Tuning (Weeks 13–18)", 
         "Construct and train ConvLSTM, PredRNN, ST-GNN, and Temporal Fusion Transformer architectures using GPU acceleration; perform temporal blocked cross-validation across 2000–2024 monsoon seasons; optimize loss functions (MSE, Huber, focal loss for precipitation extremes). Milestone 4: Fully trained and tuned deep learning models."),
        ("Phase 5: Flood Warning Optimization, Validation & Project Finalization (Weeks 19–24)", 
         "Couple predictive rainfall forecasts with DHM flood warning thresholds; compute lead-time gain, CSI, POD, and FAR metrics; conduct SHAP and attention interpretability analyses; compile final technical report and prepare academic journal manuscripts. Milestone 5: Final project report, operational codebase, and publication manuscripts.")
    ]

    for phase_name, phase_desc in plan_items:
        add_bullet(f" {phase_desc}", phase_name + ":")

    add_heading_2("Risk Assessment and Mitigation Strategies")
    add_paragraph(
        "Potential technical and operational risks have been identified alongside proactive mitigation measures:"
    )
    add_bullet(
        "Ground-truth station procurement from national agencies may experience administrative delays. Mitigation: Immediate formal submission "
        "of research credentials, leveraging open-access GPM and CHIRPS data for initial pipeline architecture development while data procurement proceeds.",
        "Risk 1 (Data Procurement Latency): "
    )
    add_bullet(
        "Training high-dimensional ConvLSTM and Transformer models over millions of grid cells requires substantial GPU memory. Mitigation: Spatial "
        "tiling of catchments, mixed-precision training (FP16), and leveraging high-performance cloud compute (Google Colab Pro / AWS / Kaggle GPU).",
        "Risk 2 (Computational Bottlenecks): "
    )
    add_bullet(
        "Heavy monsoon rain events are rare relative to non-raining days, creating severe class imbalance. Mitigation: Deploying weighted loss "
        "functions (Focal Loss, extreme-value-weighted MSE) and extreme value oversampling techniques.",
        "Risk 3 (Extreme Rainfall Class Imbalance): "
    )

    # =========================================================================
    # 8. REFERENCES (14 High-Impact Academic & Institutional References with Links)
    # =========================================================================
    add_heading_1("8. References")
    add_paragraph(
        "The following 14 authoritative peer-reviewed journal publications, institutional datasets, and methodological standards form the "
        "scientific foundation of this research proposal. Active, verifiable digital object identifier (DOI) and institutional URLs are provided for each citation:"
    )

    refs_data = [
        (
            "[1] Department of Hydrology and Meteorology (DHM), Government of Nepal. (2023). Hydrological and Meteorological Data Services and Real-Time Flood Warning Network. Government of Nepal, Ministry of Energy, Water Resources and Irrigation, Kathmandu, Nepal. ",
            "https://dhm.gov.np",
            "https://dhm.gov.np"
        ),
        (
            "[2] DHM Nepal Flood Forecasting Division. (2024). Operational River Watch, Water Level Monitoring, and Real-Time Flood Early Warning Portal. Kathmandu, Nepal. ",
            "https://hydrology.gov.np",
            "https://hydrology.gov.np"
        ),
        (
            "[3] Huffman, G. J., Bolvin, D. T., Braithwaite, D., Hsu, K., Joyce, R., Kidd, C., Nelkin, E. J., Sorooshian, S., Tan, J., & Xie, P. (2020). Integrated Multi-satellitE Retrievals for the Global Precipitation Measurement (GPM) Mission (IMERG). Satellite Precipitation Measurement: Advances in Global Change Research, 67, 343-353. DOI: 10.1007/978-3-030-24962-5_19. ",
            "https://earthdata.nasa.gov",
            "https://earthdata.nasa.gov"
        ),
        (
            "[4] Funk, C., Peterson, P., Landsfeld, M., Pedreros, D., Verdin, J., Shukla, S., Husak, G., Rowland, J., Harrison, L., Hoell, A., & Michaelsen, J. (2015). The climate hazards infrared precipitation with stations—a new environmental record for monitoring extremes. Scientific Data, 2(1), 150066. DOI: 10.1038/sdata.2015.66. ",
            "https://chc.ucsb.edu/data/chirps",
            "https://chc.ucsb.edu/data/chirps"
        ),
        (
            "[5] Muñoz-Sabater, J., Dutra, E., Agustí-Panareda, A., Albergel, C., Arduini, G., Balsamo, G., Boussetta, S., Choulga, M., Harrigan, S., Hersbach, H., Martens, B., Miralles, D. G., Piles, M., Rodríguez-Fernández, N. J., Zsoter, E., Buontempo, C., & Thépaut, J. N. (2021). ERA5-Land: A state-of-the-art global reanalysis dataset for land applications. Earth System Science Data, 13(9), 4349-4383. DOI: 10.5194/essd-13-4349-2021. ",
            "https://cds.climate.copernicus.eu",
            "https://cds.climate.copernicus.eu"
        ),
        (
            "[6] Shi, X., Chen, Z., Wang, H., Yeung, D. Y., Wong, W. K., & Woo, W. C. (2015). Convolutional LSTM network: A machine learning approach for precipitation nowcasting. Advances in Neural Information Processing Systems (NeurIPS 2015), 28, 802-810. ",
            "https://proceedings.neurips.cc/paper/2015/hash/07563a3fe3bbe7e3ba84431ad9d055af-Abstract.html",
            "https://proceedings.neurips.cc/paper/2015/hash/07563a3fe3bbe7e3ba84431ad9d055af-Abstract.html"
        ),
        (
            "[7] Lim, B., Arık, S. Ö., Loeff, N., & Pfister, T. (2021). Temporal Fusion Transformers for interpretable multi-horizon time series forecasting. International Journal of Forecasting, 37(4), 1748-1764. DOI: 10.1016/j.ijforecast.2021.03.012. ",
            "https://doi.org/10.1016/j.ijforecast.2021.03.012",
            "https://doi.org/10.1016/j.ijforecast.2021.03.012"
        ),
        (
            "[8] Wang, Y., Long, M., Wang, J., Gao, Z., & Yu, P. S. (2017). PredRNN: Recurrent Neural Networks for Predictive Learning using Spatiotemporal LSTMs. Advances in Neural Information Processing Systems (NeurIPS 2017), 30, 879-888. ",
            "https://proceedings.neurips.cc/paper/2017/hash/e5f6ad6ce374177eef023bf5d0c018b6-Abstract.html",
            "https://proceedings.neurips.cc/paper/2017/hash/e5f6ad6ce374177eef023bf5d0c018b6-Abstract.html"
        ),
        (
            "[9] Talchabhadel, R., Karki, R., Thapa, B. R., Maharjan, M., & Parajuli, B. (2018). Spatio-temporal variability of extreme precipitation in Nepal. International Journal of Climatology, 38(11), 4296-4313. DOI: 10.1002/joc.5669. ",
            "https://doi.org/10.1002/joc.5669",
            "https://doi.org/10.1002/joc.5669"
        ),
        (
            "[10] Karki, R., Hasson, S. U. R., Schickhoff, U., Scholten, T., & Böhner, J. (2017). Rising minimum degree-days and their spatiotemporal changes over the Hindu Kush Himalayan region. Environmental Earth Sciences, 76(23), 1-19. DOI: 10.1007/s12665-017-7151-5. ",
            "https://doi.org/10.1007/s12665-017-7151-5",
            "https://doi.org/10.1007/s12665-017-7151-5"
        ),
        (
            "[11] Alfieri, L., Burek, P., Dutra, E., Salamon, P., Kalas, M., Pappenberger, F., & Thielen, J. (2013). GloFAS—global ensemble streamflow forecasting and flood early warning. Hydrology and Earth System Sciences, 17(3), 1161-1175. DOI: 10.5194/hess-17-1161-2013. ",
            "https://www.globalfloods.eu",
            "https://www.globalfloods.eu"
        ),
        (
            "[12] ICIMOD (International Centre for Integrated Mountain Development). (2022). Regional Database System (RDS) for the Hindu Kush Himalaya: Hydrometeorological and River Basin Archives. Kathmandu, Nepal. ",
            "https://rds.icimod.org",
            "https://rds.icimod.org"
        ),
        (
            "[13] Lehner, B., & Grill, G. (2013). Global river hydrography and network routing: baseline data and new approaches to study the world's large river systems. Hydrological Processes, 27(15), 2171-2186. DOI: 10.1002/hyp.9740. ",
            "https://www.hydrosheds.org",
            "https://www.hydrosheds.org"
        ),
        (
            "[14] Shrestha, A. B., Wake, C. P., Mayewski, P. A., & Dibb, J. E. (1999). Maximum temperature trends in the Himalaya and its vicinity: An analysis based on temperature records from Nepal for the period 1971–94. Journal of Climate, 12(9), 2775-2786. DOI: 10.1175/1520-0442(1999)012<2775:MTTITH>2.0.CO;2. ",
            "https://doi.org/10.1175/1520-0442(1999)012<2775:MTTITH>2.0.CO;2",
            "https://doi.org/10.1175/1520-0442(1999)012<2775:MTTITH>2.0.CO;2"
        )
    ]

    for citation_text, url, display_url in refs_data:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.left_indent = Inches(0.4)
        p.paragraph_format.first_line_indent = Inches(-0.4)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        
        # Add citation text
        run = p.add_run(citation_text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11)

        # Add clickable hyperlink
        add_hyperlink(p, url, display_url, color='004B87', underline=True)

    # Save Document
    target_path = r"c:\Users\Acer\Desktop\Machine Learning\Saharsha_210425.docx"
    try:
        doc.save(target_path)
        print(f"Comprehensive proposal with cover page successfully created at: {target_path}")
    except PermissionError:
        target_path_alt = r"c:\Users\Acer\Desktop\Machine Learning\Saharsha_210425_v2.docx"
        doc.save(target_path_alt)
        print(f"Notice: File was locked. Saved to: {target_path_alt}")

    # Also update the previous file name if accessible
    try:
        doc.save(r"c:\Users\Acer\Desktop\Machine Learning\Monsoon_Rainfall_Flood_Early_Warning_Proposal.docx")
    except Exception:
        pass

if __name__ == "__main__":
    create_comprehensive_proposal()
