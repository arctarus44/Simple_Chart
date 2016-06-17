# coding=utf-8
# indent-tabs-mode: 1
# tab-width: 4

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPainter, QPen, QFontMetrics, QFont

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
