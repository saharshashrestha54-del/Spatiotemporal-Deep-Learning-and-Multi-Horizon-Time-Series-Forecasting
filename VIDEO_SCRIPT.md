# Nepal Monsoon FEWS: Live Video Walkthrough Script
**Project:** Spatiotemporal Machine Learning & Multi-Horizon Deep Learning for Monsoon Precipitation Forecasting and Proactive Flood Early Warning in Nepal  
**Presenter:** Saharsha | MSc Data Science & AI, Softwarica College  
**Estimated Time:** ~3:30 to 4:00 minutes  

---

## [0:00 – 0:40] Scene 1: Introduction & The Core Problem
*(Stay on dashboard home view. Move cursor over title and sidebar).*

> **Say:**  
> "Hello everyone. Today I'm demonstrating my MSc project: **The Nepal Monsoon Flood Early Warning System (FEWS)**.  
>  
> Every year between June and September, the summer monsoon brings over 80% of Nepal's annual rainfall. Because our steep Himalayan river systems drop thousands of meters into the flat southern Terai plains in under 150 kilometers, heavy cloudbursts quickly cause catastrophic flash floods.  
>  
> Traditional river stage gauges only warn downstream communities **2 to 4 hours** before a river overflows—which is barely enough time to evacuate safely. This web dashboard demonstrates an operational, data-driven early warning system that combines satellite precipitation, soil hydrology physics, and deep learning to extend proactive flood lead times to **12 to 24 hours**.  
>  
> Let’s walk through the four core modules of the system."

---

## [0:40 – 1:35] Scene 2: Tab 1 — Live Early Warning Monitor
*(Click **🚨 Live Early Warning Monitor** in sidebar. Move the date slider).*

> **Say:**  
> "We start with the **Live Early Warning Monitor**.  
>  
> In steep mountainous basins, rain alone doesn't trigger a flood—what matters is how wet the ground already is. Here, we track daily satellite precipitation from CHIRPS alongside top-layer volumetric soil moisture from ECMWF ERA5-Land reanalysis.  
>  
> Using the date slider at the top, disaster managers can navigate any day during the active monsoon season. For each day, the dashboard computes our custom **Runoff Potential Index (RPI)**.  
>  
> Notice what happens when I select an early season date in June:  
> *(Drag slider to mid-June)*  
> Even when moderate rain falls, the antecedent soil moisture is low, meaning the ground absorbs water easily. The RPI remains below 0.50, and the status shows a safe **GREEN: NORMAL STATUS**, preventing false alarms.  
>  
> Now watch as we advance into peak monsoon season in late August:  
> *(Drag slider to mid/late August, e.g., 2022-08-22 or 2022-09-14)*  
> Now the soil moisture has reached high saturation around 0.40 cubic meters per cubic meter. With the soil saturated, even moderate rain causes the RPI to spike, automatically escalating the badge to a **YELLOW WATCH**, **ORANGE WARNING**, or **RED EVACUATION LEVEL**.  
>  
> Scrolling down to the **Monsoon Timeline**, the dynamic hydrograph visually confirms this non-linear coupling: when rainfall spikes coincide with peak soil saturation, runoff potential escalates dramatically."

---

## [1:35 – 2:25] Scene 3: Tab 2 — Multi-Horizon Forecast Explorer
*(Click **📈 Multi-Horizon Forecast Explorer**. Hover cursor over Plotly chart).*

> **Say:**  
> "Next, let's switch to the **Multi-Horizon Forecast Explorer**.  
>  
> Here we evaluate predictive forecasting over a **24-hour forward lead-time horizon**. This gives disaster response teams and local municipalities a full day of advance notice before extreme water volumes enter river drainage channels.  
>  
> The interactive Plotly chart displays the daily observed rainfall series alongside our 24-hour forward prediction target across the entire 122-day monsoon season.  
>  
> By hovering over individual dates, decision-makers can inspect predicted storm surges against historical extremes. On the right, the dashboard emphasizes the operational impact: instead of waiting for downstream stage gauges to detect bank overflow with only a 2-hour window, anticipating convective storm cells upstream extends actionable evacuation windows to 12 to 24 hours."

---

## [2:25 – 3:15] Scene 4: Tab 3 — AI Model Benchmark Hub
*(Click **🤖 AI Model Benchmark Hub**. Scroll to show table and bar chart).*

> **Say:**  
> "In the third tab, the **AI Model Benchmark Hub**, we present the empirical evaluation results of our predictive machine learning models.  
>  
> We benchmarked classical models against recurrent deep learning architectures for 24-hour lead-time forecasting across Nepal’s major basins:  
>  
> As shown in the table and comparison chart:  
> • Our baseline regularized linear model, **Ridge Regression**, yielded an RMSE of 6.85 millimeters.  
> • The **Random Forest Regressor** improved performance to 6.54 millimeters.  
> • Our 2-layer **Bidirectional LSTM** deep neural network with a 7-day lookback sequence window achieved an RMSE of 6.24 millimeters, capturing multi-day storm build-up.  
> • And our tuned **XGBoost ensemble** delivered the best overall continuous performance, achieving an RMSE of 6.16 millimeters and a Mean Absolute Error of 4.12 millimeters.  
>  
> In ablation tests, incorporating antecedent soil moisture reduced our False Alarm Ratio to 0.21 and increased our Critical Success Index to 0.68."

---

## [3:15 – 3:55] Scene 5: Tab 4 — Transboundary Basin Cartography
*(Click **🗺️ Transboundary Basin Cartography**. Zoom in/out, click stations).*

> **Say:**  
> "Finally, we navigate to the **Transboundary Basin Cartography** module.  
>  
> This interactive geospatial view anchors our machine learning predictions across Nepal's four major macro-river basins: the **Koshi**, the **Gandaki**, the **Karnali**, and the flash-flood prone **West Rapti**.  
>  
> The map uses real-time topographic relief tiles to represent the extreme elevation gradients of the Himalayas. Plotted across the corridors are critical hydrological monitoring stations:  
> *(Click on markers as you speak)*  
> • Here is **Chisapani** in the western Karnali basin, currently showing Normal status in green.  
> • Here is **Devghat** at the confluence of the Narayani basin in yellow Watch status.  
> • Here is **Chatara** in the Koshi river corridor in orange Warning status.  
> • And here is **Kusum** along the West Rapti basin in red Evacuation status, alerting emergency teams to immediate downstream inundation risk.  
>  
> Using the layer control in the upper right corner, users can toggle between standard OpenStreetMap street maps and high-contrast Himalayan topographic relief."

---

## [3:55 – 4:15] Scene 6: Conclusion
*(Stay on map or scroll back to top of dashboard).*

> **Say:**  
> "In conclusion, this web-based Early Warning System proves that combining satellite Earth observation, soil moisture physics, and machine learning can effectively transform flood management in Nepal from reactive emergency response to proactive anticipation.  
>  
> Thank you very much for watching this demonstration."

