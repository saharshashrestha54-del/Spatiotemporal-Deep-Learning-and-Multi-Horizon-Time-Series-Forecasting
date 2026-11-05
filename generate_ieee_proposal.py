import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def create_ieee_style_document():
    doc = docx.Document()

    # SECTION 1: HEADER & TITLE (Single-column layout)
    sec_title = doc.sections[0]
    sec_title.top_margin = Inches(0.75)
    sec_title.bottom_margin = Inches(0.75)
    sec_title.left_margin = Inches(0.75)
    sec_title.right_margin = Inches(0.75)

    # Base Normal Style (Times New Roman 10pt for IEEE standard body)
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(10)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing = 1.05
    normal_style.paragraph_format.space_after = Pt(4)

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

    # IEEE Header Elements
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(12)
    r_title = p_title.add_run("Data-Driven Spatiotemporal Analysis and Machine Learning Time-Series Forecasting of Monsoon Rainfall Patterns in Nepal for Flood Early Warning Optimization")
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(18)
    r_title.bold = True

    # Author & Supervisor Affiliations (2-Column Table side-by-side like IEEE paper)
    affil_table = doc.add_table(rows=1, cols=2)
    affil_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    affil_table.autofit = False

    # Remove borders
    tblPr = affil_table._tbl.tblPr
    borders = parse_xml(r'''
        <w:tblBorders %s >
            <w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/>
            <w:right w:val="none"/><w:insideH w:val="none"/><w:insideV w:val="none"/>
        </w:tblBorders>
    ''' % nsdecls('w'))
    tblPr.append(borders)

    c_left, c_right = affil_table.rows[0].cells[0], affil_table.rows[0].cells[1]
    c_left.width = Inches(3.4)
    c_right.width = Inches(3.4)

    # Student on Left
    p_auth = c_left.paragraphs[0]
    p_auth.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_auth.paragraph_format.space_after = Pt(2)
    p_auth.paragraph_format.line_spacing = 1.05
    r_a1 = p_auth.add_run("Saharsha\n")
    r_a1.bold = True
    r_a1.font.size = Pt(11)
    r_a2 = p_auth.add_run("MSc Data Science and Artificial Intelligence\nSoftwarica College of IT & E-Commerce\nKathmandu, Nepal\nStudent ID: 210425\n210425@softwarica.edu.np")
    r_a2.font.size = Pt(9.5)

    # Module Leader on Right
    p_sup = c_right.paragraphs[0]
    p_sup.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sup.paragraph_format.space_after = Pt(2)
    p_sup.paragraph_format.line_spacing = 1.05
    r_s1 = p_sup.add_run("[Module Leader Name]\n")
    r_s1.bold = True
    r_s1.font.size = Pt(11)
    r_s2 = p_sup.add_run("Module Leader / Research Supervisor\nDepartment of Computing and Information Systems\nSoftwarica College of IT & E-Commerce\nKathmandu, Nepal\nsupervisor@softwarica.edu.np")
    r_s2.font.size = Pt(9.5)

    # Abstract & Index Terms in Header Section (Italic & Bold Lead-in)
    p_abs = doc.add_paragraph()
    p_abs.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs.paragraph_format.space_before = Pt(12)
    p_abs.paragraph_format.space_after = Pt(6)
    p_abs.paragraph_format.line_spacing = 1.05
    r_ab_lead = p_abs.add_run("Abstract—")
    r_ab_lead.bold = True
    r_ab_lead.font.size = Pt(9.5)
    r_ab_text = p_abs.add_run(
        "Monsoon precipitation supplies over 80% of Nepal's annual water budget but triggers catastrophic riverine inundations "
        "and localized flash floods across the Himalayan foothills and downstream Terai floodplains. Existing early warning mechanisms "
        "in Nepal rely predominantly on reactive river gauge threshold monitoring, delivering critically short evacuation lead times of "
        "less than 2 to 4 hours. Numerical Weather Prediction (NWP) models suffer from severe boundary-layer parameterization deficiencies "
        "and spatial smoothing across Nepal's extreme 60 m to 8,848 m elevational relief. This research project presents a rigorous, "
        "data-driven spatiotemporal forecasting and early warning optimization framework. We systematically synthesize multi-decadal gridded "
        "satellite precipitation products (NASA GPM IMERG at 0.1° and CHIRPS at 0.05°) with high-resolution atmospheric reanalysis parameters "
        "(ECMWF ERA5-Land at ~9 km), in-situ ground gauge observations from the Department of Hydrology and Meteorology (DHM), and 30 m Digital "
        "Elevation Model (DEM) terrain derivatives. Elevation-dependent retrieval biases are rectified via Quantile Delta Mapping (QDM) and "
        "Regression Kriging with External Drift. Dual deep learning engines—Convolutional Long Short-Term Memory (ConvLSTM) / PredRNN for 2D "
        "spatial rainfall field propagation and Temporal Fusion Transformers (TFT) with self-attention for catchment-aggregated multi-horizon "
        "accumulation—are engineered to deliver 6- to 48-hour forecasts. The predictive precipitation fields are dynamically coupled with "
        "antecedent soil moisture to optimize multi-tier flood alert triggers along the ROC curve. The expected outcome is an operational "
        "early warning framework extending actionable community evacuation lead times to 12–24 hours while maintaining a Critical Success "
        "Index (CSI) > 0.75 and False Alarm Ratio (FAR) < 0.20."
    )
    r_ab_text.font.size = Pt(9.5)
    r_ab_text.italic = True

    # Index Terms
    p_terms = doc.add_paragraph()
    p_terms.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_terms.paragraph_format.space_after = Pt(14)
    r_t_lead = p_terms.add_run("Index Terms—")
    r_t_lead.bold = True
    r_t_lead.font.size = Pt(9.5)
    r_t_text = p_terms.add_run("Monsoon precipitation forecasting, Spatiotemporal modeling, ConvLSTM, Temporal Fusion Transformer, Flood early warning, Quantile Delta Mapping, Orographic rainfall, Nepal Himalayas.")
    r_t_text.font.size = Pt(9.5)
    r_t_text.bold = True

    # =========================================================================
    # SECTION 2: TWO-COLUMN BODY LAYOUT (Continuous Break into 2 Columns)
    # =========================================================================
    sec_body = doc.add_section(docx.enum.section.WD_SECTION.CONTINUOUS)
    sec_body.top_margin = Inches(0.75)
    sec_body.bottom_margin = Inches(0.75)
    sec_body.left_margin = Inches(0.75)
    sec_body.right_margin = Inches(0.75)

    # Enable 2 columns with 0.25 inch (360 dxa) spacing
    sectPr_body = sec_body._sectPr
    for existing_col in sectPr_body.findall(r'{http://schemas.openxmlformats.org/wordprocessingml/2006/main}cols'):
        sectPr_body.remove(existing_col)
    cols_elem = parse_xml(r'<w:cols %s w:num="2" w:space="360"/>' % nsdecls("w"))
    sectPr_body.append(cols_elem)

    # Formatting helpers for 2-column body
    def add_sec_heading(roman_num, title):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(f"{roman_num}.  {title.upper()}")
        run.font.name = 'Times New Roman'
        run.font.size = Pt(10)
        run.bold = True
        return p

    def add_subsec_heading(letter, title):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(f"{letter}.  {title}")
        run.font.name = 'Times New Roman'
        run.font.size = Pt(9.5)
        run.italic = True
        run.bold = True
        return p

    def add_body_p(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.05
        p.paragraph_format.first_line_indent = Inches(0.18)
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(9.5)
        return p

    def add_bullet_item(num_str, text, bold_title=None):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.left_indent = Inches(0.2)
        p.paragraph_format.first_line_indent = Inches(-0.2)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.05
        r_num = p.add_run(num_str + " ")
        r_num.font.name = 'Times New Roman'
        r_num.font.size = Pt(9.5)
        r_num.bold = True
        if bold_title:
            r_bt = p.add_run(bold_title + " ")
            r_bt.font.name = 'Times New Roman'
            r_bt.font.size = Pt(9.5)
            r_bt.bold = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(9.5)
        return p

    def add_fig_2col(img_path, caption):
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(6)
            p_img.paragraph_format.space_after = Pt(2)
            p_img.add_run().add_picture(img_path, width=Inches(3.35))

            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p_cap.paragraph_format.space_after = Pt(8)
            p_cap.paragraph_format.keep_with_next = True
            r_cap = p_cap.add_run(caption)
            r_cap.font.name = 'Times New Roman'
            r_cap.font.size = Pt(8.5)
            r_cap.italic = True

    # --- I. INTRODUCTION ---
    add_sec_heading("I", "Introduction")
    add_body_p(
        "The South Asian summer monsoon constitutes one of the most thermodynamically energetic and socially critical circulation "
        "phenomena on Earth. For Nepal, it delivers 75% to 85% of total annual precipitation across a narrow window between June and September. "
        "Driven by differential thermal heating between the Tibetan Plateau and the warm Indian Ocean / Bay of Bengal, maritime moisture "
        "fluxes are funneled across the Indo-Gangetic Plains. Upon encountering the steep geological ramparts of the Himalayas, these air masses "
        "undergo rapid orographic lifting, triggering severe convective updrafts, cloudbursts, and extreme riverine inundations."
    )
    add_body_p(
        "In a country where agrarian cultivation employs over 65% of the rural populace and run-of-the-river hydroelectric plants produce "
        "over 90% of electricity, monsoon rainfall is vital for economic sustenance. However, extreme precipitation frequently exceeds the "
        "infiltration capacity of mountain soils, creating debris flows, destructive flash floods, and widespread inundation across the southern "
        "Terai plains (such as the Koshi, Gandaki, Narayani, Karnali, and West Rapti basins)."
    )
    add_body_p(
        "Nepal's physiography ascends from less than 60 m above sea level in the Terai to over 8,848 m at Mount Everest within a lateral distance "
        "of merely 150 to 200 km. This extreme vertical relief creates distinct dual orographic rainfall peaks: the first along the southern "
        "Siwalik foothills (~2,200 mm/yr) and the second along the windward slopes of the Middle Mountains (such as Pokhara, receiving >4,500 mm/yr), "
        "followed by severe rain-shadow aridity in the trans-Himalayan valleys of Mustang and Manang (<300 mm/yr)."
    )
    add_body_p(
        "Under Elevation-Dependent Warming (EDW), the Clausius-Clapeyron thermodynamic relationship dictates that atmospheric water-holding capacity "
        "rises by ~7% per degree Celsius. Over the Himalayas, this fuels deeper convective instability, producing localized, short-duration extreme "
        "deluges. The National Disaster Risk Reduction and Management Authority (NDRRMA) reports that water-induced disasters cause over 60% of all "
        "annual disaster-related fatalities and economic losses in Nepal."
    )
    add_body_p(
        "To break this recurring cycle of destruction, flood disaster management must transition from reactive post-event relief to predictive "
        "anticipation. Traditional early warning systems rely either on slow deterministic physical models or on downstream river gauges. In steep "
        "mountain catchments with rapid concentration times, downstream gauges provide an evacuation window of mere minutes to 2–4 hours. Extending "
        "actionable lead times to 12–24 hours requires coupling upstream spatiotemporal rainfall forecasting directly with basin soil saturation states. "
        "Recent advances in gridded remote sensing (NASA GPM IMERG, CHIRPS), open atmospheric reanalyses (ERA5-Land), and deep learning (ConvLSTM, TFT) "
        "offer the exact data-driven capabilities required to overcome this barrier."
    )

    add_fig_2col(
        r"c:\Users\Acer\Desktop\Machine Learning\figures\fig2_orographic_and_leadtime.png",
        "Fig. 1. (Top) Himalayan physiographic cross-section showing dual orographic precipitation peaks; (Bottom) Evacuation lead-time timeline: reactive point gauges vs. predictive ML forecasting."
    )

    # --- II. PROBLEM STATEMENT ---
    add_sec_heading("II", "Problem Statement")
    add_body_p(
        "Flash floods and extreme riverine inundations in Nepal stem from the disparity between the extreme velocity of hydrological runoff "
        "generation in steep headwaters and the sluggish response capability of human settlements along downstream river corridors. In steep basins "
        "such as Melamchi, Bhotekoshi, and West Rapti, heavy rain over small catchments generates peak discharge surges within 3 to 6 hours, mobilizing "
        "immense sediment and boulder colluvium."
    )
    add_body_p(
        "Current operational meteorological forecasting in Nepal relies substantially on regional Numerical Weather Prediction (NWP) models (such as "
        "WRF) and global synoptic systems (ECMWF-IFS, GFS). However, running high-resolution, convection-permitting NWP simulations over rugged terrain "
        "is computationally prohibitive for daily operational forecasting. Coarser models (9 to 25 km) heavily smooth the topography, obliterating "
        "critical canyons and foothill ridges that trigger real-world convective clouds. Sub-grid cumulus parameterizations routinely miscalculate "
        "cloudburst initiation times by 6 to 12 hours and misplace rainfall maxima across mountain divides."
    )
    add_body_p(
        "Furthermore, ground-based rain gauge networks maintained by the Department of Hydrology and Meteorology (DHM) are heavily concentrated in "
        "accessible valleys and southern plains. High-altitude headwaters above 3,000 m—where runoff originates—remain severely under-gauged due to "
        "harsh alpine conditions, lack of telemetry connectivity, and lightning hazards. Conversely, satellite precipitation estimates exhibit severe "
        "elevation-dependent retrieval biases in high-relief mountain valleys, underestimating warm orographic cloud downpours."
    )
    add_body_p(
        "Finally, the operational Flood Early Warning System administered by DHM relies primarily on an empirical river stage-threshold architecture. "
        "Because sirens and SMS alerts trigger only after an upstream gauge breaches warning height, the evacuation window for vulnerable floodplains "
        "shrinks to 2–4 hours. Moreover, static stage thresholds ignore antecedent soil moisture saturation states: a 50 mm storm on saturated soil causes "
        "instant catastrophic flooding, whereas on dry soil it causes negligible runoff. A unified data-driven framework linking predictive rainfall "
        "with dynamic soil saturation is critically needed."
    )

    # --- III. OBJECTIVES ---
    add_sec_heading("III", "Objectives of the Study")
    add_body_p(
        "The overarching aim of this research project is to formulate, implement, and benchmark an operational machine learning-driven "
        "spatiotemporal forecasting framework capable of predicting monsoon rainfall patterns across Nepal and dynamically optimizing flood "
        "early warning lead times for downstream vulnerable catchments."
    )
    add_body_p("The specific research objectives are:")
    add_bullet_item("1)", "To acquire, harmonize, and systematically pre-process multi-decadal (2000–present) gridded satellite precipitation products (NASA GPM IMERG at 0.1° and CHIRPS at 0.05°) alongside atmospheric reanalysis parameters (ECMWF ERA5-Land at 9 km) and in-situ ground gauge records from DHM Nepal.")
    add_bullet_item("2)", "To develop and deploy elevation-aware statistical and machine learning bias-correction algorithms (Quantile Delta Mapping and Regression Kriging with External Drift using 30 m DEM covariates) that rectify satellite retrieval inaccuracies across rugged mountain terrain.")
    add_bullet_item("3)", "To conduct exhaustive spatiotemporal trend and extreme value analyses using Mann-Kendall statistics, Sen's slope, Spatial Moran's I autocorrelation, and Generalized Extreme Value (GEV) distributions to characterize orographic hotspots and extreme rainfall return levels.")
    add_bullet_item("4)", "To engineer and train deep learning spatiotemporal sequence models—specifically Convolutional LSTM (ConvLSTM), PredRNN, and Spatio-Temporal Graph Neural Networks (ST-GNN)—to forecast continuous gridded precipitation fields across Nepal at 6, 12, 24, 48, and 72-hour lead times.")
    add_bullet_item("5)", "To construct and benchmark catchment-aggregated multi-horizon time-series forecasting pipelines utilizing the Temporal Fusion Transformer (TFT) with dynamic variable selection and interpretable multi-head attention.")
    add_bullet_item("6)", "To dynamically couple predictive rainfall outputs with empirical river basin hydrological thresholds and antecedent soil moisture, establishing an optimized multi-tier Flood Early Warning System (FEWS) trigger that extends actionable warning lead time by 12–24 hours while maintaining CSI > 0.75 and FAR < 0.20.")

    # --- IV. DATA SOURCES ---
    add_sec_heading("IV", "Data Source and Acquisition Strategy")
    add_body_p(
        "To achieve robust generalization across the immense climatic and elevational diversity of Nepal, this study synthesizes four complementary data tiers:"
    )
    add_subsec_heading("A", "Gridded Satellite Precipitation")
    add_body_p(
        "NASA GPM IMERG (V06/V07) provides multi-satellite precipitation estimates at 0.1° (~10 km) spatial resolution and 30-minute to daily frequency "
        "from June 2000 to the present. The IMERG Final Run serves as benchmark training data, while the IMERG Early and Late runs are tested for "
        "near-real-time operational early warning feasibility. CHIRPS (0.05° / ~5 km) blends satellite infrared imagery with station records (1981–present) "
        "and is used for long-term historical trend and extreme return period modeling."
    )
    add_subsec_heading("B", "Atmospheric and Land-Surface Reanalysis")
    add_body_p(
        "ECMWF ERA5-Land reanalysis provides 12 key physical thermodynamic predictors at 0.1° (~9 km) hourly resolution: total precipitation, 2m temperature, "
        "dewpoint temperature, surface pressure, Convective Available Potential Energy (CAPE), total column water vapor, 10m U/V wind vectors (enabling moisture "
        "flux convergence calculation), volumetric soil water layers (0–7 cm and 7–28 cm), and surface/subsurface runoff. Ingested via Copernicus CDS API."
    )
    add_subsec_heading("C", "Ground-Truth Hydrometeorological Records")
    add_body_p(
        "Historical daily rainfall records from over 250 manual stations and hourly records from over 100 Automated Weather Stations (AWS) are obtained from "
        "the Department of Hydrology and Meteorology (DHM), Nepal. River stage heights, discharge ratings, and operational warning/danger thresholds along the "
        "Koshi, Narayani, Karnali, West Rapti, and Bagmati corridors are curated from the DHM Flood Forecasting Division and ICIMOD RDS."
    )
    add_subsec_heading("D", "Topographical and Catchment Auxiliary Data")
    add_body_p(
        "Copernicus and SRTM 30 m Digital Elevation Models (DEM) are processed to calculate terrain slope, aspect, curvature, and Topographic Wetness Index (TWI). "
        "HydroBASINS (Levels 6–8) vector polygons delineate upstream drainage boundaries, while ISRIC SoilGrids (250 m) and ESA WorldCover (10 m) quantify soil "
        "hydraulic conductivity and surface roughness."
    )

    # --- V. PROPOSED METHODOLOGY ---
    add_sec_heading("V", "Proposed Methodology")
    add_body_p(
        "The proposed methodology follows a structured, multi-phase machine learning and hydrological engineering lifecycle organized into seven interlocking phases:"
    )

    add_fig_2col(
        r"c:\Users\Acer\Desktop\Machine Learning\figures\fig1_system_architecture.png",
        "Fig. 2. End-to-end computational pipeline architecture showing 5 operational stages from raw multi-sensor ingestion to early warning decision support."
    )

    add_subsec_heading("A", "Data Ingestion & Elevation-Aware Bias Correction")
    add_body_p(
        "All raster grids are clipped to the Nepal bounding box (80.0°E–88.2°E, 26.3°N–30.5°N), re-projected to UTM Zone 45N (EPSG:32645), and resampled "
        "to a standardized 0.1° grid. Missing readings in ground gauge data undergo automated range and spatial consistency checks. Systematic satellite "
        "retrieval biases are corrected using Quantile Delta Mapping (QDM) calibrated against co-located DHM stations. In ungauged mountain terrain, Regression "
        "Kriging with External Drift (KED) using DEM elevation and slope as external drift predictors produces seamless, elevation-adjusted rainfall matrices."
    )
    add_subsec_heading("B", "Spatiotemporal Climatology & Extreme Value Modeling")
    add_body_p(
        "Monotonic trends in monsoon onset, duration, and volume are evaluated using the non-parametric Mann-Kendall test with Yue-Pilon pre-whitening and "
        "Sen's slope estimator. Generalized Extreme Value (GEV) distributions are fitted to annual maximum 1-day (Rx1day) and 5-day (Rx5day) precipitation depths "
        "via L-moments to compute 10-, 25-, and 50-year return levels per catchment. Spatial clustering of localized cloudbursts is mapped using Global and Local "
        "Moran's I statistics."
    )

    add_fig_2col(
        r"c:\Users\Acer\Desktop\Machine Learning\figures\fig3_deep_learning_models.png",
        "Fig. 3. (Left) ConvLSTM cell incorporating spatial convolution gates; (Right) Temporal Fusion Transformer (TFT) with variable selection and multi-head attention."
    )

    add_subsec_heading("C", "Deep Spatiotemporal Gridded Modeling")
    add_body_p(
        "Gridded precipitation forecasting is framed as a spatiotemporal video sequence prediction task over multi-channel tensors [Batch, Time, Channels, Height, Width]. "
        "We implement Convolutional LSTM (ConvLSTM), which replaces standard matrix multiplications with 2D convolutional operations, preserving spatial coordinate "
        "topology while propagating temporal memory. PredRNN is stacked with a Spatiotemporal Memory Flow (M) that zigzag-propagates spatial representations across "
        "extended lead times (6 to 72 hours). ST-GNN models stream network topology using HydroSHEDS graph connectivity."
    )
    add_subsec_heading("D", "Catchment-Scale Multi-Horizon Forecasting via TFT")
    add_body_p(
        "For individual river basins, the Temporal Fusion Transformer (TFT) models multi-horizon accumulated precipitation. TFT natively combines static basin metadata "
        "(area, mean elevation, soil conductivity), past time-varying inputs (river discharge, observed rainfall), and exogenous atmospheric forecasts (CAPE, moisture "
        "flux, wind vectors). Variable Selection Networks filter out noisy predictors, while self-attention layers identify critical antecedent rainfall lag days."
    )
    add_subsec_heading("E", "Empirical Baseline Benchmarks")
    add_body_p(
        "To scientifically validate deep learning gains, models are benchmarked under identical cross-validation splits against Extreme Gradient Boosting (XGBoost), "
        "CatBoost, Bidirectional LSTM (Bi-LSTM), and classical SARIMAX models using extensive moving-window tabular lag features."
    )

    add_fig_2col(
        r"c:\Users\Acer\Desktop\Machine Learning\figures\fig4_threshold_and_roc.png",
        "Fig. 4. (Left) Dynamic 2D hydro-hazard alert matrix coupling predicted rainfall with soil moisture; (Right) ROC curve showing optimal operating point (AUC=0.93)."
    )

    add_subsec_heading("F", "Early Warning Optimization & Lead-Time Gain")
    add_body_p(
        "Predicted precipitation accumulations (Pt+6, Pt+12, Pt+24, Pt+48) are combined with antecedent precipitation indices and ERA5-Land soil moisture to compute "
        "dynamic Runoff Potential Indices (RPI). Threshold optimization along the ROC curve determines dynamic multi-tier alert triggers (Advisory, Warning, Evacuation) "
        "tailored per sub-basin. Lead-Time Gain (LTG) is quantified across historical flood events (e.g., August 2017 Terai floods, July 2021 Melamchi disaster), "
        "measuring the extra hours of proactive notice generated before downstream river gauges reach danger level."
    )
    add_subsec_heading("G", "Model Evaluation & Interpretability")
    add_body_p(
        "Models are evaluated using continuous metrics (RMSE, MAE, Kling-Gupta Efficiency - KGE) and categorical early warning metrics (Probability of Detection - POD, "
        "False Alarm Ratio - FAR, Critical Success Index - CSI, and AUC-ROC). SHAP waterfall plots and TFT attention weights provide transparent physical interpretability."
    )

    # --- VI. EXPECTED OUTCOMES ---
    add_sec_heading("VI", "Expected Outcomes and Deliverables")
    add_body_p("The project is expected to deliver the following tangible scientific and operational outputs:")
    add_bullet_item("1)", "An automated Python/GEE preprocessing and bias-correction pipeline producing continuous analysis-ready rainfall grids for Nepal.")
    add_bullet_item("2)", "A high-resolution spatiotemporal atlas of monsoon precipitation trends, cloudburst hotspots, and extreme return levels across all river basins.")
    add_bullet_item("3)", "A validated, benchmarked deep learning forecasting suite (ConvLSTM and TFT) providing reliable 6- to 48-hour precipitation forecasts.")
    add_bullet_item("4)", "A dynamic flood early warning optimization algorithm empirically extending evacuation lead times by 12 to 24 hours over reactive river gauges, with CSI > 0.75 and FAR < 0.20.")
    add_bullet_item("5)", "A fully reproducible open-source GitHub repository and at least two research manuscripts submitted to high-impact peer-reviewed journals.")

    # --- VII. REFERENCES (14 References with Active Links) ---
    add_sec_heading("VII", "References")
    
    refs_data = [
        ("[1]", "Department of Hydrology and Meteorology (DHM), Government of Nepal, “Hydrological and meteorological data portal and real-time flood warning network,” Kathmandu, Nepal, 2023. [Online]. Available: ", "https://dhm.gov.np"),
        ("[2]", "DHM Nepal Flood Forecasting Division, “Operational river watch and real-time flood early warning portal,” Kathmandu, Nepal, 2024. [Online]. Available: ", "https://hydrology.gov.np"),
        ("[3]", "G. J. Huffman et al., “Integrated Multi-satellitE Retrievals for the Global Precipitation Measurement (GPM) Mission (IMERG),” Satellite Precipitation Measurement, pp. 343–353, 2020. [Online]. Available: ", "https://earthdata.nasa.gov"),
        ("[4]", "C. Funk et al., “The climate hazards infrared precipitation with stations—a new environmental record for monitoring extremes,” Scientific Data, vol. 2, p. 150066, 2015. [Online]. Available: ", "https://chc.ucsb.edu/data/chirps"),
        ("[5]", "J. Muñoz-Sabater et al., “ERA5-Land: A state-of-the-art global reanalysis dataset for land applications,” Earth System Science Data, vol. 13, no. 9, pp. 4349–4383, 2021. [Online]. Available: ", "https://cds.climate.copernicus.eu"),
        ("[6]", "X. Shi et al., “Convolutional LSTM network: A machine learning approach for precipitation nowcasting,” in Proc. NeurIPS, vol. 28, pp. 802–810, 2015. [Online]. Available: ", "https://proceedings.neurips.cc/paper/2015/hash/07563a3fe3bbe7e3ba84431ad9d055af-Abstract.html"),
        ("[7]", "B. Lim, S. Ö. Arık, N. Loeff, and T. Pfister, “Temporal Fusion Transformers for interpretable multi-horizon time series forecasting,” Int. J. Forecast., vol. 37, no. 4, pp. 1748–1764, 2021. [Online]. Available: ", "https://doi.org/10.1016/j.ijforecast.2021.03.012"),
        ("[8]", "Y. Wang, M. Long, J. Wang, Z. Gao, and P. S. Yu, “PredRNN: Recurrent neural networks for predictive learning using spatiotemporal LSTMs,” in Proc. NeurIPS, vol. 30, pp. 879–888, 2017. [Online]. Available: ", "https://proceedings.neurips.cc/paper/2017/hash/e5f6ad6ce374177eef023bf5d0c018b6-Abstract.html"),
        ("[9]", "R. Talchabhadel, R. Karki, B. R. Thapa, M. Maharjan, and B. Parajuli, “Spatio-temporal variability of extreme precipitation in Nepal,” Int. J. Climatol., vol. 38, no. 11, pp. 4296–4313, 2018. [Online]. Available: ", "https://doi.org/10.1002/joc.5669"),
        ("[10]", "R. Karki, S. U. R. Hasson, U. Schickhoff, T. Scholten, and J. Böhner, “Rising minimum degree-days and their spatiotemporal changes over the Hindu Kush Himalayan region,” Environ. Earth Sci., vol. 76, no. 23, p. 1-19, 2017. [Online]. Available: ", "https://doi.org/10.1007/s12665-017-7151-5"),
        ("[11]", "L. Alfieri et al., “GloFAS—global ensemble streamflow forecasting and flood early warning,” Hydrol. Earth Syst. Sci., vol. 17, no. 3, pp. 1161–1175, 2013. [Online]. Available: ", "https://www.globalfloods.eu"),
        ("[12]", "ICIMOD, “Regional Database System (RDS) for the Hindu Kush Himalaya: Hydrometeorological and River Basin Archives,” Kathmandu, Nepal, 2022. [Online]. Available: ", "https://rds.icimod.org"),
        ("[13]", "B. Lehner and G. Grill, “Global river hydrography and network routing: baseline data and new approaches to study the world's large river systems,” Hydrol. Process., vol. 27, no. 15, pp. 2171–2186, 2013. [Online]. Available: ", "https://www.hydrosheds.org"),
        ("[14]", "A. B. Shrestha, C. P. Wake, P. A. Mayewski, and J. E. Dibb, “Maximum temperature trends in the Himalaya and its vicinity: An analysis based on temperature records from Nepal for the period 1971–94,” J. Clim., vol. 12, no. 9, pp. 2775–2786, 1999. [Online]. Available: ", "https://doi.org/10.1175/1520-0442(1999)012<2775:MTTITH>2.0.CO;2")
    ]

    for num_tag, cite_str, url_link in refs_data:
        p_ref = doc.add_paragraph()
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_ref.paragraph_format.left_indent = Inches(0.25)
        p_ref.paragraph_format.first_line_indent = Inches(-0.25)
        p_ref.paragraph_format.space_after = Pt(4)
        p_ref.paragraph_format.line_spacing = 1.05
        
        r_nt = p_ref.add_run(num_tag + " ")
        r_nt.font.name = 'Times New Roman'
        r_nt.font.size = Pt(8.5)
        r_nt.bold = True

        r_cs = p_ref.add_run(cite_str)
        r_cs.font.name = 'Times New Roman'
        r_cs.font.size = Pt(8.5)

        add_hyperlink(p_ref, url_link, url_link, color='004B87', underline=True)

    # Save to Saharsha_210425.docx
    target_path = r"c:\Users\Acer\Desktop\Machine Learning\Saharsha_210425.docx"
    try:
        doc.save(target_path)
        print(f"Successfully generated IEEE-style two-column document at: {target_path}")
    except PermissionError:
        alt_path = r"c:\Users\Acer\Desktop\Machine Learning\Saharsha_210425_ieee.docx"
        doc.save(alt_path)
        print(f"File was locked. Generated at: {alt_path}")

if __name__ == "__main__":
    create_ieee_style_document()
