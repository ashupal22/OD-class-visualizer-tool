#!/usr/bin/env python3
"""
Quick Fix Script - Creates the optimized visualization tool file
Run this script to create the missing optimized_interactive_visualization_tool.py file
"""

import os

def create_optimized_tool_file():
    """Create the optimized visualization tool file."""
    
    optimized_code = '''#!/usr/bin/env python3
"""
Optimized Interactive Histogram Visualization Tool for Medical Image Analysis
Memory-efficient version that prevents X11 rendering errors by limiting table size.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import cv2
import numpy as np
import json
import os
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time

class MedicalImageVisualizationTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Medical Image Histogram Visualization Tool (Optimized)")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # Data variables
        self.histogram_data = {}
        self.frame_info = {}
        self.class_mapping = {}
        self.frame_list = []
        self.current_frame_index = 0
        
        # Class selection variables - OPTIMIZED
        self.selected_classes = set()
        self.class_buttons = {}
        self.max_display_classes = 6  # HARD LIMIT to prevent X11 errors
        
        # Play control variables
        self.is_playing = False
        self.play_thread = None
        self.play_fps = 20
        
        # Load data
        self.load_data()
        
        # Create GUI
        self.create_widgets()
        
        # Initialize with first 6 classes selected
        self.select_initial_classes()
        
        # Initialize display
        if self.frame_list:
            self.update_display()
    
    def load_data(self):
        """Load data with basic error handling."""
        data_folder = "visualization_data"
        
        try:
            # Load histogram data (simplified loading)
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
            messagebox.showerror("Error", f"Data files not found: {e}\\nPlease run the data preparation script first.")
            self.root.quit()
    
    def create_widgets(self):
        """Create optimized GUI widgets."""
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=2)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=0)
        
        # Left panel for histogram
        left_panel = ttk.LabelFrame(main_frame, text="Histogram Analysis (Max 6 Classes)", padding="5")
        left_panel.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        left_panel.columnconfigure(0, weight=1)
        left_panel.rowconfigure(0, weight=1)
        
        # Right panel for image and class selection
        right_panel = ttk.Frame(main_frame)
        right_panel.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        right_panel.columnconfigure(0, weight=1)
        right_panel.rowconfigure(0, weight=1)
        right_panel.rowconfigure(1, weight=1)
        
        # Image panel (top right)
        image_panel = ttk.LabelFrame(right_panel, text="Detection Results", padding="5")
        image_panel.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 5))
        image_panel.columnconfigure(0, weight=1)
        image_panel.rowconfigure(0, weight=1)
        
        # Class selection panel (bottom right)
        class_panel = ttk.LabelFrame(right_panel, text="Class Selector (Select up to 6)", padding="5")
        class_panel.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(5, 0))
        class_panel.columnconfigure(0, weight=1)
        class_panel.rowconfigure(1, weight=1)
        
        # Histogram canvas - SMALLER figure
        self.fig, _ = plt.subplots(figsize=(8, 5))
        self.histogram_canvas = FigureCanvasTkAgg(self.fig, left_panel)
        self.histogram_canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Image display
        self.image_label = ttk.Label(image_panel)
        self.image_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Class selection controls
        self.create_class_selector(class_panel)
        
        # Control panel
        control_frame = ttk.LabelFrame(main_frame, text="Navigation Controls", padding="10")
        control_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Navigation buttons
        nav_frame = ttk.Frame(control_frame)
        nav_frame.grid(row=0, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Button(nav_frame, text="◀◀ First", command=self.go_to_first).grid(row=0, column=0, padx=5)
        ttk.Button(nav_frame, text="◀ Previous", command=self.previous_frame).grid(row=0, column=1, padx=5)
        ttk.Button(nav_frame, text="Next ▶", command=self.next_frame).grid(row=0, column=2, padx=5)
        ttk.Button(nav_frame, text="Last ▶▶", command=self.go_to_last).grid(row=0, column=3, padx=5)
        
        # Play controls
        play_frame = ttk.Frame(control_frame)
        play_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.play_button = ttk.Button(play_frame, text="▶ Play", command=self.toggle_play)
        self.play_button.grid(row=0, column=0, padx=5)
        
        ttk.Button(play_frame, text="⏹ Stop", command=self.stop_play).grid(row=0, column=1, padx=5)
        
        # Frame info
        info_frame = ttk.Frame(control_frame)
        info_frame.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E))
        
        ttk.Label(info_frame, text="Frame:").grid(row=0, column=0, padx=5)
        self.current_frame_label = ttk.Label(info_frame, text="", font=('Arial', 10, 'bold'))
        self.current_frame_label.grid(row=0, column=1, padx=5)
        
        ttk.Label(info_frame, text="Index:").grid(row=0, column=2, padx=5)
        self.frame_index_label = ttk.Label(info_frame, text="", font=('Arial', 10, 'bold'))
        self.frame_index_label.grid(row=0, column=3, padx=5)
        
        # Key bindings
        self.root.bind('<Left>', lambda e: self.previous_frame())
        self.root.bind('<Right>', lambda e: self.next_frame())
        self.root.bind('<space>', lambda e: self.toggle_play())
        self.root.focus_set()
    
    def create_class_selector(self, parent):
        """Create simple class selection."""
        
        # Warning label
        warning_label = ttk.Label(parent, text="⚠️ Max 6 classes for optimal performance", 
                                 font=('Arial', 9, 'bold'), foreground='red')
        warning_label.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Control buttons
        control_frame = ttk.Frame(parent)
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Button(control_frame, text="Clear All", command=self.deselect_all_classes).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="First 6", command=self.select_initial_classes).pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.class_status_label = ttk.Label(parent, text="", font=('Arial', 9))
        self.class_status_label.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Class list frame
        list_frame = ttk.Frame(parent)
        list_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(5, 0))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Scrollable listbox
        self.class_listbox = tk.Listbox(list_frame, selectmode=tk.MULTIPLE, height=10)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.class_listbox.yview)
        self.class_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.class_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Populate listbox
        for class_idx in sorted([int(k) for k in self.class_mapping.keys()]):
            class_name = self.class_mapping[str(class_idx)]
            display_text = f"[{class_idx:2d}] {class_name}"
            self.class_listbox.insert(tk.END, display_text)
        
        # Bind selection event
        self.class_listbox.bind('<<ListboxSelect>>', self.on_class_selection_change)
        
        self.update_class_status()
    
    def on_class_selection_change(self, event):
        """Handle class selection change."""
        selected_indices = self.class_listbox.curselection()
        
        if len(selected_indices) > self.max_display_classes:
            messagebox.showwarning("Limit Reached", f"Maximum {self.max_display_classes} classes allowed!")
            # Revert to previous selection
            return
        
        # Update selected classes
        self.selected_classes = set()
        for idx in selected_indices:
            class_idx = sorted([int(k) for k in self.class_mapping.keys()])[idx]
            self.selected_classes.add(class_idx)
        
        self.update_class_status()
        self.update_display()
    
    def select_initial_classes(self):
        """Select first 6 classes."""
        self.class_listbox.selection_clear(0, tk.END)
        for i in range(min(6, self.class_listbox.size())):
            self.class_listbox.selection_set(i)
        self.on_class_selection_change(None)
    
    def deselect_all_classes(self):
        """Deselect all classes."""
        self.class_listbox.selection_clear(0, tk.END)
        self.selected_classes.clear()
        self.update_class_status()
        self.update_display()
    
    def update_class_status(self):
        """Update status label."""
        selected_count = len(self.selected_classes)
        status_text = f"{selected_count}/{self.max_display_classes} classes selected"
        self.class_status_label.config(text=status_text)
    
    def create_histogram_plot(self, current_frame_name):
        """Create simplified histogram plot."""
        self.fig.clear()
        
        if not self.selected_classes:
            ax = self.fig.add_subplot(111)
            ax.text(0.5, 0.5, 'No classes selected.\\nSelect classes from the right panel.', 
                   ha='center', va='center', fontsize=12, transform=ax.transAxes)
            ax.axis('off')
            self.histogram_canvas.draw()
            return
        
        # Get histogram data for current frame
        if current_frame_name in self.histogram_data:
            hist_data = np.array(self.histogram_data[current_frame_name])
        else:
            hist_data = np.zeros((100, len(self.class_mapping)))
        
        # Select data for selected classes
        selected_class_indices = sorted(list(self.selected_classes))
        if hist_data.shape[1] > max(selected_class_indices):
            selected_data = hist_data[:, selected_class_indices]
            
            # Create simplified bar chart
            ax = self.fig.add_subplot(111)
            
            # Sum over all bins for each class
            class_totals = selected_data.sum(axis=0)
            
            # Create bar chart
            class_names = [self.class_mapping[str(i)][:10] for i in selected_class_indices]
            bars = ax.bar(range(len(class_totals)), class_totals, 
                         color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD'][:len(class_totals)])
            
            ax.set_xlabel('Classes')
            ax.set_ylabel('Total Detections')
            ax.set_title(f'Class Detections - Frame {self.current_frame_index + 1}')
            ax.set_xticks(range(len(class_names)))
            ax.set_xticklabels(class_names, rotation=45, ha='right')
            
            # Add value labels on bars
            for bar, value in zip(bars, class_totals):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(value)}', ha='center', va='bottom')
        
        plt.tight_layout()
        self.histogram_canvas.draw()
    
    def load_and_display_image(self, frame_name):
        """Load and display image."""
        image_path = os.path.join("visualization_data", "cropped_images", f"{frame_name}.jpg")
        
        if os.path.exists(image_path):
            try:
                img = cv2.imread(image_path)
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                
                # Resize for display
                h, w = img_rgb.shape[:2]
                max_size = 350
                
                if h > max_size or w > max_size:
                    scale = min(max_size / h, max_size / w)
                    new_h, new_w = int(h * scale), int(w * scale)
                    img_rgb = cv2.resize(img_rgb, (new_w, new_h))
                
                img_pil = Image.fromarray(img_rgb)
                img_tk = ImageTk.PhotoImage(img_pil)
                
                self.image_label.configure(image=img_tk, text="")
                self.image_label.image = img_tk
                
            except Exception as e:
                self.image_label.configure(image='', text=f"Error loading image: {e}")
        else:
            self.image_label.configure(image='', text=f"Image not found: {frame_name}")
    
    def update_display(self):
        """Update display."""
        if not self.frame_list:
            return
        
        current_frame = self.frame_list[self.current_frame_index]
        
        try:
            self.create_histogram_plot(current_frame)
            self.load_and_display_image(current_frame)
            
            self.current_frame_label.configure(text=current_frame)
            self.frame_index_label.configure(text=f"{self.current_frame_index + 1}/{len(self.frame_list)}")
            
        except Exception as e:
            print(f"Error updating display: {e}")
    
    # Navigation methods
    def next_frame(self):
        if self.current_frame_index < len(self.frame_list) - 1:
            self.current_frame_index += 1
            self.update_display()
    
    def previous_frame(self):
        if self.current_frame_index > 0:
            self.current_frame_index -= 1
            self.update_display()
    
    def go_to_first(self):
        self.current_frame_index = 0
        self.update_display()
    
    def go_to_last(self):
        self.current_frame_index = len(self.frame_list) - 1
        self.update_display()
    
    def toggle_play(self):
        if self.is_playing:
            self.stop_play()
        else:
            self.start_play()
    
    def start_play(self):
        if self.is_playing:
            return
        
        self.is_playing = True
        self.play_button.configure(text="⏸ Pause")
        
        self.play_thread = threading.Thread(target=self._play_worker, daemon=True)
        self.play_thread.start()
    
    def stop_play(self):
        self.is_playing = False
        self.play_button.configure(text="▶ Play")
    
    def _play_worker(self):
        while self.is_playing and self.current_frame_index < len(self.frame_list) - 1:
            self.root.after(0, self.next_frame)
            time.sleep(0.05)  # 20 FPS
        
        if self.is_playing:
            self.root.after(0, self.stop_play)


def main():
    """Main function."""
    if not os.path.exists("visualization_data"):
        print("❌ Error: 'visualization_data' folder not found!")
        print("Please run the data preparation script first.")
        return
    
    root = tk.Tk()
    app = MedicalImageVisualizationTool(root)
    
    style = ttk.Style()
    style.theme_use('clam')
    
    print("🚀 Starting Optimized Medical Image Visualization Tool...")
    print("📋 Features:")
    print("   - Maximum 6 classes (prevents X11 errors)")
    print("   - Simplified histogram display")
    print("   - Memory efficient")
    print("   - Smooth navigation")
    
    try:
        root.mainloop()
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
'''
    
    # Write the file
    filename = "optimized_interactive_visualization_tool.py"
    
    try:
        with open(filename, 'w') as f:
            f.write(optimized_code)
        
        print(f"✅ Successfully created {filename}")
        print(f"📁 File size: {len(optimized_code)} characters")
        print(f"🚀 You can now run: python optimized_runner.py")
        return True
        
    except Exception as e:
        print(f"❌ Error creating file: {e}")
        return False

def main():
    print("🔧 Quick Fix Script - Creating Optimized Visualization Tool")
    print("="*60)
    
    if os.path.exists("optimized_interactive_visualization_tool.py"):
        response = input("File already exists. Overwrite? (y/N): ").strip().lower()
        if response != 'y':
            print("Cancelled.")
            return
    
    success = create_optimized_tool_file()
    
    if success:
        print("\n✅ Setup complete!")
        print("\nNext steps:")
        print("1. Run: python optimized_runner.py")
        print("2. Choose option 2 (Optimized Visualization Tool)")
        print("3. Enjoy the memory-efficient visualization!")
    else:
        print("\n❌ Setup failed. Please check the error above.")

if __name__ == "__main__":
    main()