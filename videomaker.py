# #!/usr/bin/env python3
# """
# HD Video Maker for Medical Image Analysis
# Creates high-quality videos from exported HD frames at specified FPS
# """

# import cv2
# import os
# import glob
# import numpy as np
# from tqdm import tqdm
# import argparse
# from datetime import datetime
# import json

# class VideoMaker:
#     def __init__(self):
#         self.supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
        
#     def get_frame_files(self, input_dir, pattern="frame_*.jpg"):
#         """Get all frame files sorted by frame number."""
#         # Look for HD exported frames
#         pattern_path = os.path.join(input_dir, pattern)
#         frame_files = glob.glob(pattern_path)
        
#         if not frame_files:
#             # Try alternative patterns
#             for ext in ['.jpg', '.jpeg', '.png']:
#                 pattern_path = os.path.join(input_dir, f"*{ext}")
#                 frame_files = glob.glob(pattern_path)
#                 if frame_files:
#                     break
        
#         if not frame_files:
#             print(f"❌ No frame files found in {input_dir}")
#             return []
        
#         # Sort files naturally by frame number
#         def extract_frame_number(filename):
#             basename = os.path.basename(filename)
#             # Extract number from filename like "frame_0001_name_HD.jpg"
#             try:
#                 parts = basename.split('_')
#                 for part in parts:
#                     if part.isdigit():
#                         return int(part)
#                 # Fallback: try to extract any number
#                 import re
#                 numbers = re.findall(r'\d+', basename)
#                 return int(numbers[0]) if numbers else 0
#             except:
#                 return 0
        
#         frame_files.sort(key=extract_frame_number)
#         print(f"✅ Found {len(frame_files)} frame files")
#         return frame_files
    
#     def create_video(self, input_dir, output_path, fps=20, quality='high', 
#                     codec='mp4v', include_audio=False):
#         """Create video from frame images."""
        
#         # Get frame files
#         frame_files = self.get_frame_files(input_dir)
#         if not frame_files:
#             return False
        
#         # Read first frame to get dimensions
#         first_frame = cv2.imread(frame_files[0])
#         if first_frame is None:
#             print(f"❌ Cannot read first frame: {frame_files[0]}")
#             return False
        
#         height, width, channels = first_frame.shape
#         print(f"📐 Video dimensions: {width}x{height}")
#         print(f"🎬 Creating video with {len(frame_files)} frames at {fps} FPS")
        
#         # Set up video codec and quality
#         fourcc_codes = {
#             'mp4v': cv2.VideoWriter_fourcc(*'mp4v'),  # MP4 (good compatibility)
#             'xvid': cv2.VideoWriter_fourcc(*'XVID'),  # AVI with Xvid
#             'h264': cv2.VideoWriter_fourcc(*'H264'),  # H.264 (best quality)
#             'mjpg': cv2.VideoWriter_fourcc(*'MJPG'),  # Motion JPEG
#         }
        
#         fourcc = fourcc_codes.get(codec.lower(), cv2.VideoWriter_fourcc(*'mp4v'))
        
#         # Ensure output directory exists
#         os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
        
#         # Create VideoWriter object
#         out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
#         if not out.isOpened():
#             print(f"❌ Failed to create video writer for {output_path}")
#             return False
        
#         # Process each frame
#         print(f"🎥 Encoding video...")
        
#         for i, frame_file in enumerate(tqdm(frame_files, desc="Processing frames")):
#             frame = cv2.imread(frame_file)
            
#             if frame is None:
#                 print(f"⚠️  Warning: Cannot read frame {frame_file}, skipping...")
#                 continue
            
#             # Ensure frame has correct dimensions
#             if frame.shape[:2] != (height, width):
#                 frame = cv2.resize(frame, (width, height))
            
#             # Write frame to video
#             out.write(frame)
        
#         # Release everything
#         out.release()
#         cv2.destroyAllWindows()
        
#         # Verify video was created
#         if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
#             file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
#             duration = len(frame_files) / fps
#             print(f"✅ Video created successfully!")
#             print(f"📁 Output: {output_path}")
#             print(f"📊 Size: {file_size:.1f} MB")
#             print(f"⏱️  Duration: {duration:.1f} seconds")
#             print(f"🎬 Resolution: {width}x{height} @ {fps} FPS")
#             return True
#         else:
#             print(f"❌ Failed to create video file")
#             return False
    
#     def create_video_with_transitions(self, input_dir, output_path, fps=20, 
#                                     transition_frames=5, transition_type='fade'):
#         """Create video with smooth transitions between frames."""
#         frame_files = self.get_frame_files(input_dir)
#         if not frame_files:
#             return False
        
#         first_frame = cv2.imread(frame_files[0])
#         height, width, channels = first_frame.shape
        
#         fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#         out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
#         print(f"🎬 Creating video with {transition_type} transitions...")
        
#         for i, frame_file in enumerate(tqdm(frame_files, desc="Processing with transitions")):
#             current_frame = cv2.imread(frame_file)
#             if current_frame is None:
#                 continue
            
#             # Write the main frame
#             out.write(current_frame)
            
#             # Add transition to next frame (except for last frame)
#             if i < len(frame_files) - 1:
#                 next_frame = cv2.imread(frame_files[i + 1])
#                 if next_frame is not None:
#                     # Create transition frames
#                     for t in range(transition_frames):
#                         alpha = (t + 1) / (transition_frames + 1)
                        
#                         if transition_type == 'fade':
#                             # Fade transition
#                             blended = cv2.addWeighted(current_frame, 1 - alpha, next_frame, alpha, 0)
#                         elif transition_type == 'slide':
#                             # Slide transition (left to right)
#                             split_point = int(width * alpha)
#                             blended = current_frame.copy()
#                             blended[:, :split_point] = next_frame[:, :split_point]
#                         else:
#                             # Default to fade
#                             blended = cv2.addWeighted(current_frame, 1 - alpha, next_frame, alpha, 0)
                        
#                         out.write(blended)
        
#         out.release()
#         cv2.destroyAllWindows()
        
#         if os.path.exists(output_path):
#             print(f"✅ Video with transitions created: {output_path}")
#             return True
#         return False
    
#     def create_video_with_text_overlay(self, input_dir, output_path, fps=20, 
#                                      show_frame_info=True, show_timestamp=True):
#         """Create video with enhanced text overlays."""
#         frame_files = self.get_frame_files(input_dir)
#         if not frame_files:
#             return False
        
#         first_frame = cv2.imread(frame_files[0])
#         height, width, channels = first_frame.shape
        
#         fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#         out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
#         print(f"🎬 Creating video with enhanced overlays...")
        
#         for i, frame_file in enumerate(tqdm(frame_files, desc="Adding overlays")):
#             frame = cv2.imread(frame_file)
#             if frame is None:
#                 continue
            
#             # Add frame counter
#             if show_frame_info:
#                 frame_text = f"Frame {i+1}/{len(frame_files)}"
#                 cv2.putText(frame, frame_text, (width - 200, 30), 
#                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
#                 cv2.putText(frame, frame_text, (width - 202, 28), 
#                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)  # Shadow
            
#             # Add timestamp
#             if show_timestamp:
#                 time_seconds = i / fps
#                 minutes = int(time_seconds // 60)
#                 seconds = int(time_seconds % 60)
#                 time_text = f"{minutes:02d}:{seconds:02d}"
#                 cv2.putText(frame, time_text, (width - 100, height - 20), 
#                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
#                 cv2.putText(frame, time_text, (width - 102, height - 22), 
#                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)  # Shadow
            
#             out.write(frame)
        
#         out.release()
#         cv2.destroyAllWindows()
        
#         if os.path.exists(output_path):
#             print(f"✅ Enhanced video created: {output_path}")
#             return True
#         return False
    
#     def create_multiple_formats(self, input_dir, base_output_name, fps=20):
#         """Create video in multiple formats for different use cases."""
#         formats = [
#             {'ext': 'mp4', 'codec': 'mp4v', 'desc': 'Standard MP4'},
#             {'ext': 'avi', 'codec': 'xvid', 'desc': 'AVI with Xvid'},
#             {'ext': 'mov', 'codec': 'mp4v', 'desc': 'QuickTime MOV'},
#         ]
        
#         created_videos = []
        
#         for fmt in formats:
#             output_path = f"{base_output_name}.{fmt['ext']}"
#             print(f"\n🎬 Creating {fmt['desc']} video...")
            
#             success = self.create_video(input_dir, output_path, fps, codec=fmt['codec'])
#             if success:
#                 created_videos.append(output_path)
        
#         print(f"\n✅ Created {len(created_videos)} video formats:")
#         for video in created_videos:
#             print(f"   📹 {video}")
        
#         return created_videos

# def main():
#     """Main function with command-line interface."""
#     parser = argparse.ArgumentParser(description='Create video from HD exported frames')
#     parser.add_argument('input_dir', nargs='?', default='hd_exports', 
#                        help='Directory containing frame images (default: hd_exports)')
#     parser.add_argument('-o', '--output', default=None,
#                        help='Output video path (default: auto-generated)')
#     parser.add_argument('-fps', '--framerate', type=int, default=20,
#                        help='Frames per second (default: 20)')
#     parser.add_argument('-c', '--codec', default='mp4v',
#                        choices=['mp4v', 'xvid', 'h264', 'mjpg'],
#                        help='Video codec (default: mp4v)')
#     parser.add_argument('-t', '--transitions', action='store_true',
#                        help='Add fade transitions between frames')
#     parser.add_argument('-e', '--enhanced', action='store_true',
#                        help='Add frame counter and timestamp overlays')
#     parser.add_argument('-m', '--multiple', action='store_true',
#                        help='Create multiple video formats')
    
#     args = parser.parse_args()
    
#     # Check input directory
#     if not os.path.exists(args.input_dir):
#         print(f"❌ Input directory not found: {args.input_dir}")
#         return
    
#     # Generate output filename if not provided
#     if args.output is None:
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         if args.multiple:
#             args.output = f"medical_analysis_{timestamp}"  # No extension for multiple formats
#         else:
#             args.output = f"medical_analysis_{timestamp}.mp4"
    
#     # Create video maker
#     video_maker = VideoMaker()
    
#     print("🎬 Medical Image Video Creator")
#     print("=" * 50)
#     print(f"📁 Input directory: {args.input_dir}")
#     print(f"🎯 Output: {args.output}")
#     print(f"⚡ Frame rate: {args.framerate} FPS")
#     print(f"🔧 Codec: {args.codec}")
    
#     # Create video based on options
#     if args.multiple:
#         # Create multiple formats
#         created_videos = video_maker.create_multiple_formats(
#             args.input_dir, args.output, args.framerate)
        
#     elif args.transitions:
#         # Create video with transitions
#         success = video_maker.create_video_with_transitions(
#             args.input_dir, args.output, args.framerate)
        
#     elif args.enhanced:
#         # Create video with enhanced overlays
#         success = video_maker.create_video_with_text_overlay(
#             args.input_dir, args.output, args.framerate)
        
#     else:
#         # Create standard video
#         success = video_maker.create_video(
#             args.input_dir, args.output, args.framerate, codec=args.codec)
    
#     if not args.multiple and success:
#         print(f"\n🎉 Video creation completed successfully!")
#     elif not args.multiple:
#         print(f"\n❌ Video creation failed!")

# def interactive_mode():
#     """Interactive mode for non-command-line usage."""
#     print("🎬 Medical Image Video Creator - Interactive Mode")
#     print("=" * 60)
    
#     # Get input directory
#     input_dir = input("📁 Enter frames directory (default: hd_exports): ").strip()
#     if not input_dir:
#         input_dir = "hd_exports"
    
#     if not os.path.exists(input_dir):
#         print(f"❌ Directory not found: {input_dir}")
#         return
    
#     # Get FPS
#     try:
#         fps = int(input("⚡ Enter frame rate (default: 20): ") or "20")
#     except ValueError:
#         fps = 20
    
#     # Get output filename
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     default_output = f"medical_analysis_{timestamp}.mp4"
#     output_path = input(f"🎯 Enter output filename (default: {default_output}): ").strip()
#     if not output_path:
#         output_path = default_output
    
#     # Video options
#     print("\n🎬 Video Options:")
#     print("1. Standard video")
#     print("2. Video with fade transitions")
#     print("3. Video with enhanced overlays")
#     print("4. Multiple formats (MP4, AVI, MOV)")
    
#     try:
#         choice = int(input("Choose option (1-4): ") or "1")
#     except ValueError:
#         choice = 1
    
#     # Create video
#     video_maker = VideoMaker()
    
#     print(f"\n🎬 Creating video...")
#     print(f"📁 Input: {input_dir}")
#     print(f"🎯 Output: {output_path}")
#     print(f"⚡ FPS: {fps}")
    
#     if choice == 1:
#         success = video_maker.create_video(input_dir, output_path, fps)
#     elif choice == 2:
#         success = video_maker.create_video_with_transitions(input_dir, output_path, fps)
#     elif choice == 3:
#         success = video_maker.create_video_with_text_overlay(input_dir, output_path, fps)
#     elif choice == 4:
#         base_name = output_path.rsplit('.', 1)[0] if '.' in output_path else output_path
#         created_videos = video_maker.create_multiple_formats(input_dir, base_name, fps)
#         success = len(created_videos) > 0
#     else:
#         success = video_maker.create_video(input_dir, output_path, fps)
    
#     if success:
#         print(f"\n🎉 Video creation completed successfully!")
#     else:
#         print(f"\n❌ Video creation failed!")

# if __name__ == "__main__":
#     import sys
    
#     # If no command line arguments, run interactive mode
#     if len(sys.argv) == 1:
#         interactive_mode()
#     else:
#         main()

#!/usr/bin/env python3
"""
Medical Image Video Generator
Creates MP4 videos showing histogram analysis and detection results at 20 FPS.
Excludes navigation controls and class selector from the video output.
"""

import cv2
import numpy as np
import json
import os
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from datetime import datetime
import argparse
import sys

class MedicalImageVideoGenerator:
    def __init__(self, data_folder="visualization_data", output_folder="videos"):
        self.data_folder = data_folder
        self.output_folder = output_folder
        
        # Data variables
        self.histogram_data = {}
        self.frame_info = {}
        self.class_mapping = {}
        self.frame_list = []
        
        # Video settings
        self.fps = 20
        self.video_width = 1600
        self.video_height = 800
        
        # Create output folder
        os.makedirs(self.output_folder, exist_ok=True)
        
        # Load data
        self.load_data()
    
    def load_data(self):
        """Load all data files."""
        try:
            # Load histogram data
            with open(os.path.join(self.data_folder, "histogram_data.json"), 'r') as f:
                self.histogram_data = json.load(f)
            
            # Load frame info
            with open(os.path.join(self.data_folder, "frame_info.json"), 'r') as f:
                self.frame_info = json.load(f)
            
            # Load class mapping
            with open(os.path.join(self.data_folder, "class_mapping.json"), 'r') as f:
                self.class_mapping = json.load(f)
            
            # Load frame list
            with open(os.path.join(self.data_folder, "frame_list.json"), 'r') as f:
                self.frame_list = json.load(f)
                
            print(f"✅ Loaded {len(self.frame_list)} frames successfully!")
            
        except FileNotFoundError as e:
            print(f"❌ Error: Data files not found: {e}")
            print("Please run the data preparation script first.")
            sys.exit(1)
    
    def get_selected_classes_from_user(self):
        """Interactive class selection."""
        print("\n📋 Available Classes:")
        print("=" * 60)
        
        # Display all classes
        sorted_classes = sorted([(int(k), v) for k, v in self.class_mapping.items()])
        for idx, (class_idx, class_name) in enumerate(sorted_classes):
            print(f"{idx+1:2d}. Class {class_idx:2d}: {class_name}")
        
        print("\n🎯 Class Selection Options:")
        print("  - Enter 'all' to select all classes")
        print("  - Enter specific class indices (e.g., '0,1,5,12')")
        print("  - Enter class numbers from list above (e.g., '1,2,6,13')")
        
        while True:
            try:
                selection = input("\nEnter your selection: ").strip().lower()
                
                if selection == 'all':
                    return set(int(k) for k in self.class_mapping.keys())
                
                if ',' in selection:
                    # Parse comma-separated values
                    parts = [part.strip() for part in selection.split(',')]
                    selected_indices = []
                    
                    for part in parts:
                        num = int(part)
                        # Check if it's a list number (1-based) or class index (0-based)
                        if 1 <= num <= len(sorted_classes):
                            # Treat as list number (1-based)
                            class_idx = sorted_classes[num-1][0]
                            selected_indices.append(class_idx)
                        elif num in [cls[0] for cls in sorted_classes]:
                            # Treat as class index
                            selected_indices.append(num)
                        else:
                            print(f"❌ Invalid selection: {num}")
                            raise ValueError()
                    
                    if selected_indices:
                        selected_set = set(selected_indices)
                        print(f"\n✅ Selected classes: {sorted(selected_set)}")
                        return selected_set
                else:
                    print("❌ Please enter 'all' or comma-separated numbers")
                    
            except (ValueError, IndexError):
                print("❌ Invalid input. Please try again.")
    
    def create_histogram_image(self, current_frame_index, selected_classes):
        """Create histogram visualization as image."""
        # Get selected class information
        selected_class_indices = sorted(list(selected_classes))
        selected_class_names = [self.class_mapping[str(i)] for i in selected_class_indices]
        
        if not selected_class_indices:
            # Create blank image with message
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.text(0.5, 0.5, 'No classes selected', 
                   ha='center', va='center', fontsize=20, transform=ax.transAxes)
            ax.axis('off')
        else:
            # Score ranges and frame labels
            score_ranges = ["90-100%", "80-90%", "70-80%", "60-70%", "50-60%", 
                           "40-50%", "30-40%", "20-30%", "10-20%", "0-10%"]
            frame_labels = ["0", "-1", "-2", "-3", "-4"]
            
            # Get histogram data for current + last 4 frames
            hist_frames = []
            
            for i in range(current_frame_index, max(-1, current_frame_index - 5), -1):
                if i >= 0 and i < len(self.frame_list):
                    frame_name = self.frame_list[i]
                    if frame_name in self.histogram_data:
                        hist_data = np.array(self.histogram_data[frame_name])
                        hist_frames.append(hist_data)
            
            # Pad with empty frames if needed
            while len(hist_frames) < 5:
                all_class_indices = [int(k) for k in self.class_mapping.keys()]
                hist_frames.append(np.zeros((100, max(all_class_indices) + 1)))
            
            # Process histogram data
            all_binned_data = []
            for hist_data in hist_frames:
                all_class_indices = [int(k) for k in self.class_mapping.keys()]
                if hist_data.shape[1] < max(all_class_indices) + 1:
                    padded_histogram = np.zeros((100, max(all_class_indices) + 1))
                    if hist_data.shape[1] > 0:
                        padded_histogram[:, :hist_data.shape[1]] = hist_data
                    hist_data = padded_histogram
                
                selected_columns = hist_data[:, selected_class_indices]
                
                try:
                    binned_counts = selected_columns.reshape(10, 10, len(selected_class_indices)).sum(axis=1)
                except (ValueError, IndexError):
                    binned_counts = np.zeros((10, len(selected_class_indices)))
                
                all_binned_data.append(binned_counts)
            
            # Create matplotlib figure
            fig, ax = plt.subplots(figsize=(14, 8))
            ax.axis('off')
            
            # Build table data
            main_headers = ['Class Name']
            for score_range in score_ranges:
                main_headers.extend([score_range, '', '', '', ''])
            
            sub_headers = ['']
            for _ in score_ranges:
                sub_headers.extend(frame_labels)
            
            table_data = [sub_headers]
            
            # Add data rows
            for class_idx, class_name in enumerate(selected_class_names):
                short_name = class_name[:15]
                class_display = f"{short_name} ({selected_class_indices[class_idx]})"
                row = [class_display]
                
                for score_idx in range(10):
                    for frame_idx in range(5):
                        if frame_idx < len(all_binned_data):
                            try:
                                value = int(all_binned_data[frame_idx][score_idx, class_idx])
                                if value >= 99999:
                                    formatted_value = "99k+"
                                elif value >= 1000:
                                    formatted_value = f"{value//1000}k"
                                elif value >= 100:
                                    formatted_value = f"{value//100}h"
                                else:
                                    formatted_value = str(value)
                                row.append(formatted_value)
                            except (IndexError, ValueError):
                                row.append('0')
                        else:
                            row.append('0')
                
                table_data.append(row)
            
            # Create table
            table = ax.table(cellText=table_data,
                            colLabels=main_headers,
                            cellLoc='center',
                            loc='center',
                            bbox=[0, 0, 1, 1])
            
            # Style table
            table.auto_set_font_size(False)
            table.set_fontsize(8)
            table.scale(1.0, 1.0)
            
            # Color scheme
            score_range_colors = ['#FF3333', '#FF5555', '#FF7777', '#FF9999', '#FFBB99',
                                 '#FFDD99', '#DDFF99', '#BBFF99', '#99FF99', '#77FF99']
            
            num_cols = len(main_headers)
            cell_height = 0.08
            
            # Set column widths
            class_name_width = 4.0 / (num_cols + 3)
            data_width = 1.0 / (num_cols + 3)
            
            for col in range(num_cols):
                for row in range(len(table_data) + 1):
                    cell = table[(row, col)]
                    if col == 0:
                        cell.set_width(class_name_width)
                    else:
                        cell.set_width(data_width)
                    cell.set_height(cell_height)
            
            # Style headers
            for col in range(num_cols):
                cell = table[(0, col)]
                if col == 0:
                    cell.set_facecolor('#2C3E50')
                    cell.set_text_props(weight='bold', color='white', size=9)
                else:
                    score_idx = (col - 1) // 5
                    if score_idx < len(score_range_colors) and (col - 1) % 5 == 0:
                        cell.set_facecolor(score_range_colors[score_idx])
                        cell.set_text_props(weight='bold', color='black', size=9)
                    else:
                        score_idx = (col - 1) // 5
                        if score_idx < len(score_range_colors):
                            cell.set_facecolor(score_range_colors[score_idx])
                            cell.set_text_props(color=score_range_colors[score_idx], size=1)
                cell.set_edgecolor('white')
                cell.set_linewidth(2)
            
            # Style sub-headers
            for col in range(num_cols):
                cell = table[(1, col)]
                if col == 0:
                    cell.set_facecolor('#2C3E50')
                    cell.set_text_props(color='white', size=1)
                else:
                    frame_idx = (col - 1) % 5
                    score_idx = (col - 1) // 5
                    
                    if frame_idx == 0:
                        cell.set_facecolor('#E74C3C')
                        cell.set_text_props(weight='bold', color='white', size=9)
                    else:
                        if score_idx < len(score_range_colors):
                            cell.set_facecolor(score_range_colors[score_idx])
                            cell.set_text_props(weight='bold', color='black', size=9)
                cell.set_edgecolor('white')
                cell.set_linewidth(2)
            
            # Style data cells
            for row in range(2, len(table_data) + 1):
                for col in range(num_cols):
                    cell = table[(row, col)]
                    
                    if col == 0:
                        cell.set_facecolor('#ECF0F1')
                        cell.set_text_props(weight='bold', size=8, ha='left')
                        cell.set_edgecolor('#BDC3C7')
                    else:
                        frame_idx = (col - 1) % 5
                        score_idx = (col - 1) // 5
                        
                        try:
                            value_str = table_data[row-1][col]
                            if value_str.endswith('k+'):
                                value = 99999
                            elif value_str.endswith('k'):
                                value = int(value_str[:-1]) * 1000
                            elif value_str.endswith('h'):
                                value = int(value_str[:-1]) * 100
                            else:
                                value = int(value_str) if value_str.isdigit() else 0
                            
                            if value > 0:
                                if frame_idx == 0:
                                    cell.set_edgecolor('#E74C3C')
                                    cell.set_linewidth(3)
                                    cell.set_text_props(weight='bold', size=8, color='darkred')
                                else:
                                    cell.set_text_props(size=8)
                                
                                if score_idx < len(score_range_colors):
                                    base_color = score_range_colors[score_idx]
                                    r = int(base_color[1:3], 16) / 255.0
                                    g = int(base_color[3:5], 16) / 255.0
                                    b = int(base_color[5:7], 16) / 255.0
                                    cell.set_facecolor((r, g, b, 0.3))
                            else:
                                cell.set_facecolor('#F8F9FA')
                                cell.set_text_props(size=8, color='gray')
                        except (ValueError, IndexError):
                            cell.set_facecolor('#FFFFFF')
                            cell.set_text_props(size=8)
                        
                        cell.set_edgecolor('#D5DBDB')
                        cell.set_linewidth(0.5)
            
            # Title
            current_frame_name = self.frame_list[current_frame_index]
            title = f'Medical Image Histogram Analysis - Frame {current_frame_index + 1}/{len(self.frame_list)} ({current_frame_name})'
            fig.suptitle(title, fontsize=14, fontweight='bold', y=0.95)
        
        plt.tight_layout()
        
        # Convert to image
        fig.canvas.draw()
        buf = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        buf = buf.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        
        plt.close(fig)
        return buf
    
    def load_detection_image(self, frame_name):
        """Load detection result image."""
        image_path = os.path.join(self.data_folder, "cropped_images", f"{frame_name}.jpg")
        
        if os.path.exists(image_path):
            try:
                img = cv2.imread(image_path)
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                return img_rgb
            except Exception as e:
                print(f"⚠️ Error loading image {frame_name}: {e}")
                return self.create_placeholder_image(f"Error loading\n{frame_name}")
        else:
            return self.create_placeholder_image(f"Image not found\n{frame_name}")
    
    def create_placeholder_image(self, text):
        """Create placeholder image with text."""
        img = Image.new('RGB', (400, 300), color='lightgray')
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        # Get text bounding box
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center text
        x = (400 - text_width) // 2
        y = (300 - text_height) // 2
        
        draw.text((x, y), text, fill='black', font=font)
        
        return np.array(img)
    
    def create_combined_frame(self, current_frame_index, selected_classes):
        """Create combined frame with histogram and detection image."""
        # Get histogram image
        hist_img = self.create_histogram_image(current_frame_index, selected_classes)
        
        # Get detection image
        frame_name = self.frame_list[current_frame_index]
        detection_img = self.load_detection_image(frame_name)
        
        # Create combined frame first
        combined_frame = np.ones((self.video_height, self.video_width, 3), dtype=np.uint8) * 255
        
        # Define layout areas with proper bounds checking
        margin = 10
        label_height = 50
        bottom_margin = 50
        gap = 20
        
        # Available area for content
        content_height = self.video_height - label_height - bottom_margin
        content_width = self.video_width - 2 * margin - gap
        
        # Split content area: 65% for histogram, 35% for detection
        hist_area_width = int(content_width * 0.65)
        det_area_width = content_width - hist_area_width
        
        # Position calculations
        hist_x = margin
        hist_y = label_height
        det_x = hist_x + hist_area_width + gap
        det_y = label_height
        
        # Resize histogram image to fit in allocated area
        hist_height, hist_width = hist_img.shape[:2]
        hist_scale = min(hist_area_width / hist_width, content_height / hist_height)
        new_hist_width = int(hist_width * hist_scale)
        new_hist_height = int(hist_height * hist_scale)
        
        # Ensure dimensions don't exceed available space
        new_hist_width = min(new_hist_width, hist_area_width)
        new_hist_height = min(new_hist_height, content_height)
        
        try:
            hist_resized = cv2.resize(hist_img, (new_hist_width, new_hist_height))
            
            # Center histogram image in its area
            hist_center_x = hist_x + (hist_area_width - new_hist_width) // 2
            hist_center_y = hist_y + (content_height - new_hist_height) // 2
            
            # Bounds checking for histogram placement
            hist_end_y = hist_center_y + new_hist_height
            hist_end_x = hist_center_x + new_hist_width
            
            if (hist_center_y >= 0 and hist_end_y <= self.video_height and 
                hist_center_x >= 0 and hist_end_x <= self.video_width):
                combined_frame[hist_center_y:hist_end_y, hist_center_x:hist_end_x] = hist_resized
            else:
                print(f"⚠️ Warning: Histogram placement out of bounds, skipping...")
                
        except Exception as e:
            print(f"⚠️ Warning: Error resizing histogram image: {e}")
        
        # Resize detection image to fit in allocated area
        det_height, det_width = detection_img.shape[:2]
        det_scale = min(det_area_width / det_width, content_height / det_height)
        new_det_width = int(det_width * det_scale)
        new_det_height = int(det_height * det_scale)
        
        # Ensure dimensions don't exceed available space
        new_det_width = min(new_det_width, det_area_width)
        new_det_height = min(new_det_height, content_height)
        
        try:
            detection_resized = cv2.resize(detection_img, (new_det_width, new_det_height))
            
            # Center detection image in its area
            det_center_x = det_x + (det_area_width - new_det_width) // 2
            det_center_y = det_y + (content_height - new_det_height) // 2
            
            # Bounds checking for detection placement
            det_end_y = det_center_y + new_det_height
            det_end_x = det_center_x + new_det_width
            
            if (det_center_y >= 0 and det_end_y <= self.video_height and 
                det_center_x >= 0 and det_end_x <= self.video_width):
                combined_frame[det_center_y:det_end_y, det_center_x:det_end_x] = detection_resized
            else:
                print(f"⚠️ Warning: Detection image placement out of bounds, skipping...")
                
        except Exception as e:
            print(f"⚠️ Warning: Error resizing detection image: {e}")
        
        # Add section labels with bounds checking
        try:
            cv2.putText(combined_frame, "Histogram Analysis", (hist_x, 35), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)
            cv2.putText(combined_frame, "Detection Results", (det_x, 35), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)
        except Exception as e:
            print(f"⚠️ Warning: Error adding section labels: {e}")
        
        # Add frame info overlay with bounds checking
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")
            frame_text = f"Frame: {current_frame_index + 1}/{len(self.frame_list)} | {frame_name} | {timestamp}"
            cv2.putText(combined_frame, frame_text, (margin, self.video_height - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        except Exception as e:
            print(f"⚠️ Warning: Error adding frame info: {e}")
        
        return combined_frame
    
    def generate_video(self, selected_classes, output_filename=None, frame_range=None):
        """Generate video with selected classes."""
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            class_count = len(selected_classes)
            output_filename = f"medical_visualization_{class_count}classes_{timestamp}.mp4"
        
        output_path = os.path.join(self.output_folder, output_filename)
        
        # Determine frame range
        if frame_range is None:
            start_frame, end_frame = 0, len(self.frame_list)
        else:
            start_frame, end_frame = frame_range
            start_frame = max(0, start_frame)
            end_frame = min(len(self.frame_list), end_frame)
        
        total_frames = end_frame - start_frame
        
        print(f"🎬 Generating video: {output_filename}")
        print(f"📊 Selected classes: {sorted(selected_classes)}")
        print(f"🎞️ Frame range: {start_frame+1} to {end_frame} ({total_frames} frames)")
        print(f"⚡ FPS: {self.fps}")
        print(f"📐 Resolution: {self.video_width}x{self.video_height}")
        
        # Initialize video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(output_path, fourcc, self.fps, 
                                     (self.video_width, self.video_height))
        
        if not video_writer.isOpened():
            print("❌ Error: Could not initialize video writer")
            return False
        
        try:
            # Generate frames
            for frame_idx in range(start_frame, end_frame):
                print(f"\r🎥 Processing frame {frame_idx + 1 - start_frame}/{total_frames}...", end="", flush=True)
                
                # Create combined frame
                combined_frame = self.create_combined_frame(frame_idx, selected_classes)
                
                # Convert RGB to BGR for OpenCV
                combined_frame_bgr = cv2.cvtColor(combined_frame, cv2.COLOR_RGB2BGR)
                
                # Write frame to video
                video_writer.write(combined_frame_bgr)
            
            print(f"\n✅ Video generation complete!")
            print(f"📁 Output: {output_path}")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error during video generation: {e}")
            return False
            
        finally:
            video_writer.release()
    
    def interactive_video_generation(self):
        """Interactive video generation with user input."""
        print("🎬 Medical Image Video Generator")
        print("=" * 50)
        
        # Class selection
        selected_classes = self.get_selected_classes_from_user()
        
        # Frame range selection
        print(f"\n🎞️ Frame Range Selection (Total: {len(self.frame_list)} frames):")
        print("  - Press Enter for all frames")
        print("  - Enter 'start,end' for specific range (e.g., '1,100')")
        
        frame_range = None
        range_input = input("Enter frame range: ").strip()
        
        if range_input:
            try:
                start, end = map(int, range_input.split(','))
                frame_range = (start - 1, end)  # Convert to 0-based indexing
                print(f"✅ Frame range: {start} to {end}")
            except ValueError:
                print("⚠️ Invalid range format, using all frames")
        
        # Custom filename
        print(f"\n📁 Output filename:")
        print("  - Press Enter for auto-generated name")
        print("  - Enter custom filename (without .mp4)")
        
        custom_name = input("Enter filename: ").strip()
        output_filename = f"{custom_name}.mp4" if custom_name else None
        
        # Generate video
        print(f"\n🚀 Starting video generation...")
        success = self.generate_video(selected_classes, output_filename, frame_range)
        
        if success:
            print(f"🎉 Video generation completed successfully!")
        else:
            print(f"💥 Video generation failed!")
        
        return success

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Generate medical image analysis videos")
    parser.add_argument("--data", default="visualization_data", 
                       help="Path to data folder (default: visualization_data)")
    parser.add_argument("--output", default="videos", 
                       help="Output folder for videos (default: videos)")
    parser.add_argument("--classes", 
                       help="Comma-separated class indices (e.g., '0,1,5') or 'all'")
    parser.add_argument("--frames", 
                       help="Frame range as 'start,end' (1-based, e.g., '1,100')")
    parser.add_argument("--filename", 
                       help="Output filename (without .mp4 extension)")
    parser.add_argument("--fps", type=int, default=20, 
                       help="Video frame rate (default: 20)")
    
    args = parser.parse_args()
    
    # Create video generator
    generator = MedicalImageVideoGenerator(args.data, args.output)
    generator.fps = args.fps
    
    if args.classes:
        # Non-interactive mode
        if args.classes.lower() == 'all':
            selected_classes = set(int(k) for k in generator.class_mapping.keys())
        else:
            try:
                selected_classes = set(map(int, args.classes.split(',')))
            except ValueError:
                print("❌ Error: Invalid class indices format")
                return 1
        
        frame_range = None
        if args.frames:
            try:
                start, end = map(int, args.frames.split(','))
                frame_range = (start - 1, end)
            except ValueError:
                print("❌ Error: Invalid frame range format")
                return 1
        
        output_filename = f"{args.filename}.mp4" if args.filename else None
        
        success = generator.generate_video(selected_classes, output_filename, frame_range)
        return 0 if success else 1
    else:
        # Interactive mode
        success = generator.interactive_video_generation()
        return 0 if success else 1

if __name__ == "__main__":
    exit(main())