# 🚀 Pushing TomatoSort Pro to GitHub

Follow these steps once to publish this repository.

## 1. Drop in your original files
- Put your PDF report in `docs/` and rename it to **`technical-report.pdf`** (then delete `docs/PLACE_REPORT_HERE.txt`).
- Put your slides in `docs/` and rename them to **`presentation.pptx`** (then delete `docs/PLACE_SLIDES_HERE.txt`).
- Unzip your source code (`tomato_project`, `project`) and move each part into the matching folder (`vision/`, `backend/`, `frontend/`, etc.).
- Put your dataset (or a small sample + a data card) in `dataset/`. **Do not commit large image archives** — they're already ignored by `.gitignore`.

## 2. Create the repo on GitHub
Go to https://github.com/new and create an **empty** repository named `tomatosort-pro` (no README, no .gitignore — this project already has them).

## 3. Initialize and push
From inside this folder:

```bash
git init
git add .
git commit -m "Initial commit: TomatoSort Pro — intelligent tomato sorting system"
git branch -M main
git remote add origin https://github.com/<your-username>/tomatosort-pro.git
git push -u origin main
```

## 4. (Optional) Handle big files properly
Model weights and datasets don't belong in normal git. Two good options:

**Git LFS** — for weights you still want in the repo:
```bash
git lfs install
git lfs track "*.pt" "*.onnx" "*.engine"
git add .gitattributes
```

**GitHub Releases** — attach weights/datasets as downloadable assets on a tagged release instead of committing them.

## 5. Polish the repo page
- Add a short **description** and **topics** (`computer-vision`, `yolo`, `industry-4-0`, `mlops`, `fastapi`, `kafka`) on the repo's main page.
- Add a **screenshot or demo GIF** to `docs/assets/` and reference it near the top of `README.md` for maximum appeal.
- Pin the repo to your profile.

Done! 🍅
