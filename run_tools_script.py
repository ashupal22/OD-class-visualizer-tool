#!/usr/bin/env python3
"""
Medical Image Analysis Tool Runner

This script provides a menu to run either:
1. Data preparation (process images and generate data files)
2. Interactive visualization tool (browse and analyze processed data)
"""

import os
import sys

def check_dependencies():
    """Check if required packages are installed."""
    required_packages = [
        'opencv-python', 'numpy', 'onnxruntime', 'tqdm', 
        'matplotlib', 'Pillow', 'tkinter'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'opencv-python':
                import cv2
            elif package == 'tkinter':
                import tkinter
            elif package == 'Pillow':
                import PIL
            else:
                __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("Missing required packages:")
        for pkg in missing_packages:
            print(f"  - {pkg}")
        print(f"\nInstall them with: pip install {' '.join(missing_packages)}")
        return False
    return True

def check_model_file():
    """Check if ONNX model file exists."""
    model_path = "cerebro_v6.0.1_od_model.onnx"
    if not os.path.exists(model_path):
        print(f"Error: Model file '{model_path}' not found!")
        print("Please ensure the ONNX model file is in the current directory.")
        return False
    return True

def check_input_folder():
    """Check if input folder exists."""
    input_folder = "recra"
    if not os.path.exists(input_folder):
        print(f"Error: Input folder '{input_folder}' not found!")
        print("Please create the folder and add your input images (.jpg files).")
        return False
    
    # Check for images
    import glob
    images = glob.glob(os.path.join(input_folder, "*.jpg"))
    if not images:
        print(f"Error: No .jpg images found in '{input_folder}' folder!")
        print("Please add your input images to the folder.")
        return False
    
    print(f"Found {len(images)} images in '{input_folder}' folder.")
    return True

def run_data_preparation():
    """Run the data preparation script."""
    print("\n" + "="*60)
    print("RUNNING DATA PREPARATION")
    print("="*60)
    
    if not check_model_file() or not check_input_folder():
        return False
    
    try:
        # Import and run data preparation
        from data_preparation_tool import main
        main()
        return True
    except Exception as e:
        print(f"Error during data preparation: {e}")
        return False

def run_visualization_tool():
    """Run the interactive visualization tool."""
    print("\n" + "="*60)
    print("RUNNING VISUALIZATION TOOL")
    print("="*60)
    
    # Check if data folder exists
    if not os.path.exists("visualization_data"):
        print("Error: Data not prepared yet!")
        print("Please run option 1 (Data Preparation) first.")
        return False
    
    try:
        # Import and run visualization tool
        from interactive_visualization_tool import main as run_viz
        run_viz()
        return True
    except Exception as e:
        print(f"Error running visualization tool: {e}")
        return False

def main_menu():
    """Display main menu and handle user choice."""
    while True:
        print("\n" + "="*60)
        print("MEDICAL IMAGE HISTOGRAM ANALYSIS TOOL")
        print("="*60)
        print("1. Prepare Data (Process images and generate data files)")
        print("2. Open Visualization Tool (Browse and analyze processed data)")
        print("3. Check System Requirements")
        print("4. Exit")
        print("-" * 60)
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            if check_dependencies():
                success = run_data_preparation()
                if success:
                    print("\n✅ Data preparation completed successfully!")
                    print("You can now run the visualization tool (option 2).")
                else:
                    print("\n❌ Data preparation failed. Please check the errors above.")
            else:
                print("\n❌ Missing dependencies. Please install required packages.")
        
        elif choice == '2':
            if check_dependencies():
                run_visualization_tool()
            else:
                print("\n❌ Missing dependencies. Please install required packages.")
        
        elif choice == '3':
            print("\n" + "="*60)
            print("SYSTEM REQUIREMENTS CHECK")
            print("="*60)
            
            print("\n1. Checking Python packages...")
            deps_ok = check_dependencies()
            if deps_ok:
                print("✅ All required packages are installed.")
            
            print("\n2. Checking model file...")
            model_ok = check_model_file()
            if model_ok:
                print("✅ ONNX model file found.")
            
            print("\n3. Checking input folder...")
            input_ok = check_input_folder()
            if input_ok:
                print("✅ Input folder and images found.")
            
            print("\n4. Checking data preparation status...")
            if os.path.exists("visualization_data"):
                print("✅ Processed data found.")
            else:
                print("ℹ️  No processed data found. Run data preparation first.")
            
            overall_status = deps_ok and model_ok and input_ok
            print(f"\nOverall Status: {'✅ Ready' if overall_status else '❌ Issues found'}")
        
        elif choice == '4':
            print("\nGoodbye!")
            break
        
        else:
            print("\n❌ Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        print("Please check your setup and try again.")