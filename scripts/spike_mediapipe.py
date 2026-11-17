"""Spike: MediaPipe hand detection rate over Espejel dataset images.

Story 02: registers the hand detection percentage that decided the
landmark pipeline (Plan B: hands only, 42 points). Gamma is applied
inside Capture.detect, so these numbers are the shipped behavior.
"""

import glob

import cv2

from g11.capture import Capture

COUNT = 20


class Spike:
    """Measure the MediaPipe hand detection rate over dataset images."""

    def __init__(self, root):
        self.root = root
        self.capture = Capture(camera=False)

    def sample(self, count=COUNT):
        """List the first image of each signer over the first classes."""
        paths = []
        for signer in sorted(glob.glob(f"{self.root}/0*/0*")):
            images = sorted(glob.glob(f"{signer}/*.jpg"))
            if images:
                paths.append(images[0])
            if len(paths) >= count:
                break
        return paths

    def run(self, count=COUNT):
        """Detect hands on the sample; return the hit count.

        Args:
            count: Number of images to probe.

        Returns:
            Number of images with at least one detected hand.
        """
        hands = 0
        for path in self.sample(count):
            hands += self.capture.detect(cv2.imread(path)).sum() > 0
        return hands


def main():
    """Run the spike over the sample and print the detection rate."""
    spike = Spike("dataset/espejel")
    print(f"hands detected: {spike.run()}/{COUNT}")


if __name__ == "__main__":
    main()
