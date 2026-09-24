def classFactory(iface):
    from .plugin import HydroSHEDSDownloaderPlugin
    return HydroSHEDSDownloaderPlugin(iface)
