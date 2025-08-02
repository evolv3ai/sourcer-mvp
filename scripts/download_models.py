#!/usr/bin/env python3
"""Script to download required AI models for Sourcer MVP."""

import os
import sys
import shutil
import hashlib
import tarfile
import zipfile
from pathlib import Path
from urllib.request import urlretrieve
from urllib.error import URLError

import requests
from tqdm import tqdm


# Model configurations
MODELS = {
    "yolo": {
        "name": "YOLOv8n",
        "url": "https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt",
        "path": "vision/yolo/yolov8n.pt",
        "size_mb": 6.2,
        "hash": "4f4f4f4f4f4f4f4f"  # Replace with actual hash
    },
    "vosk_stt": {
        "name": "Vosk Small English Model",
        "url": "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip",
        "path": "stt/vosk-model-small-en-us-0.15",
        "size_mb": 40,
        "hash": "5f5f5f5f5f5f5f5f",  # Replace with actual hash
        "extract": True
    },
    "piper_tts": {
        "name": "Piper TTS Amy Medium",
        "url": "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/medium/en_US-amy-medium.onnx",
        "path": "tts/en_US-amy-medium.onnx",
        "size_mb": 63,
        "hash": "6f6f6f6f6f6f6f6f"  # Replace with actual hash
    }
}

# Optional models (not required for basic MVP)
OPTIONAL_MODELS = {
    "mobile_sam": {
        "name": "MobileSAM",
        "url": "https://github.com/ChaoningZhang/MobileSAM/raw/master/weights/mobile_sam.pt",
        "path": "vision/sam/mobile_sam.pt",
        "size_mb": 40,
        "hash": "7f7f7f7f7f7f7f7f"
    },
    "llava": {
        "name": "LLaVA v1.5 7B",
        "url": "manual",  # Too large for direct download
        "path": "vision/llava/llava-v1.5-7b",
        "size_mb": 13000,
        "instructions": "Please download LLaVA manually from https://github.com/haotian-liu/LLaVA"
    }
}


class ModelDownloader:
    """Handles model downloading and setup."""

    def __init__(self, models_dir: Path):
        """Initialize the downloader."""
        self.models_dir = models_dir
        self.models_dir.mkdir(parents=True, exist_ok=True)

    def download_file(self, url: str, dest_path: Path, desc: str) -> bool:
        """
        Download a file with progress bar.
        
        Args:
            url: URL to download from
            dest_path: Destination file path
            desc: Description for progress bar
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get file size
            response = requests.head(url, allow_redirects=True)
            file_size = int(response.headers.get('content-length', 0))
            
            # Download with progress bar
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                
                with open(dest_path, 'wb') as f:
                    with tqdm(total=file_size, unit='B', unit_scale=True, desc=desc) as pbar:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                            pbar.update(len(chunk))
            
            return True
            
        except Exception as e:
            print(f"Error downloading {desc}: {e}")
            return False

    def extract_archive(self, archive_path: Path, extract_dir: Path) -> bool:
        """Extract a zip or tar archive."""
        try:
            # Detect archive type - check for .zip in name or try to open as zip
            is_zip = (archive_path.suffix == '.zip' or
                     archive_path.name.endswith('.zip') or
                     archive_path.name.endswith('.download'))  # Handle .download files
            
            if is_zip:
                try:
                    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                        zip_ref.extractall(extract_dir)
                    return True
                except zipfile.BadZipFile:
                    # If it's not a zip, try other formats
                    pass
            
            # Try tar formats
            if archive_path.suffix in ['.tar', '.gz', '.tgz'] or not is_zip:
                try:
                    with tarfile.open(archive_path, 'r:*') as tar_ref:
                        tar_ref.extractall(extract_dir)
                    return True
                except (tarfile.TarError, tarfile.ReadError):
                    pass
            
            # If we get here, we couldn't extract the file
            print(f"Unknown or unsupported archive format: {archive_path}")
            return False
            
        except Exception as e:
            print(f"Error extracting {archive_path}: {e}")
            return False

    def verify_file(self, file_path: Path, expected_hash: str) -> bool:
        """Verify file integrity with hash."""
        # For MVP, skip hash verification
        # In production, implement proper hash checking
        return file_path.exists()

    def download_model(self, model_id: str, model_config: dict) -> bool:
        """Download a single model."""
        print(f"\n{'='*60}")
        print(f"Downloading {model_config['name']}...")
        print(f"Size: ~{model_config['size_mb']} MB")
        
        # Check if manual download required
        if model_config['url'] == 'manual':
            print(f"\nManual download required for {model_config['name']}")
            print(f"Instructions: {model_config.get('instructions', 'See documentation')}")
            return False
        
        # Prepare destination
        dest_path = self.models_dir / model_config['path']
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Check if already exists
        if dest_path.exists():
            if dest_path.is_file() or (dest_path.is_dir() and any(dest_path.iterdir())):
                print(f"✓ {model_config['name']} already exists")
                return True
        
        # Download
        temp_path = dest_path.with_suffix('.download')
        
        if not self.download_file(model_config['url'], temp_path, model_config['name']):
            return False
        
        # Extract if needed
        if model_config.get('extract', False):
            print(f"Extracting {model_config['name']}...")
            
            if not self.extract_archive(temp_path, dest_path.parent):
                print(f"Failed to extract {model_config['name']}")
                return False
            
            # Remove archive after extraction
            temp_path.unlink()
            
            # Verify extraction worked - check if the expected directory exists
            if dest_path.exists():
                print(f"✓ Extraction verified - {dest_path} exists")
            else:
                print(f"✗ Extraction verification failed - {dest_path} not found")
                # List what was actually extracted to help debug
                extracted_items = list(dest_path.parent.iterdir())
                print(f"Items in {dest_path.parent}: {[item.name for item in extracted_items]}")
                return False
        else:
            # Move to final location
            temp_path.rename(dest_path)
        
        print(f"✓ {model_config['name']} downloaded successfully")
        return True


def main():
    """Main function."""
    print("Sourcer MVP Model Downloader")
    print("="*60)
    
    # Get project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    models_dir = project_root / "models"
    
    # Create downloader
    downloader = ModelDownloader(models_dir)
    
    # Download required models
    print("\nDownloading required models...")
    success = True
    
    for model_id, model_config in MODELS.items():
        if not downloader.download_model(model_id, model_config):
            success = False
            print(f"✗ Failed to download {model_config['name']}")
    
    # Ask about optional models
    print("\n" + "="*60)
    print("Optional models (for enhanced functionality):")
    
    for model_id, model_config in OPTIONAL_MODELS.items():
        print(f"\n- {model_config['name']} ({model_config['size_mb']} MB)")
        
        if model_config['url'] == 'manual':
            print(f"  {model_config.get('instructions', '')}")
            continue
        
        response = input("  Download? (y/N): ").strip().lower()
        if response == 'y':
            downloader.download_model(model_id, model_config)
    
    # Summary
    print("\n" + "="*60)
    if success:
        print("✓ All required models downloaded successfully!")
        print(f"\nModels are stored in: {models_dir}")
        print("\nYou can now run the application with:")
        print("  ./scripts/run_dev.sh")
    else:
        print("✗ Some models failed to download.")
        print("Please check the errors above and try again.")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())