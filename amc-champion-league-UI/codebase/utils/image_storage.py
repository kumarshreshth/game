import boto3
import os
from fastapi import UploadFile
from typing import List, Optional
import uuid

# Import config manager
from codebase.utils.config_manager import config

# Get storage configuration
storage_config = config.get_storage_config()
S3_BUCKET_NAME = storage_config["s3_bucket_name"]
S3_REGION = storage_config["s3_region"]
USE_S3 = storage_config["use_s3"]
LOCAL_IMAGE_DIR = storage_config["local_image_dir"]

# Initialize S3 client if S3 is enabled
s3_client = boto3.client('s3') if USE_S3 else None

# Ensure local directory exists if not using S3
if not USE_S3:
    os.makedirs(LOCAL_IMAGE_DIR, exist_ok=True)
    os.makedirs(os.path.join(LOCAL_IMAGE_DIR, "games"), exist_ok=True)
    os.makedirs(os.path.join(LOCAL_IMAGE_DIR, "franchises"), exist_ok=True)
    os.makedirs(os.path.join(LOCAL_IMAGE_DIR, "players"), exist_ok=True)
    os.makedirs(os.path.join(LOCAL_IMAGE_DIR, "gallery"), exist_ok=True)

async def upload_image_to_storage(file: UploadFile, folder: str = "gallery") -> str:
    """
    Upload an image to S3 or local storage and return the path/URL
    
    Args:
        file: The uploaded file
        folder: Subfolder to store the image in (games, franchises, players, gallery)
        
    Returns:
        str: The path/URL to the uploaded image
    """
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    
    # Full path for the file
    file_path = f"{folder}/{unique_filename}"
    
    # Read file content
    file_content = await file.read()
    
    if USE_S3:
        # Upload to S3
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=file_path,
            Body=file_content
        )
        return f"s3://{S3_BUCKET_NAME}/{file_path}"
    else:
        # Save to local filesystem
        local_path = os.path.join(LOCAL_IMAGE_DIR, file_path)
        with open(local_path, "wb") as f:
            f.write(file_content)
        return f"/images/{file_path}"

def list_images_from_storage(folder: str = "gallery") -> List[str]:
    """
    List all images in a specific folder from S3 or local storage
    
    Args:
        folder: The folder to list images from
        
    Returns:
        List[str]: List of image paths/URLs
    """
    if USE_S3:
        # List objects from S3
        response = s3_client.list_objects_v2(
            Bucket=S3_BUCKET_NAME,
            Prefix=folder
        )
        
        if 'Contents' in response:
            return [f"s3://{S3_BUCKET_NAME}/{item['Key']}" for item in response['Contents']]
        return []
    else:
        # List files from local directory
        folder_path = os.path.join(LOCAL_IMAGE_DIR, folder)
        if not os.path.exists(folder_path):
            return []
            
        files = os.listdir(folder_path)
        return [f"/images/{folder}/{file}" for file in files]

def delete_image_from_storage(image_path: str) -> bool:
    """
    Delete an image from S3 or local storage
    
    Args:
        image_path: The full path/URL to the image
        
    Returns:
        bool: True if deletion was successful
    """
    try:
        if USE_S3 and image_path.startswith(f"s3://{S3_BUCKET_NAME}/"):
            # Extract key from S3 URL
            key = image_path.replace(f"s3://{S3_BUCKET_NAME}/", "")
            s3_client.delete_object(Bucket=S3_BUCKET_NAME, Key=key)
        elif image_path.startswith("/images/"):
            # Delete from local filesystem
            local_path = os.path.join(LOCAL_IMAGE_DIR, image_path.replace("/images/", ""))
            if os.path.exists(local_path):
                os.remove(local_path)
        return True
    except Exception as e:
        print(f"Error deleting image {image_path}: {str(e)}")
        return False
