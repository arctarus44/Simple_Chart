# coding=utf-8
# indent-tabs-mode: 1
# tab-width: 4

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPainter, QPen, QFontMetrics, QFont
class SimpleChart(QWidget):

	MARGIN = 60
	ABS_GUIDE_LEN = 15
	__PERCENT = "%"
	__MAX_PERCENT = 100
	__ORD_LBL_SPACING = 15
	__ABS_LBL_SPACING = 10


	def __init__(self):
		super(SimpleChart, self).__init__()
		self.ord_max_value = 100
		self.abs_max_value = 100
		self.unit_abs = None
		self.unit_ord = None

		# Graphical property
		self.setAutoFillBackground(True)
		self.__updateOrdAbsPos()

		# QPen use for the drawing
		self.__axis_pen = QPen(Qt.darkGray , 2, Qt.SolidLine)
		self.__guides_pen = QPen(Qt.lightGray , 2, Qt.SolidLine)
		self.__label_pen = QPen(Qt.darkGray , 2, Qt.SolidLine)

		# Fonts
		self.__lbl_font = QFont("serif", 7, QFont.Light)
		self.__lbl_ft_metrics = QFontMetrics(self.__lbl_font)


	def __updateOrdAbsPos(self):
		# FIXME : handle the case where size.height() < self.MARGIN
		size = self.size()
		self.max_ord_pos = QPoint(self.MARGIN, self.MARGIN)
		self.max_abs_pos = QPoint(size.width() - self.MARGIN,
		                          size.height() - self.MARGIN)
		self.zero_pos = QPoint(self.MARGIN, size.height() - self.MARGIN)

	def resizeEvent(self, event):
		self.__updateOrdAbsPos()

	def paintEvent(self, event):
		qpainter = QPainter()
		qpainter.begin(self)
		self.__drawBackground(qpainter)
		qpainter.end()

	def __drawBackground(self, qpainter):
		# Set background Color
		pal = self.palette()
		pal.setColor(self.backgroundRole(), Qt.white)
		self.setPalette(pal)

		# DEBUG
		# print("Ord  ("+ str(self.max_ord_pos.x()) + ',' + str(self.max_ord_pos.y())+ ")")
		# print("Abs  ("+ str(self.max_abs_pos.x()) + ',' + str(self.max_abs_pos.y())+ ")")
		# print("Zero ("+ str(self.zero_pos.x()) + ',' + str(self.zero_pos.y())+ ")")
		# END DEBUG

		# draw axis
		qpainter.setPen(self.__axis_pen)
		qpainter.drawLine(self.zero_pos, self.max_ord_pos)
		qpainter.drawLine(self.zero_pos, self.max_abs_pos)

		# draw guides
		qpainter.setPen(self.__guides_pen)
		ord_guide = QPoint(self.max_abs_pos.x(), self.max_ord_pos.y())
		qpainter.drawLine(self.max_ord_pos, ord_guide)
		point = QPoint(self.max_abs_pos.x(),
		               self.max_abs_pos.y() - self.ABS_GUIDE_LEN)
		qpainter.drawLine(self.max_abs_pos, point)


		# draw ordinate label
		qpainter.setPen(self.__label_pen)

		ord_lbl = str(self.ord_max_value) + self.unit_ord
		width = self.__lbl_ft_metrics.width(ord_lbl)
		height = self.__lbl_ft_metrics.height()

		lbl_pt = QPoint(self.max_ord_pos.x() - self.__ORD_LBL_SPACING - width,
		                self.max_ord_pos.y() + height / 2)
		qpainter.drawText(lbl_pt, ord_lbl)

		# draw abscissa label
		abs_lbl = str(self.abs_max_value) + self.unit_abs
		width = self.__lbl_ft_metrics.width(abs_lbl)

		lbl_pt = QPoint(self.max_abs_pos.x() - width / 2,
		                self.max_abs_pos.y() + self.__ABS_LBL_SPACING + height)
		qpainter.drawText(lbl_pt, abs_lbl)
