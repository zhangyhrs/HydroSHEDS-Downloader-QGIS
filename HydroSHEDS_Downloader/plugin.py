# -*- coding: utf-8 -*-
"""HydroSHEDS Downloader for QGIS 3.x."""
import math
import os
from pathlib import Path

from qgis.PyQt.QtCore import Qt, QSize, pyqtSignal
from qgis.PyQt.QtGui import QColor, QIcon
from qgis.PyQt.QtWidgets import (
    QAction, QApplication, QButtonGroup, QCheckBox, QComboBox, QDockWidget,
    QFileDialog, QFrame, QHBoxLayout, QLabel, QLineEdit, QMessageBox,
    QProgressBar, QPushButton, QRadioButton, QScrollArea, QSizePolicy,
    QToolButton, QVBoxLayout, QWidget,
)
from qgis.core import (
    Qgis, QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsFeature,
    QgsField, QgsFillSymbol, QgsGeometry, QgsPalLayerSettings, QgsProject,
    QgsRasterLayer, QgsRectangle, QgsTextFormat, QgsVectorLayer,
    QgsVectorLayerSimpleLabeling, QgsWkbTypes,
)
from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand
from qgis.PyQt.QtCore import QVariant
import processing

PLUGIN_VERSION = "2.1.2"
PLUGIN_DIR = os.path.dirname(__file__)
ICON_PATH = os.path.join(PLUGIN_DIR, "icon.svg")

BASEMAPS = {
    "Esri World Imagery": ("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", 19),
    "OpenStreetMap Standard": ("https://tile.openstreetmap.org/{z}/{x}/{y}.png", 19),
    "OpenStreetMap Humanitarian (HOT)": ("https://a.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png", 19),
    "OpenStreetMap France": ("https://a.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png", 20),
    "OpenStreetMap DE": ("https://tile.openstreetmap.de/{z}/{x}/{y}.png", 19),
    "CyclOSM": ("https://a.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png", 20),
    "OpenTopoMap": ("https://a.tile.opentopomap.org/{z}/{x}/{y}.png", 17),
}

TEXT = {
    "zh": {
        "title": "HydroSHEDS 数据下载", "extent": "下载范围", "current": "当前地图范围",
        "draw": "地图绘制范围", "layer": "当前面图层", "file": "外部矢量文件",
        "selected": "仅使用选中要素", "products": "数据产品", "output": "输出",
        "basemap": "底图与格网", "check": "检查数据", "download": "开始下载",
        "clip": "自动裁剪到研究区", "load": "下载后自动加载到 QGIS",
        "clear": "清除绘制范围", "grid": "添加 HydroSHEDS 格网",
        "onlygrid": "仅显示当前范围涉及格网", "addmap": "添加底图",
        "ready": "就绪", "browse": "浏览…",
    },
    "en": {
        "title": "HydroSHEDS Downloader", "extent": "Download extent", "current": "Current map extent",
        "draw": "Draw rectangle on map", "layer": "Polygon layer", "file": "Vector file",
        "selected": "Selected features only", "products": "Products", "output": "Output",
        "basemap": "Basemap & grid", "check": "Check data", "download": "Download",
        "clip": "Clip to study area", "load": "Add outputs to QGIS",
        "clear": "Clear drawn extent", "grid": "Add HydroSHEDS grid",
        "onlygrid": "Only tiles intersecting current extent", "addmap": "Add basemap",
        "ready": "Ready", "browse": "Browse…",
    },
}


def language():
    from qgis.PyQt.QtCore import QLocale
    return "zh" if QLocale.system().name().lower().startswith("zh") else "en"


class CollapsibleSection(QWidget):
    toggled = pyqtSignal(bool)

    def __init__(self, title, expanded=True, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.header = QToolButton()
        self.header.setText(title)
        self.header.setCheckable(True)
        self.header.setChecked(expanded)
        self.header.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.header.setArrowType(Qt.ArrowType.DownArrow if expanded else Qt.ArrowType.RightArrow)
        self.header.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.header.setStyleSheet("QToolButton{border:0;padding:6px 4px;font-weight:600;text-align:left;}")
        layout.addWidget(self.header)
        line = QFrame(); line.setFrameShape(QFrame.Shape.HLine); layout.addWidget(line)
        self.content = QWidget()
        self.box = QVBoxLayout(self.content)
        self.box.setContentsMargins(8, 6, 6, 8)
        self.box.setSpacing(6)
        self.content.setVisible(expanded)
        self.content.setMaximumHeight(16777215 if expanded else 0)
        layout.addWidget(self.content)
        self.header.toggled.connect(self._toggle)

    def _toggle(self, checked):
        self.content.setVisible(checked)
        self.content.setMaximumHeight(16777215 if checked else 0)
        self.header.setArrowType(Qt.ArrowType.DownArrow if checked else Qt.ArrowType.RightArrow)
        self.updateGeometry()
        self.toggled.emit(checked)


class RectangleTool(QgsMapToolEmitPoint):
    def __init__(self, canvas, callback):
        super().__init__(canvas)
        self.canvas, self.callback, self.start = canvas, callback, None
        self.rb = QgsRubberBand(canvas, Qgis.GeometryType.Polygon)
        self.rb.setStrokeColor(QColor(0, 120, 215, 220))
        self.rb.setFillColor(QColor(0, 120, 215, 35))
        self.rb.setWidth(2)

    def canvasPressEvent(self, e):
        self.start = self.toMapCoordinates(e.pos())

    def canvasMoveEvent(self, e):
        if self.start:
            self.rb.setToGeometry(QgsGeometry.fromRect(QgsRectangle(self.start, self.toMapCoordinates(e.pos()))), None)

    def canvasReleaseEvent(self, e):
        if not self.start:
            return
        rect = QgsRectangle(self.start, self.toMapCoordinates(e.pos()))
        self.start = None
        self.rb.reset(Qgis.GeometryType.Polygon)
        if rect.width() > 0 and rect.height() > 0:
            self.callback(rect, self.canvas.mapSettings().destinationCrs())


class HydroDock(QDockWidget):
    def __init__(self, plugin):
        self.plugin = plugin
        self.t = TEXT[plugin.lang]
        super().__init__(self.t["title"])
        self.setObjectName("HydroSHEDSDownloaderDock")
        self.setMinimumWidth(330)
        self.draw_rect = self.draw_crs = None
        self._build()

    def _section(self, root, title, expanded=True):
        s = CollapsibleSection(title, expanded)
        s.toggled.connect(lambda _: self.widget().adjustSize())
        root.addWidget(s)
        return s.box

    def _build(self):
        body = QWidget(); outer = QVBoxLayout(body); outer.setContentsMargins(0,0,0,0)
        scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setFrameShape(QFrame.Shape.NoFrame)
        inner = QWidget(); root = QVBoxLayout(inner); root.setContentsMargins(8,6,8,8); root.setSpacing(3)

        box = self._section(root, self.t["extent"], True)
        self.group = QButtonGroup(self)
        self.rb_current = QRadioButton(self.t["current"]); self.rb_current.setChecked(True)
        self.rb_draw = QRadioButton(self.t["draw"]); self.rb_layer = QRadioButton(self.t["layer"]); self.rb_file = QRadioButton(self.t["file"])
        for r in (self.rb_current,self.rb_draw,self.rb_layer,self.rb_file): self.group.addButton(r); box.addWidget(r)
        h = QHBoxLayout(); self.layer_combo = QComboBox(); self.selected = QCheckBox(self.t["selected"]); h.addWidget(self.layer_combo,1); h.addWidget(self.selected); box.addLayout(h)
        h = QHBoxLayout(); self.file_edit = QLineEdit(); h.addWidget(self.file_edit,1); b=QPushButton(self.t["browse"]); b.clicked.connect(self.choose_file); h.addWidget(b); box.addLayout(h)
        b = QPushButton(self.t["draw"]); b.clicked.connect(plugin.start_draw); box.addWidget(b)
        self.scope_info = QLabel("—"); self.scope_info.setWordWrap(True); box.addWidget(self.scope_info)
        b = QPushButton(self.t["clear"]); b.clicked.connect(plugin.clear_drawn_extent); box.addWidget(b)

        box = self._section(root, self.t["products"], True)
        self.products = {}
        for key, label in (("DIR","Flow Direction (DIR)"),("ACC","Flow Accumulation (ACC)"),("ACA","Catchment Area (ACA)"),("RIV","River Network (RIV)"),("BAS","Sub-basins (BAS)")):
            c=QCheckBox(label); c.setChecked(key in ("DIR","ACC")); box.addWidget(c); self.products[key]=c
        self.products["ACA"].setEnabled(False)

        box = self._section(root, self.t["output"], True)
        h=QHBoxLayout(); self.out_edit=QLineEdit(); h.addWidget(self.out_edit,1); b=QPushButton(self.t["browse"]); b.clicked.connect(self.choose_output); h.addWidget(b); box.addLayout(h)
        self.clip=QCheckBox(self.t["clip"]); self.clip.setChecked(True); self.load=QCheckBox(self.t["load"]); self.load.setChecked(True); box.addWidget(self.clip); box.addWidget(self.load)

        box = self._section(root, self.t["basemap"], False)
        h=QHBoxLayout(); self.basemap_combo=QComboBox(); self.basemap_combo.addItems(BASEMAPS); h.addWidget(self.basemap_combo,1); b=QPushButton(self.t["addmap"]); b.clicked.connect(plugin.add_basemap); h.addWidget(b); box.addLayout(h)
        self.onlygrid=QCheckBox(self.t["onlygrid"]); self.onlygrid.setChecked(True); box.addWidget(self.onlygrid); b=QPushButton(self.t["grid"]); b.clicked.connect(plugin.add_grid); box.addWidget(b)

        self.progress=QProgressBar(); root.addWidget(self.progress); self.status=QLabel(self.t["ready"]); self.status.setWordWrap(True); root.addWidget(self.status)
        h=QHBoxLayout(); b=QPushButton(self.t["check"]); b.clicked.connect(plugin.check_data); h.addWidget(b); b=QPushButton(self.t["download"]); b.clicked.connect(plugin.download); h.addWidget(b); root.addLayout(h); root.addStretch(1)
        scroll.setWidget(inner); outer.addWidget(scroll); self.setWidget(body)
        self.refresh_layers()
        for r in (self.rb_current,self.rb_draw,self.rb_layer,self.rb_file): r.toggled.connect(lambda _: plugin.update_scope_info())

    def refresh_layers(self):
        self.layer_combo.clear(); self.layer_combo.addItem("—", None)
        for lyr in QgsProject.instance().mapLayers().values():
            if isinstance(lyr,QgsVectorLayer) and QgsWkbTypes.geometryType(lyr.wkbType()) == Qgis.GeometryType.Polygon:
                self.layer_combo.addItem(lyr.name(), lyr.id())

    def choose_file(self):
        p,_=QFileDialog.getOpenFileName(self,"Vector","","Vector (*.shp *.gpkg *.geojson *.json)")
        if p: self.file_edit.setText(p); self.rb_file.setChecked(True)

    def choose_output(self):
        p=QFileDialog.getExistingDirectory(self,self.t["output"])
        if p: self.out_edit.setText(p)


class HydroSHEDSDownloaderPlugin:
    def __init__(self, iface):
        self.iface=iface; self.canvas=iface.mapCanvas(); self.lang=language(); self.t=TEXT[self.lang]
        self.action=self.dock=self.map_tool=self.scope_rb=None

    def initGui(self):
        self.action=QAction(QIcon(ICON_PATH),self.t["title"],self.iface.mainWindow())
        self.action.triggered.connect(self.show_dock); self.iface.addPluginToMenu("&HydroSHEDS Downloader",self.action); self.iface.addToolBarIcon(self.action)

    def unload(self):
        if self.action: self.iface.removePluginMenu("&HydroSHEDS Downloader",self.action); self.iface.removeToolBarIcon(self.action)
        if self.dock: self.iface.removeDockWidget(self.dock); self.dock.deleteLater(); self.dock=None

    def show_dock(self):
        if self.dock is None:
            self.dock=HydroDock(self); self.iface.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea,self.dock)
            self.canvas.extentsChanged.connect(lambda: self.dock and self.dock.rb_current.isChecked() and self.update_scope_info())
        self.dock.refresh_layers(); self.dock.show(); self.dock.raise_(); self.update_scope_info()

    def start_draw(self):
        if not self.dock: self.show_dock()
        self.dock.rb_draw.setChecked(True); self.map_tool=RectangleTool(self.canvas,self._draw_done); self.canvas.setMapTool(self.map_tool)

    def _draw_done(self,rect,crs):
        self.dock.draw_rect,self.dock.draw_crs=rect,crs
        if self.scope_rb is None:
            self.scope_rb=QgsRubberBand(self.canvas,Qgis.GeometryType.Polygon); self.scope_rb.setStrokeColor(QColor(0,120,215,235)); self.scope_rb.setFillColor(QColor(0,120,215,45)); self.scope_rb.setWidth(3)
        self.scope_rb.setToGeometry(QgsGeometry.fromRect(rect),None); self.canvas.unsetMapTool(self.map_tool); self.canvas.refresh(); self.update_scope_info()

    def clear_drawn_extent(self):
        if self.dock: self.dock.draw_rect=self.dock.draw_crs=None
        if self.scope_rb: self.scope_rb.reset(Qgis.GeometryType.Polygon)
        self.update_scope_info()

    def _wgs84(self,rect,crs):
        if crs.authid()=="EPSG:4326": return rect
        return QgsCoordinateTransform(crs,QgsCoordinateReferenceSystem("EPSG:4326"),QgsProject.instance()).transformBoundingBox(rect)

    def _scope(self):
        d=self.dock
        if d.rb_current.isChecked(): return self._wgs84(self.canvas.extent(),self.canvas.mapSettings().destinationCrs()),None
        if d.rb_draw.isChecked(): return (self._wgs84(d.draw_rect,d.draw_crs),None) if d.draw_rect else (None,None)
        if d.rb_layer.isChecked():
            lyr=QgsProject.instance().mapLayer(d.layer_combo.currentData()) if d.layer_combo.currentData() else None
            return (self._wgs84(lyr.extent(),lyr.crs()),lyr) if lyr else (None,None)
        if d.rb_file.isChecked():
            p=d.file_edit.text().strip(); lyr=QgsVectorLayer(p,Path(p).stem,"ogr") if p else None
            return (self._wgs84(lyr.extent(),lyr.crs()),lyr) if lyr and lyr.isValid() else (None,None)
        return None,None

    @staticmethod
    def tile_names(rect):
        xs=range(int(math.floor(rect.xMinimum()/10))*10,int(math.floor((rect.xMaximum()-1e-10)/10))*10+1,10)
        ys=range(int(math.floor(rect.yMinimum()/10))*10,int(math.floor((rect.yMaximum()-1e-10)/10))*10+1,10)
        def n(y,x): return f"{'n' if y>=0 else 's'}{abs(y):02d}{'e' if x>=0 else 'w'}{abs(x):03d}"
        return [n(y,x) for y in ys for x in xs]

    def update_scope_info(self):
        if not self.dock: return
        rect,_=self._scope()
        if not rect: self.dock.scope_info.setText("—"); return
        tiles=self.tile_names(rect); show=", ".join(tiles if len(tiles)<=10 else tiles[:8]+["…"])
        self.dock.scope_info.setText(f"WGS84: {rect.xMinimum():.5f}, {rect.yMinimum():.5f}, {rect.xMaximum():.5f}, {rect.yMaximum():.5f}\nTiles ({len(tiles)}): {show}")

    def _v2_region(self,rect):
        cx=(rect.xMinimum()+rect.xMaximum())/2; cy=(rect.yMinimum()+rect.yMaximum())/2
        if not (-170<=cx<=-30 and -60<=cy<=85): return None
        return ("South_America","south-america") if cy<12 and cx>-95 else ("North_America","north-america")

    def _v2_url(self,product,rect):
        reg=self._v2_region(rect)
        if not reg or product not in ("DIR","ACC"): return None
        folder,base=reg; return f"https://download.geoservice.dlr.de/HYDROSHEDS_v2/files/{folder}/{base}_{product}_1s_v2r0.tif"

    def add_basemap(self):
        old=QgsRectangle(self.canvas.extent()); name=self.dock.basemap_combo.currentText(); url,zmax=BASEMAPS[name]
        lyr=QgsRasterLayer(f"type=xyz&url={url}&zmin=0&zmax={zmax}&crs=EPSG3857",name,"wms")
        if lyr.isValid(): QgsProject.instance().addMapLayer(lyr); self.canvas.setExtent(old); self.canvas.refresh()

    def add_grid(self):
        rect,_=self._scope() if self.dock.onlygrid.isChecked() else (None,None)
        layer=QgsVectorLayer("Polygon?crs=EPSG:4326","HydroSHEDS 10°×10° Grid","memory"); pr=layer.dataProvider(); pr.addAttributes([QgsField("tile_id",QVariant.String)]); layer.updateFields(); feats=[]
        for y in range(-90,90,10):
            for x in range(-180,180,10):
                cell=QgsRectangle(x,y,x+10,y+10)
                if rect and not cell.intersects(rect): continue
                f=QgsFeature(layer.fields()); f.setGeometry(QgsGeometry.fromRect(cell)); f["tile_id"]=f"{'n' if y>=0 else 's'}{abs(y):02d}{'e' if x>=0 else 'w'}{abs(x):03d}"; feats.append(f)
        pr.addFeatures(feats); layer.updateExtents(); layer.renderer().setSymbol(QgsFillSymbol.createSimple({"color":"0,0,0,0","outline_color":"45,125,210,210","outline_width":"0.45","outline_style":"dash"}))
        pal=QgsPalLayerSettings(); pal.fieldName="tile_id"; pal.enabled=True; fmt=QgsTextFormat(); fmt.setSize(8); fmt.setColor(QColor(35,92,150)); pal.setFormat(fmt); layer.setLabeling(QgsVectorLayerSimpleLabeling(pal)); layer.setLabelsEnabled(True); QgsProject.instance().addMapLayer(layer)

    def check_data(self):
        rect,_=self._scope()
        if not rect: QMessageBox.warning(self.dock,self.t["title"],"No valid extent."); return
        reg=self._v2_region(rect); QMessageBox.information(self.dock,self.t["check"],f"Tiles: {', '.join(self.tile_names(rect))}\nv2 region: {reg[1] if reg else '—'}")

    def download(self):
        rect,mask=self._scope(); out=self.dock.out_edit.text().strip() if self.dock else ""
        if not rect or not out: QMessageBox.warning(self.dock,self.t["title"],"Please define an extent and output folder."); return
        products=[k for k,c in self.dock.products.items() if c.isChecked()]
        unsupported=[p for p in products if p not in ("DIR","ACC")]
        if unsupported: QMessageBox.information(self.dock,self.t["title"],"V2.1.2 stable direct download currently handles DIR/ACC. Other products remain listed for staged extension: "+", ".join(unsupported))
        os.makedirs(out,exist_ok=True); made=[]
        for i,p in enumerate([x for x in products if x in ("DIR","ACC")],1):
            url=self._v2_url(p,rect)
            if not url: continue
            dst=os.path.join(out,f"HydroSHEDS_{p}.tif"); ext=f"{rect.xMinimum()},{rect.xMaximum()},{rect.yMinimum()},{rect.yMaximum()} [EPSG:4326]"; self.dock.status.setText(url); QApplication.processEvents()
            processing.run("gdal:cliprasterbyextent",{"INPUT":"/vsicurl/"+url,"PROJWIN":ext,"OVERCRS":True,"NODATA":None,"OPTIONS":"COMPRESS=LZW","DATA_TYPE":0,"EXTRA":"","OUTPUT":dst}); made.append(dst); self.dock.progress.setValue(int(i*100/max(1,len(products))))
            if self.dock.load.isChecked():
                lyr=QgsRasterLayer(dst,Path(dst).stem)
                if lyr.isValid(): QgsProject.instance().addMapLayer(lyr)
        QMessageBox.information(self.dock,self.t["title"],"Completed:\n"+"\n".join(made) if made else "No output created.")
