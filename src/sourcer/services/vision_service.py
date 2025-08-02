"""Vision analysis service integrating YOLO, MobileSAM, and LLaVA."""

import logging
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

import numpy as np
import cv2
import torch
from ultralytics import YOLO
from transformers import AutoProcessor, LlavaForConditionalGeneration
from PIL import Image

from sourcer.utils.config_loader import ConfigLoader


class VisionService:
    """Service for visual analysis using AI models."""

    def __init__(self, config: ConfigLoader) -> None:
        """
        Initialize the vision service.
        
        Args:
            config: Configuration loader instance
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Model instances
        self.yolo_model: Optional[YOLO] = None
        self.sam_model: Optional[Any] = None  # MobileSAM model
        self.llava_model: Optional[LlavaForConditionalGeneration] = None
        self.llava_processor: Optional[AutoProcessor] = None
        
        # Configuration
        self.target_objects = self.config.get_list("Vision", "target_objects")
        self.confidence_threshold = self.config.get_float("Vision", "confidence_threshold", 0.5)
        self.max_detections = self.config.get_int("Vision", "max_detections", 10)
        self.enable_gpu = self.config.get_bool("Performance", "enable_gpu", True)
        
        # Device setup
        self.device = "cuda" if torch.cuda.is_available() and self.enable_gpu else "cpu"
        self.is_initialized = False

    def initialize(self) -> bool:
        """
        Initialize vision models.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Check for mock mode
            if self.config.get_bool("Development", "MOCK_MODELS", False):
                self.logger.info("Using mock vision models")
                self.is_initialized = True
                return True
            
            # Load YOLO model
            if not self._load_yolo():
                return False
            
            # Load SAM model
            if not self._load_sam():
                return False
            
            # Load LLaVA model
            if not self._load_llava():
                return False
            
            self.is_initialized = True
            self.logger.info("Vision service initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize vision service: {e}")
            return False

    def _load_yolo(self) -> bool:
        """Load YOLO model."""
        try:
            model_path = self.config.get_path("Models", "yolo_model")
            if not model_path or not model_path.exists():
                self.logger.error(f"YOLO model not found at {model_path}")
                return False
            
            self.logger.info(f"Loading YOLO model from {model_path}")
            self.yolo_model = YOLO(str(model_path))
            self.yolo_model.to(self.device)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load YOLO model: {e}")
            return False

    def _load_sam(self) -> bool:
        """Load MobileSAM model."""
        try:
            model_path = self.config.get_path("Models", "sam_model")
            if not model_path or not model_path.exists():
                self.logger.warning(f"SAM model not found at {model_path}")
                # SAM is optional for MVP
                return True
            
            # TODO: Implement MobileSAM loading
            # For now, we'll skip SAM as it's used for context enhancement
            self.logger.info("SAM model loading skipped for MVP")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load SAM model: {e}")
            return False

    def _load_llava(self) -> bool:
        """Load LLaVA model."""
        try:
            model_path = self.config.get_path("Models", "llava_model")
            if not model_path or not model_path.exists():
                self.logger.warning(f"LLaVA model not found at {model_path}")
                # For MVP, we can work without LLaVA
                return True
            
            self.logger.info(f"Loading LLaVA model from {model_path}")
            
            # Load processor and model
            self.llava_processor = AutoProcessor.from_pretrained(str(model_path))
            self.llava_model = LlavaForConditionalGeneration.from_pretrained(
                str(model_path),
                torch_dtype=torch.float16 if self.enable_gpu else torch.float32,
                low_cpu_mem_usage=True
            )
            
            if self.enable_gpu:
                self.llava_model = self.llava_model.to(self.device)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load LLaVA model: {e}")
            # LLaVA is optional for MVP
            return True

    def detect_objects(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """
        Detect objects in a frame using YOLO.
        
        Args:
            frame: Input frame as numpy array
            
        Returns:
            List of detected objects with bounding boxes
        """
        if not self.is_initialized:
            return []
        
        if self.config.get_bool("Development", "MOCK_MODELS", False):
            return self._mock_detect_objects()
        
        try:
            # Run YOLO detection
            results = self.yolo_model(frame, conf=self.confidence_threshold)
            
            detections = []
            for r in results:
                boxes = r.boxes
                if boxes is None:
                    continue
                
                for i, box in enumerate(boxes):
                    if i >= self.max_detections:
                        break
                    
                    # Get class name
                    class_id = int(box.cls)
                    class_name = self.yolo_model.names.get(class_id, "unknown")
                    
                    # Filter by target objects if specified
                    if self.target_objects and class_name not in self.target_objects:
                        continue
                    
                    # Extract detection info
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    confidence = float(box.conf)
                    
                    detection = {
                        "label": class_name,
                        "confidence": confidence,
                        "bbox": {
                            "x1": int(x1),
                            "y1": int(y1),
                            "x2": int(x2),
                            "y2": int(y2)
                        },
                        "center": {
                            "x": int((x1 + x2) / 2),
                            "y": int((y1 + y2) / 2)
                        }
                    }
                    
                    detections.append(detection)
            
            return detections
            
        except Exception as e:
            self.logger.error(f"Error during object detection: {e}")
            return []

    def _mock_detect_objects(self) -> List[Dict[str, Any]]:
        """Generate mock object detections."""
        import random
        
        mock_objects = ["person", "laptop", "chair", "table", "cup", "phone"]
        detections = []
        
        num_objects = random.randint(1, 3)
        for i in range(num_objects):
            obj = random.choice(mock_objects)
            detections.append({
                "label": obj,
                "confidence": random.uniform(0.7, 0.95),
                "bbox": {
                    "x1": random.randint(50, 200),
                    "y1": random.randint(50, 200),
                    "x2": random.randint(250, 400),
                    "y2": random.randint(250, 400)
                },
                "center": {
                    "x": random.randint(150, 300),
                    "y": random.randint(150, 300)
                }
            })
        
        return detections

    def describe_scene(self, frame: np.ndarray, detections: List[Dict[str, Any]]) -> str:
        """
        Generate a scene description using LLaVA.
        
        Args:
            frame: Input frame
            detections: Object detections from YOLO
            
        Returns:
            Scene description text
        """
        if not self.is_initialized:
            return "Vision service not initialized."
        
        if self.config.get_bool("Development", "MOCK_MODELS", False):
            return self._mock_describe_scene(detections)
        
        # If LLaVA is not available, use basic description
        if not self.llava_model:
            return self._basic_scene_description(detections)
        
        try:
            # Convert frame to PIL Image
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            
            # Prepare prompt
            prompt = self._create_scene_prompt(detections)
            
            # Process with LLaVA
            inputs = self.llava_processor(prompt, image, return_tensors="pt")
            if self.enable_gpu:
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate description
            with torch.no_grad():
                output = self.llava_model.generate(
                    **inputs,
                    max_new_tokens=100,
                    temperature=0.7
                )
            
            description = self.llava_processor.decode(output[0], skip_special_tokens=True)
            
            # Extract only the generated part
            if prompt in description:
                description = description.replace(prompt, "").strip()
            
            return description
            
        except Exception as e:
            self.logger.error(f"Error generating scene description: {e}")
            return self._basic_scene_description(detections)

    def _create_scene_prompt(self, detections: List[Dict[str, Any]]) -> str:
        """Create prompt for LLaVA based on detections."""
        objects = [d["label"] for d in detections]
        object_list = ", ".join(objects) if objects else "no specific objects"
        
        prompt = (
            f"You are looking at a scene that contains {object_list}. "
            f"Please provide a brief, natural description of what you see in the image. "
            f"Focus on the spatial relationships and overall context."
        )
        
        return prompt

    def _basic_scene_description(self, detections: List[Dict[str, Any]]) -> str:
        """Generate basic scene description without LLaVA."""
        if not detections:
            return "I don't see any specific objects in the current view."
        
        # Count objects
        object_counts: Dict[str, int] = {}
        for det in detections:
            label = det["label"]
            object_counts[label] = object_counts.get(label, 0) + 1
        
        # Build description
        parts = []
        for obj, count in object_counts.items():
            if count == 1:
                parts.append(f"a {obj}")
            else:
                parts.append(f"{count} {obj}s")
        
        if len(parts) == 1:
            description = f"I can see {parts[0]} in the scene."
        elif len(parts) == 2:
            description = f"I can see {parts[0]} and {parts[1]} in the scene."
        else:
            description = f"I can see {', '.join(parts[:-1])}, and {parts[-1]} in the scene."
        
        # Add spatial information
        if len(detections) > 1:
            description += " The objects appear to be arranged in your immediate environment."
        
        return description

    def _mock_describe_scene(self, detections: List[Dict[str, Any]]) -> str:
        """Generate mock scene description."""
        if not detections:
            return "The scene appears to be empty."
        
        descriptions = [
            "I see a typical workspace environment",
            "This appears to be an office or study area",
            "The scene shows a comfortable working space",
            "I can see various objects arranged in the room"
        ]
        
        import random
        base = random.choice(descriptions)
        
        objects = [d["label"] for d in detections]
        if objects:
            base += f" with {', '.join(objects)} visible."
        
        return base

    def analyze_frame(self, frame: np.ndarray) -> Dict[str, Any]:
        """
        Perform complete visual analysis on a frame.
        
        Args:
            frame: Input frame
            
        Returns:
            Analysis results including detections and description
        """
        # Detect objects
        detections = self.detect_objects(frame)
        
        # Generate scene description
        description = self.describe_scene(frame, detections)
        
        # Compile results
        results = {
            "detections": detections,
            "description": description,
            "object_count": len(detections),
            "detected_classes": list(set(d["label"] for d in detections))
        }
        
        return results

    def cleanup(self) -> None:
        """Clean up vision service resources."""
        # Clear model references
        self.yolo_model = None
        self.sam_model = None
        self.llava_model = None
        self.llava_processor = None
        
        # Clear GPU cache if using CUDA
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        self.is_initialized = False
        self.logger.info("Vision service cleaned up")

    def get_status(self) -> Dict[str, Any]:
        """
        Get vision service status.
        
        Returns:
            Status dictionary
        """
        return {
            "is_initialized": self.is_initialized,
            "device": self.device,
            "models_loaded": {
                "yolo": self.yolo_model is not None,
                "sam": self.sam_model is not None,
                "llava": self.llava_model is not None
            },
            "target_objects": self.target_objects,
            "confidence_threshold": self.confidence_threshold
        }