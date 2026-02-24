import boto3
import os
import time

# AWS S3 Configuration
AWS_REGION = "ap-south-1"
AWS_BUCKET_NAME = "lidarimages"
AWS_ACCESS_KEY = ""
AWS_SECRET_KEY = ""

# Directory where captured images are stored
STORAGE_DIR = "captured_files"
os.makedirs(STORAGE_DIR, exist_ok=True)

# Initialize AWS S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

def determine_s3_subfolder(file_name):
    """Determine subfolder inside Depth_Images/ based on filename pattern."""
    if file_name.lower().startswith("rgb_snapshot"):
        return "RGB_Images/"
    elif file_name.lower().startswith("depth_snapshot"):
        return "Depth_Images/"
    elif file_name.lower().endswith(".ply"):
        return "PointCloud_Files/"
    else:
        return None  # Skip unrecognized files

def upload_files():
    """Uploads all files to respective folders under Depth_Images/ in S3 and deletes them after upload."""
    try:
        while True:
            files = os.listdir(STORAGE_DIR)
            if not files:
                time.sleep(1)
                continue

            for file_name in files:
                file_path = os.path.join(STORAGE_DIR, file_name)
                if not os.path.isfile(file_path):
                    continue  # skip non-files

                subfolder = determine_s3_subfolder(file_name)
                if subfolder is None:
                    print(f"⚠ Skipping unrecognized file: {file_name}")
                    continue

                # Full S3 key includes parent folder Depth_Images/
                s3_key = f"Depth_Images/{subfolder}{file_name}"

                try:
                    s3_client.upload_file(file_path, AWS_BUCKET_NAME, s3_key)
                    print(f"✅ Uploaded to S3: {file_name} → {s3_key}")
                    os.remove(file_path)
                    print(f"🗑 Deleted local file: {file_name}")
                except Exception as e:
                    print(f"❌ Error uploading {file_name}: {e}")

    except KeyboardInterrupt:
        print("🛑 Upload process interrupted. Stopping...")

if _name_ == "_main_":
    upload_files()