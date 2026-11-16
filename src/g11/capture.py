"""Webcam capture with MediaPipe Tasks pose and hand detection."""

from pathlib import Path

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks.python.core.base_options import BaseOptions
from mediapipe.tasks.python.vision import (
    HandLandmarker,
    HandLandmarkerOptions,
    PoseLandmarker,
    PoseLandmarkerOptions,
)
from mediapipe.tasks.python.vision.core.vision_task_running_mode import (
    VisionTaskRunningMode,
)

ROOT = Path(__file__).resolve().parent.parent.parent
POSE_TASK = ROOT / "models" / "pose_landmarker.task"
HAND_TASK = ROOT / "models" / "hand_landmarker.task"
IMAGE_MODE = VisionTaskRunningMode.IMAGE


class Capture:
    """Capture webcam frames and detect pose and hand landmarks."""

    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        self.pose = PoseLandmarker.create_from_options(
            PoseLandmarkerOptions(**self._options(POSE_TASK))
        )
        self.hands = HandLandmarker.create_from_options(
            HandLandmarkerOptions(num_hands=2, **self._options(HAND_TASK))
        )

    def _options(self, path):
        """Build the landmarker options for one local .task model.

        Args:
            path: Path to the MediaPipe .task model file.
        """
        options = BaseOptions(model_asset_path=str(path))
        return {"base_options": options, "running_mode": IMAGE_MODE}

    def _points(self, landmarks):
        """Convert a MediaPipe landmark list to a (N, 3) float array."""
        return np.array([[p.x, p.y, p.z] for p in landmarks], dtype=np.float32)

    def frame(self):
        """Grab one BGR frame from the webcam.

        Returns:
            Tuple (ok, frame); ok is False when the camera is unavailable.
        """
        return self.camera.read()

    def detect(self, frame):
        """Detect pose and hand landmarks in one BGR frame.

        Args:
            frame: BGR image from the webcam.

        Returns:
            Tuple (pose, hands) as float arrays: pose (33, 3) and hands
            (2, 21, 3); zeros when the person or a hand is not detected.
        """
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        return self._pose(image), self._hands(image)

    def _pose(self, image):
        """Return the (33, 3) pose points, or zeros when not detected."""
        result = self.pose.detect(image)
        if not result.pose_landmarks:
            return np.zeros((33, 3), dtype=np.float32)
        return self._points(result.pose_landmarks[0])

    def _hands(self, image):
        """Return the (2, 21, 3) hand points; zeros for a missing hand."""
        result = self.hands.detect(image)
        hands = np.zeros((2, 21, 3), dtype=np.float32)
        for index, hand in enumerate(result.hand_landmarks[:2]):
            hands[index] = self._points(hand)
        return hands

    def close(self):
        """Release the camera and the landmarker sessions."""
        self.camera.release()
