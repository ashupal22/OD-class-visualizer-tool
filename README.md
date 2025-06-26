# 🧠 OD-class-visualizer-tool

A comprehensive visual analysis tool for medical image object detection. This tool processes `.jpg` medical images using a pretrained ONNX model, generates class-wise histograms, enables interactive frame-wise visualization, and produces high-quality videos for analysis and reporting.
---

## 🚀 Features

- **🔧 Data Preparation**
  - Runs ONNX-based object detection on raw `.jpg` images.
  - Crops detected regions and saves annotated images.
  - Computes class confidence histograms for each frame.
  - Saves processed data in structured formats.

- **🖼️ Interactive Visualization**
  - Tkinter-based GUI to navigate and inspect image frames.
  - View detection overlays on cropped images.
  - Compare class-wise histograms for the current and previous 4 frames.
  - Select/deselect specific classes for focused analysis.
  - Frame navigation via buttons or keyboard shortcuts.

- **🎬 Video Generation**
  - Generate `.mp4` videos summarizing detection + histogram insights.
  - Filter by class and frame range.
  - Choose output filenames and frame rate.

---

## 📁 Project Structure

OD-class-visualizer-tool/
├── cerebro_v6.0.1_od_model.onnx # Pretrained ONNX model
├── recra/ # Input folder for .jpg images
│ ├── image_001.jpg
│ └── ...
├── main_runner.py # Entry point for the tool
├── data_preparation_tool.py # Preprocessing + histogram generation
├── interactive_visualization_tool.py # GUI for interactive exploration
├── video_generator.py # Creates videos from detection results
├── visualization_data/ # Stores all processed output
│ ├── cropped_images/ # Detected images with overlays
│ ├── class_mapping.json
│ ├── frame_info.json
│ ├── frame_list.json
│ ├── histogram_data.json
│ └── histogram_data.npz
└── videos/ # Exported .mp4 analysis videos

yaml
Copy
Edit

---

## 📦 Installation

### ✅ Requirements

- Python 3.7+
- pip

###▶️ How to Run the Tool
#####1. Prepare Your Data
Place all your .jpg medical images inside the recra/ folder:
recra/
├── image_001.jpg
├── image_002.jpg
└── scan_003.jpg

#####3. Add the Model
Ensure cerebro_v6.0.1_od_model.onnx is present in the project root directory.

#####4. Run the Tool
python3 main_runner.py

5. Choose from the Main Menu
============================================================
             MEDICAL IMAGE HISTOGRAM ANALYSIS TOOL
============================================================
1. Prepare Data (Process images and generate data files)
2. Open Visualization Tool (Browse and analyze processed data)
3. Check System Requirements
4. Exit
------------------------------------------------------------
Enter your choice (1-4):
