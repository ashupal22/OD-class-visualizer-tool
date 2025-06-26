# #!/usr/bin/env python3
# """
# Interactive Histogram Visualization Tool for Medical Image Analysis
# Shows comprehensive histogram tables and detection results with navigation controls.
# """

# import tkinter as tk
# from tkinter import ttk, messagebox
# import cv2
# import numpy as np
# import json
# import os
# from PIL import Image, ImageTk
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# class MedicalImageVisualizationTool:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Medical Image Histogram Visualization Tool")
#         self.root.geometry("1800x1000")  # Increased width for class selector
#         self.root.configure(bg='#f0f0f0')
        
#         # Data variables
#         self.histogram_data = {}
#         self.frame_info = {}
#         self.class_mapping = {}
#         self.frame_list = []
#         self.current_frame_index = 0
        
#         # Class selection variables
#         self.selected_classes = set()  # Set of selected class indices
#         self.class_buttons = {}  # Dictionary to store class button references
        
#         # Load data
#         self.load_data()
        
#         # Create GUI
#         self.create_widgets()
        
#         # Initialize with all classes selected
#         self.select_all_classes()
        
#         # Initialize display
#         if self.frame_list:
#             self.update_display()
    
#     def load_data(self):
#         """Load all data files."""
#         data_folder = "visualization_data"
        
#         try:
#             # Load histogram data
#             with open(os.path.join(data_folder, "histogram_data.json"), 'r') as f:
#                 self.histogram_data = json.load(f)
            
#             # Load frame info
#             with open(os.path.join(data_folder, "frame_info.json"), 'r') as f:
#                 self.frame_info = json.load(f)
            
#             # Load class mapping
#             with open(os.path.join(data_folder, "class_mapping.json"), 'r') as f:
#                 self.class_mapping = json.load(f)
            
#             # Load frame list
#             with open(os.path.join(data_folder, "frame_list.json"), 'r') as f:
#                 self.frame_list = json.load(f)
                
#             print(f"✅ Loaded {len(self.frame_list)} frames successfully!")
            
#         except FileNotFoundError as e:
#             messagebox.showerror("Error", f"Data files not found: {e}\nPlease run the data preparation script first.")
#             self.root.quit()
    
#     def create_widgets(self):
#         """Create all GUI widgets."""
        
#         # Main container
#         main_frame = ttk.Frame(self.root, padding="10")
#         main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
#         # Configure grid weights
#         self.root.columnconfigure(0, weight=1)
#         self.root.rowconfigure(0, weight=1)
#         main_frame.columnconfigure(0, weight=2)  # Histogram gets more space
#         main_frame.columnconfigure(1, weight=1)  # Image panel
#         main_frame.rowconfigure(0, weight=1)
#         main_frame.rowconfigure(1, weight=1)
        
#         # Left panel for histogram
#         left_panel = ttk.LabelFrame(main_frame, text="Histogram Analysis (Selected Classes)", padding="5")
#         left_panel.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
#         left_panel.columnconfigure(0, weight=1)
#         left_panel.rowconfigure(0, weight=1)
        
#         # Right panel for image
#         right_panel = ttk.LabelFrame(main_frame, text="Detection Results", padding="5")
#         right_panel.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
#         right_panel.columnconfigure(0, weight=1)
#         right_panel.rowconfigure(0, weight=1)
        
#         # Bottom right panel for class selection
#         bottom_right_panel = ttk.LabelFrame(main_frame, text="Class Selector", padding="5")
#         bottom_right_panel.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0), pady=(5, 0))
#         bottom_right_panel.columnconfigure(0, weight=1)
#         bottom_right_panel.rowconfigure(1, weight=1)
        
#         # Histogram canvas
#         self.fig, _ = plt.subplots(figsize=(12, 8))
#         self.histogram_canvas = FigureCanvasTkAgg(self.fig, left_panel)
#         self.histogram_canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
#         # Image display
#         self.image_label = ttk.Label(right_panel)
#         self.image_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
#         # Class selection controls
#         self.create_class_selector(bottom_right_panel)
        
#         # Control panel
#         control_frame = ttk.LabelFrame(main_frame, text="Navigation Controls", padding="10")
#         control_frame.grid(row=1, column=0, columnspan=1, sticky=(tk.W, tk.E), pady=(10, 0))
        
#         # Frame navigation
#         nav_frame = ttk.Frame(control_frame)
#         nav_frame.grid(row=0, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
#         ttk.Button(nav_frame, text="◀◀ First", command=self.go_to_first).grid(row=0, column=0, padx=5)
#         ttk.Button(nav_frame, text="◀ Previous", command=self.previous_frame).grid(row=0, column=1, padx=5)
#         ttk.Button(nav_frame, text="Next ▶", command=self.next_frame).grid(row=0, column=2, padx=5)
#         ttk.Button(nav_frame, text="Last ▶▶", command=self.go_to_last).grid(row=0, column=3, padx=5)
        
#         # Frame info
#         info_frame = ttk.Frame(control_frame)
#         info_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
#         ttk.Label(info_frame, text="Current Frame:").grid(row=0, column=0, padx=5)
#         self.current_frame_label = ttk.Label(info_frame, text="", font=('Arial', 10, 'bold'))
#         self.current_frame_label.grid(row=0, column=1, padx=5)
        
#         ttk.Label(info_frame, text="Frame Index:").grid(row=0, column=2, padx=5)
#         self.frame_index_label = ttk.Label(info_frame, text="", font=('Arial', 10, 'bold'))
#         self.frame_index_label.grid(row=0, column=3, padx=5)
        
#         # Jump to frame
#         jump_frame = ttk.Frame(control_frame)
#         jump_frame.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
#         ttk.Label(jump_frame, text="Jump to Frame:").grid(row=0, column=0, padx=5)
#         self.jump_entry = ttk.Entry(jump_frame, width=10)
#         self.jump_entry.grid(row=0, column=1, padx=5)
#         ttk.Button(jump_frame, text="Go", command=self.jump_to_frame).grid(row=0, column=2, padx=5)
        
#         # Bind Enter key to jump
#         self.jump_entry.bind('<Return>', lambda e: self.jump_to_frame())
        
#         # # Class mapping display
#         # mapping_frame = ttk.LabelFrame(control_frame, text="Class Index Mapping", padding="5")
#         # mapping_frame.grid(row=3, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(10, 0))
        
#         # Create scrollable text widget for mapping
#         mapping_text = tk.Text(mapping_frame, height=4, width=80, wrap=tk.WORD)  # Reduced height
#         mapping_scrollbar = ttk.Scrollbar(mapping_frame, orient=tk.VERTICAL, command=mapping_text.yview)
#         mapping_text.configure(yscrollcommand=mapping_scrollbar.set)
        
#         mapping_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
#         mapping_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
#         # Populate mapping text
#         mapping_str = "Class Index → Name Mapping:\n" + "="*50 + "\n"
#         for idx, name in sorted(self.class_mapping.items(), key=lambda x: int(x[0])):
#             mapping_str += f"Class {idx:2s}: {name}\n"
        
#         mapping_text.insert(tk.END, mapping_str)
#         mapping_text.config(state=tk.DISABLED)
        
#         # Key bindings
#         self.root.bind('<Left>', lambda e: self.previous_frame())
#         self.root.bind('<Right>', lambda e: self.next_frame())
#         self.root.bind('<Home>', lambda e: self.go_to_first())
#         self.root.bind('<End>', lambda e: self.go_to_last())
        
#         # Focus on root for key bindings
#         self.root.focus_set()
    
#     def create_class_selector(self, parent):
#         """Create class selection interface in NxM table format."""
        
#         # Control buttons frame
#         control_buttons = ttk.Frame(parent)
#         control_buttons.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
#         control_buttons.columnconfigure(0, weight=1)
#         control_buttons.columnconfigure(1, weight=1)
        
#         # Select All / Deselect All buttons
#         ttk.Button(control_buttons, text="Select All", 
#                   command=self.select_all_classes).grid(row=0, column=0, padx=(0, 5), sticky=(tk.W, tk.E))
#         ttk.Button(control_buttons, text="Deselect All", 
#                   command=self.deselect_all_classes).grid(row=0, column=1, padx=(5, 0), sticky=(tk.W, tk.E))
        
#         # Status label
#         self.class_status_label = ttk.Label(parent, text="", font=('Arial', 9, 'italic'))
#         self.class_status_label.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
#         # Scrollable frame for class table
#         canvas = tk.Canvas(parent)
#         scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
#         scrollable_frame = ttk.Frame(canvas)
        
#         scrollable_frame.bind(
#             "<Configure>",
#             lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
#         )
        
#         canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
#         canvas.configure(yscrollcommand=scrollbar.set)
        
#         canvas.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
#         scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        
#         # Create class table in NxM format
#         all_class_indices = sorted([int(k) for k in self.class_mapping.keys()])
#         total_classes = len(all_class_indices)
        
#         # Calculate optimal grid size (try to make it roughly square)
#         import math
#         cols = math.ceil(math.sqrt(total_classes))
#         rows = math.ceil(total_classes / cols)
        
#         # Add "Class Name" header at position (0,0)
#         header_label = tk.Label(scrollable_frame, 
#                                text="Class ",
#                                font=('Arial', 8, 'bold'),
#                                bg='#34495E',
#                                fg='white',
#                                relief=tk.RAISED,
#                                bd=2,
#                                width=15,
#                                height=2)
#         header_label.grid(row=0, column=0, padx=1, pady=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
#         # Create class toggle buttons in table format
#         button_index = 0
#         for row in range(1, rows + 1):  # Start from row 1 (row 0 has header)
#             for col in range(cols):
#                 if button_index < total_classes:
#                     class_idx = all_class_indices[button_index]
#                     class_name = self.class_mapping[str(class_idx)]
                    
#                     # Truncate long names for button display
#                     display_name = class_name[:12] + "..." if len(class_name) > 12 else class_name
#                     button_text = f"[{class_idx}]\n{display_name}"
                    
#                     # Create toggle button with fixed size
#                     btn = tk.Button(scrollable_frame, 
#                                    text=button_text,
#                                    command=lambda idx=class_idx: self.toggle_class(idx),
#                                    relief=tk.RAISED,
#                                    bg='#E8F5E8',
#                                    fg='#2E7D32',
#                                    font=('Arial', 7),
#                                    width=15,
#                                    height=2,
#                                    wraplength=100)
                    
#                     btn.grid(row=row, column=col, padx=1, pady=1, sticky=(tk.W, tk.E, tk.N, tk.S))
#                     self.class_buttons[class_idx] = btn
#                     button_index += 1
#                 else:
#                     # Empty cell for incomplete grid
#                     empty_label = tk.Label(scrollable_frame, 
#                                          text="",
#                                          width=15,
#                                          height=2)
#                     empty_label.grid(row=row, column=col, padx=1, pady=1)
        
#         # Configure column weights for uniform sizing
#         for col in range(cols):
#             scrollable_frame.columnconfigure(col, weight=1, minsize=120)
        
#         # Bind mousewheel to canvas
#         def _on_mousewheel(event):
#             canvas.yview_scroll(int(-1*(event.delta/120)), "units")
#         canvas.bind("<MouseWheel>", _on_mousewheel)
        
#         self.update_class_status()
    
#     def toggle_class(self, class_idx):
#         """Toggle class selection and update display."""
#         if class_idx in self.selected_classes:
#             self.selected_classes.remove(class_idx)
#             # Update button appearance - deselected
#             self.class_buttons[class_idx].config(
#                 relief=tk.RAISED,
#                 bg='#FFEBEE',
#                 fg='#C62828'
#             )
#         else:
#             self.selected_classes.add(class_idx)
#             # Update button appearance - selected
#             self.class_buttons[class_idx].config(
#                 relief=tk.SUNKEN,
#                 bg='#E8F5E8',
#                 fg='#2E7D32'
#             )
        
#         self.update_class_status()
#         self.update_display()
    
#     def select_all_classes(self):
#         """Select all classes."""
#         all_class_indices = [int(k) for k in self.class_mapping.keys()]
#         self.selected_classes = set(all_class_indices)
        
#         # Update all button appearances
#         for class_idx in all_class_indices:
#             self.class_buttons[class_idx].config(
#                 relief=tk.SUNKEN,
#                 bg='#E8F5E8',
#                 fg='#2E7D32'
#             )
        
#         self.update_class_status()
#         self.update_display()
    
#     def deselect_all_classes(self):
#         """Deselect all classes."""
#         self.selected_classes.clear()
        
#         # Update all button appearances
#         for class_idx in self.class_buttons:
#             self.class_buttons[class_idx].config(
#                 relief=tk.RAISED,
#                 bg='#FFEBEE',
#                 fg='#C62828'
#             )
        
#         self.update_class_status()
#         self.update_display()
    
#     def update_class_status(self):
#         """Update class selection status label."""
#         total_classes = len(self.class_mapping)
#         selected_count = len(self.selected_classes)
        
#         if selected_count == 0:
#             status_text = "No classes selected"
#         elif selected_count == total_classes:
#             status_text = f"All {total_classes} classes selected"
#         else:
#             status_text = f"{selected_count} of {total_classes} classes selected"
        
#         self.class_status_label.config(text=status_text)
    
#     def create_histogram_plot(self, current_frame_name):
#         """Create comprehensive histogram table with selected classes only."""
#         # Clear the figure
#         self.fig.clear()
        
#         # Check if any classes are selected
#         if not self.selected_classes:
#             ax = self.fig.add_subplot(111)
#             ax.text(0.5, 0.5, 'No classes selected.\nPlease select classes from the right panel.', 
#                    ha='center', va='center', fontsize=16, transform=ax.transAxes)
#             ax.axis('off')
#             self.histogram_canvas.draw()
#             return

#         # Get selected class information (sorted by index)
#         selected_class_indices = sorted(list(self.selected_classes))
#         selected_class_names = [self.class_mapping[str(i)] for i in selected_class_indices]

#         # Score ranges
#         score_ranges = ["90-100%", "80-90%", "70-80%", "60-70%", "50-60%", 
#                        "40-50%", "30-40%", "20-30%", "10-20%", "0-10%"]

#         # Frame labels (0=current, -1=previous, etc.)
#         frame_labels = ["0", "-1", "-2", "-3", "-4"]

#         # Get histogram data for current + last 4 frames (total 5 frames)
#         hist_frames = []
#         frame_names = []
#         current_idx = self.current_frame_index

#         # Collect 5 frames (current + 4 previous)
#         for i in range(current_idx, max(-1, current_idx - 5), -1):
#             if i >= 0 and i < len(self.frame_list):
#                 frame_name = self.frame_list[i]
#                 if frame_name in self.histogram_data:
#                     hist_data = np.array(self.histogram_data[frame_name])
#                     hist_frames.append(hist_data)
#                     frame_names.append(frame_name)

#         # Pad with empty frames if needed
#         while len(hist_frames) < 5:
#             # Use max of all possible class indices for padding
#             all_class_indices = [int(k) for k in self.class_mapping.keys()]
#             hist_frames.append(np.zeros((100, max(all_class_indices) + 1)))
#             frame_names.append("Empty")

#         # Process histogram data for selected classes and all frames
#         all_binned_data = []
#         for hist_data in hist_frames:
#             # Ensure histogram has enough classes
#             all_class_indices = [int(k) for k in self.class_mapping.keys()]
#             if hist_data.shape[1] < max(all_class_indices) + 1:
#                 padded_histogram = np.zeros((100, max(all_class_indices) + 1))
#                 if hist_data.shape[1] > 0:
#                     padded_histogram[:, :hist_data.shape[1]] = hist_data
#                 hist_data = padded_histogram

#             # Select columns for selected classes only
#             selected_columns = hist_data[:, selected_class_indices]

#             # Bin the data (100 bins -> 10 score ranges)
#             try:
#                 binned_counts = selected_columns.reshape(10, 10, len(selected_class_indices)).sum(axis=1)
#             except (ValueError, IndexError):
#                 binned_counts = np.zeros((10, len(selected_class_indices)))

#             all_binned_data.append(binned_counts)

#         # Create single subplot for the comprehensive table
#         ax = self.fig.add_subplot(111)
#         ax.axis('off')

#         # Build table headers with proper structure
#         # Row 0: Score ranges (each spanning 5 columns) + "Class Name" cell
#         main_headers = ['Class Name']  # Header cell at (0,0)

#         # Add score ranges, each appearing once but will span 5 columns
#         for score_range in score_ranges:
#             main_headers.extend([score_range, '', '', '', ''])  # One label + 4 empty for spanning

#         # Row 1: Frame labels repeated under each score range + empty cell for class name header
#         sub_headers = ['']  # Empty cell under "Class Name" header

#         # Add frame labels repeated for each score range
#         for _ in score_ranges:  # For each score range
#             sub_headers.extend(frame_labels)  # Add all 5 frame labels

#         # Build table data with enhanced formatting
#         table_data = []

#         # Add sub-header row
#         table_data.append(sub_headers)

#         # Add data rows for each selected class
#         for class_idx, class_name in enumerate(selected_class_names):
#             # Format class name to fit in 1 cell - REDUCED SIZE
#             short_name = class_name[:12]  # Reduced from 20 to 12 chars
#             class_display = f"{short_name} ({selected_class_indices[class_idx]})"

#             # Create row with class name in single cell
#             row = [class_display]  # Only class name, no empty cells

#             # Add data for each score range and frame combination
#             for score_idx in range(10):
#                 for frame_idx in range(5):
#                     if frame_idx < len(all_binned_data):
#                         try:
#                             value = int(all_binned_data[frame_idx][score_idx, class_idx])
#                             # Enhanced number formatting: h for hundreds, k for thousands
#                             if value >= 99999:
#                                 formatted_value = "99k+"
#                             elif value >= 1000:
#                                 formatted_value = f"{value//1000}k"
#                             elif value >= 100:
#                                 formatted_value = f"{value//100}h"
#                             else:
#                                 formatted_value = str(value)
#                             row.append(formatted_value)
#                         except (IndexError, ValueError):
#                             row.append('0')
#                     else:
#                         row.append('0')

#             table_data.append(row)

#         # Create table with proper structure
#         table = ax.table(cellText=table_data,
#                         colLabels=main_headers,
#                         cellLoc='center',
#                         loc='center',
#                         bbox=[0, 0, 1, 1])

#         # Enhanced styling for better readability
#         table.auto_set_font_size(False)
#         table.set_fontsize(7)  # Slightly larger font
#         table.scale(1.0, 1.0)  # FIXED: Constant scaling to maintain cell sizes

#         # Color scheme for score ranges
#         score_range_colors = ['#FF3333', '#FF5555', '#FF7777', '#FF9999', '#FFBB99',
#                              '#FFDD99', '#DDFF99', '#BBFF99', '#99FF99', '#77FF99']

#         num_cols = len(main_headers)
#         cell_height = 0.05  # Fixed height for all cells

#         # # Set CONSTANT column widths - class name column 3x wider
#         # class_name_width = 3.0 / (num_cols + 2)  # Class name gets 3x weight out of total
#         # data_width = 1.0 / (num_cols + 2)        # Data columns get 1x weight each
        
#         # Set CONSTANT column widths - class name column wider
#         class_name_multiplier = 5.0  # Increase this value to make class name column wider (was 3.0)
#         class_name_width = class_name_multiplier / (num_cols + class_name_multiplier - 1)
#         data_width = 1.0 / (num_cols + class_name_multiplier - 1)
#         for col in range(num_cols):
#             for row in range(len(table_data) + 1):
#                 cell = table[(row, col)]
#                 if col == 0:  # Class name column - 3x wider
#                     cell.set_width(class_name_width)
#                 else:  # Data columns - normal width
#                     cell.set_width(data_width)
#                 cell.set_height(cell_height)  # Same height for all cells

#         # Style main headers (Row 0) - Score ranges + Class Name header
#         for col in range(num_cols):
#             cell = table[(0, col)]
#             if col == 0:  # Class Name header cell
#                 cell.set_facecolor('#2C3E50')
#                 cell.set_text_props(weight='bold', color='white', size=8)
#                 cell.set_edgecolor('white')
#             else:
#                 # Score range headers
#                 score_idx = (col - 1) // 5
#                 if score_idx < len(score_range_colors) and (col - 1) % 5 == 0:
#                     # This is the first column of a score range - show the label
#                     cell.set_facecolor(score_range_colors[score_idx])
#                     cell.set_text_props(weight='bold', color='black', size=8)
#                 else:
#                     # This is a continuation of the score range - same color, no text
#                     score_idx = (col - 1) // 5
#                     if score_idx < len(score_range_colors):
#                         cell.set_facecolor(score_range_colors[score_idx])
#                         cell.set_text_props(color=score_range_colors[score_idx], size=1)  # Hide text
#             cell.set_edgecolor('white')
#             cell.set_linewidth(2)

#         # Style sub-headers (Row 1) - Frame labels
#         for col in range(num_cols):
#             cell = table[(1, col)]
#             if col == 0:  # Class name area
#                 cell.set_facecolor('#2C3E50')
#                 cell.set_text_props(color='white', size=1)  # Hide text
#                 cell.set_edgecolor('white')
#             else:
#                 # Frame labels
#                 frame_idx = (col - 1) % 5
#                 score_idx = (col - 1) // 5

#                 if frame_idx == 0:  # Current frame
#                     cell.set_facecolor('#E74C3C')
#                     cell.set_text_props(weight='bold', color='white', size=8)
#                 else:
#                     if score_idx < len(score_range_colors):
#                         base_color = score_range_colors[score_idx]
#                         cell.set_facecolor(base_color)
#                         cell.set_text_props(weight='bold', color='black', size=8)
#             cell.set_edgecolor('white')
#             cell.set_linewidth(2)

#         # Style data cells
#         for row in range(2, len(table_data) + 1):
#             for col in range(num_cols):
#                 cell = table[(row, col)]

#                 if col == 0:  # Class name column
#                     cell.set_facecolor('#ECF0F1')
#                     cell.set_text_props(weight='bold', size=7, ha='left')  # Reduced font size
#                     cell.set_edgecolor('#BDC3C7')
#                     cell.set_linewidth(2)
#                 else:
#                     # Data cells
#                     try:
#                         value_str = table_data[row-1][col]

#                         # Parse formatted values back to numbers for color intensity
#                         if value_str.endswith('k+'):
#                             value = 99999
#                         elif value_str.endswith('k'):
#                             value = int(value_str[:-1]) * 1000
#                         elif value_str.endswith('h'):
#                             value = int(value_str[:-1]) * 100
#                         else:
#                             value = int(value_str) if value_str.isdigit() else 0

#                         frame_idx = (col - 1) % 5
#                         score_idx = (col - 1) // 5

#                         if value > 0:
#                             # Calculate color intensity
#                             class_row_idx = row - 2
#                             max_val = 0

#                             # Find max value for this class
#                             for c in range(1, num_cols):
#                                 try:
#                                     check_val_str = table_data[class_row_idx + 1][c]
#                                     if check_val_str.endswith('k+'):
#                                         check_val = 99999
#                                     elif check_val_str.endswith('k'):
#                                         check_val = int(check_val_str[:-1]) * 1000
#                                     elif check_val_str.endswith('h'):
#                                         check_val = int(check_val_str[:-1]) * 100
#                                     else:
#                                         check_val = int(check_val_str) if check_val_str.isdigit() else 0
#                                     max_val = max(max_val, check_val)
#                                 except (ValueError, IndexError):
#                                     pass
                                
#                             if max_val > 0:
#                                 intensity = min(value / max_val, 1.0)

#                                 if score_idx < len(score_range_colors):
#                                     base_color = score_range_colors[score_idx]
#                                     r = int(base_color[1:3], 16) / 255.0
#                                     g = int(base_color[3:5], 16) / 255.0
#                                     b = int(base_color[5:7], 16) / 255.0

#                                     alpha = 0.3 + intensity * 0.7
#                                     cell.set_facecolor((r, g, b, alpha))

#                                     # High value indicator
#                                     if intensity > 0.7:
#                                         cell.set_edgecolor('#2C3E50')
#                                         cell.set_linewidth(2)

#                                 # Highlight current frame
#                                 if frame_idx == 0:
#                                     cell.set_edgecolor('#E74C3C')
#                                     cell.set_linewidth(3)
#                                     cell.set_text_props(weight='bold', size=8, color='darkred')
#                                 else:
#                                     cell.set_text_props(size=8)
#                             else:
#                                 cell.set_facecolor('#FFFFFF')
#                                 cell.set_text_props(size=8)
#                         else:
#                             cell.set_facecolor('#F8F9FA')
#                             cell.set_text_props(size=8, color='gray')

#                     except (ValueError, IndexError):
#                         cell.set_facecolor('#FFFFFF')
#                         cell.set_text_props(size=8)

#                     # Grid lines for data cells
#                     cell.set_edgecolor('#D5DBDB')
#                     cell.set_linewidth(0.5)

#         # Enhanced title
#         selected_count = len(self.selected_classes)
#         total_count = len(self.class_mapping)
#         title = f'Medical Image Histogram Analysis - Frame {current_idx + 1}/{len(self.frame_list)} ({current_frame_name}) | {selected_count}/{total_count} Classes'
#         self.fig.suptitle(title, fontsize=12, fontweight='bold', y=0.98)

#         # Enhanced subtitle
#         subtitle = f'Showing {selected_count} selected classes | Toggle classes in right panel'
#         ax.text(0.5, 0.02, subtitle, transform=ax.transAxes, fontsize=9, 
#                ha='center', style='italic', color='gray')

#         # Adjust layout
#         plt.subplots_adjust(left=0.01, right=0.99, top=0.95, bottom=0.05)

#         # Draw the canvas
#         self.histogram_canvas.draw()
        
#     def load_and_display_image(self, frame_name):
#         """Load and display the cropped image with detections."""
#         image_path = os.path.join("visualization_data", "cropped_images", f"{frame_name}.jpg")
        
#         if os.path.exists(image_path):
#             try:
#                 # Load image
#                 img = cv2.imread(image_path)
#                 img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                
#                 # Resize image to fit in the panel (max 600x600)
#                 h, w = img_rgb.shape[:2]
#                 max_size = 600
                
#                 if h > max_size or w > max_size:
#                     scale = min(max_size / h, max_size / w)
#                     new_h, new_w = int(h * scale), int(w * scale)
#                     img_rgb = cv2.resize(img_rgb, (new_w, new_h))
                
#                 # Convert to PhotoImage
#                 img_pil = Image.fromarray(img_rgb)
#                 img_tk = ImageTk.PhotoImage(img_pil)
                
#                 # Update label
#                 self.image_label.configure(image=img_tk, text="")
#                 self.image_label.image = img_tk  # Keep a reference
                
#             except Exception as e:
#                 self.image_label.configure(image='', text=f"Error loading image:\n{e}")
#         else:
#             # Show placeholder if image not found
#             self.image_label.configure(image='', text=f"Image not found:\n{frame_name}")
    
#     def update_display(self):
#         """Update both histogram and image display."""
#         if not self.frame_list:
#             return
        
#         current_frame = self.frame_list[self.current_frame_index]
        
#         try:
#             # Update histogram
#             self.create_histogram_plot(current_frame)
            
#             # Update image
#             self.load_and_display_image(current_frame)
            
#             # Update labels
#             self.current_frame_label.configure(text=current_frame)
#             self.frame_index_label.configure(text=f"{self.current_frame_index + 1} / {len(self.frame_list)}")
            
#             # Update window title
#             self.root.title(f"Medical Image Visualization - Frame: {current_frame}")
            
#         except Exception as e:
#             print(f"Error updating display: {e}")
#             messagebox.showerror("Error", f"Error updating display: {e}")
    
#     def next_frame(self):
#         """Go to next frame."""
#         if self.current_frame_index < len(self.frame_list) - 1:
#             self.current_frame_index += 1
#             self.update_display()
    
#     def previous_frame(self):
#         """Go to previous frame."""
#         if self.current_frame_index > 0:
#             self.current_frame_index -= 1
#             self.update_display()
    
#     def go_to_first(self):
#         """Go to first frame."""
#         self.current_frame_index = 0
#         self.update_display()
    
#     def go_to_last(self):
#         """Go to last frame."""
#         self.current_frame_index = len(self.frame_list) - 1
#         self.update_display()
    
#     def jump_to_frame(self):
#         """Jump to specific frame number."""
#         try:
#             frame_num = int(self.jump_entry.get())
#             if 1 <= frame_num <= len(self.frame_list):
#                 self.current_frame_index = frame_num - 1
#                 self.update_display()
#                 self.jump_entry.delete(0, tk.END)
#             else:
#                 messagebox.showerror("Error", f"Frame number must be between 1 and {len(self.frame_list)}")
#         except ValueError:
#             messagebox.showerror("Error", "Please enter a valid frame number")

# def main():
#     """Main function to run the visualization tool."""
    
#     # Check if data folder exists
#     if not os.path.exists("visualization_data"):
#         print("❌ Error: 'visualization_data' folder not found!")
#         print("Please run the data preparation script first.")
#         return
    
#     # Create and run the application
#     root = tk.Tk()
#     app = MedicalImageVisualizationTool(root)
    
#     # Add some styling
#     style = ttk.Style()
#     style.theme_use('clam')#!/usr/bin/env python3
# """
# Interactive Histogram Visualization Tool for Medical Image Analysis
# Shows comprehensive histogram tables and detection results with navigation controls.
# """

# import tkinter as tk
# from tkinter import ttk, messagebox
# import cv2
# import numpy as np
# import json
# import os
# from PIL import Image, ImageTk
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# class MedicalImageVisualizationTool:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Medical Image Histogram Visualization Tool")
#         self.root.geometry("1800x1000")  # Increased width for class selector
#         self.root.configure(bg='#f0f0f0')
        
#         # Data variables
#         self.histogram_data = {}
#         self.frame_info = {}
#         self.class_mapping = {}
#         self.frame_list = []
#         self.current_frame_index = 0
        
#         # Class selection variables
#         self.selected_classes = set()  # Set of selected class indices
#         self.class_buttons = {}  # Dictionary to store class button references
        
#         # Load data
#         self.load_data()
        
#         # Create GUI
#         self.create_widgets()
        
#         # Initialize with all classes selected
#         self.select_all_classes()
        
#         # Initialize display
#         if self.frame_list:
#             self.update_display()
    
#     def load_data(self):
#         """Load all data files."""
#         data_folder = "visualization_data"
        
#         try:
#             # Load histogram data
#             with open(os.path.join(data_folder, "histogram_data.json"), 'r') as f:
#                 self.histogram_data = json.load(f)
            
#             # Load frame info
#             with open(os.path.join(data_folder, "frame_info.json"), 'r') as f:
#                 self.frame_info = json.load(f)
            
#             # Load class mapping
#             with open(os.path.join(data_folder, "class_mapping.json"), 'r') as f:
#                 self.class_mapping = json.load(f)
            
#             # Load frame list
#             with open(os.path.join(data_folder, "frame_list.json"), 'r') as f:
#                 self.frame_list = json.load(f)
                
#             print(f"✅ Loaded {len(self.frame_list)} frames successfully!")
            
#         except FileNotFoundError as e:
#             messagebox.showerror("Error", f"Data files not found: {e}\nPlease run the data preparation script first.")
#             self.root.quit()
    
#     def create_widgets(self):
#         """Create all GUI widgets."""
        
#         # Main container
#         main_frame = ttk.Frame(self.root, padding="10")
#         main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
#         # Configure grid weights
#         self.root.columnconfigure(0, weight=1)
#         self.root.rowconfigure(0, weight=1)
#         main_frame.columnconfigure(0, weight=1)  # Histogram panel - equal weight
#         main_frame.columnconfigure(1, weight=1)  # Image panel - equal weight
#         main_frame.rowconfigure(0, weight=1)
#         main_frame.rowconfigure(1, weight=1)
        
#         # Left panel for histogram
#         left_panel = ttk.LabelFrame(main_frame, text="Histogram Analysis (Selected Classes)", padding="5")
#         left_panel.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
#         left_panel.columnconfigure(0, weight=1)
#         left_panel.rowconfigure(0, weight=1)
        
#         # Right panel for image
#         right_panel = ttk.LabelFrame(main_frame, text="Detection Results", padding="5")
#         right_panel.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
#         right_panel.columnconfigure(0, weight=1)
#         right_panel.rowconfigure(0, weight=1)
        
#         # Bottom right panel for class selection
#         bottom_right_panel = ttk.LabelFrame(main_frame, text="Class Selector", padding="5")
#         bottom_right_panel.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0), pady=(5, 0))
#         bottom_right_panel.columnconfigure(0, weight=1)
#         bottom_right_panel.rowconfigure(1, weight=1)
        
#         # Histogram canvas
#         self.fig, _ = plt.subplots(figsize=(12, 8))
#         self.histogram_canvas = FigureCanvasTkAgg(self.fig, left_panel)
#         self.histogram_canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
#         # Image display
#         self.image_label = ttk.Label(right_panel)
#         self.image_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
#         # Class selection controls
#         self.create_class_selector(bottom_right_panel)
        
#         # Control panel
#         control_frame = ttk.LabelFrame(main_frame, text="Navigation Controls", padding="10")
#         control_frame.grid(row=1, column=0, columnspan=1, sticky=(tk.W, tk.E), pady=(10, 0))
        
#         # Frame navigation
#         nav_frame = ttk.Frame(control_frame)
#         nav_frame.grid(row=0, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
#         ttk.Button(nav_frame, text="◀◀ First", command=self.go_to_first).grid(row=0, column=0, padx=5)
#         ttk.Button(nav_frame, text="◀ Previous", command=self.previous_frame).grid(row=0, column=1, padx=5)
#         ttk.Button(nav_frame, text="Next ▶", command=self.next_frame).grid(row=0, column=2, padx=5)
#         ttk.Button(nav_frame, text="Last ▶▶", command=self.go_to_last).grid(row=0, column=3, padx=5)
        
#         # Frame info
#         info_frame = ttk.Frame(control_frame)
#         info_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
#         ttk.Label(info_frame, text="Current Frame:").grid(row=0, column=0, padx=5)
#         self.current_frame_label = ttk.Label(info_frame, text="", font=('Arial', 10, 'bold'))
#         self.current_frame_label.grid(row=0, column=1, padx=5)
        
#         ttk.Label(info_frame, text="Frame Index:").grid(row=0, column=2, padx=5)
#         self.frame_index_label = ttk.Label(info_frame, text="", font=('Arial', 10, 'bold'))
#         self.frame_index_label.grid(row=0, column=3, padx=5)
        
#         # Jump to frame
#         jump_frame = ttk.Frame(control_frame)
#         jump_frame.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
#         ttk.Label(jump_frame, text="Jump to Frame:").grid(row=0, column=0, padx=5)
#         self.jump_entry = ttk.Entry(jump_frame, width=10)
#         self.jump_entry.grid(row=0, column=1, padx=5)
#         ttk.Button(jump_frame, text="Go", command=self.jump_to_frame).grid(row=0, column=2, padx=5)
        
#         # Bind Enter key to jump
#         self.jump_entry.bind('<Return>', lambda e: self.jump_to_frame())
        
#         # Class mapping display
#         mapping_frame = ttk.LabelFrame(control_frame, text="Class Index Mapping", padding="5")
#         mapping_frame.grid(row=3, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(10, 0))
        
#         # Create scrollable text widget for mapping
#         mapping_text = tk.Text(mapping_frame, height=4, width=80, wrap=tk.WORD)  # Reduced height
#         mapping_scrollbar = ttk.Scrollbar(mapping_frame, orient=tk.VERTICAL, command=mapping_text.yview)
#         mapping_text.configure(yscrollcommand=mapping_scrollbar.set)
        
#         mapping_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
#         mapping_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
#         # Populate mapping text
#         mapping_str = "Class Index → Name Mapping:\n" + "="*50 + "\n"
#         for idx, name in sorted(self.class_mapping.items(), key=lambda x: int(x[0])):
#             mapping_str += f"Class {idx:2s}: {name}\n"
        
#         mapping_text.insert(tk.END, mapping_str)
#         mapping_text.config(state=tk.DISABLED)
        
#         # Key bindings
#         self.root.bind('<Left>', lambda e: self.previous_frame())
#         self.root.bind('<Right>', lambda e: self.next_frame())
#         self.root.bind('<Home>', lambda e: self.go_to_first())
#         self.root.bind('<End>', lambda e: self.go_to_last())
        
#         # Focus on root for key bindings
#         self.root.focus_set()
    
#     def create_class_selector(self, parent):
#         """Create class selection interface in NxM table format."""

#         # ========== CONFIGURATION SECTION ==========
#         # Set your desired grid dimensions here
#         FIXED_COLS = 5  # Set N (number of columns) - change this value
#         FIXED_ROWS = None  # Set M (number of rows) - set to None for auto-calculation or specific number

#         # Cell size configuration
#         CELL_WIDTH = 13      # Width of each class button (characters)
#         CELL_HEIGHT = 2      # Height of each class button (lines)
#         MIN_COL_SIZE = 100   # Minimum column size in pixels

#         # Text configuration
#         MAX_CLASS_NAME_LENGTH = 15  # Maximum characters to show in class name
#         BUTTON_FONT_SIZE = 10        # Font size for buttons
#         # ==========================================

#         # Control buttons frame
#         control_buttons = ttk.Frame(parent)
#         control_buttons.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
#         control_buttons.columnconfigure(0, weight=1)
#         control_buttons.columnconfigure(1, weight=1)

#         # Select All / Deselect All buttons
#         ttk.Button(control_buttons, text="Select All", 
#                   command=self.select_all_classes).grid(row=0, column=0, padx=(0, 5), sticky=(tk.W, tk.E))
#         ttk.Button(control_buttons, text="Deselect All", 
#                   command=self.deselect_all_classes).grid(row=0, column=1, padx=(5, 0), sticky=(tk.W, tk.E))

#         # Status label
#         self.class_status_label = ttk.Label(parent, text="", font=('Arial', 9, 'italic'))
#         self.class_status_label.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(5, 0))

#         # Scrollable frame for class table
#         canvas = tk.Canvas(parent)
#         scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
#         scrollable_frame = ttk.Frame(canvas)

#         scrollable_frame.bind(
#             "<Configure>",
#             lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
#         )

#         canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
#         canvas.configure(yscrollcommand=scrollbar.set)

#         canvas.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
#         scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))

#         # Create class table in NxM format
#         all_class_indices = sorted([int(k) for k in self.class_mapping.keys()])
#         total_classes = len(all_class_indices)

#         # Calculate grid dimensions based on configuration
#         import math
#         if FIXED_COLS:
#             cols = FIXED_COLS
#             if FIXED_ROWS:
#                 rows = FIXED_ROWS
#             else:
#                 rows = math.ceil(total_classes / cols)
#         else:
#             # Auto-calculate (original behavior)
#             cols = math.ceil(math.sqrt(total_classes))
#             rows = math.ceil(total_classes / cols)

#         print(f"Grid Configuration: {rows} rows × {cols} columns for {total_classes} classes")

#         # Add "Class Name" header at position (0,0)
#         header_label = tk.Label(scrollable_frame, 
#                                text="Class Name",
#                                font=('Arial', 8, 'bold'),
#                                bg='#34495E',
#                                fg='white',
#                                relief=tk.RAISED,
#                                bd=2,
#                                width=CELL_WIDTH,
#                                height=CELL_HEIGHT)
#         header_label.grid(row=0, column=0, padx=1, pady=1, sticky=(tk.W, tk.E, tk.N, tk.S))

#         # Create class toggle buttons in table format
#         button_index = 0
#         for row in range(1, rows + 1):  # Start from row 1 (row 0 has header)
#             for col in range(cols):
#                 if button_index < total_classes:
#                     class_idx = all_class_indices[button_index]
#                     class_name = self.class_mapping[str(class_idx)]

#                     # Truncate long names for button display
#                     display_name = class_name[:MAX_CLASS_NAME_LENGTH] + "..." if len(class_name) > MAX_CLASS_NAME_LENGTH else class_name
#                     button_text = f"[{class_idx}]\n{display_name}"

#                     # Create toggle button with configured size
#                     btn = tk.Button(scrollable_frame, 
#                                    text=button_text,
#                                    command=lambda idx=class_idx: self.toggle_class(idx),
#                                    relief=tk.RAISED,
#                                    bg='#E8F5E8',
#                                    fg='#2E7D32',
#                                    font=('Arial', BUTTON_FONT_SIZE),
#                                    width=CELL_WIDTH,
#                                    height=CELL_HEIGHT,
#                                    wraplength=MIN_COL_SIZE - 20)  # Wrap text based on column size

#                     btn.grid(row=row, column=col, padx=1, pady=1, sticky=(tk.W, tk.E, tk.N, tk.S))
#                     self.class_buttons[class_idx] = btn
#                     button_index += 1
#                 else:
#                     # Empty cell for incomplete grid
#                     empty_label = tk.Label(scrollable_frame, 
#                                          text="",
#                                          width=CELL_WIDTH,
#                                          height=CELL_HEIGHT)
#                     empty_label.grid(row=row, column=col, padx=1, pady=1)

#         # Configure column weights for uniform sizing
#         for col in range(cols):
#             scrollable_frame.columnconfigure(col, weight=1, minsize=MIN_COL_SIZE)

#         # Bind mousewheel to canvas
#         def _on_mousewheel(event):
#             canvas.yview_scroll(int(-1*(event.delta/120)), "units")
#         canvas.bind("<MouseWheel>", _on_mousewheel)

#         self.update_class_status() 
        
#     def toggle_class(self, class_idx):
#         """Toggle class selection and update display."""
#         if class_idx in self.selected_classes:
#             self.selected_classes.remove(class_idx)
#             # Update button appearance - deselected
#             self.class_buttons[class_idx].config(
#                 relief=tk.RAISED,
#                 bg='#FFEBEE',
#                 fg='#C62828'
#             )
#         else:
#             self.selected_classes.add(class_idx)
#             # Update button appearance - selected
#             self.class_buttons[class_idx].config(
#                 relief=tk.SUNKEN,
#                 bg='#E8F5E8',
#                 fg='#2E7D32'
#             )
#         self.update_class_status()
#         self.update_display()

#     def select_all_classes(self):
#         """Select all classes."""
#         all_class_indices = [int(k) for k in self.class_mapping.keys()]
#         self.selected_classes = set(all_class_indices)
        
#         # Update all button appearances
#         for class_idx in all_class_indices:
#             self.class_buttons[class_idx].config(
#                 relief=tk.SUNKEN,
#                 bg='#E8F5E8',
#                 fg='#2E7D32'
#             )
        
#         self.update_class_status()
#         self.update_display()
    
#     def deselect_all_classes(self):
#         """Deselect all classes."""
#         self.selected_classes.clear()
        
#         # Update all button appearances
#         for class_idx in self.class_buttons:
#             self.class_buttons[class_idx].config(
#                 relief=tk.RAISED,
#                 bg='#FFEBEE',
#                 fg='#C62828'
#             )
        
#         self.update_class_status()
#         self.update_display()
    
#     def update_class_status(self):
#         """Update class selection status label."""
#         total_classes = len(self.class_mapping)
#         selected_count = len(self.selected_classes)
        
#         if selected_count == 0:
#             status_text = "No classes selected"
#         elif selected_count == total_classes:
#             status_text = f"All {total_classes} classes selected"
#         else:
#             status_text = f"{selected_count} of {total_classes} classes selected"
        
#         self.class_status_label.config(text=status_text)
    
#     def create_histogram_plot(self, current_frame_name):
#         """Create comprehensive histogram table with selected classes only."""
#         # Clear the figure
#         self.fig.clear()
        
#         # Check if any classes are selected
#         if not self.selected_classes:
#             ax = self.fig.add_subplot(111)
#             ax.text(0.5, 0.5, 'No classes selected.\nPlease select classes from the right panel.', 
#                    ha='center', va='center', fontsize=16, transform=ax.transAxes)
#             ax.axis('off')
#             self.histogram_canvas.draw()
#             return

#         # Get selected class information (sorted by index)
#         selected_class_indices = sorted(list(self.selected_classes))
#         selected_class_names = [self.class_mapping[str(i)] for i in selected_class_indices]

#         # Score ranges
#         score_ranges = ["90-100%", "80-90%", "70-80%", "60-70%", "50-60%", 
#                        "40-50%", "30-40%", "20-30%", "10-20%", "0-10%"]

#         # Frame labels (0=current, -1=previous, etc.)
#         frame_labels = ["0", "-1", "-2", "-3", "-4"]

#         # Get histogram data for current + last 4 frames (total 5 frames)
#         hist_frames = []
#         frame_names = []
#         current_idx = self.current_frame_index

#         # Collect 5 frames (current + 4 previous)
#         for i in range(current_idx, max(-1, current_idx - 5), -1):
#             if i >= 0 and i < len(self.frame_list):
#                 frame_name = self.frame_list[i]
#                 if frame_name in self.histogram_data:
#                     hist_data = np.array(self.histogram_data[frame_name])
#                     hist_frames.append(hist_data)
#                     frame_names.append(frame_name)

#         # Pad with empty frames if needed
#         while len(hist_frames) < 5:
#             # Use max of all possible class indices for padding
#             all_class_indices = [int(k) for k in self.class_mapping.keys()]
#             hist_frames.append(np.zeros((100, max(all_class_indices) + 1)))
#             frame_names.append("Empty")

#         # Process histogram data for selected classes and all frames
#         all_binned_data = []
#         for hist_data in hist_frames:
#             # Ensure histogram has enough classes
#             all_class_indices = [int(k) for k in self.class_mapping.keys()]
#             if hist_data.shape[1] < max(all_class_indices) + 1:
#                 padded_histogram = np.zeros((100, max(all_class_indices) + 1))
#                 if hist_data.shape[1] > 0:
#                     padded_histogram[:, :hist_data.shape[1]] = hist_data
#                 hist_data = padded_histogram

#             # Select columns for selected classes only
#             selected_columns = hist_data[:, selected_class_indices]

#             # Bin the data (100 bins -> 10 score ranges)
#             try:
#                 binned_counts = selected_columns.reshape(10, 10, len(selected_class_indices)).sum(axis=1)
#             except (ValueError, IndexError):
#                 binned_counts = np.zeros((10, len(selected_class_indices)))

#             all_binned_data.append(binned_counts)

#         # Create single subplot for the comprehensive table
#         ax = self.fig.add_subplot(111)
#         ax.axis('off')

#         # Build table headers with proper structure
#         # Row 0: Score ranges (each spanning 5 columns) + "Class Name" cell
#         main_headers = ['Class Name']  # Header cell at (0,0)

#         # Add score ranges, each appearing once but will span 5 columns
#         for score_range in score_ranges:
#             main_headers.extend([score_range, '', '', '', ''])  # One label + 4 empty for spanning

#         # Row 1: Frame labels repeated under each score range + empty cell for class name header
#         sub_headers = ['']  # Empty cell under "Class Name" header

#         # Add frame labels repeated for each score range
#         for _ in score_ranges:  # For each score range
#             sub_headers.extend(frame_labels)  # Add all 5 frame labels

#         # Build table data with enhanced formatting
#         table_data = []

#         # Add sub-header row
#         table_data.append(sub_headers)

#         # Add data rows for each selected class
#         for class_idx, class_name in enumerate(selected_class_names):
#             # Format class name to fit in 1 cell - REDUCED SIZE
#             short_name = class_name[:12]  # Reduced from 20 to 12 chars
#             class_display = f"{short_name} ({selected_class_indices[class_idx]})"

#             # Create row with class name in single cell
#             row = [class_display]  # Only class name, no empty cells

#             # Add data for each score range and frame combination
#             for score_idx in range(10):
#                 for frame_idx in range(5):
#                     if frame_idx < len(all_binned_data):
#                         try:
#                             value = int(all_binned_data[frame_idx][score_idx, class_idx])
#                             # Enhanced number formatting: h for hundreds, k for thousands
#                             if value >= 99999:
#                                 formatted_value = "99k+"
#                             elif value >= 1000:
#                                 formatted_value = f"{value//1000}k"
#                             elif value >= 100:
#                                 formatted_value = f"{value//100}h"
#                             else:
#                                 formatted_value = str(value)
#                             row.append(formatted_value)
#                         except (IndexError, ValueError):
#                             row.append('0')
#                     else:
#                         row.append('0')

#             table_data.append(row)

#         # Create table with proper structure
#         table = ax.table(cellText=table_data,
#                         colLabels=main_headers,
#                         cellLoc='center',
#                         loc='center',
#                         bbox=[0, 0, 1, 1])

#         # Enhanced styling for better readability
#         table.auto_set_font_size(False)
#         table.set_fontsize(7)  # Slightly larger font
#         table.scale(1.0, 1.0)  # FIXED: Constant scaling to maintain cell sizes

#         # Color scheme for score ranges
#         score_range_colors = ['#FF3333', '#FF5555', '#FF7777', '#FF9999', '#FFBB99',
#                              '#FFDD99', '#DDFF99', '#BBFF99', '#99FF99', '#77FF99']

#         num_cols = len(main_headers)
#         cell_height = 0.05  # Fixed height for all cells

#         # Set CONSTANT column widths - class name column 3x wider
#         class_name_width = 3.0 / (num_cols + 2)  # Class name gets 3x weight out of total
#         data_width = 1.0 / (num_cols + 2)        # Data columns get 1x weight each
        
#         for col in range(num_cols):
#             for row in range(len(table_data) + 1):
#                 cell = table[(row, col)]
#                 if col == 0:  # Class name column - 3x wider
#                     cell.set_width(class_name_width)
#                 else:  # Data columns - normal width
#                     cell.set_width(data_width)
#                 cell.set_height(cell_height)  # Same height for all cells

#         # Style main headers (Row 0) - Score ranges + Class Name header
#         for col in range(num_cols):
#             cell = table[(0, col)]
#             if col == 0:  # Class Name header cell
#                 cell.set_facecolor('#2C3E50')
#                 cell.set_text_props(weight='bold', color='white', size=8)
#                 cell.set_edgecolor('white')
#             else:
#                 # Score range headers
#                 score_idx = (col - 1) // 5
#                 if score_idx < len(score_range_colors) and (col - 1) % 5 == 0:
#                     # This is the first column of a score range - show the label
#                     cell.set_facecolor(score_range_colors[score_idx])
#                     cell.set_text_props(weight='bold', color='black', size=8)
#                 else:
#                     # This is a continuation of the score range - same color, no text
#                     score_idx = (col - 1) // 5
#                     if score_idx < len(score_range_colors):
#                         cell.set_facecolor(score_range_colors[score_idx])
#                         cell.set_text_props(color=score_range_colors[score_idx], size=1)  # Hide text
#             cell.set_edgecolor('white')
#             cell.set_linewidth(2)

#         # Style sub-headers (Row 1) - Frame labels
#         for col in range(num_cols):
#             cell = table[(1, col)]
#             if col == 0:  # Class name area
#                 cell.set_facecolor('#2C3E50')
#                 cell.set_text_props(color='white', size=1)  # Hide text
#                 cell.set_edgecolor('white')
#             else:
#                 # Frame labels
#                 frame_idx = (col - 1) % 5
#                 score_idx = (col - 1) // 5

#                 if frame_idx == 0:  # Current frame
#                     cell.set_facecolor('#E74C3C')
#                     cell.set_text_props(weight='bold', color='white', size=8)
#                 else:
#                     if score_idx < len(score_range_colors):
#                         base_color = score_range_colors[score_idx]
#                         cell.set_facecolor(base_color)
#                         cell.set_text_props(weight='bold', color='black', size=8)
#             cell.set_edgecolor('white')
#             cell.set_linewidth(2)

#         # Style data cells
#         for row in range(2, len(table_data) + 1):
#             for col in range(num_cols):
#                 cell = table[(row, col)]

#                 if col == 0:  # Class name column
#                     cell.set_facecolor('#ECF0F1')
#                     cell.set_text_props(weight='bold', size=7, ha='left')  # Reduced font size
#                     cell.set_edgecolor('#BDC3C7')
#                     cell.set_linewidth(2)
#                 else:
#                     # Data cells
#                     try:
#                         value_str = table_data[row-1][col]

#                         # Parse formatted values back to numbers for color intensity
#                         if value_str.endswith('k+'):
#                             value = 99999
#                         elif value_str.endswith('k'):
#                             value = int(value_str[:-1]) * 1000
#                         elif value_str.endswith('h'):
#                             value = int(value_str[:-1]) * 100
#                         else:
#                             value = int(value_str) if value_str.isdigit() else 0

#                         frame_idx = (col - 1) % 5
#                         score_idx = (col - 1) // 5

#                         if value > 0:
#                             # Calculate color intensity
#                             class_row_idx = row - 2
#                             max_val = 0

#                             # Find max value for this class
#                             for c in range(1, num_cols):
#                                 try:
#                                     check_val_str = table_data[class_row_idx + 1][c]
#                                     if check_val_str.endswith('k+'):
#                                         check_val = 99999
#                                     elif check_val_str.endswith('k'):
#                                         check_val = int(check_val_str[:-1]) * 1000
#                                     elif check_val_str.endswith('h'):
#                                         check_val = int(check_val_str[:-1]) * 100
#                                     else:
#                                         check_val = int(check_val_str) if check_val_str.isdigit() else 0
#                                     max_val = max(max_val, check_val)
#                                 except (ValueError, IndexError):
#                                     pass
                                
#                             if max_val > 0:
#                                 intensity = min(value / max_val, 1.0)

#                                 if score_idx < len(score_range_colors):
#                                     base_color = score_range_colors[score_idx]
#                                     r = int(base_color[1:3], 16) / 255.0
#                                     g = int(base_color[3:5], 16) / 255.0
#                                     b = int(base_color[5:7], 16) / 255.0

#                                     alpha = 0.3 + intensity * 0.7
#                                     cell.set_facecolor((r, g, b, alpha))

#                                     # High value indicator
#                                     if intensity > 0.7:
#                                         cell.set_edgecolor('#2C3E50')
#                                         cell.set_linewidth(2)

#                                 # Highlight current frame
#                                 if frame_idx == 0:
#                                     cell.set_edgecolor('#E74C3C')
#                                     cell.set_linewidth(3)
#                                     cell.set_text_props(weight='bold', size=8, color='darkred')
#                                 else:
#                                     cell.set_text_props(size=8)
#                             else:
#                                 cell.set_facecolor('#FFFFFF')
#                                 cell.set_text_props(size=8)
#                         else:
#                             cell.set_facecolor('#F8F9FA')
#                             cell.set_text_props(size=8, color='gray')

#                     except (ValueError, IndexError):
#                         cell.set_facecolor('#FFFFFF')
#                         cell.set_text_props(size=8)

#                     # Grid lines for data cells
#                     cell.set_edgecolor('#D5DBDB')
#                     cell.set_linewidth(0.5)

#         # Enhanced title
#         selected_count = len(self.selected_classes)
#         total_count = len(self.class_mapping)
#         title = f'Medical Image Histogram Analysis - Frame {current_idx + 1}/{len(self.frame_list)} ({current_frame_name}) | {selected_count}/{total_count} Classes'
#         self.fig.suptitle(title, fontsize=12, fontweight='bold', y=0.98)

#         # Enhanced subtitle
#         subtitle = f'Showing {selected_count} selected classes | Toggle classes in right panel'
#         ax.text(0.5, 0.02, subtitle, transform=ax.transAxes, fontsize=9, 
#                ha='center', style='italic', color='gray')

#         # Adjust layout
#         plt.subplots_adjust(left=0.01, right=0.99, top=0.95, bottom=0.05)

#         # Draw the canvas
#         self.histogram_canvas.draw()
        
#     def load_and_display_image(self, frame_name):
#         """Load and display the cropped image with detections."""
#         image_path = os.path.join("visualization_data", "cropped_images", f"{frame_name}.jpg")
        
#         if os.path.exists(image_path):
#             try:
#                 # Load image
#                 img = cv2.imread(image_path)
#                 img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                
#                 # Resize image to fit in the panel (max 600x600)
#                 h, w = img_rgb.shape[:2]
#                 max_size = 600
                
#                 if h > max_size or w > max_size:
#                     scale = min(max_size / h, max_size / w)
#                     new_h, new_w = int(h * scale), int(w * scale)
#                     img_rgb = cv2.resize(img_rgb, (new_w, new_h))
                
#                 # Convert to PhotoImage
#                 img_pil = Image.fromarray(img_rgb)
#                 img_tk = ImageTk.PhotoImage(img_pil)
                
#                 # Update label
#                 self.image_label.configure(image=img_tk, text="")
#                 self.image_label.image = img_tk  # Keep a reference
                
#             except Exception as e:
#                 self.image_label.configure(image='', text=f"Error loading image:\n{e}")
#         else:
#             # Show placeholder if image not found
#             self.image_label.configure(image='', text=f"Image not found:\n{frame_name}")
    
#     def update_display(self):
#         """Update both histogram and image display."""
#         if not self.frame_list:
#             return
        
#         current_frame = self.frame_list[self.current_frame_index]
        
#         try:
#             # Update histogram
#             self.create_histogram_plot(current_frame)
            
#             # Update image
#             self.load_and_display_image(current_frame)
            
#             # Update labels
#             self.current_frame_label.configure(text=current_frame)
#             self.frame_index_label.configure(text=f"{self.current_frame_index + 1} / {len(self.frame_list)}")
            
#             # Update window title
#             self.root.title(f"Medical Image Visualization - Frame: {current_frame}")
            
#         except Exception as e:
#             print(f"Error updating display: {e}")
#             messagebox.showerror("Error", f"Error updating display: {e}")
    
#     def next_frame(self):
#         """Go to next frame."""
#         if self.current_frame_index < len(self.frame_list) - 1:
#             self.current_frame_index += 1
#             self.update_display()
    
#     def previous_frame(self):
#         """Go to previous frame."""
#         if self.current_frame_index > 0:
#             self.current_frame_index -= 1
#             self.update_display()
    
#     def go_to_first(self):
#         """Go to first frame."""
#         self.current_frame_index = 0
#         self.update_display()
    
#     def go_to_last(self):
#         """Go to last frame."""
#         self.current_frame_index = len(self.frame_list) - 1
#         self.update_display()
    
#     def jump_to_frame(self):
#         """Jump to specific frame number."""
#         try:
#             frame_num = int(self.jump_entry.get())
#             if 1 <= frame_num <= len(self.frame_list):
#                 self.current_frame_index = frame_num - 1
#                 self.update_display()
#                 self.jump_entry.delete(0, tk.END)
#             else:
#                 messagebox.showerror("Error", f"Frame number must be between 1 and {len(self.frame_list)}")
#         except ValueError:
#             messagebox.showerror("Error", "Please enter a valid frame number")

# def main():
#     """Main function to run the visualization tool."""
    
#     # Check if data folder exists
#     if not os.path.exists("visualization_data"):
#         print("❌ Error: 'visualization_data' folder not found!")
#         print("Please run the data preparation script first.")
#         return
    
#     # Create and run the application
#     root = tk.Tk()
#     app = MedicalImageVisualizationTool(root)
    
#     # Add some styling
#     style = ttk.Style()
#     style.theme_use('clam')
    
#     print("🚀 Starting Medical Image Histogram Visualization Tool...")
#     print("📋 Controls:")
#     print("   - Use arrow keys (← →) to navigate frames")
#     print("   - Use Home/End keys to jump to first/last frame")
#     print("   - Click buttons or enter frame number to jump to specific frame")
#     print("   - Current frame is highlighted in RED in the histogram tables")
#     print("   - Toggle class buttons in right panel to show/hide classes in histogram")
    
#     try:
#         root.mainloop()
#     except Exception as e:
#         print(f"❌ Error running application: {e}")
#         messagebox.showerror("Application Error", f"Error running application: {e}")

# if __name__ == "__main__":
#     main()
    
#     print("🚀 Starting Medical Image Histogram Visualization Tool...")
#     print("📋 Controls:")
#     print("   - Use arrow keys (← →) to navigate frames")
#     print("   - Use Home/End keys to jump to first/last frame")
#     print("   - Click buttons or enter frame number to jump to specific frame")
#     print("   - Current frame is highlighted in RED in the histogram tables")
#     print("   - Toggle class buttons in right panel to show/hide classes in histogram")
    
#     try:
#         root.mainloop()
#     except Exception as e:
#         print(f"❌ Error running application: {e}")
#         messagebox.showerror("Application Error", f"Error running application: {e}")

# if __name__ == "__main__":
#     main()

#!/usr/bin/env python3
"""
Interactive Histogram Visualization Tool for Medical Image Analysis
Shows comprehensive histogram tables and detection results with navigation controls.
Enhanced with video recording capability.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import cv2
import numpy as np
import json
import os
from PIL import Image, ImageTk, ImageDraw
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time
from datetime import datetime

class MedicalImageVisualizationTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Medical Image Histogram Visualization Tool")
        self.root.geometry("1800x1000")  # Increased width for class selector
        self.root.configure(bg='#f0f0f0')
        
        # Data variables
        self.histogram_data = {}
        self.frame_info = {}
        self.class_mapping = {}
        self.frame_list = []
        self.current_frame_index = 0
        
        # Class selection variables
        self.selected_classes = set()  # Set of selected class indices
        self.class_buttons = {}  # Dictionary to store class button references
        
        # Video recording variables
        self.is_recording = False
        self.video_writer = None
        self.video_thread = None
        self.video_fps = 20
        self.video_frame_count = 0
        self.video_output_path = ""
        
        # Load data
        self.load_data()
        
        # Create GUI
        self.create_widgets()
        
        # Initialize with all classes selected
        self.select_all_classes()
        
        # Initialize display
        if self.frame_list:
            self.update_display()
    
    def load_data(self):
        """Load all data files."""
        data_folder = "visualization_data"
        
        try:
            # Load histogram data
            with open(os.path.join(data_folder, "histogram_data.json"), 'r') as f:
                self.histogram_data = json.load(f)
            
            # Load frame info
            with open(os.path.join(data_folder, "frame_info.json"), 'r') as f:
                self.frame_info = json.load(f)
            
            # Load class mapping
            with open(os.path.join(data_folder, "class_mapping.json"), 'r') as f:
                self.class_mapping = json.load(f)
            
            # Load frame list
            with open(os.path.join(data_folder, "frame_list.json"), 'r') as f:
                self.frame_list = json.load(f)
                
            print(f"✅ Loaded {len(self.frame_list)} frames successfully!")
            
        except FileNotFoundError as e:
            messagebox.showerror("Error", f"Data files not found: {e}\nPlease run the data preparation script first.")
            self.root.quit()
    
    def create_widgets(self):
        """Create all GUI widgets."""
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)  # Histogram panel - equal weight
        main_frame.columnconfigure(1, weight=1)  # Image panel - equal weight
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Left panel for histogram
        self.left_panel = ttk.LabelFrame(main_frame, text="Histogram Analysis (Selected Classes)", padding="5")
        self.left_panel.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        self.left_panel.columnconfigure(0, weight=1)
        self.left_panel.rowconfigure(0, weight=1)
        
        # Right panel for image
        self.right_panel = ttk.LabelFrame(main_frame, text="Detection Results", padding="5")
        self.right_panel.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        self.right_panel.columnconfigure(0, weight=1)
        self.right_panel.rowconfigure(0, weight=1)
        
        # Bottom right panel for class selection
        self.bottom_right_panel = ttk.LabelFrame(main_frame, text="Class Selector", padding="5")
        self.bottom_right_panel.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0), pady=(5, 0))
        self.bottom_right_panel.columnconfigure(0, weight=1)
        self.bottom_right_panel.rowconfigure(1, weight=1)
        
        # Histogram canvas
        self.fig, _ = plt.subplots(figsize=(12, 8))
        self.histogram_canvas = FigureCanvasTkAgg(self.fig, self.left_panel)
        self.histogram_canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Image display
        self.image_label = ttk.Label(self.right_panel)
        self.image_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Class selection controls
        self.create_class_selector(self.bottom_right_panel)
        
        # Control panel
        self.control_frame = ttk.LabelFrame(main_frame, text="Navigation Controls", padding="10")
        self.control_frame.grid(row=1, column=0, columnspan=1, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Video recording controls
        video_frame = ttk.LabelFrame(self.control_frame, text="Video Recording", padding="10")
        video_frame.grid(row=0, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.record_button = ttk.Button(video_frame, text="🎥 Start Recording", command=self.toggle_recording)
        self.record_button.grid(row=0, column=0, padx=5)
        
        self.video_status_label = ttk.Label(video_frame, text="Ready to record", font=('Arial', 9, 'italic'))
        self.video_status_label.grid(row=0, column=1, padx=10)
        
        ttk.Label(video_frame, text="FPS:").grid(row=0, column=2, padx=5)
        self.fps_var = tk.StringVar(value="20")
        fps_entry = ttk.Entry(video_frame, textvariable=self.fps_var, width=5)
        fps_entry.grid(row=0, column=3, padx=5)
        
        # Frame navigation
        nav_frame = ttk.Frame(self.control_frame)
        nav_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(nav_frame, text="◀◀ First", command=self.go_to_first).grid(row=0, column=0, padx=5)
        ttk.Button(nav_frame, text="◀ Previous", command=self.previous_frame).grid(row=0, column=1, padx=5)
        ttk.Button(nav_frame, text="Next ▶", command=self.next_frame).grid(row=0, column=2, padx=5)
        ttk.Button(nav_frame, text="Last ▶▶", command=self.go_to_last).grid(row=0, column=3, padx=5)
        
        # Frame info
        info_frame = ttk.Frame(self.control_frame)
        info_frame.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(info_frame, text="Current Frame:").grid(row=0, column=0, padx=5)
        self.current_frame_label = ttk.Label(info_frame, text="", font=('Arial', 10, 'bold'))
        self.current_frame_label.grid(row=0, column=1, padx=5)
        
        ttk.Label(info_frame, text="Frame Index:").grid(row=0, column=2, padx=5)
        self.frame_index_label = ttk.Label(info_frame, text="", font=('Arial', 10, 'bold'))
        self.frame_index_label.grid(row=0, column=3, padx=5)
        
        # Jump to frame
        jump_frame = ttk.Frame(self.control_frame)
        jump_frame.grid(row=3, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(jump_frame, text="Jump to Frame:").grid(row=0, column=0, padx=5)
        self.jump_entry = ttk.Entry(jump_frame, width=10)
        self.jump_entry.grid(row=0, column=1, padx=5)
        ttk.Button(jump_frame, text="Go", command=self.jump_to_frame).grid(row=0, column=2, padx=5)
        
        # Bind Enter key to jump
        self.jump_entry.bind('<Return>', lambda e: self.jump_to_frame())
        
        # Class mapping display
        mapping_frame = ttk.LabelFrame(self.control_frame, text="Class Index Mapping", padding="5")
        mapping_frame.grid(row=4, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Create scrollable text widget for mapping
        mapping_text = tk.Text(mapping_frame, height=4, width=80, wrap=tk.WORD)  # Reduced height
        mapping_scrollbar = ttk.Scrollbar(mapping_frame, orient=tk.VERTICAL, command=mapping_text.yview)
        mapping_text.configure(yscrollcommand=mapping_scrollbar.set)
        
        mapping_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        mapping_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Populate mapping text
        mapping_str = "Class Index → Name Mapping:\n" + "="*50 + "\n"
        for idx, name in sorted(self.class_mapping.items(), key=lambda x: int(x[0])):
            mapping_str += f"Class {idx:2s}: {name}\n"
        
        mapping_text.insert(tk.END, mapping_str)
        mapping_text.config(state=tk.DISABLED)
        
        # Key bindings
        self.root.bind('<Left>', lambda e: self.previous_frame())
        self.root.bind('<Right>', lambda e: self.next_frame())
        self.root.bind('<Home>', lambda e: self.go_to_first())
        self.root.bind('<End>', lambda e: self.go_to_last())
        
        # Focus on root for key bindings
        self.root.focus_set()
    
    def create_class_selector(self, parent):
        """Create class selection interface in NxM table format."""

        # ========== CONFIGURATION SECTION ==========
        # Set your desired grid dimensions here
        FIXED_COLS = 5  # Set N (number of columns) - change this value
        FIXED_ROWS = None  # Set M (number of rows) - set to None for auto-calculation or specific number

        # Cell size configuration
        CELL_WIDTH = 13      # Width of each class button (characters)
        CELL_HEIGHT = 2      # Height of each class button (lines)
        MIN_COL_SIZE = 100   # Minimum column size in pixels

        # Text configuration
        MAX_CLASS_NAME_LENGTH = 15  # Maximum characters to show in class name
        BUTTON_FONT_SIZE = 10        # Font size for buttons
        # ==========================================

        # Control buttons frame
        control_buttons = ttk.Frame(parent)
        control_buttons.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        control_buttons.columnconfigure(0, weight=1)
        control_buttons.columnconfigure(1, weight=1)

        # Select All / Deselect All buttons
        ttk.Button(control_buttons, text="Select All", 
                  command=self.select_all_classes).grid(row=0, column=0, padx=(0, 5), sticky=(tk.W, tk.E))
        ttk.Button(control_buttons, text="Deselect All", 
                  command=self.deselect_all_classes).grid(row=0, column=1, padx=(5, 0), sticky=(tk.W, tk.E))

        # Status label
        self.class_status_label = ttk.Label(parent, text="", font=('Arial', 9, 'italic'))
        self.class_status_label.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(5, 0))

        # Scrollable frame for class table
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))

        # Create class table in NxM format
        all_class_indices = sorted([int(k) for k in self.class_mapping.keys()])
        total_classes = len(all_class_indices)

        # Calculate grid dimensions based on configuration
        import math
        if FIXED_COLS:
            cols = FIXED_COLS
            if FIXED_ROWS:
                rows = FIXED_ROWS
            else:
                rows = math.ceil(total_classes / cols)
        else:
            # Auto-calculate (original behavior)
            cols = math.ceil(math.sqrt(total_classes))
            rows = math.ceil(total_classes / cols)

        print(f"Grid Configuration: {rows} rows × {cols} columns for {total_classes} classes")

        # Add "Class Name" header at position (0,0)
        header_label = tk.Label(scrollable_frame, 
                               text="Class Name",
                               font=('Arial', 8, 'bold'),
                               bg='#34495E',
                               fg='white',
                               relief=tk.RAISED,
                               bd=2,
                               width=CELL_WIDTH,
                               height=CELL_HEIGHT)
        header_label.grid(row=0, column=0, padx=1, pady=1, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create class toggle buttons in table format
        button_index = 0
        for row in range(1, rows + 1):  # Start from row 1 (row 0 has header)
            for col in range(cols):
                if button_index < total_classes:
                    class_idx = all_class_indices[button_index]
                    class_name = self.class_mapping[str(class_idx)]

                    # Truncate long names for button display
                    display_name = class_name[:MAX_CLASS_NAME_LENGTH] + "..." if len(class_name) > MAX_CLASS_NAME_LENGTH else class_name
                    button_text = f"[{class_idx}]\n{display_name}"

                    # Create toggle button with configured size
                    btn = tk.Button(scrollable_frame, 
                                   text=button_text,
                                   command=lambda idx=class_idx: self.toggle_class(idx),
                                   relief=tk.RAISED,
                                   bg='#E8F5E8',
                                   fg='#2E7D32',
                                   font=('Arial', BUTTON_FONT_SIZE),
                                   width=CELL_WIDTH,
                                   height=CELL_HEIGHT,
                                   wraplength=MIN_COL_SIZE - 20)  # Wrap text based on column size

                    btn.grid(row=row, column=col, padx=1, pady=1, sticky=(tk.W, tk.E, tk.N, tk.S))
                    self.class_buttons[class_idx] = btn
                    button_index += 1
                else:
                    # Empty cell for incomplete grid
                    empty_label = tk.Label(scrollable_frame, 
                                         text="",
                                         width=CELL_WIDTH,
                                         height=CELL_HEIGHT)
                    empty_label.grid(row=row, column=col, padx=1, pady=1)

        # Configure column weights for uniform sizing
        for col in range(cols):
            scrollable_frame.columnconfigure(col, weight=1, minsize=MIN_COL_SIZE)

        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind("<MouseWheel>", _on_mousewheel)

        self.update_class_status() 
        
    def toggle_class(self, class_idx):
        """Toggle class selection and update display."""
        if class_idx in self.selected_classes:
            self.selected_classes.remove(class_idx)
            # Update button appearance - deselected
            self.class_buttons[class_idx].config(
                relief=tk.RAISED,
                bg='#FFEBEE',
                fg='#C62828'
            )
        else:
            self.selected_classes.add(class_idx)
            # Update button appearance - selected
            self.class_buttons[class_idx].config(
                relief=tk.SUNKEN,
                bg='#E8F5E8',
                fg='#2E7D32'
            )
        self.update_class_status()
        self.update_display()

    def select_all_classes(self):
        """Select all classes."""
        all_class_indices = [int(k) for k in self.class_mapping.keys()]
        self.selected_classes = set(all_class_indices)
        
        # Update all button appearances
        for class_idx in all_class_indices:
            self.class_buttons[class_idx].config(
                relief=tk.SUNKEN,
                bg='#E8F5E8',
                fg='#2E7D32'
            )
        
        self.update_class_status()
        self.update_display()
    
    def deselect_all_classes(self):
        """Deselect all classes."""
        self.selected_classes.clear()
        
        # Update all button appearances
        for class_idx in self.class_buttons:
            self.class_buttons[class_idx].config(
                relief=tk.RAISED,
                bg='#FFEBEE',
                fg='#C62828'
            )
        
        self.update_class_status()
        self.update_display()
    
    def update_class_status(self):
        """Update class selection status label."""
        total_classes = len(self.class_mapping)
        selected_count = len(self.selected_classes)
        
        if selected_count == 0:
            status_text = "No classes selected"
        elif selected_count == total_classes:
            status_text = f"All {total_classes} classes selected"
        else:
            status_text = f"{selected_count} of {total_classes} classes selected"
        
        self.class_status_label.config(text=status_text)
    
    def capture_video_frame(self):
        """Capture current frame for video recording."""
        try:
            # Get the current window size
            self.root.update_idletasks()
            
            # Calculate positions of the two panels we want to capture
            left_x = self.left_panel.winfo_rootx()
            left_y = self.left_panel.winfo_rooty()
            left_width = self.left_panel.winfo_width()
            left_height = self.left_panel.winfo_height()
            
            right_x = self.right_panel.winfo_rootx()
            right_y = self.right_panel.winfo_rooty()
            right_width = self.right_panel.winfo_width()
            right_height = self.right_panel.winfo_height()
            
            # Determine the combined area to capture
            min_x = min(left_x, right_x)
            min_y = min(left_y, right_y)
            max_x = max(left_x + left_width, right_x + right_width)
            max_y = max(left_y + left_height, right_y + right_height)
            
            total_width = max_x - min_x
            total_height = max_y - min_y
            
            # Create a screenshot of the combined area
            import PIL.ImageGrab as ImageGrab
            screenshot = ImageGrab.grab(bbox=(min_x, min_y, max_x, max_y))
            
            # Convert PIL image to numpy array for OpenCV
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            # Add frame counter and timestamp overlay
            timestamp = datetime.now().strftime("%H:%M:%S")
            frame_text = f"Frame: {self.current_frame_index + 1}/{len(self.frame_list)} | {timestamp}"
            
            # Add text overlay
            cv2.putText(frame, frame_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            
            return frame, total_width, total_height
            
        except Exception as e:
            print(f"Error capturing frame: {e}")
            return None, 0, 0
    
    def toggle_recording(self):
        """Start or stop video recording."""
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
    
    def start_recording(self):
        """Start video recording."""
        try:
            # Get FPS from entry
            try:
                self.video_fps = int(self.fps_var.get())
                if self.video_fps <= 0:
                    self.video_fps = 20
            except ValueError:
                self.video_fps = 20
                self.fps_var.set("20")
            
            # Ask user for output file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"medical_visualization_{timestamp}.mp4"
            
            self.video_output_path = filedialog.asksaveasfilename(
                defaultextension=".mp4",
                filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")],
                initialvalue=default_filename,
                title="Save Video As"
            )
            
            if not self.video_output_path:
                return
            
            # Capture initial frame to get dimensions
            frame, width, height = self.capture_video_frame()
            if frame is None:
                messagebox.showerror("Error", "Failed to capture initial frame")
                return
            
            # Initialize video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.video_writer = cv2.VideoWriter(self.video_output_path, fourcc, self.video_fps, (width, height))
            
            if not self.video_writer.isOpened():
                messagebox.showerror("Error", "Failed to initialize video writer")
                return
            
            # Start recording
            self.is_recording = True
            self.video_frame_count = 0
            
            # Update UI
            self.record_button.config(text="⏹ Stop Recording", style="Accent.TButton")
            self.video_status_label.config(text=f"Recording... Frame: 0", foreground="red")
            
            # Start recording thread
            self.video_thread = threading.Thread(target=self.recording_loop, daemon=True)
            self.video_thread.start()
            
            print(f"✅ Started recording to: {self.video_output_path}")
            print(f"📹 Recording at {self.video_fps} FPS")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start recording: {e}")
            print(f"❌ Error starting recording: {e}")
    
    def stop_recording(self):
        """Stop video recording."""
        try:
            self.is_recording = False
            
            # Wait for recording thread to finish
            if self.video_thread and self.video_thread.is_alive():
                self.video_thread.join(timeout=2.0)
            
            # Close video writer
            if self.video_writer:
                self.video_writer.release()
                self.video_writer = None
            
            # Update UI
            self.record_button.config(text="🎥 Start Recording")
            self.video_status_label.config(text=f"Recording saved: {self.video_frame_count} frames", foreground="green")
            
            print(f"✅ Recording stopped. Saved {self.video_frame_count} frames to: {self.video_output_path}")
            messagebox.showinfo("Recording Complete", 
                               f"Video saved successfully!\n\nFile: {os.path.basename(self.video_output_path)}\n"
                               f"Frames: {self.video_frame_count}\n"
                               f"FPS: {self.video_fps}")
            
        except Exception as e:
            print(f"❌ Error stopping recording: {e}")
            messagebox.showerror("Error", f"Error stopping recording: {e}")
    
    def recording_loop(self):
        """Main recording loop running in separate thread."""
        frame_duration = 1.0 / self.video_fps
        last_frame_time = time.time()
        
        try:
            while self.is_recording:
                current_time = time.time()
                
                # Check if it's time for the next frame
                if current_time - last_frame_time >= frame_duration:
                    # Capture frame on main thread
                    self.root.after(0, self.record_current_frame)
                    last_frame_time = current_time
                
                # Small sleep to prevent excessive CPU usage
                time.sleep(0.001)
                
        except Exception as e:
            print(f"❌ Error in recording loop: {e}")
            self.root.after(0, self.stop_recording)
    
    def record_current_frame(self):
        """Record current frame (called from main thread)."""
        try:
            if not self.is_recording or not self.video_writer:
                return
            
            # Capture frame
            frame, width, height = self.capture_video_frame()
            if frame is not None:
                # Write frame to video
                self.video_writer.write(frame)
                self.video_frame_count += 1
                
                # Update status
                self.video_status_label.config(text=f"Recording... Frame: {self.video_frame_count}")
                
        except Exception as e:
            print(f"❌ Error recording frame: {e}")
    
    def create_histogram_plot(self, current_frame_name):
        """Create comprehensive histogram table with selected classes only."""
        # Clear the figure
        self.fig.clear()
        
        # Check if any classes are selected
        if not self.selected_classes:
            ax = self.fig.add_subplot(111)
            ax.text(0.5, 0.5, 'No classes selected.\nPlease select classes from the right panel.', 
                   ha='center', va='center', fontsize=16, transform=ax.transAxes)
            ax.axis('off')
            self.histogram_canvas.draw()
            return

        # Get selected class information (sorted by index)
        selected_class_indices = sorted(list(self.selected_classes))
        selected_class_names = [self.class_mapping[str(i)] for i in selected_class_indices]

        # Score ranges
        score_ranges = ["90-100%", "80-90%", "70-80%", "60-70%", "50-60%", 
                       "40-50%", "30-40%", "20-30%", "10-20%", "0-10%"]

        # Frame labels (0=current, -1=previous, etc.)
        frame_labels = ["0", "-1", "-2", "-3", "-4"]

        # Get histogram data for current + last 4 frames (total 5 frames)
        hist_frames = []
        frame_names = []
        current_idx = self.current_frame_index

        # Collect 5 frames (current + 4 previous)
        for i in range(current_idx, max(-1, current_idx - 5), -1):
            if i >= 0 and i < len(self.frame_list):
                frame_name = self.frame_list[i]
                if frame_name in self.histogram_data:
                    hist_data = np.array(self.histogram_data[frame_name])
                    hist_frames.append(hist_data)
                    frame_names.append(frame_name)

        # Pad with empty frames if needed
        while len(hist_frames) < 5:
            # Use max of all possible class indices for padding
            all_class_indices = [int(k) for k in self.class_mapping.keys()]
            hist_frames.append(np.zeros((100, max(all_class_indices) + 1)))
            frame_names.append("Empty")

        # Process histogram data for selected classes and all frames
        all_binned_data = []
        for hist_data in hist_frames:
            # Ensure histogram has enough classes
            all_class_indices = [int(k) for k in self.class_mapping.keys()]
            if hist_data.shape[1] < max(all_class_indices) + 1:
                padded_histogram = np.zeros((100, max(all_class_indices) + 1))
                if hist_data.shape[1] > 0:
                    padded_histogram[:, :hist_data.shape[1]] = hist_data
                hist_data = padded_histogram

            # Select columns for selected classes only
            selected_columns = hist_data[:, selected_class_indices]

            # Bin the data (100 bins -> 10 score ranges)
            try:
                binned_counts = selected_columns.reshape(10, 10, len(selected_class_indices)).sum(axis=1)
            except (ValueError, IndexError):
                binned_counts = np.zeros((10, len(selected_class_indices)))

            all_binned_data.append(binned_counts)

        # Create single subplot for the comprehensive table
        ax = self.fig.add_subplot(111)
        ax.axis('off')

        # Build table headers with proper structure
        # Row 0: Score ranges (each spanning 5 columns) + "Class Name" cell
        main_headers = ['Class Name']  # Header cell at (0,0)

        # Add score ranges, each appearing once but will span 5 columns
        for score_range in score_ranges:
            main_headers.extend([score_range, '', '', '', ''])  # One label + 4 empty for spanning

        # Row 1: Frame labels repeated under each score range + empty cell for class name header
        sub_headers = ['']  # Empty cell under "Class Name" header

        # Add frame labels repeated for each score range
        for _ in score_ranges:  # For each score range
            sub_headers.extend(frame_labels)  # Add all 5 frame labels

        # Build table data with enhanced formatting
        table_data = []

        # Add sub-header row
        table_data.append(sub_headers)

        # Add data rows for each selected class
        for class_idx, class_name in enumerate(selected_class_names):
            # Format class name to fit in 1 cell - REDUCED SIZE
            short_name = class_name[:12]  # Reduced from 20 to 12 chars
            class_display = f"{short_name} ({selected_class_indices[class_idx]})"

            # Create row with class name in single cell
            row = [class_display]  # Only class name, no empty cells

            # Add data for each score range and frame combination
            for score_idx in range(10):
                for frame_idx in range(5):
                    if frame_idx < len(all_binned_data):
                        try:
                            value = int(all_binned_data[frame_idx][score_idx, class_idx])
                            # Enhanced number formatting: h for hundreds, k for thousands
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

        # Create table with proper structure
        table = ax.table(cellText=table_data,
                        colLabels=main_headers,
                        cellLoc='center',
                        loc='center',
                        bbox=[0, 0, 1, 1])

        # Enhanced styling for better readability
        table.auto_set_font_size(False)
        table.set_fontsize(7)  # Slightly larger font
        table.scale(1.0, 1.0)  # FIXED: Constant scaling to maintain cell sizes

        # Color scheme for score ranges
        score_range_colors = ['#FF3333', '#FF5555', '#FF7777', '#FF9999', '#FFBB99',
                             '#FFDD99', '#DDFF99', '#BBFF99', '#99FF99', '#77FF99']

        num_cols = len(main_headers)
        cell_height = 0.05  # Fixed height for all cells

        # Set CONSTANT column widths - class name column 3x wider
        class_name_width = 3.0 / (num_cols + 2)  # Class name gets 3x weight out of total
        data_width = 1.0 / (num_cols + 2)        # Data columns get 1x weight each
        
        for col in range(num_cols):
            for row in range(len(table_data) + 1):
                cell = table[(row, col)]
                if col == 0:  # Class name column - 3x wider
                    cell.set_width(class_name_width)
                else:  # Data columns - normal width
                    cell.set_width(data_width)
                cell.set_height(cell_height)  # Same height for all cells

        # Style main headers (Row 0) - Score ranges + Class Name header
        for col in range(num_cols):
            cell = table[(0, col)]
            if col == 0:  # Class Name header cell
                cell.set_facecolor('#2C3E50')
                cell.set_text_props(weight='bold', color='white', size=8)
                cell.set_edgecolor('white')
            else:
                # Score range headers
                score_idx = (col - 1) // 5
                if score_idx < len(score_range_colors) and (col - 1) % 5 == 0:
                    # This is the first column of a score range - show the label
                    cell.set_facecolor(score_range_colors[score_idx])
                    cell.set_text_props(weight='bold', color='black', size=8)
                else:
                    # This is a continuation of the score range - same color, no text
                    score_idx = (col - 1) // 5
                    if score_idx < len(score_range_colors):
                        cell.set_facecolor(score_range_colors[score_idx])
                        cell.set_text_props(color=score_range_colors[score_idx], size=1)  # Hide text
            cell.set_edgecolor('white')
            cell.set_linewidth(2)

        # Style sub-headers (Row 1) - Frame labels
        for col in range(num_cols):
            cell = table[(1, col)]
            if col == 0:  # Class name area
                cell.set_facecolor('#2C3E50')
                cell.set_text_props(color='white', size=1)  # Hide text
                cell.set_edgecolor('white')
            else:
                # Frame labels
                frame_idx = (col - 1) % 5
                score_idx = (col - 1) // 5

                if frame_idx == 0:  # Current frame
                    cell.set_facecolor('#E74C3C')
                    cell.set_text_props(weight='bold', color='white', size=8)
                else:
                    if score_idx < len(score_range_colors):
                        base_color = score_range_colors[score_idx]
                        cell.set_facecolor(base_color)
                        cell.set_text_props(weight='bold', color='black', size=8)
            cell.set_edgecolor('white')
            cell.set_linewidth(2)

        # Style data cells
        for row in range(2, len(table_data) + 1):
            for col in range(num_cols):
                cell = table[(row, col)]

                if col == 0:  # Class name column
                    cell.set_facecolor('#ECF0F1')
                    cell.set_text_props(weight='bold', size=7, ha='left')  # Reduced font size
                    cell.set_edgecolor('#BDC3C7')
                    cell.set_linewidth(2)
                else:
                    # Data cells
                    try:
                        value_str = table_data[row-1][col]

                        # Parse formatted values back to numbers for color intensity
                        if value_str.endswith('k+'):
                            value = 99999
                        elif value_str.endswith('k'):
                            value = int(value_str[:-1]) * 1000
                        elif value_str.endswith('h'):
                            value = int(value_str[:-1]) * 100
                        else:
                            value = int(value_str) if value_str.isdigit() else 0

                        frame_idx = (col - 1) % 5
                        score_idx = (col - 1) // 5

                        if value > 0:
                            # Calculate color intensity
                            class_row_idx = row - 2
                            max_val = 0

                            # Find max value for this class
                            for c in range(1, num_cols):
                                try:
                                    check_val_str = table_data[class_row_idx + 1][c]
                                    if check_val_str.endswith('k+'):
                                        check_val = 99999
                                    elif check_val_str.endswith('k'):
                                        check_val = int(check_val_str[:-1]) * 1000
                                    elif check_val_str.endswith('h'):
                                        check_val = int(check_val_str[:-1]) * 100
                                    else:
                                        check_val = int(check_val_str) if check_val_str.isdigit() else 0
                                    max_val = max(max_val, check_val)
                                except (ValueError, IndexError):
                                    pass
                                
                            if max_val > 0:
                                intensity = min(value / max_val, 1.0)

                                if score_idx < len(score_range_colors):
                                    base_color = score_range_colors[score_idx]
                                    r = int(base_color[1:3], 16) / 255.0
                                    g = int(base_color[3:5], 16) / 255.0
                                    b = int(base_color[5:7], 16) / 255.0

                                    alpha = 0.3 + intensity * 0.7
                                    cell.set_facecolor((r, g, b, alpha))

                                    # High value indicator
                                    if intensity > 0.7:
                                        cell.set_edgecolor('#2C3E50')
                                        cell.set_linewidth(2)

                                # Highlight current frame
                                if frame_idx == 0:
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

                    # Grid lines for data cells
                    cell.set_edgecolor('#D5DBDB')
                    cell.set_linewidth(0.5)

        # Enhanced title
        selected_count = len(self.selected_classes)
        total_count = len(self.class_mapping)
        title = f'Medical Image Histogram Analysis - Frame {current_idx + 1}/{len(self.frame_list)} ({current_frame_name}) | {selected_count}/{total_count} Classes'
        self.fig.suptitle(title, fontsize=12, fontweight='bold', y=0.98)

        # Enhanced subtitle
        subtitle = f'Showing {selected_count} selected classes | Toggle classes in right panel'
        ax.text(0.5, 0.02, subtitle, transform=ax.transAxes, fontsize=9, 
               ha='center', style='italic', color='gray')

        # Adjust layout
        plt.subplots_adjust(left=0.01, right=0.99, top=0.95, bottom=0.05)

        # Draw the canvas
        self.histogram_canvas.draw()
        
    def load_and_display_image(self, frame_name):
        """Load and display the cropped image with detections."""
        image_path = os.path.join("visualization_data", "cropped_images", f"{frame_name}.jpg")
        
        if os.path.exists(image_path):
            try:
                # Load image
                img = cv2.imread(image_path)
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                
                # Resize image to fit in the panel (max 600x600)
                h, w = img_rgb.shape[:2]
                max_size = 600
                
                if h > max_size or w > max_size:
                    scale = min(max_size / h, max_size / w)
                    new_h, new_w = int(h * scale), int(w * scale)
                    img_rgb = cv2.resize(img_rgb, (new_w, new_h))
                
                # Convert to PhotoImage
                img_pil = Image.fromarray(img_rgb)
                img_tk = ImageTk.PhotoImage(img_pil)
                
                # Update label
                self.image_label.configure(image=img_tk, text="")
                self.image_label.image = img_tk  # Keep a reference
                
            except Exception as e:
                self.image_label.configure(image='', text=f"Error loading image:\n{e}")
        else:
            # Show placeholder if image not found
            self.image_label.configure(image='', text=f"Image not found:\n{frame_name}")
    
    def update_display(self):
        """Update both histogram and image display."""
        if not self.frame_list:
            return
        
        current_frame = self.frame_list[self.current_frame_index]
        
        try:
            # Update histogram
            self.create_histogram_plot(current_frame)
            
            # Update image
            self.load_and_display_image(current_frame)
            
            # Update labels
            self.current_frame_label.configure(text=current_frame)
            self.frame_index_label.configure(text=f"{self.current_frame_index + 1} / {len(self.frame_list)}")
            
            # Update window title
            self.root.title(f"Medical Image Visualization - Frame: {current_frame}")
            
        except Exception as e:
            print(f"Error updating display: {e}")
            messagebox.showerror("Error", f"Error updating display: {e}")
    
    def next_frame(self):
        """Go to next frame."""
        if self.current_frame_index < len(self.frame_list) - 1:
            self.current_frame_index += 1
            self.update_display()
    
    def previous_frame(self):
        """Go to previous frame."""
        if self.current_frame_index > 0:
            self.current_frame_index -= 1
            self.update_display()
    
    def go_to_first(self):
        """Go to first frame."""
        self.current_frame_index = 0
        self.update_display()
    
    def go_to_last(self):
        """Go to last frame."""
        self.current_frame_index = len(self.frame_list) - 1
        self.update_display()
    
    def jump_to_frame(self):
        """Jump to specific frame number."""
        try:
            frame_num = int(self.jump_entry.get())
            if 1 <= frame_num <= len(self.frame_list):
                self.current_frame_index = frame_num - 1
                self.update_display()
                self.jump_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", f"Frame number must be between 1 and {len(self.frame_list)}")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid frame number")

def main():
    """Main function to run the visualization tool."""
    
    # Check if data folder exists
    if not os.path.exists("visualization_data"):
        print("❌ Error: 'visualization_data' folder not found!")
        print("Please run the data preparation script first.")
        return
    
    # Create and run the application
    root = tk.Tk()
    app = MedicalImageVisualizationTool(root)
    
    # Add some styling
    style = ttk.Style()
    style.theme_use('clam')
    
    print("🚀 Starting Medical Image Histogram Visualization Tool...")
    print("📋 Controls:")
    print("   - Use arrow keys (← →) to navigate frames")
    print("   - Use Home/End keys to jump to first/last frame")
    print("   - Click buttons or enter frame number to jump to specific frame")
    print("   - Current frame is highlighted in RED in the histogram tables")
    print("   - Toggle class buttons in right panel to show/hide classes in histogram")
    print("   - Click '🎥 Start Recording' to record video of histogram and detection panels")
    
    try:
        root.mainloop()
    except Exception as e:
        print(f"❌ Error running application: {e}")
        messagebox.showerror("Application Error", f"Error running application: {e}")

if __name__ == "__main__":
    main()