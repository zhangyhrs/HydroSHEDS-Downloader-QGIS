<div align="center">

# HydroSHEDS Downloader for QGIS

**Download and clip HydroSHEDS data directly by study area in QGIS**

[**🇺🇸 English**](./README.md) · [🇨🇳 中文](./README_CN.md)

<img src="https://img.shields.io/badge/QGIS-3.28%2B-589632?style=flat-square&logo=qgis&logoColor=white" />
<img src="https://img.shields.io/badge/Version-2.1.2-1565C0?style=flat-square" />
<img src="https://img.shields.io/badge/HydroSHEDS-v2-00838F?style=flat-square" />
<img src="https://img.shields.io/badge/Python-PyQGIS-3776AB?style=flat-square&logo=python&logoColor=white" />

</div>

---

## Overview

**HydroSHEDS Downloader** is a lightweight QGIS plugin for retrieving HydroSHEDS products by a user-defined study area. It reduces repetitive work in identifying data regions, locating HydroSHEDS tiles, downloading source products, clipping them to the target extent, and loading results back into QGIS.

The plugin follows the native QGIS interface style and supports the current map extent, an interactively drawn rectangle, polygon layers, and external SHP/GPKG/GeoJSON files as study areas.

## Features

- Current map extent, drawn rectangle, polygon layer, or external vector file as study area.
- HydroSHEDS 10° × 10° grid and tile ID display.
- HydroSHEDS v2 regional recognition and direct DIR/ACC access for the current Americas release.
- Esri World Imagery and multiple OpenStreetMap-based contextual basemaps.
- Automatic clipping and optional loading of outputs back into QGIS.
- Collapsible sections using the native QGIS/Qt visual style.
- English/Chinese interface according to the QGIS/system locale.

## HydroSHEDS v2

HydroSHEDS v2 is being released progressively by region. As of September 2026, the first official v2 release covers North America and South America. The plugin therefore checks regional availability instead of treating v2 as a completed global replacement for HydroSHEDS v1.1.

For v2 DIR and ACC in the Americas, the plugin uses the official DLR EOC continental GeoTIFF resources through GDAL remote access and reads only the requested study extent where supported.

## Source Code

The QGIS plugin source code is stored in [`HydroSHEDS_Downloader`](./HydroSHEDS_Downloader):

```text
HydroSHEDS_Downloader/
├─ __init__.py
├─ plugin.py
├─ metadata.txt
└─ icon.svg
```

## Installation

Clone or download this repository, package the `HydroSHEDS_Downloader` folder as a ZIP, then open **QGIS → Plugins → Manage and Install Plugins → Install from ZIP**.

## Links

- HydroSHEDS: https://www.hydrosheds.org/
- HydroSHEDS v2 downloads: https://www.hydrosheds.org/downloads-core-data-v2
- Repository: https://github.com/zhangyhrs/HydroSHEDS-Downloader-QGIS

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
