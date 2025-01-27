import json
from itertools import chain

from qgis.PyQt.Qsci import QsciScintilla, QsciLexerXML, QsciLexerJSON
from qgis.PyQt.QtGui import QFont, QColor, QFontMetrics
from qgis.PyQt.QtWidgets import QVBoxLayout
from qgis.utils import iface

from bridgestyle.qgis import layerStyleAsSld, layerStyleAsMapbox, layerStyleAsMapfile
from bridgestyle.qgis.togeostyler import convert
from geocatbridge.utils.layers import isSupported
from geocatbridge.utils import gui

WIDGET, BASE = gui.loadUiType(__file__)


class StyleviewerWidget(BASE, WIDGET):

    def __init__(self, ):
        super(StyleviewerWidget, self).__init__(iface.mainWindow())
        self.setupUi(self)

        self.txtSld = EditorWidget(QsciLexerXML())
        layout = QVBoxLayout()
        layout.addWidget(self.txtSld)
        self.widgetSld.setLayout(layout)

        self.txtGeostyler = EditorWidget(QsciLexerJSON())
        layout = QVBoxLayout()
        layout.addWidget(self.txtGeostyler)
        self.widgetGeostyler.setLayout(layout)

        self.txtMapbox = EditorWidget(QsciLexerJSON())
        layout = QVBoxLayout()
        layout.addWidget(self.txtMapbox)
        self.widgetMapbox.setLayout(layout)

        self.txtMapserver = EditorWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.txtMapserver)
        self.widgetMapserver.setLayout(layout)        

        self.updateForCurrentLayer()

    def updateLayer(self, layer):
        active_layer = iface.activeLayer()
        if active_layer is None or layer.id() == iface.activeLayer().id():
            self.updateForCurrentLayer()

    def updateForCurrentLayer(self):
        layer = iface.activeLayer()        
        sld = ""
        geostyler = ""
        mapbox = ""
        mapserver = ""
        warnings = set()
        if isSupported(layer):
            sld, _, sld_warnings = layerStyleAsSld(layer)
            geostyler, _, _, geostyler_warnings = convert(layer)
            geostyler = json.dumps(geostyler, indent=4)
            mapbox, _, mapbox_warnings = layerStyleAsMapbox(layer)
            mapserver, _, _, mapserver_warnings = layerStyleAsMapfile(layer)
            warnings.update(chain(sld_warnings, geostyler_warnings, mapbox_warnings, mapserver_warnings))
        self.txtSld.setText(sld)
        self.txtGeostyler.setText(geostyler)
        self.txtMapbox.setText(mapbox)
        self.txtMapserver.setText(mapserver)
        self.txtWarnings.setPlainText("\n".join(warnings))


class EditorWidget(QsciScintilla):
    ARROW_MARKER_NUM = 8

    def __init__(self, lexer=None):
        super(EditorWidget, self).__init__()

        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(10)
        self.setFont(font)
        self.setMarginsFont(font)
        
        fontmetrics = QFontMetrics(font)
        self.setMarginsFont(font)
        self.setMarginWidth(0, fontmetrics.width("00000") + 6)
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QColor("#cccccc"))

        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#ffe4e4"))

        if lexer is not None:
            lexer.setDefaultFont(font)        
            self.setLexer(lexer)

        self.setReadOnly(True)
        self.SendScintilla(QsciScintilla.SCI_STYLESETFONT, 1, 'Courier'.encode())
