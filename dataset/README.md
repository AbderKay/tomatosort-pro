# 📦 Dataset — Cherry Tomatoes (Data Card)

The model is trained on the **Cherry Tomatoes** dataset, annotated in YOLOv8 format.

🔗 **Full dataset (1,000 images):** https://universe.roboflow.com/toumi-amina/cherry-tomatoes-p2lng-tamr2
📄 **License:** CC BY 4.0

> The full image set is **not** committed to git (standard ML practice). A few sample
> images live in `samples/` so you can see what the data looks like; download the full
> set from the Roboflow link above, or export it and unzip into this folder.

## Summary

| | |
|---|---|
| **Task** | Object detection (tomato vs. foreign object) |
| **Classes** | `0: tomato` · `1: foreign_object` |
| **Total images** | 1,000 |
| **Split** | 734 train · 204 valid · 104 test |
| **Format** | YOLOv8 (images + `.txt` labels) |
| **Annotation source** | Roboflow |

## Expected layout (after download)

```
dataset/
├── data.yaml
├── train/ (images/ + labels/)
├── valid/ (images/ + labels/)
└── test/  (images/ + labels/)
```
