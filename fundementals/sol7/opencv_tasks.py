import os
os.environ["QT_QPA_PLATFORM"] = "xcb"
import cv2
import numpy as np
from datetime import datetime
from pathlib import Path
import itertools


# 33 ms delay keeps the requirement and gives ~30 FPS responsiveness
KEY_WAIT_MS = 33

# Key codes for Z/X/C (case-insensitive)
CAPTURE_KEYS = {ord("z"), ord("Z")}
RECORD_START_KEYS = {ord("x"), ord("X")}
RECORD_STOP_KEYS = {ord("c"), ord("C")}
ESC_KEY = 27


def timestamped_filename(prefix: str, suffix: str) -> Path:
    """Build a timestamped filename inside sol7."""
    stamp = datetime.now().strftime("%Y%m%d_%H-%M-%S")
    return Path(__file__).parent / f"{prefix}_{stamp}.{suffix}"


def ensure_placeholder_images(image_dir: Path) -> None:
    """Create a couple of simple placeholder images if none are present."""
    if any(image_dir.glob("*")):
        return

    image_dir.mkdir(parents=True, exist_ok=True)
    colors = [
        (255, 204, 128),
        (204, 255, 153),
        (153, 204, 255),
    ]

    for idx, (b, g, r) in enumerate(colors, start=1):
        canvas = np.full((480, 640, 3), (b, g, r), dtype=np.uint8)
        cv2.putText(
            canvas,
            f"Sample Image {idx}",
            (80, 240),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            (50, 50, 50),
            3,
            cv2.LINE_AA,
        )
        image_path = image_dir / f"sample_{idx:02d}.png"
        cv2.imwrite(str(image_path), canvas)


def display_images(image_paths: list[Path]) -> bool:
    """Show images one by one. Return False if ESC is pressed to abort."""
    for image_path in image_paths:
        image = cv2.imread(str(image_path))
        if image is None:
            print(f"[WARN] {image_path.name} could not be loaded.")
            continue

        window_title = f"Image Preview - {image_path.name}"
        window_open = False
        try:
            cv2.imshow(window_title, image)
            window_open = True
        except cv2.error as exc:
            print(f"[ERROR] Failed to display {image_path.name}: {exc}")
            return False
        elapsed_steps = 0
        last_key = -1
        while True:
            key = cv2.waitKey(KEY_WAIT_MS)
            if key != -1:
                last_key = key & 0xFF
                break
            elapsed_steps += 1
            if elapsed_steps * KEY_WAIT_MS >= 5000:
                break
        if window_open:
            try:
                cv2.destroyWindow(window_title)
            except cv2.error as exc:
                print(f"[WARN] Failed to close window {window_title}: {exc}")
        if last_key == ESC_KEY:
            print("[INFO] ESC pressed during image preview. Exiting.")
            return False
    return True

def iterate_image_paths(image_dir: Path) -> list[Path]:
    """Collect image paths across common formats."""
    patterns = ("*.png", "*.jpg", "*.jpeg", "*.bmp", "*.tif", "*.tiff")
    files = itertools.chain.from_iterable(image_dir.glob(pattern) for pattern in patterns)
    return sorted(files)


def control_video_playback(video_path: Path, captures_dir: Path, recordings_dir: Path) -> None:
    captures_dir.mkdir(parents=True, exist_ok=True)
    recordings_dir.mkdir(parents=True, exist_ok=True)

    capture = cv2.VideoCapture(str(video_path))
    if not capture.isOpened():
        raise FileNotFoundError(f"Cannot open video: {video_path}")

    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = capture.get(cv2.CAP_PROP_FPS) or (1000 / KEY_WAIT_MS)

    writer = None
    window_title = f"Video Playback - {video_path.name}"
    print("[INFO] Press ESC to exit, Z to capture image, X to start recording, C to stop recording.")

    while True:
        ret, frame = capture.read()
        if not ret:
            print("[INFO] End of video stream.")
            break

        try:
            cv2.imshow(window_title, frame)
        except cv2.error as exc:
            print(f"[ERROR] Failed to display video frame: {exc}")
            break

        if writer is not None:
            writer.write(frame)

        key = cv2.waitKey(KEY_WAIT_MS)
        if key == -1:
            continue

        if key == ESC_KEY:
            print("[INFO] ESC pressed. Exiting.")
            break
        if key in CAPTURE_KEYS:
            image_file = timestamped_filename("capture", "png")
            image_file = captures_dir / image_file.name
            cv2.imwrite(str(image_file), frame)
            print(f"[INFO] Captured frame -> {image_file.name}")
        elif key in RECORD_START_KEYS:
            if writer is not None:
                print("[WARN] Recording already in progress.")
                continue
            writer_path = timestamped_filename("recording", "mp4")
            writer_path = recordings_dir / writer_path.name
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            writer = cv2.VideoWriter(str(writer_path), fourcc, fps, (width, height))
            if not writer.isOpened():
                writer = None
                print("[ERROR] Failed to start video writer.")
            else:
                print(f"[INFO] Recording started -> {writer_path.name}")
        elif key in RECORD_STOP_KEYS:
            if writer is None:
                print("[WARN] Recording has not started.")
                continue
            writer.release()
            writer = None
            print("[INFO] Recording stopped.")

    if writer is not None:
        writer.release()
        print("[INFO] Recording stopped (EOF).")

    capture.release()
    try:
        cv2.destroyWindow(window_title)
    except cv2.error:
        pass


def main() -> None:
    base_dir = Path(__file__).parent
    image_dir = base_dir / "images"
    captures_dir = base_dir / "captures"
    recordings_dir = base_dir / "recordings"
    video_path = base_dir / "pirate.mp4"

    images = list(iterate_image_paths(image_dir))
    if images:
        if not display_images(images):
            cv2.destroyAllWindows()
            return
    else:
        print(f"[WARN] No images found in {image_dir}")

    if video_path.exists():
        control_video_playback(video_path, captures_dir, recordings_dir)
    else:
        print(f"[ERROR] Video file not found at {video_path}")

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
