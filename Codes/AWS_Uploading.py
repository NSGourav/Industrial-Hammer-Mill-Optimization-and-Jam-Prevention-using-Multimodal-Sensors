import boto3
import os
import time

# AWS S3 Configuration
AWS_REGION = "ap-south-1"  # e.g., "us-east-1"
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

def upload_files():
    """Uploads all stored files to the Depth_Images folder in S3 and deletes them after upload."""
    try:
        while True:
            files = os.listdir(STORAGE_DIR)
            if not files:
                time.sleep(1)  # Check every second for new files
                continue

            for file_name in files:
                file_path = os.path.join(STORAGE_DIR, file_name)
                try:
                    # Specify the folder name in the S3 key (i.e., Depth_Images/)
                    s3_key = f"Depth_Images/{file_name}"

                    # Upload the file to the specified folder in the S3 bucket
                    s3_client.upload_file(file_path, AWS_BUCKET_NAME, s3_key)
                    print(f"✅ Uploaded to S3: {file_name} into Depth_Images folder")
                    os.remove(file_path)  # Delete after successful upload
                    print(f"🗑️ Deleted local file: {file_name}")
                except Exception as e:
                    print(f"❌ Error uploading {file_name}: {e}")

    except KeyboardInterrupt:
        print("🛑 Upload process interrupted. Stopping...")

if __name__ == "__main__":
    upload_files()

