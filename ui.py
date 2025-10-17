import cv2
import numpy as np


class UI:
    def __init__(self, window_name="Optical_Flow"):
        self.window_name = window_name

        self.pyr_scale = 0.5
        self.levels = 5
        self.winsize = 13
        self.iterations = 10
        self.poly_sigma = 1.1
        self.poly_n = 5
        self.gaussian = 1
        self.slow_motion = 1  # 0.01 to 1.0
        self.optical_mode = 0
        self.feedback = 0

        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.createTrackbar(
            "pyr_scale", self.window_name, int(self.pyr_scale * 100), 99, self._nothing
        )
        cv2.createTrackbar(
            "levels", self.window_name, int(self.levels), 10, self._nothing
        )
        cv2.createTrackbar(
            "winsize", self.window_name, int(self.winsize), 50, self._nothing
        )
        cv2.createTrackbar(
            "iterations", self.window_name, int(self.iterations), 20, self._nothing
        )
        cv2.createTrackbar(
            "poly_sigma", self.window_name, int(self.poly_sigma * 10), 30, self._nothing
        )
        cv2.createTrackbar(
            "poly_n", self.window_name, int(self.poly_n), 20, self._nothing
        )
        cv2.createTrackbar(
            "gaussian", self.window_name, int(self.gaussian), 1, self._nothing
        )
        cv2.createTrackbar(
            "slow_motion",
            self.window_name,
            int(self.slow_motion * 100),
            100,
            self._nothing,
        )
        cv2.createTrackbar(
            "optical_mode",
            self.window_name,
            int(self.optical_mode),
            2,
            self._nothing,
        )
        cv2.createTrackbar(
            "feedback",
            self.window_name,
            int(self.feedback),
            1,
            self._nothing,
        )

    def _nothing(self, x):
        """Callback function for trackbars (does nothing)"""
        pass

    def update(self):
        """Update current values from all trackbars"""
        self.pyr_scale = cv2.getTrackbarPos("pyr_scale", self.window_name) / 100.0
        self.levels = max(1, cv2.getTrackbarPos("levels", self.window_name))
        self.winsize = max(1, cv2.getTrackbarPos("winsize", self.window_name))
        self.iterations = cv2.getTrackbarPos("iterations", self.window_name)
        self.poly_n = cv2.getTrackbarPos("poly_n", self.window_name)
        self.poly_sigma = cv2.getTrackbarPos("poly_sigma", self.window_name) / 10.0
        self.gaussian = int(cv2.getTrackbarPos("gaussian", self.window_name))
        self.slow_motion = max(
            0.01, cv2.getTrackbarPos("slow_motion", self.window_name) / 100
        )
        self.optical_mode = int(cv2.getTrackbarPos("optical_mode", self.window_name))
        self.feedback = int(cv2.getTrackbarPos("feedback", self.window_name))

    def show(self, *images):
        """Display the given images in the window"""
        cv2.imshow(self.window_name, np.hstack(images))

    def cleanup(self):
        """Clean up OpenCV windows"""
        cv2.destroyAllWindows()
