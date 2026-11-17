"""Webcam capture with MediaPipe Tasks hand detection (Plan B, story 02)."""

from pathlib import Path

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks.python.core.base_options import BaseOptions
from mediapipe.tasks.python.vision import HandLandmarker, HandLandmarkerOptions
from mediapipe.tasks.python.vision.core.vision_task_running_mode import (
    VisionTaskRunningMode,
)

ROOT = Path(__file__).resolve().parent.parent.parent
HAND_TASK = ROOT / "models" / "hand_landmarker.task"
IMAGE_MODE = VisionTaskRunningMode.IMAGE
VIDEO_MODE = VisionTaskRunningMode.VIDEO
GAMMA = 0.5


class Capture:
    """Capture webcam frames and detect hand landmarks.

    Pose is dropped (story 02 spike): the anonymized faces and dark
    clothing keep pose detection near 55 percent, while hands reach 90
    percent with a gamma brightening pass.
    """

    def __init__(self, camera=True, video=False):
        self.camera = cv2.VideoCapture(0) if camera else None
        mode = VIDEO_MODE if video else IMAGE_MODE
        self.hands = HandLandmarker.create_from_options(
            HandLandmarkerOptions(num_hands=2, **self._options(HAND_TASK, mode))
        )

    def _options(self, path, mode):
        """Build the landmarker options for one local .task model.

        Args:
            path: Path to the MediaPipe .task model file.
            mode: Running mode of the landmarker (image or video).
        """
        options = BaseOptions(model_asset_path=str(path))
        return {"base_options": options, "running_mode": mode}

    def brighten(self, frame):
        """Apply the gamma brightening pass from the story 02 spike.

        Args:
            frame: BGR image; dataset images are dark (mean 16-38/255).

        Returns:
            Brightened BGR image of the same shape.
        """
        lut = ((np.arange(256) / 255) ** GAMMA * 255).astype(np.uint8)
        return cv2.LUT(frame, lut)

    def frame(self):
        """Grab one BGR frame from the webcam.

        Returns:
            Tuple (ok, frame); ok is False when the camera is unavailable
            or disabled (camera=False).
        """
        if self.camera is None:
            return False, None
        return self.camera.read()

    def detect(self, frame):
        """Detect hand landmarks in one BGR frame.

        Args:
            frame: BGR image from the webcam or from disk.

        Returns:
            Array (2, 21, 3) of hand points; zeros for a missing hand.
        """
        rgb = cv2.cvtColor(self.brighten(frame), cv2.COLOR_BGR2RGB)
        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        result = self.hands.detect(image)
        hands = np.zeros((2, 21, 3), dtype=np.float32)
        for index, hand in enumerate(result.hand_landmarks[:2]):
            hands[index] = self._points(hand)
        return hands

    def detect_video(self, frame, timestamp_ms):
        """Detect hand landmarks in one frame of a video stream.

        Args:
            frame: BGR image from a video.
            timestamp_ms: Monotonic millisecond timestamp of the frame.

        Returns:
            Array (2, 21, 3) of hand points; zeros for a missing hand.
        """
        rgb = cv2.cvtColor(self.brighten(frame), cv2.COLOR_BGR2RGB)
        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        result = self.hands.detect_for_video(image, timestamp_ms)
        hands = np.zeros((2, 21, 3), dtype=np.float32)
        for index, hand in enumerate(result.hand_landmarks[:2]):
            hands[index] = self._points(hand)
        return hands

    def _points(self, landmarks):
        """Convert a MediaPipe landmark list to a (N, 3) float array."""
        return np.array([[p.x, p.y, p.z] for p in landmarks], dtype=np.float32)

    def close(self):
        """Release the camera and the landmarker session."""
        if self.camera is not None:
            self.camera.release()
        self.hands.close()
