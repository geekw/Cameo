import cv2
import numpy
import os

class CaptureManager(object):

	def __init__(self, capture, previewWindowManager = None,
			shouldMirrorPreview = False):

		self.previewWindowManager = previewWindowManager
		self.shouldMirrorPreview = shouldMirrorPreview

		self._capture = _capture
		self._channel = 0
		self._enteredFrame = False
		self._frame = None
		self._imageFilename = None
		self._videoFilename = None
		self._videoEncoding = None 
		self._videoWriter = None
		
		self._startTime = None
		self._framesElapsed = long(0)
		self._fpsEstimate = None

	@property
	def channel(self, value):
		return self._channel

	@channel.setter
	def channel(self, value):
		if self._channel != value:
			self._channel = value
			self._frame = None

	@property
	def frame(self):
		if self._enteredFrame and self._frame is None:
			_, self._frame = self._capture.retrieve(channel = self._channel)
		return self._frame

	@property
	def isWritingImage(self):
		return self._imageFilename is not None

	@property
	def isWritingVideo(self):
		return self._imageFilename is not None
