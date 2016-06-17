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
