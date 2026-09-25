<div align="center">

# HydroSHEDS Downloader for QGIS

**Download and clip HydroSHEDS data by study area directly in QGIS**

[**🇺🇸 English**](./README.md) · [🇨🇳 中文](./README_CN.md)

<img src="https://img.shields.io/badge/QGIS-3.28%2B-589632?style=flat-square&logo=qgis&logoColor=white" />
<img src="https://img.shields.io/badge/Version-1.0.1-1565C0?style=flat-square" />
<img src="https://img.shields.io/badge/HydroSHEDS-v2-00838F?style=flat-square" />
<img src="https://img.shields.io/badge/Python-PyQGIS-3776AB?style=flat-square&logo=python&logoColor=white" />

[![QGIS Plugins](https://img.shields.io/badge/QGIS_Plugins-Official_Page-589632?style=flat-square&logo=qgis&logoColor=white)](https://plugins.qgis.org/plugins/HydroSHEDS_Downloader/)

</div>

---

## Overview

**HydroSHEDS Downloader** is a lightweight QGIS plugin for retrieving and clipping HydroSHEDS hydrological data by a user-defined study area. It reduces repetitive work in identifying data regions, locating HydroSHEDS tiles, accessing official products, clipping outputs, and loading results back into QGIS.

The plugin follows the native QGIS interface style and supports the current map extent, an interactively drawn rectangle, polygon layers, and external SHP/GPKG/GeoJSON files as study areas.

## Features

- Current map extent, drawn rectangle, polygon layer, or external polygon file as study area.
- HydroSHEDS 10° × 10° grid and tile ID display.
- HydroSHEDS v2 regional recognition and official data access where available.
- Esri World Imagery and multiple OpenStreetMap-based contextual basemaps.
- Automatic clipping and optional loading of outputs back into QGIS.
- Collapsible sections using the native QGIS/Qt visual style.
- English/Chinese interface according to the QGIS/system locale.

## HydroSHEDS v2

HydroSHEDS v2 is being released progressively by region. The plugin checks regional and product availability instead of treating v2 as a completed global replacement for HydroSHEDS v1.1.

For supported v2 raster products, the plugin uses official HydroSHEDS/DLR EOC resources and reads the requested study extent through QGIS/GDAL capabilities where applicable.

## Source Code

The QGIS plugin source code is stored in [`HydroSHEDS_Downloader`](./HydroSHEDS_Downloader):

```text
HydroSHEDS_Downloader/
├─ __init__.py
├─ plugin.py
├─ metadata.txt
├─ icon.png
├─ README.md
├─ README_CN.md
├─ CHANGELOG.md
└─ LICENSE
```

## Installation

### QGIS Plugin Repository

Install directly from **QGIS → Plugins → Manage and Install Plugins**, then search for **HydroSHEDS Downloader**.

Official plugin page: https://plugins.qgis.org/plugins/HydroSHEDS_Downloader/

### Manual installation

Clone or download this repository, package the `HydroSHEDS_Downloader` folder as a ZIP, then open **QGIS → Plugins → Manage and Install Plugins → Install from ZIP**.

## Links

- QGIS Plugin Repository: https://plugins.qgis.org/plugins/HydroSHEDS_Downloader/
- HydroSHEDS: https://www.hydrosheds.org/
- HydroSHEDS v2 downloads: https://www.hydrosheds.org/downloads-core-data-v2
- GitHub repository: https://github.com/zhangyhrs/HydroSHEDS-Downloader-QGIS
- Issues: https://github.com/zhangyhrs/HydroSHEDS-Downloader-QGIS/issues

---

## Connect

<table align="center">
  <tr>
    <th width="33%">WeChat Official Account<br>微信公众号：测绘地信</th>
    <th width="33%">WeChat Mini Program<br>微信小程序：测绘地信</th>
    <th width="33%">Knowledge Planet<br>知识星球：测绘地理信息共享中心</th>
  </tr>
  <tr>
    <td align="center"><img src="https://raw.githubusercontent.com/zhangyhrs/GeoStar-Selector-QGIS/main/assets/wechat-official-account.png" height="150"></td>
    <td align="center"><img src="https://raw.githubusercontent.com/zhangyhrs/GeoStar-Selector-QGIS/main/assets/wechat-mini-program.jpg" height="150"></td>
    <td align="center"><img src="https://raw.githubusercontent.com/zhangyhrs/GeoStar-Selector-QGIS/main/assets/knowledge-planet.jpg" height="150"></td>
  </tr>
</table>

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-@zhangyhrs-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/zhangyhrs)

</div>
