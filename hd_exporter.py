#!/usr/bin/env python3
"""
HD Image Exporter for Medical Image Analysis
Exports combined histogram plots and detection images in HD resolution (1920x1080)
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import cv2
import numpy as np
import json
import os
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.patches as mpatches
from tqdm import tqdm

class HDImageExporter:
    def __init__(self):
        # Data variables
        self.histogram_data = {}
        self.frame_info = {}
        self.class_mapping = {}
        self.frame_list = []
        
        # Load data
        self.load_data()
    
    def load_data(self):
        """Load all data files with intelligent format selection."""
        data_folder = "visualization_data"
        
        try:
            # Try to load histogram data in order of preference
            histogram_loaded = False
            
            # 1. Try compressed NumPy format first (fastest)
            histogram_npz_file = os.path.join(data_folder, "histogram_data.npz")
            if os.path.exists(histogram_npz_file):
                print("📦 Loading compressed NumPy histogram data...")
                histogram_npz = np.load(histogram_npz_file)
                self.histogram_data = {key: histogram_npz[key].tolist() for key in histogram_npz.files}
                histogram_loaded = True
                print(f"✅ Loaded {len(self.histogram_data)} frame histograms from NPZ")
            
            # 2. Try sparse JSON format
            elif os.path.exists(os.path.join(data_folder, "histogram_data_sparse.json")):
                print("🗜️ Loading sparse histogram data...")
                with open(os.path.join(data_folder, "histogram_data_sparse.json"), 'r') as f:
                    sparse_data = json.load(f)
                
                # Reconstruct full histogram from sparse format
                self.histogram_data = {}
                for frame_name, sparse_hist in sparse_data.items():
                    shape = sparse_hist['shape']
                    indices = sparse_hist['indices']
                    values = sparse_hist['values']
                    
                    # Reconstruct full histogram
                    full_hist = np.zeros(shape)
                    if len(values) > 0:
                        full_hist[indices[0], indices[1]] = values
                    
                    self.histogram_data[frame_name] = full_hist.tolist()
                
                histogram_loaded = True
                print(f"✅ Loaded {len(self.histogram_data)} frame histograms from sparse JSON")
            
            # 3. Fallback to compact JSON
            elif os.path.exists(os.path.join(data_folder, "histogram_data.json")):
                print("📄 Loading compact JSON histogram data...")
                with open(os.path.join(data_folder, "histogram_data.json"), 'r') as f:
                    self.histogram_data = json.load(f)
                histogram_loaded = True
                print(f"✅ Loaded {len(self.histogram_data)} frame histograms from JSON")
            
            if not histogram_loaded:
                raise FileNotFoundError("No histogram data file found")
            
            # Load frame info
            with open(os.path.join(data_folder, "frame_info.json"), 'r') as f:
                self.frame_info = json.load(f)
            
            # Load class mapping
            with open(os.path.join(data_folder, "class_mapping.json"), 'r') as f:
                self.class_mapping = json.load(f)
            
            # Load frame list
            with open(os.path.join(data_folder, "frame_list.json"), 'r') as f:
                self.frame_list = json.load(f)
                
            print(f"✅ Successfully loaded {len(self.frame_list)} frames!")
            
        except FileNotFoundError as e:
            print(f"❌ Error: Data files not found: {e}")
            print("Please run the data preparation script first.")
            return False
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
        
        return True
    
    def create_histogram_plot_hd(self, current_frame_index, save_mode=True):
        """Create HD histogram plot for export."""
        current_frame_name = self.frame_list[current_frame_index]
        
        # Create high-resolution figure for HD export
        fig = plt.figure(figsize=(12, 8), dpi=120)
        fig.patch.set_facecolor('white')
        
        # Get all class names from mapping (sorted by index)
        all_class_indices = sorted([int(k) for k in self.class_mapping.keys()])
        all_class_names = [self.class_mapping[str(i)] for i in all_class_indices]
        
        # Score ranges
        score_ranges = ["90-100%", "80-90%", "70-80%", "60-70%", "50-60%", 
                       "40-50%", "30-40%", "20-30%", "10-20%", "0-10%"]
        
        # Frame labels (0=current, -1=previous, etc.)
        frame_labels = ["0", "-1", "-2", "-3", "-4"]
        
        # Get histogram data for current + last 4 frames (total 5 frames)
        hist_frames = []
        frame_names = []
        
        # Collect 5 frames (current + 4 previous)
        for i in range(current_frame_index, max(-1, current_frame_index - 5), -1):
            if i >= 0 and i < len(self.frame_list):
                frame_name = self.frame_list[i]
                if frame_name in self.histogram_data:
                    hist_data = np.array(self.histogram_data[frame_name])
                    hist_frames.append(hist_data)
                    frame_names.append(frame_name)
        
        # Pad with empty frames if needed
        while len(hist_frames) < 5:
            hist_frames.append(np.zeros((100, len(all_class_indices))))
            frame_names.append("Empty")
        
        # Process histogram data for all classes and all frames
        all_binned_data = []
        for hist_data in hist_frames:
            # Ensure histogram has enough classes
            if hist_data.shape[1] < max(all_class_indices) + 1:
                padded_histogram = np.zeros((100, max(all_class_indices) + 1))
                if hist_data.shape[1] > 0:
                    padded_histogram[:, :hist_data.shape[1]] = hist_data
                hist_data = padded_histogram
            
            # Select columns for all classes
            selected_columns = hist_data[:, all_class_indices]
            
            # Bin the data (100 bins -> 10 score ranges)
            try:
                binned_counts = selected_columns.reshape(10, 10, len(all_class_indices)).sum(axis=1)
            except (ValueError, IndexError):
                binned_counts = np.zeros((10, len(all_class_indices)))
            
            all_binned_data.append(binned_counts)
        
        # Create subplot for the comprehensive table
        ax = fig.add_subplot(111)
        ax.axis('off')
        
        # Build table headers
        main_headers = ['Class Name']
        sub_headers = ['']
        
        for score_range in score_ranges:
            main_headers.extend([score_range] + [''] * 4)
            sub_headers.extend(frame_labels)
        
        # Build table data
        table_data = []
        table_data.append(sub_headers)
        
        # Add data rows for each class
        for class_idx, class_name in enumerate(all_class_names):
            row = [class_name[:18]]  # Truncate for better display
            
            for score_idx in range(10):
                for frame_idx in range(5):
                    if frame_idx < len(all_binned_data):
                        try:
                            value = int(all_binned_data[frame_idx][score_idx, class_idx])
                            row.append(str(value))
                        except (IndexError, ValueError):
                            row.append('0')
                    else:
                        row.append('0')
            
            table_data.append(row)
        
        # Create table with enhanced styling for HD
        table = ax.table(cellText=table_data,
                        colLabels=main_headers,
                        cellLoc='center',
                        loc='center',
                        bbox=[0, 0, 1, 1])
        
        # Enhanced styling for HD export
        table.auto_set_font_size(False)
        table.set_fontsize(8)  # Larger font for HD
        table.scale(1.0, 1.8)  # More spacing for clarity
        
        # Color scheme for score ranges
        score_range_colors = ['#FF4444', '#FF6666', '#FF8888', '#FFAA88', '#FFCC88',
                             '#FFEE88', '#DDFF88', '#BBFF88', '#99FF88', '#77FF88']
        
        # Style headers and cells (same logic as before but with enhanced clarity)
        num_cols = len(main_headers)
        
        # Main headers
        for col in range(num_cols):
            cell = table[(0, col)]
            if col == 0:
                cell.set_facecolor('#2C3E50')
                cell.set_text_props(weight='bold', color='white', size=9)
            else:
                score_idx = (col - 1) // 5
                if score_idx < len(score_range_colors):
                    cell.set_facecolor(score_range_colors[score_idx])
                    cell.set_text_props(weight='bold', color='black', size=8)
            cell.set_edgecolor('white')
            cell.set_linewidth(2)
        
        # Sub-headers (frame labels)
        for col in range(num_cols):
            cell = table[(1, col)]
            if col == 0:
                cell.set_facecolor('#34495E')
                cell.set_text_props(weight='bold', color='white', size=8)
            else:
                frame_idx = (col - 1) % 5
                if frame_idx == 0:  # Current frame
                    cell.set_facecolor('#E74C3C')
                    cell.set_text_props(weight='bold', color='white', size=8)
                else:
                    score_idx = (col - 1) // 5
                    if score_idx < len(score_range_colors):
                        base_color = score_range_colors[score_idx]
                        cell.set_facecolor(base_color)
                        cell.set_text_props(weight='bold', color='black', size=8)
            cell.set_edgecolor('white')
            cell.set_linewidth(2)
        
        # Style data cells with enhanced visibility
        for row in range(2, len(table_data) + 1):
            for col in range(num_cols):
                cell = table[(row, col)]
                
                if col == 0:  # Class name column
                    cell.set_facecolor('#ECF0F1')
                    cell.set_text_props(weight='bold', size=8)
                else:
                    try:
                        value_str = table_data[row-1][col]
                        value = int(value_str)
                        
                        frame_idx = (col - 1) % 5
                        score_idx = (col - 1) // 5
                        
                        if value > 0:
                            # Enhanced coloring for HD visibility
                            class_row_idx = row - 2
                            max_val = 0
                            for c in range(1, num_cols):
                                try:
                                    max_val = max(max_val, int(table_data[class_row_idx + 1][c]))
                                except (ValueError, IndexError):
                                    pass
                            
                            if max_val > 0:
                                intensity = min(value / max_val, 1.0)
                                
                                if score_idx < len(score_range_colors):
                                    base_color = score_range_colors[score_idx]
                                    r = int(base_color[1:3], 16) / 255.0
                                    g = int(base_color[3:5], 16) / 255.0
                                    b = int(base_color[5:7], 16) / 255.0
                                    
                                    alpha = 0.4 + intensity * 0.6
                                    cell.set_facecolor((r, g, b, alpha))
                                
                                if frame_idx == 0:  # Current frame highlight
                                    cell.set_edgecolor('#E74C3C')
                                    cell.set_linewidth(3)
                                    cell.set_text_props(weight='bold', size=8, color='darkred')
                                else:
                                    cell.set_text_props(size=8)
                            else:
                                cell.set_facecolor('#FFFFFF')
                                cell.set_text_props(size=8)
                        else:
                            cell.set_facecolor('#F8F9FA')
                            cell.set_text_props(size=8, color='gray')
                            
                    except (ValueError, IndexError):
                        cell.set_facecolor('#FFFFFF')
                        cell.set_text_props(size=8)
                
                if not (col == 0 or ((col - 1) % 5 == 0 and col > 0)):
                    cell.set_edgecolor('#BDC3C7')
                    cell.set_linewidth(1)
        
        # Enhanced title for HD
        title = f'Medical Image Histogram Analysis - Frame {current_frame_index + 1}/{len(self.frame_list)} ({current_frame_name})'
        fig.suptitle(title, fontsize=14, fontweight='bold', y=0.98)
        
        # Enhanced subtitle
        subtitle = 'Score Ranges: 90-100% to 0-10% | Frames: 0=Current, -1 to -4=Previous'
        ax.text(0.5, 0.02, subtitle, transform=ax.transAxes, fontsize=10, 
               ha='center', style='italic', color='gray')
        
        plt.subplots_adjust(left=0.01, right=0.99, top=0.94, bottom=0.06)
        
        if save_mode:
            return fig
        else:
            plt.show()
            return None
   
   

    def load_detection_image_hd(self, frame_name):
        """Load detection image for HD export."""
        image_path = os.path.join("visualization_data", "cropped_images", f"{frame_name}.jpg")
        
        if os.path.exists(image_path):
            try:
                img = cv2.imread(image_path)
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                return img_rgb
            except Exception as e:
                print(f"Error loading image {frame_name}: {e}")
                return None
        else:
            print(f"Image not found: {frame_name}")
            return None
    
    def combine_images_hd(self, histogram_fig, detection_img, frame_name, frame_index):
        """Combine histogram and detection image side by side in HD resolution."""
        # Convert matplotlib figure to image
        canvas = FigureCanvasAgg(histogram_fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()
        
        # Convert to numpy array
        hist_img = np.frombuffer(raw_data, dtype=np.uint8).reshape((int(size[1]), int(size[0]), 3))
        
        # Target HD dimensions
        target_width = 1920
        target_height = 1080
        
        # Calculate dimensions for side-by-side layout
        hist_width = target_width // 2  # Left half
        det_width = target_width // 2   # Right half
        
        # Resize histogram image to fit left half
        hist_img_resized = cv2.resize(hist_img, (hist_width, target_height-100))
        
        # Resize detection image to fit right half
        if detection_img is not None:
            det_img_resized = cv2.resize(detection_img, (det_width, target_height-100))
        else:
            # Create placeholder if no detection image
            det_img_resized = np.ones((target_height, det_width, 3), dtype=np.uint8) * 240
            cv2.putText(det_img_resized, "No Image Available", 
                       (det_width//4, target_height//2), 
                       cv2.FONT_HERSHEY_SIMPLEX, 2, (128, 128, 128), 3)
        
        # Combine side by side
        combined_img = np.hstack([hist_img_resized, det_img_resized])
        
        # Add frame info overlay
        overlay_height = 60
        overlay = np.ones((overlay_height, target_width, 3), dtype=np.uint8) * 50
        
        # Frame information text
        frame_text = f"Frame: {frame_name} ({frame_index + 1}/{len(self.frame_list)})"
        cv2.putText(overlay, frame_text, (20, 35), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
        
        # Detection info if available
        if frame_name in self.frame_info:
            det_count = self.frame_info[frame_name].get('detections', 0)
            det_text = f"Detections: {det_count}"
            cv2.putText(overlay, det_text, (target_width - 300, 35), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
        
        # Add overlay to top of combined image
        final_img = np.vstack([overlay, combined_img])
        
        # Close the matplotlib figure to free memory
        plt.close(histogram_fig)
        
        return final_img
    
    def export_single_frame_hd(self, frame_index, output_dir):
        """Export single frame in HD resolution."""
        frame_name = self.frame_list[frame_index]
        
        # Create histogram plot
        hist_fig = self.create_histogram_plot_hd(frame_index, save_mode=True)
        
        # Load detection image
        det_img = self.load_detection_image_hd(frame_name)
        
        # Combine images
        combined_img = self.combine_images_hd(hist_fig, det_img, frame_name, frame_index)
        
        # Save HD image
        output_path = os.path.join(output_dir, f"frame_{frame_index+1:04d}_{frame_name}_HD.jpg")
        cv2.imwrite(output_path, cv2.cvtColor(combined_img, cv2.COLOR_RGB2BGR), 
                   [cv2.IMWRITE_JPEG_QUALITY, 95])
        
        return output_path
    
    def export_all_frames_hd(self, output_dir="hd_exports"):
        """Export all frames in HD resolution."""
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"🎬 Exporting {len(self.frame_list)} frames in HD (1920x1080)...")
        
        exported_files = []
        
        for frame_index in tqdm(range(len(self.frame_list)), desc="Exporting HD frames"):
            try:
                output_path = self.export_single_frame_hd(frame_index, output_dir)
                exported_files.append(output_path)
                
            except Exception as e:
                print(f"❌ Error exporting frame {frame_index + 1}: {e}")
                continue
        
        print(f"✅ Successfully exported {len(exported_files)} HD frames to: {output_dir}")
        return exported_files
    
    def export_frame_range_hd(self, start_frame, end_frame, output_dir="hd_exports"):
        """Export a range of frames in HD resolution."""
        # Validate range
        start_frame = max(0, start_frame - 1)  # Convert to 0-based indexing
        end_frame = min(len(self.frame_list), end_frame)
        
        if start_frame >= end_frame:
            print("❌ Invalid frame range!")
            return []
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        frame_count = end_frame - start_frame
        print(f"🎬 Exporting frames {start_frame + 1} to {end_frame} in HD (1920x1080)...")
        
        exported_files = []
        
        for frame_index in tqdm(range(start_frame, end_frame), desc="Exporting HD frames"):
            try:
                output_path = self.export_single_frame_hd(frame_index, output_dir)
                exported_files.append(output_path)
                
            except Exception as e:
                print(f"❌ Error exporting frame {frame_index + 1}: {e}")
                continue
        
        print(f"✅ Successfully exported {len(exported_files)} HD frames to: {output_dir}")
        return exported_files


def main():
    """Main function with user interface for HD export."""
    print("🎬 Medical Image HD Exporter")
    print("=" * 50)
    
    # Initialize exporter
    exporter = HDImageExporter()
    
    if not exporter.frame_list:
        print("❌ No data loaded. Please run data preparation first.")
        return
    
    print(f"📊 Loaded {len(exporter.frame_list)} frames")
    print("\nExport Options:")
    print("1. Export single frame")
    print("2. Export frame range")
    print("3. Export all frames")
    print("4. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == '1':
                # Single frame export
                frame_num = int(input(f"Enter frame number (1-{len(exporter.frame_list)}): "))
                if 1 <= frame_num <= len(exporter.frame_list):
                    output_dir = input("Enter output directory (press Enter for 'hd_exports'): ").strip()
                    if not output_dir:
                        output_dir = "hd_exports"
                    
                    print(f"🎬 Exporting frame {frame_num} in HD...")
                    output_path = exporter.export_single_frame_hd(frame_num - 1, output_dir)
                    print(f"✅ Frame exported: {output_path}")
                else:
                    print("❌ Invalid frame number!")
                    
            elif choice == '2':
                # Frame range export
                start = int(input(f"Enter start frame (1-{len(exporter.frame_list)}): "))
                end = int(input(f"Enter end frame (1-{len(exporter.frame_list)}): "))
                
                output_dir = input("Enter output directory (press Enter for 'hd_exports'): ").strip()
                if not output_dir:
                    output_dir = "hd_exports"
                
                exported_files = exporter.export_frame_range_hd(start, end, output_dir)
                
            elif choice == '3':
                # Export all frames
                output_dir = input("Enter output directory (press Enter for 'hd_exports'): ").strip()
                if not output_dir:
                    output_dir = "hd_exports"
                
                confirm = input(f"Export all {len(exporter.frame_list)} frames? This may take a while. (y/n): ")
                if confirm.lower() == 'y':
                    exported_files = exporter.export_all_frames_hd(output_dir)
                else:
                    print("Export cancelled.")
                    
            elif choice == '4':
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice! Please enter 1-4.")
                
        except ValueError:
            print("❌ Please enter a valid number!")
        except KeyboardInterrupt:
            print("\n👋 Export cancelled by user.")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()