import pyrealsense2 as rs
import numpy as np
import cv2
import datetime
import os
import time

# Directory to store images
STORAGE_DIR = "captured_files"
os.makedirs(STORAGE_DIR, exist_ok=True)

# Initialize RealSense pipeline
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 1024, 768, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 30)
pipeline.start(config)

# Define trapezium crop points
src_points = np.float32([
    [195, 0],       # top-left (remove 195px from top-left)
    [1800, 0],      # top-right (remove 120px from top-right)
    [1919, 1079],   # bottom-right
    [30, 1079]      # bottom-left (remove 30px from bottom-left)
])
output_width, output_height = 1500, 1080
dst_points = np.float32([
    [0, 0],
    [output_width - 1, 0],
    [output_width - 1, output_height - 1],
    [0, output_height - 1]
])
# Compute transformation matrix once
perspective_matrix = cv2.getPerspectiveTransform(src_points, dst_points)

def capture_frames():
    """Captures RGB (with trapezium crop), Depth, and PLY files every 5 seconds and saves them locally."""
    try:
        while True:
            for _ in range(10):  # Skip initial frames for better quality
                pipeline.wait_for_frames()

            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()

            if not depth_frame or not color_frame:
                print("❌ No frames captured")
                continue

            # Convert depth frame to image
            depth_image = np.asanyarray(depth_frame.get_data())
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

            # Convert RGB frame to image
            color_image = np.asanyarray(color_frame.get_data())

            # Apply trapezium crop (perspective warp)
            cropped_color = cv2.warpPerspective(color_image, perspective_matrix, (output_width, output_height))

            # Generate file names
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            depth_filename = os.path.join(STORAGE_DIR, f"depth_snapshot_{timestamp}.png")
            color_filename = os.path.join(STORAGE_DIR, f"rgb_snapshot_{timestamp}.png")
            ply_filename = os.path.join(STORAGE_DIR, f"pointcloud_{timestamp}.ply")

            # Save images locally
            cv2.imwrite(depth_filename, depth_colormap)
            cv2.imwrite(color_filename, cropped_color)
            print(f"📸 Captured: {depth_filename}, {color_filename}")

            # Save PLY file (based on full color + depth frame)
            pc = rs.pointcloud()
            pc.map_to(color_frame)
            pointcloud = pc.calculate(depth_frame)
            pointcloud.export_to_ply(ply_filename, color_frame)
            print(f"📸 Captured: {ply_filename}")

            # Wait before next capture
            time.sleep(1)

    except KeyboardInterrupt:
        print("🛑 Capture process interrupted. Stopping...")
    finally:
        pipeline.stop()

if __name__ == "__main__":
    capture_frames()
