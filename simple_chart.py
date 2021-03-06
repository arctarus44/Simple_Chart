# coding=utf-8
# indent-tabs-mode: 1
# tab-width: 4

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QPoint, QLine, Qt
from PyQt5.QtGui import (QPainter, QPen, QFontMetrics, QFont, QColor,
QPainterPath)

class Line(object):
	"""docstring for Line"""

	def __init__(self, chart, pen):
		self._points = []
		self.pen = pen
		self._chart = chart

	def __iter__(self):
		return self._points.__iter__()

	def __getitem__(self, x):
		return self._points.__getitem__(x)

	def addPoint(self, point):
		self._points.append(point)
		self._points = sorted(self._points, key=lambda pt : pt.abscissa)

	def updatePointsPosition(self):
		for pt in self._points:
			pt.updatePosition()

class ChartPoint(QPoint):
	"""docstring for ChartPoint"""

	def __init__(self, abscissa, ordinate, chart):
		"""Create a new point on the chart."""
		super(ChartPoint, self).__init__()
		self.abscissa = abscissa
		self.ordinate = ordinate
		self.__chart = chart
		self.updatePosition()

	def updatePosition(self):
		x = self.abscissa / self.__chart.abs_max_value
		x *= (self.__chart.max_abs_pos.x() - self.__chart.zero_pos.x())
		self.setX(int(x + self.__chart.zero_pos.x()))

		y = self.ordinate / self.__chart.ord_max_value
		y *= (self.__chart.zero_pos.y() - self.__chart.max_ord_pos.y())
		self.setY(int(self.__chart.zero_pos.y() - y))

class ChartPointPen(ChartPoint):
	"""docstring for ChartPointPen"""
	def __init__(self, abscissa, ordinate, chart, pen):
		super(ChartPointPen, self).__init__(abscissa, ordinate, chart)
		self._pen = pen


class LinesHandler:
	"""docstring for LineHandler"""

	def addLine(self, lineKey, pen):
		# TODO : add decorator to initialize _data
		if self._data is None:
			self._data = {}
		self._data[lineKey] = Line(self, pen)

	def addPoint(self, lineKey, abscissa, ordinate):
		# TODO : add decorator to initialize _data
		if self._data is None:
			self._data = {}

		self._data[lineKey].addPoint(ChartPoint(abscissa, ordinate, self))

		if self._pt_max_abs < abscissa:
			self._updateMaxAbscissa(abscissa)
		elif self._pt_max_ord < ordinate:
			self._updateMaxOrdinate(ordinate)

	def _drawData(self, qpainter):
		# TODO : add decorator to initialize _data
		if self._data is None:
			self._data = {}
		for k in self._data.keys():
			line = self._data[k]
			qpainter.setPen(line.pen)
			prev_pt = line[0]

			for pt in line[1:]:
				qpainter.drawLine(prev_pt, pt)
				prev_pt = pt

	def _updateDataPosition(self):
		# TODO : add decorator to initialize _data
		if self._data is None:
			self._data = {}
		for k in self._data.keys():
			line = self._data[k]
			line.updatePointsPosition()

class AreaHandler(LinesHandler):
	"""docstring for LinesAreaHandler"""

	def _drawArea(self, qpainter, lines, pen):
		color = QColor(*pen.color().getRgb())
		color.setAlpha(40)
		qpainter.setPen(color)

		for line in lines:
			# right equation ya = m * xa + p
			p1 = line.p1()
			p2 = line.p2()
			m = line.dy() / line.dx()
			p = p2.y() - p2.x() * m

			for x in range(p1.x(), p2.x()):
				y = m * x + p
				qpainter.drawLine(x, y, x, self.zero_pos.y())


	def _drawData(self, qpainter):
		# TODO : add decorator to initialize _data
		if self._data is None:
			self._data = {}

		for k in self._data.keys():
			drawedLine = []
			chartLine = self._data[k]
			qpainter.setPen(chartLine.pen)
			prev_pt = chartLine[0]

			for pt in chartLine[1:]:
				line = QLine(prev_pt, pt)
				drawedLine.append(line)
				qpainter.drawLine(line)
				prev_pt = pt

			self._drawArea(qpainter, drawedLine, chartLine.pen)


class DotsHandler:
	"""docstring for DotsHandler"""

	def addPoint(self, abscissa, ordinate, pen):
		# TODO : add decorator to initialize _data
		if self._data is None:
			self._data = []
		self._data.append(ChartPointPen(abscissa, ordinate, self, pen))

		if self._pt_max_abs < abscissa:
			self._updateMaxAbscissa(abscissa)
		elif self._pt_max_ord < ordinate:
			self._updateMaxOrdinate(ordinate)

	def _drawData(self, qpainter):
		# TODO : add decorator to initialize _data
		if self._data is None:
			self._data = []
		for pt in self._data:
			qpainter.setPen(pt._pen)
			qpainter.drawPoint(pt)

	def _updateDataPosition(self):
		# TODO : add decorator to initialize _data
		if self._data is None:
			self._data = []
		for pt in self._data:
			pt.updatePosition()


class BaseChart(QWidget):

	MARGIN = 60
	ABS_GUIDE_LEN = 15
	ZERO = "0"
	__PERCENT = "%"
	__MAX_PERCENT = 100
	__ORD_LBL_SPACING = 15
	__ABS_LBL_SPACING = 10

	def __init__(self):
		super(BaseChart, self).__init__()
		self.ord_max_value = 100
		self.abs_max_value = 100
		self.unit_abs = None
		self.unit_ord = None
		self._pt_max_abs = 0
		self._pt_max_ord = 0
		self._data = None

		# Graphical properties
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
		self._updateDataPosition()

	def paintEvent(self, event):
		qpainter = QPainter()
		qpainter.begin(self)
		self._drawBackground(qpainter)
		self._drawData(qpainter)
		qpainter.end()

	def __drawLabels(self, qpainter):
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
		zero_lbl = self.ZERO
		width = self.__lbl_ft_metrics.width(zero_lbl)
		lbl_pt = QPoint(self.zero_pos.x() - self.__ORD_LBL_SPACING,
		                self.zero_pos.y() + self.__ORD_LBL_SPACING)
		qpainter.drawText(lbl_pt, zero_lbl)

	def __drawAxis(self, qpainter):
		qpainter.setPen(self.__axis_pen)
		qpainter.drawLine(self.zero_pos, self.max_ord_pos)
		qpainter.drawLine(self.zero_pos, self.max_abs_pos)

	def __drawGuides(self, qpainter):
		qpainter.setPen(self.__guides_pen)
		ord_guide = QPoint(self.max_abs_pos.x(), self.max_ord_pos.y())
		qpainter.drawLine(self.max_ord_pos, ord_guide)
		point = QPoint(self.max_abs_pos.x(),
		               self.max_abs_pos.y() - self.ABS_GUIDE_LEN)
		qpainter.drawLine(self.max_abs_pos, point)

	def _drawBackground(self, qpainter):
		# Set background Color
		pal = self.palette()
		pal.setColor(self.backgroundRole(), Qt.white)
		self.setPalette(pal)

		# DEBUG
		# print("Ord  ("+ str(self.max_ord_pos.x()) + ',' + str(self.max_ord_pos.y())+ ")")
		# print("Abs  ("+ str(self.max_abs_pos.x()) + ',' + str(self.max_abs_pos.y())+ ")")
		# print("Zero ("+ str(self.zero_pos.x()) + ',' + str(self.zero_pos.y())+ ")")
		# END DEBUG

		self.__drawAxis(qpainter)
		self.__drawGuides(qpainter)
		self.__drawLabels(qpainter)

	def _updateMaxAbscissa(self, abscissa):
		self._updateMaxOrdAbs(abscissa, None)

	def _updateMaxOrdinate(self, ordinate):
		self._updateMaxOrdAbs(None, ordinate)

	def _updateMaxOrdAbs(self, abscissa, ordinate):
		if abscissa is not None:
			value = abscissa
		else:
			value = ordinate

		maximum = None
		range_end = 100
		while maximum == None:
			if value == range_end:
				maximum = value
			if value < range_end:
				tmp = range_end / 10
				maximum = int(int(value / tmp) * tmp + tmp)

			range_end *= 10

		if abscissa is not None:
			self.abs_max_value = maximum
			self._updateDataPosition()
		else:
			self.ord_max_value = maximum
			self._updateDataPosition()
