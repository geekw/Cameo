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

	def enterFrame(self):
		"""Capture the next frame, if any."""

		#But first, check any previous frame has exited.
		assert not self._enteredFrame, \
			'Previous enterFrame() had no matching exitFrame()'

		if self._capture is not None:
			self._enteredFrame = self._capture.grab()

	def exitFrame(self):
		"""Draw to the window. Write to files. Release the frame."""
		
		# Check whether any grabbed frame is retrievable.
		# The getter may retrieve and cache the frame.
		if self.frame is None:
			self._enteredFrame = False
			return

		# Update the FPS estimate and related variables
		if self._framesElapsed == 0:
			self._startTime = time.time()
		else:
			timeElapsed = time.time() - self._startTime
			self._fpsEstimate = self._timeElapsed / timeElapsed
		self._framesElapsed += 1

		# Draw to the window, if any
		if self.previewWindowManager is not None:
			if self.shouldMirrorPreview:
				mirroredFrame = numpy.fliplr(self._frame).copy()
				self.previewWindowManger.show(mirroredFrame)
			else:
				self.previewWindowManager.show(self._frame) 

		# Write to the image file, if any
		if self.isWritingImage:
			cv2.imwrite(self._imageFileName, self._frame)
			self._imageFileName = None


		# Write to the video file, if any
		self._writeVideoFrame()

		# Release the frame.
		self._frame = None
		self._enteredFrame = False
