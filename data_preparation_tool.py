#!/usr/bin/env python3
"""
Data Preparation Script for Medical Image Analysis
Processes images and generates histogram data for visualization tool.
"""

import os
import cv2
import glob
import numpy as np
import onnxruntime
from tqdm import tqdm
import json

def letterbox_resize(img, new_shape=(416, 416), color=(114, 114, 114)):
    """Resize and pad image while maintaining aspect ratio."""
    shape = img.shape[:2]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    new_unpad = (int(round(shape[1] * r)), int(round(shape[0] * r)))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]
    dw /= 2
    dh /= 2

    if shape[::-1] != new_unpad:
        resized_img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
    else:
        resized_img = img

    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    padded_img = cv2.copyMakeBorder(resized_img, top, bottom, left, right,
                                    cv2.BORDER_CONSTANT, value=color)
    return padded_img

def preprocess_image(img, input_size=(416, 416)):
    """Preprocess image for model input."""
    img_letterboxed = letterbox_resize(img, new_shape=input_size)
    img_rgb = img_letterboxed[:, :, ::-1]
    img_transposed = img_rgb.transpose(2, 0, 1)
    img_normalized = np.ascontiguousarray(img_transposed) / 255.0
    return img_normalized

def generate_cls_histogram(prediction):
    """Generate class confidence histogram."""
    prediction = np.array(prediction[0][0])
    class_probs = prediction[:, 5:]
    num_classes = class_probs.shape[1]
    num_bins = 100
    
    bins = np.linspace(0.0, 1.0, num_bins + 1)
    class_confidence_histogram = np.zeros((num_bins, num_classes))
    
    for class_idx in range(num_classes):
        hist, _ = np.histogram(class_probs[:, class_idx], bins=bins)
        class_confidence_histogram[:, class_idx] = hist
    
    return np.flipud(class_confidence_histogram)

def xywh2xyxy(x):
    """Convert nx4 boxes from [x, y, w, h] to [x1, y1, x2, y2]"""
    y = np.copy(x)
    y[:, 0] = x[:, 0] - x[:, 2] / 2
    y[:, 1] = x[:, 1] - x[:, 3] / 2
    y[:, 2] = x[:, 0] + x[:, 2] / 2
    y[:, 3] = x[:, 1] + x[:, 3] / 2
    return y

def nms(dets, scores, thresh):
    """Non-Maximum Suppression implementation"""
    x1, y1, x2, y2 = dets[:, 0], dets[:, 1], dets[:, 2], dets[:, 3]
    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
    order = scores.argsort()[::-1]

    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])

        w = np.maximum(0.0, xx2 - xx1 + 1)
        h = np.maximum(0.0, yy2 - yy1 + 1)
        inter = w * h
        ovr = inter / (areas[i] + areas[order[1:]] - inter)

        inds = np.where(ovr <= thresh)[0]
        order = order[inds + 1]

    return keep

def non_max_suppression(prediction, conf_thres=0.25, iou_thres=0.45):
    """Performs Non-Maximum Suppression on inference results"""
    nc = prediction.shape[2] - 5
    xc = prediction[..., 4] > conf_thres
    
    output = [np.zeros((0, 6))] * prediction.shape[0]

    for xi, x in enumerate(prediction):
        x = x[xc[xi]]
        if not x.shape[0]:
            continue

        x[:, 5:] *= x[:, 4:5]
        box = xywh2xyxy(x[:, :4])

        i, j = (x[:, 5:] > conf_thres).nonzero()
        x = np.concatenate((box[i], x[i, j + 5, None], j[:, None].astype(np.float32)), 1)

        n = x.shape[0]
        if not n:
            continue
        elif n > 30000:
            x = x[(np.argsort(x[:, 4])[::-1])[:30000]]

        c = x[:, 5:6] * 4096
        boxes, scores = x[:, :4] + c, x[:, 4]
        i = nms(boxes, scores, iou_thres)

        if len(i) > 300:
            i = i[:300]

        output[xi] = x[i]

    return output

def postprocess_detections(prediction, conf_threshold=0.25, iou_threshold=0.45):
    """Process raw detections using NMS."""
    detections = non_max_suppression(prediction, conf_thres=conf_threshold, iou_thres=iou_threshold)
    
    if len(detections) == 0 or len(detections[0]) == 0:
        return [], [], []
    
    det = detections[0]
    boxes, scores, class_ids = [], [], []
    
    for detection in det:
        x1, y1, x2, y2, score, class_id = detection
        boxes.append([x1, y1, x2, y2])
        scores.append(float(score))
        class_ids.append(int(class_id))
    
    return boxes, scores, class_ids

def draw_detections(img, boxes, scores, class_ids, mapping, input_size=(416, 416)):
    """Draw bounding boxes and labels on the image."""
    h0, w0 = img.shape[:2]
    r = min(input_size[0] / h0, input_size[1] / w0)
    new_unpad = (int(round(w0 * r)), int(round(h0 * r)))
    dw = (input_size[1] - new_unpad[0]) / 2
    dh = (input_size[0] - new_unpad[1]) / 2
    
    result_img = img.copy()
    bbox_colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
    
    for i, (box, score, class_id) in enumerate(zip(boxes, scores, class_ids)):
        x1, y1, x2, y2 = box
        # Undo letterbox transform
        x1 = (x1 - dw) / r
        y1 = max(5, (y1 - dh) / r)
        x2 = (x2 - dw) / r
        y2 = (y2 - dh) / r
        
        color = bbox_colors[i % len(bbox_colors)]
        cv2.rectangle(result_img, (int(x1), int(y1)), (int(x2), int(y2)), color, 3)
        
        label = mapping.get(str(class_id), str(class_id))
        text = f"{label}: {score:.3f}"
        (w_text, h_text), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.rectangle(result_img, (int(x1), int(y1) - h_text - 6),
                      (int(x1) + w_text, int(y1)), color, -1)
        cv2.putText(result_img, text, (int(x1), int(y1) - 3),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    return result_img

def main():
    """Main function to prepare data for visualization tool."""
    
    # Class mapping
    mapping = {
        "0": "pyloric_valve", "1": "device", "2": "incisura", "3": "antrum_muscle",
        "4": "esophagus_cardia_junction", "5": "esophagus", "6": "incisura_arc_lower_body",
        "7": "incisura_arc_middle_upper_body", "8": "vocal_cord", "9": "d1_bulb", "10": "d2_center",
        "11": "epiglottis", "12": "teeth", "13": "tongue", "14": "pc_ring", "15": "fornix",
        "16": "left_atrium", "17": "left_main_bronchus", "18": "froth", "19": "food_residue",
        "20": "instrument_head[closed]", "21": "instrument", "22": "blood", "23": "instrument_head[open]",
        "24": "water jet", "25": "filled water area", "26": "bubbles"
    }
    
    # Paths
    model_path = "cerebro_v6.0.1_od_model.onnx"
    input_folder = "recra"
    output_folder = "visualization_data"
    cropped_folder = os.path.join(output_folder, "cropped_images")
    
    # Create output directories
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(cropped_folder, exist_ok=True)
    
    # Initialize model
    print("Loading ONNX model...")
    session = onnxruntime.InferenceSession(model_path,
                                           providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
    
    # Get image paths and sort them
    image_paths = sorted(glob.glob(os.path.join(input_folder, "*.jpg")))
    if not image_paths:
        print("No images found in the input folder!")
        return
    
    print(f"Processing {len(image_paths)} images...")
    
    # Store all histogram data
    all_histogram_data = {}
    frame_info = {}
    
    for idx, image_path in enumerate(tqdm(image_paths, desc="Processing frames")):
        original_img = cv2.imread(image_path)
        if original_img is None:
            continue

        frame_name = os.path.basename(image_path).replace('.jpg', '')
        cropped_img = original_img[40:1049, 720:1870]  # Crop to region of interest
        
        # Inference
        preprocessed_img = preprocess_image(cropped_img)
        input_tensor = np.expand_dims(preprocessed_img, axis=0).astype(np.float32)
        
        input_name = session.get_inputs()[0].name
        outputs = session.run(None, {input_name: input_tensor})
        
        # Generate histogram
        histogram_data = generate_cls_histogram(outputs)
        
        # Process detections
        prediction = np.expand_dims(outputs[0], axis=0)
        boxes, scores, class_ids = postprocess_detections(prediction)
        
        # Draw detections on cropped image
        overlay_img = draw_detections(cropped_img.copy(), boxes, scores, class_ids, mapping)
        
        # Save cropped image with detections
        cropped_output_path = os.path.join(cropped_folder, f"{frame_name}.jpg")
        cv2.imwrite(cropped_output_path, overlay_img)
        
        # Store histogram data (convert to list for JSON serialization)
        all_histogram_data[frame_name] = histogram_data.tolist()
        
        # Store frame info
        frame_info[frame_name] = {
            "index": idx,
            "detections": len(boxes),
            "classes_detected": list(set(class_ids)),
            "detection_data": [
                {
                    "class_id": int(class_id),
                    "class_name": mapping.get(str(class_id), str(class_id)),
                    "score": float(score),
                    "bbox": [float(x) for x in box]
                }
                for box, score, class_id in zip(boxes, scores, class_ids)
            ]
        }
    
    # Save all data files
    print("\nSaving data files...")
    
    # Save histogram data to JSON (compact format to reduce file size)
    histogram_file = os.path.join(output_folder, "histogram_data.json")
    with open(histogram_file, 'w') as f:
        json.dump(all_histogram_data, f, separators=(',', ':'))  # No indentation for smaller file
    
    # Also save a compressed numpy version for even better performance
    histogram_npz_file = os.path.join(output_folder, "histogram_data.npz")
    np.savez_compressed(histogram_npz_file, **{k: np.array(v) for k, v in all_histogram_data.items()})
    
    # Save frame info to JSON
    frame_info_file = os.path.join(output_folder, "frame_info.json")
    with open(frame_info_file, 'w') as f:
        json.dump(frame_info, f, indent=2)
    
    # Save class mapping
    mapping_file = os.path.join(output_folder, "class_mapping.json")
    with open(mapping_file, 'w') as f:
        json.dump(mapping, f, indent=2)
    
    # Create frame list for easy navigation
    frame_list = [os.path.basename(path).replace('.jpg', '') for path in image_paths]
    frame_list_file = os.path.join(output_folder, "frame_list.json")
    with open(frame_list_file, 'w') as f:
        json.dump(frame_list, f, indent=2)
    
    print(f"\n✅ Data preparation complete!")
    print(f"📁 Cropped images saved to: {cropped_folder}")
    print(f"📊 Histogram data saved to: {histogram_file}")
    print(f"📝 Frame info saved to: {frame_info_file}")
    print(f"🏷️  Class mapping saved to: {mapping_file}")
    print(f"📋 Frame list saved to: {frame_list_file}")
    print(f"🎯 Total frames processed: {len(frame_list)}")

if __name__ == "__main__":
    main()