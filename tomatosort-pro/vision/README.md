# 🎥 Vision Module

Two-stage computer-vision pipeline plus color analysis.

- `detection/` — **YOLO** real-time detection & localization (bounding boxes + confidence).
- `classification/` — **CNN** fine grading into Grade A / Grade B / Reject.
- `color_analysis/` — **HSV** ripeness & color evaluation, decoupled from brightness.

> Place trained weights outside git (Git LFS / DVC / GitHub Releases).
