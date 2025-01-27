import webbrowser
from functools import partial

from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtWebKitWidgets import QWebPage

from geocatbridge.utils import files, gui, meta

WIDGET, BASE = gui.loadUiType(__file__)


class GeoCatWidget(WIDGET, BASE):

    def __init__(self, parent=None):
        super(GeoCatWidget, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)

        path = files.getResourcePath(files.Path("geocat") / "index.html")
        url = QUrl.fromLocalFile(path)
        self.txtAbout.load(url)
        self.txtAbout.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        self.txtAbout.linkClicked.connect(partial(self.open_link))

        # Add version info
        name = meta.getLongAppName()
        version = meta.getVersion()
        if version and name:
            info = getattr(self.parent, 'info', '')
            self.txtInfo.setText(f'{name} v{version} {info}')

        self.btnClose.clicked.connect(parent.close)

    @staticmethod
    def open_link(url: QUrl) -> bool:
        return webbrowser.open_new_tab(url.toString())
