# HydroSHEDS Downloader for QGIS V2.1.2

A lightweight QGIS plugin for downloading HydroSHEDS data by study area.

## English

### Features
- Current map extent, drawn rectangle, polygon layer, or external SHP/GPKG/GeoJSON as study area.
- HydroSHEDS v2 first, with optional v1.1 fallback for compatible raster products.
- DIR, ACC, ACA, RIV and BAS product selection.
- Automatic 10° × 10° tile calculation for tiled raster products.
- Download, unzip, mosaic, clip and add outputs back to QGIS.
- Basemaps: Esri World Imagery, OpenStreetMap Standard, Humanitarian (HOT), OSM France, OSM DE, CyclOSM and OpenTopoMap.
- Add a labeled HydroSHEDS 10° × 10° grid to QGIS, either globally or only for the current study extent.
- Native QGIS/Qt visual style; no external Python packages required.

### Data note
HydroSHEDS v2 is being released progressively. Availability depends on region and product. The plugin resolves links from the official HydroSHEDS download page at run time and reports unavailable combinations instead of silently substituting another dataset.

### Basemap note
Online basemaps are third-party web tile services. Availability and usage limits are governed by each provider's terms and tile-use policy. They are intended as contextual basemaps, not as HydroSHEDS data sources.

### Install
QGIS → Plugins → Manage and Install Plugins → Install from ZIP → select `HydroSHEDS_Downloader_V2.1.2.zip`.

## 中文

### 主要功能
- 支持当前地图范围、地图绘制矩形、当前面图层、外部 SHP/GPKG/GeoJSON 四种研究区方式。
- 默认优先使用 HydroSHEDS v2；兼容产品可尝试回退至 v1.1。
- 支持 DIR、ACC、ACA、RIV、BAS 产品选择。
- 自动计算 10°×10° 数据瓦片。
- 自动下载、解压、拼接、裁剪并加载至 QGIS。
- 新增底图：Esri World Imagery、OSM 标准、OSM Humanitarian、OSM France、OSM DE、CyclOSM、OpenTopoMap。
- 新增 HydroSHEDS 10°×10°格网，可仅显示当前研究区涉及瓦片，并标注瓦片编号。
- 采用 QGIS 原生 Qt 风格，不依赖第三方 Python 包。

### 数据说明
HydroSHEDS v2 当前处于分区域逐步发布阶段，不同区域、不同产品的可用性并不完全一致。本插件运行时优先从 HydroSHEDS 官方下载页解析实际下载地址；未发布的数据会明确提示，不会静默替换为其他来源。

### 底图说明
在线底图仅作为定位和辅助浏览使用，数据来源、可用性和访问限制以各服务提供方的许可和瓦片使用政策为准，不属于 HydroSHEDS 数据产品。

### 安装
QGIS → 插件 → 管理并安装插件 → 从 ZIP 安装 → 选择 `HydroSHEDS_Downloader_V2.1.2.zip`。

## V2.1.2
- 修复折叠分组后界面仍保留大面积空白的问题。
- “检查数据 / 开始下载”操作区随分组折叠自动上移。
- 折叠内容不再占用隐藏高度。
- 浮动窗口模式下会根据内容重新调整高度；停靠模式下遵循 QGIS Dock 区域高度，但内容保持紧凑排列。

## V2.1.1
- 主面板改为可折叠分区，保持 QGIS 原生简洁风格。
- 修正“绘制范围后无法下载”的核心问题：v2 DIR/ACC 不再依赖网页中动态下载链接解析，而改用 DLR EOC 官方 HydroSHEDS v2 洲级 GeoTIFF，通过 GDAL `/vsicurl/` 按绘制范围远程读取并裁剪，不下载整幅洲级文件。
- 当前 v2 美洲正式发布以 DIR、ACC、RIV、BAS 为主；ACA 在自动/v2模式下暂不提供选择，避免误判为 v2 1 arc-second 产品。
- 绘制后持续显示范围、10°×10°格网编号和 v2 区域识别结果。
