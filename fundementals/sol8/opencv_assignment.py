#!/usr/bin/env python3
"""
OpenCV assignment script that demonstrates the following topics:

1. Flipping and rotating an image.
2. Resizing, scaling, and cropping (with deep copies).
3. Color conversion and negative image generation.
4. Binarization, edge detection (Sobel/Laplacian/Canny), and blurring on a
   second image.
5. HSV conversion along with separate H/S/V channel visualization.
6. Object highlighting with rectangles, labels, and connector lines.

All outputs attempt to open in GUI windows first. When GUI support is
unavailable, results are written into sol8/outputs instead.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import cv2
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_IMAGE = BASE_DIR.parent / "sol7" / "images" / "sample_image.png"
DEFAULT_BLUR_IMAGE = BASE_DIR / "blur_source.png"
DEFAULT_OUTPUT_DIR = BASE_DIR / "outputs"


class ResultPresenter:
    """Handles showing images and gracefully falls back to saving them."""

    def __init__(self, output_dir: Path, interactive: bool = True) -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.interactive = interactive
        self.gui_available = interactive
        self.counter = 0

    def show(self, title: str, image: np.ndarray, wait: int | None = None) -> None:
        self.counter += 1
        if self.gui_available:
            try:
                cv2.imshow(title, image)
                cv2.waitKey(0 if wait is None else wait)
                cv2.destroyWindow(title)
                return
            except cv2.error as exc:  # GUI might be unavailable (e.g., headless)
                self.gui_available = False
                cv2.destroyAllWindows()
                print(
                    f"[WARN] GUI display failed for '{title}' ({exc}). "
                    "Switching to save-only mode."
                )

        filename = self.output_dir / f"{self.counter:02d}_{self._slug(title)}.png"
        cv2.imwrite(str(filename), image)
        print(f"[SAVE] {title} -> {filename}")

    def cleanup(self) -> None:
        cv2.destroyAllWindows()

    @staticmethod
    def _slug(text: str) -> str:
        return re.sub(r"[^0-9A-Za-z]+", "_", text).strip("_").lower() or "image"


def read_image(path: Path, flag: int = cv2.IMREAD_COLOR) -> np.ndarray:
    image = cv2.imread(str(path), flag)
    if image is None:
        raise FileNotFoundError(f"Unable to read image at {path}")
    return image


def flips_and_rotations(image: np.ndarray, presenter: ResultPresenter) -> None:
    presenter.show("Original image", image)
    presenter.show("Flip vertical", cv2.flip(image, 0))
    presenter.show("Flip horizontal", cv2.flip(image, 1))
    presenter.show("Rotate 90 clockwise", cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE))
    presenter.show("Rotate 180", cv2.rotate(image, cv2.ROTATE_180))


def resizing_scaling_cropping(image: np.ndarray, presenter: ResultPresenter) -> None:
    resized_640x480 = cv2.resize(image, (640, 480), interpolation=cv2.INTER_LINEAR)
    resized_1024x768 = cv2.resize(image, (1024, 768), interpolation=cv2.INTER_LINEAR)
    scaled = cv2.resize(
        image,
        None,
        fx=0.3,
        fy=0.7,
        interpolation=cv2.INTER_AREA,
    )

    h, w = image.shape[:2]
    y_start, y_end = h // 4, h // 4 * 3
    x_start, x_end = w // 4, w // 4 * 3
    cropped = image[y_start:y_end, x_start:x_end].copy()  # Deep copy

    presenter.show("Resize 640x480", resized_640x480)
    presenter.show("Resize 1024x768", resized_1024x768)
    presenter.show("Scale fx=0.3 fy=0.7", scaled)
    presenter.show("Cropped center region", cropped)


def color_and_negative(image: np.ndarray, presenter: ResultPresenter) -> None:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    negative = cv2.bitwise_not(image)
    presenter.show("Color to grayscale", gray)
    presenter.show("Negative / inverted colors", negative)


def binarization_and_edges(image: np.ndarray, presenter: ResultPresenter) -> None:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    sobel_mag = cv2.magnitude(sobel_x, sobel_y)
    sobel_8u = cv2.convertScaleAbs(sobel_mag)

    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    laplacian_8u = cv2.convertScaleAbs(laplacian)

    canny = cv2.Canny(gray, 100, 200)

    presenter.show("Grayscale binary (Otsu)", binary)
    presenter.show("Edges - Sobel magnitude", sobel_8u)
    presenter.show("Edges - Laplacian", laplacian_8u)
    presenter.show("Edges - Canny", canny)


def ensure_blur_image(path: Path) -> np.ndarray:
    """Ensures a second image exists for blur demo and returns it."""
    if path.exists():
        return read_image(path)

    path.parent.mkdir(parents=True, exist_ok=True)
    height, width = 512, 512
    x = np.linspace(0, 255, width, dtype=np.uint8)
    y = np.linspace(255, 0, height, dtype=np.uint8)
    gradient_r = np.tile(x, (height, 1))
    gradient_g = np.tile(y[:, None], (1, width))
    gradient_b = ((gradient_r.astype(np.uint16) + gradient_g.astype(np.uint16)) // 2).astype(
        np.uint8
    )
    gradient_image = cv2.merge([gradient_b, gradient_g, gradient_r])
    cv2.imwrite(str(path), gradient_image)
    print(f"[INFO] Created fallback blur source at {path}")
    return read_image(path)


def blur_demo(image: np.ndarray, presenter: ResultPresenter) -> None:
    average_blur = cv2.blur(image, (9, 9))
    gaussian_blur = cv2.GaussianBlur(image, (15, 15), 0)
    median_blur = cv2.medianBlur(image, 11)

    presenter.show("Blur - Average", average_blur)
    presenter.show("Blur - Gaussian", gaussian_blur)
    presenter.show("Blur - Median", median_blur)


def hsv_channels(image: np.ndarray, presenter: ResultPresenter) -> None:
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h_channel, s_channel, v_channel = cv2.split(hsv)
    presenter.show("HSV - H channel", h_channel)
    presenter.show("HSV - S channel", s_channel)
    presenter.show("HSV - V channel", v_channel)


def annotate_objects(image: np.ndarray, presenter: ResultPresenter) -> None:
    annotated = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        presenter.show("Annotated objects (none found)", annotated)
        return

    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
    height, width = image.shape[:2]

    for idx, cnt in enumerate(contours, start=1):
        x, y, w, h = cv2.boundingRect(cnt)
        if w * h < (width * height) * 0.01:  # Skip extremely small regions
            continue
        top_left = (x, y)
        bottom_right = (x + w, y + h)
        cv2.rectangle(annotated, top_left, bottom_right, (0, 0, 255), 2)

        label = f"Object {idx}"
        text_x = min(x + w + 20, width - 120)
        text_y = max(y - 10, 20)
        text_origin = (text_x, text_y)
        cv2.putText(
            annotated,
            label,
            text_origin,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 255),
            2,
            cv2.LINE_AA,
        )

        box_center = (x + w, y + h // 2)
        cv2.line(annotated, box_center, text_origin, (0, 0, 255), 2)

    presenter.show("Annotated objects", annotated)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Complete OpenCV fundamentals assignment demonstrations."
    )
    parser.add_argument(
        "--image",
        default=str(DEFAULT_IMAGE),
        help=f"Path to the main demonstration image (default: {DEFAULT_IMAGE})",
    )
    parser.add_argument(
        "--blur-image",
        default=str(DEFAULT_BLUR_IMAGE),
        help="Second image for the blur exercise. Generated automatically if missing.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory where fallback images are saved when GUI output is unavailable.",
    )
    parser.add_argument(
        "--no-gui",
        action="store_true",
        help="Skip cv2.imshow entirely and always save results to disk.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    presenter = ResultPresenter(Path(args.output_dir), interactive=not args.no_gui)

    main_image_path = Path(args.image)
    blur_image_path = Path(args.blur_image)

    main_image = read_image(main_image_path)
    flips_and_rotations(main_image, presenter)
    resizing_scaling_cropping(main_image, presenter)
    color_and_negative(main_image, presenter)
    binarization_and_edges(main_image, presenter)

    blur_image = ensure_blur_image(blur_image_path)
    blur_demo(blur_image, presenter)

    hsv_channels(main_image, presenter)
    annotate_objects(main_image, presenter)

    presenter.cleanup()


if __name__ == "__main__":
    main()
