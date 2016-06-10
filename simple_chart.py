# coding=utf-8
# indent-tabs-mode: 1
# tab-width: 4

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPainter, QPen, QFontMetrics, QFont, QColor



class ChartPoint(QPoint):
	"""docstring for ChartPoint"""

	def __init__(self, abscissa, ordinate, chart, update_pos=True):
		"""Create a new point on the chart. If update_pos is set to False, you
		need to call by yourself the update_position method"""
		super(ChartPoint, self).__init__()
		self.abscissa = abscissa
		self.ordinate = ordinate
		self.__chart = chart

		if update_pos:
			self.updatePosition()

	def updatePosition(self):
		x = self.abscissa / self.__chart.abs_max_value
		x *= (self.__chart.max_abs_pos.x() - self.__chart.zero_pos.x())
		self.setX(int(x + self.__chart.zero_pos.x()))

		y = self.ordinate / self.__chart.ord_max_value
		y *= (self.__chart.zero_pos.y() - self.__chart.max_ord_pos.y())
		self.setY(int(self.__chart.zero_pos.y() - y))


class SimpleChart(QWidget):

	# TODO : add methods to update every points/lines

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
		self.__points = []

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

	def addPoint(self, abscissa, ordinate, update=True):
		"""Add a point on the chart"""
		# TODO : if the point is above the maximum value of the ordinate or
		# abscissa update the right maximum value and every points position
		self.__points.append(ChartPoint(abscissa, ordinate, self, update))

	def updatePointsPosition(self):
		# NOTE : this will be replaced by a method that update every lines.
		for pt in self.__points:
			pt.updatePosition()

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
		self.__drawPoints(qpainter)
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

		# draw zero label
		zero_lbl = "0"
		width = self.__lbl_ft_metrics.width(zero_lbl)
		lbl_pt = QPoint(self.zero_pos.x() - self.__ORD_LBL_SPACING,
		                self.zero_pos.y() + self.__ORD_LBL_SPACING)
		qpainter.drawText(lbl_pt, zero_lbl)

	def __drawPoints(self, qpainter):
		qpainter.setPen(QColor(Qt.red))

		for pt in self.__points:
			qpainter.drawPoint(pt)
