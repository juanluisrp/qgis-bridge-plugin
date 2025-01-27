from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.core import QgsProcessingAlgorithm

from geocatbridge.utils import meta
from geocatbridge.utils.files import getIconPath


class BridgeAlgorithm(QgsProcessingAlgorithm):

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'

    def __init__(self):
        super().__init__()

    def initAlgorithm(self, config=None):  # noqa
        super().initAlgorithm(config)

    def createInstance(self):
        return type(self)()

    def icon(self):
        return QIcon(getIconPath("geocat"))

    def group(self):
        return self.tr("Publish tools")

    def groupId(self):
        return meta.PLUGIN_NAMESPACE

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def tags(self):
        return []
