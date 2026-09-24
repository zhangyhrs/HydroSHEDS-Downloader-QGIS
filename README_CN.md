<div align="center">

# HydroSHEDS Downloader for QGIS

**在 QGIS 中按研究范围下载并裁剪 HydroSHEDS 数据**

[🇺🇸 English](./README.md) · [**🇨🇳 中文**](./README_CN.md)

<img src="https://img.shields.io/badge/QGIS-3.28%2B-589632?style=flat-square&logo=qgis&logoColor=white" />
<img src="https://img.shields.io/badge/Version-2.1.2-1565C0?style=flat-square" />
<img src="https://img.shields.io/badge/HydroSHEDS-v2-00838F?style=flat-square" />
<img src="https://img.shields.io/badge/Python-PyQGIS-3776AB?style=flat-square&logo=python&logoColor=white" />

</div>

---

## 项目简介

**HydroSHEDS Downloader** 是一个用于按研究范围获取 HydroSHEDS 数据的轻量级 QGIS 插件，主要用于减少数据区域判断、瓦片识别、下载、裁剪和加载等重复操作。

插件延续 QGIS 原生界面风格，可使用当前地图范围、地图绘制矩形、当前面图层以及外部 SHP/GPKG/GeoJSON 文件作为研究范围。

## 主要功能

- 支持当前地图范围、绘制矩形、面图层和外部矢量文件四种研究区方式。
- 显示 HydroSHEDS 10° × 10°格网及瓦片编号。
- 识别 HydroSHEDS v2 当前发布区域，并支持美洲地区 DIR/ACC 数据获取。
- 支持 Esri World Imagery 和多种 OpenStreetMap 在线底图。
- 可按研究范围裁剪数据，并在完成后自动加载至当前 QGIS 项目。
- 下载范围、数据产品、输出及底图格网等模块支持折叠。
- 根据 QGIS/系统语言自动使用中文或英文界面。

## HydroSHEDS v2

HydroSHEDS v2 正在分区域逐步发布。截至 2026 年 9 月，首批正式发布区域为北美和南美，因此当前不同区域、不同产品的可用情况并不完全一致。插件会根据研究范围进行判断，不会将 v2 直接视为已经完成全球替代的版本。

对于美洲地区的 v2 DIR 和 ACC，插件可通过 GDAL 远程访问官方 DLR EOC 洲级 GeoTIFF，并仅按研究范围读取和裁剪。

## 源代码

完整 QGIS 插件源代码位于 [`HydroSHEDS_Downloader`](./HydroSHEDS_Downloader) 目录：

```text
HydroSHEDS_Downloader/
├─ __init__.py
├─ plugin.py
├─ metadata.txt
└─ icon.svg
```

## 安装方法

克隆或下载本仓库，将 `HydroSHEDS_Downloader` 文件夹打包为 ZIP，然后进入 **QGIS → 插件 → 管理并安装插件 → 从 ZIP 安装**。

## 相关链接

- HydroSHEDS 官网：https://www.hydrosheds.org/
- HydroSHEDS v2 下载：https://www.hydrosheds.org/downloads-core-data-v2
- GitHub 仓库：https://github.com/zhangyhrs/HydroSHEDS-Downloader-QGIS

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
