# Research Blueprint & Literature Tracking Log

**Project:** Spatiotemporal Machine Learning & Multi-Horizon Deep Learning for Monsoon Precipitation Forecasting and Proactive Flood Early Warning in Nepal  
**Document Generated:** [`Experimental_Paper_Blueprint_Nepal_Monsoon.docx`](file:///c:/Users/Acer/Desktop/Machine%20Learning/Experimental_Paper_Blueprint_Nepal_Monsoon.docx)  
**Script Generator:** [`create_blueprint_docx.py`](file:///c:/Users/Acer/Desktop/Machine%20Learning/create_blueprint_docx.py)  
**Last Updated:** October 8, 2026

---

## 1. Selected Benchmark Papers (3 High-Impact & Nepal Focus)

The research blueprint has been calibrated using **3 recent (2023–2024)** papers from leading peer-reviewed venues, specifically incorporating an empirical study based directly in Nepal:

| # | Paper & Citation | Venue & Year | Focus & Role in Blueprint | Length (Excl. Refs) | Links / DOIs |
|---|---|---|---|---|---|
| **1** | **Bhattarai, Y., Duwal, S., Sharma, S., & Talchabhadel, R.**<br>*Leveraging machine learning and open-source spatial datasets to enhance flood susceptibility mapping in transboundary river basin* | *International Journal of Digital Earth*, 17(1) (**2024**) | **Nepal & Transboundary Baseline:** Assesses flood susceptibility across the Gandak River basin (Nepal/China/India) with LSTM, RF, ANN, and SVM over complex Himalayan-to-plains terrain. Serves as our regional data and topographical benchmark. | ~7,400 words | • [Taylor & Francis Journal Page](https://www.tandfonline.com/doi/full/10.1080/17538947.2024.2313857)<br>• [DOI: 10.1080/17538947.2024.2313857](https://doi.org/10.1080/17538947.2024.2313857)<br>• [ResearchGate Full Text / PDF](https://www.researchgate.net/publication/378125586_Leveraging_machine_learning_and_open-source_spatial_datasets_to_enhance_flood_susceptibility_mapping_in_transboundary_river_basin) |
| **2** | **Nearing, G., Cohen, D., Dakhari, V., et al.**<br>*Global prediction of extreme floods in ungauged watersheds using machine learning* | *Nature*, 627, 559–563 (**2024**) | **Global Operational AI Flood Prediction:** Proves that deep learning (LSTM-based hydrologic models) delivers superior 0–5 day streamflow warnings in ungauged basins worldwide compared to physics-based systems like GloFAS. Serves as our operational AI early warning benchmark. | ~6,800 words | • [Nature Article](https://www.nature.com/articles/s41586-024-07145-1)<br>• [DOI: 10.1038/s41586-024-07145-1](https://doi.org/10.1038/s41586-024-07145-1)<br>• [Google Research Blog Summary](https://research.google/blog/ai-for-global-flood-forecasting/) |
| **3** | **Zhang, Y., Long, M., Chen, K., Xing, L., Rong, R., et al.**<br>*Skilful nowcasting of extreme precipitation with NowcastNet* | *Nature*, 619, 526–532 (**2023**) | **Physics-Informed Deep Generative Nowcasting:** Introduces *NowcastNet*, blending physical advection equations with generative neural networks for convective extreme precipitation. Serves as our rainfall nowcasting methodology blueprint. | ~6,500 words | • [Nature Article](https://www.nature.com/articles/s41586-023-06184-4)<br>• [DOI: 10.1038/s41586-023-06184-4](https://doi.org/10.1038/s41586-023-06184-4)<br>• [GitHub Code Repository](https://github.com/thuml/NowcastNet) |

---

## 2. Structural & Word Budget Calibration

Based on the 3 benchmark papers, the calculated target profile is:
* **Benchmark Target Average:** **6,900 words** (without references & appendices)
* **Recommended Length Range:** **6,000 – 8,000 words**

### Section-by-Section Budget Breakdown

| Section | Recommended Word Count | Core Focus & Contents |
|---|---|---|
| **1. Introduction** | `500 – 1,000 words` | Monsoon economic impact in Nepal (75–85% annual rain), elevation-dependent warming, limitations of existing 2–4 hr downstream gauge warnings, and introduction of the multi-horizon AI approach. |
| **2. Literature Review** | `1,000 – 1,500 words` | Himalayan extreme weather climatology, physical model limitations (WRF/GloFAS), transboundary flood susceptibility (*Bhattarai et al., 2024*), global ungauged AI routing (*Nearing et al., 2024*), and convective physics-ML (*Zhang et al., 2023*). |
| **3. Theoretical Framework** | `200 – 500 words` | Orographic lifting dynamics, Clausius-Clapeyron moisture scaling (7%/°C), and hydrological time of concentration. |
| **4. Methodology** | `1,000 – 1,500 words` | Multi-source data pipeline (2001–2023 DHM stations, NASA GPM IMERG 0.1°, CHIRPS 0.05°, ERA5-Land 0.1°), quantile mapping station bias correction, spatiotemporal deep learning nowcaster + catchment multi-horizon TFT. |
| **5. Experimental Results** | `1,500 – 3,000 words` | Performance evaluation across Koshi, Gandaki, Karnali, West Rapti; RMSE/KGE comparisons against XGBoost, Bi-LSTM, SARIMAX; lead times (6h, 12h, 24h, 48h); dynamic Runoff Potential Index (RPI) alert matrices. |
| **6. Discussion** | `500 – 1,000 words` | Physical consistency vs deep learning pitfalls, attention mechanism interpretation of 3–5 day antecedent soil moisture, comparison against findings in *Nearing et al.* and *Bhattarai et al.*, and operational viability for DHM/NDRRMA. |
| **7. Conclusion & Outlook** | `500 – 1,000 words` | Practical early warning improvements (12–24 hr lead times, CSI > 0.75, FAR < 0.20), limitations regarding radar coverage and satellite latency, and next steps for PINN and edge deployments. |

---

## 3. Prior Literature & Benchmark Datasets (Direct Links & Access)

Earlier literature and benchmark datasets reviewed during initial scoping and preserved for citations:

### Primary Baseline Papers
* **Shi et al. (NeurIPS 2015):** *Convolutional LSTM Network: A Machine Learning Approach for Precipitation Nowcasting*
  - 🔗 [NeurIPS Proceedings & Open PDF](https://proceedings.neurips.cc/paper/2015/hash/07563a3fe3bbe7e3ba84431ad9d055af-Abstract.html)
  - 🔗 [arXiv:1506.04214 [cs.CV]](https://arxiv.org/abs/1506.04214)

* **Lim et al. (International Journal of Forecasting 2021):** *Temporal Fusion Transformers for Interpretable Multi-horizon Time Series Forecasting*
  - 🔗 [ScienceDirect / DOI: 10.1016/j.ijforecast.2021.03.012](https://doi.org/10.1016/j.ijforecast.2021.03.012)
  - 🔗 [arXiv:1912.09363 [stat.ML]](https://arxiv.org/abs/1912.09363)

* **Talchabhadel et al. (International Journal of Climatology 2018):** *Spatio-temporal variability of extreme precipitation in Nepal*
  - 🔗 [Wiley Online Library / DOI: 10.1002/joc.5669](https://doi.org/10.1002/joc.5669)

* **Alfieri et al. (Hydrology and Earth System Sciences 2013):** *GloFAS: Global ensemble streamflow forecasting and flood early warning*
  - 🔗 [Copernicus HESS Open Access](https://hess.copernicus.org/articles/17/1161/2013/)
  - 🔗 [DOI: 10.5194/hess-17-1161-2013](https://doi.org/10.5194/hess-17-1161-2013)

* **Funk et al. (Scientific Data - Nature 2015):** *The Climate Hazards Group InfraRed Precipitation with Stations (CHIRPS): A new environmental record for monitoring extremes*
  - 🔗 [Nature Scientific Data Open Access](https://www.nature.com/articles/sdata201566)
  - 🔗 [UCSB CHIRPS Data Download Portal](https://www.chc.ucsb.edu/data/chirps)

* **Wang et al. (NeurIPS 2017):** *PredRNN: Recurrent Neural Networks for Predictive Learning using Spatiotemporal LSTMs*
  - 🔗 [NeurIPS Proceedings](https://proceedings.neurips.cc/paper/2017/hash/e5f6ad6ce374177eef023bf5d0c018b6-Abstract.html)
  - 🔗 [arXiv:1703.08247 [cs.CV]](https://arxiv.org/abs/1703.08247)

### Hydrometeorological & Remote Sensing Portals
* **NASA Global Precipitation Measurement (GPM IMERG):**
  - 🔗 [NASA Earthdata IMERG Product](https://earthdata.nasa.gov) | [DOI: 10.1007/978-3-030-24568-9_19](https://doi.org/10.1007/978-3-030-24568-9_19)
* **ECMWF ERA5-Land Reanalysis (Soil Moisture & CAPE):**
  - 🔗 [Copernicus ESSD Paper (Muñoz-Sabater et al., 2021)](https://essd.copernicus.org/articles/13/4349/2021/)
  - 🔗 [Copernicus Climate Data Store (CDS)](https://cds.climate.copernicus.eu/)
* **Nepal Department of Hydrology and Meteorology (DHM):**
  - 🔗 [DHM Main Portal](https://dhm.gov.np)
  - 🔗 [Nepal Real-time Flood Forecasting / River Watch](https://hydrology.gov.np)

---

## 4. Current File Inventory

1. [**`Experimental_Paper_Blueprint_Nepal_Monsoon.docx`**](file:///c:/Users/Acer/Desktop/Machine%20Learning/Experimental_Paper_Blueprint_Nepal_Monsoon.docx) — Formal Word document worksheet formatted with styled navy headers, border styling, alternating rows, and pre-filled sections.
2. [**`create_blueprint_docx.py`**](file:///c:/Users/Acer/Desktop/Machine%20Learning/create_blueprint_docx.py) — Python script automating the generation of the blueprint `.docx` file.
3. [**`BLUEPRINT_PROGRESS.md`**](file:///c:/Users/Acer/Desktop/Machine%20Learning/BLUEPRINT_PROGRESS.md) — This progress tracking log.
