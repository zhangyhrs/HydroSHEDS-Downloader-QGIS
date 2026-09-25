<div align="center">

# HydroSHEDS Downloader for QGIS

**在 QGIS 中按研究范围下载并裁剪 HydroSHEDS 数据**

[🇺🇸 English](./README.md) · [**🇨🇳 中文**](./README_CN.md)

<img src="https://img.shields.io/badge/QGIS-3.28%2B-589632?style=flat-square&logo=qgis&logoColor=white" />
<img src="https://img.shields.io/badge/Version-1.0.1-1565C0?style=flat-square" />
<img src="https://img.shields.io/badge/HydroSHEDS-v2-00838F?style=flat-square" />
<img src="https://img.shields.io/badge/Python-PyQGIS-3776AB?style=flat-square&logo=python&logoColor=white" />

[![QGIS Plugins](https://img.shields.io/badge/QGIS_Plugins-官方插件页-589632?style=flat-square&logo=qgis&logoColor=white)](https://plugins.qgis.org/plugins/HydroSHEDS_Downloader/)

</div>

---

## 项目简介

**HydroSHEDS Downloader** 是一个按研究范围获取并裁剪 HydroSHEDS 水文数据的轻量级 QGIS 插件，主要用于减少数据区域判断、瓦片识别、官方数据获取、裁剪和加载等重复操作。

插件延续 QGIS 原生界面风格，可使用当前地图范围、地图绘制矩形、当前面图层以及外部 SHP/GPKG/GeoJSON 文件作为研究范围。

## 主要功能

- 支持当前地图范围、绘制矩形、面图层和外部面矢量文件四种研究区方式。
- 显示 HydroSHEDS 10° × 10° 格网及瓦片编号。
- 识别 HydroSHEDS v2 当前发布区域，并在可用区域访问官方数据。
- 支持 Esri World Imagery 和多种 OpenStreetMap 在线底图。
- 可按研究范围裁剪数据，并在完成后自动加载至当前 QGIS 项目。
- 下载范围、数据产品、输出及底图格网等模块支持折叠。
- 根据 QGIS/系统语言自动使用中文或英文界面。

## HydroSHEDS v2

HydroSHEDS v2 正在分区域逐步发布。插件会根据研究范围和数据产品判断可用性，不会将 v2 直接视为已经完成全球替代的版本。

对于当前已支持的 v2 栅格产品，插件优先使用 HydroSHEDS / DLR EOC 官方资源，并在适用情况下通过 QGIS/GDAL 按研究范围读取和裁剪。

## 源代码

完整 QGIS 插件源代码位于 [`HydroSHEDS_Downloader`](./HydroSHEDS_Downloader) 目录：

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

## 安装方法

### QGIS 官方插件库

进入 **QGIS → 插件 → 管理并安装插件**，搜索 **HydroSHEDS Downloader** 安装。

官方插件页面：https://plugins.qgis.org/plugins/HydroSHEDS_Downloader/

### ZIP 手动安装

下载或克隆本仓库，将 `HydroSHEDS_Downloader` 文件夹打包为 ZIP，然后进入 **QGIS → 插件 → 管理并安装插件 → 从 ZIP 安装**。

## 相关链接

- QGIS 官方插件页：https://plugins.qgis.org/plugins/HydroSHEDS_Downloader/
- HydroSHEDS 官网：https://www.hydrosheds.org/
- HydroSHEDS v2 下载：https://www.hydrosheds.org/downloads-core-data-v2
- GitHub 仓库：https://github.com/zhangyhrs/HydroSHEDS-Downloader-QGIS
- 问题反馈：https://github.com/zhangyhrs/HydroSHEDS-Downloader-QGIS/issues

---

## 关注交流

<table align="center">
  <tr>
    <th width="33%">微信公众号<br>测绘地信</th>
    <th width="33%">微信小程序<br>测绘地信</th>
    <th width="33%">知识星球<br>测绘地理信息共享中心</th>
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
