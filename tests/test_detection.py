# tests/test_detection.py

import pytest
import numpy as np
from app.modules.object_detection import ObjectDetection

@pytest.fixture
def detection_model_stub():
    """
    A simple fixture that returns a 'mock' detection model, 
    as we don't have a real YOLO or similar loaded for tests.
    """
    return "mock_detection_model"

@pytest.fixture
def object_detector(detection_model_stub):
    """
    Creates an ObjectDetection instance with the stub model.
    """
    return ObjectDetection(detection_model_stub)

def test_no_frame(object_detector):
    """
    If detect_objects is called with None, 
    we expect an empty list of detections.
    """
    detections = object_detector.detect_objects(None)
    assert detections == [], "Detection should return empty list when frame is None"

def test_detection_output(object_detector):
    """
    Verifies that even with a stub approach, 
    detect_objects returns at least one detection with the expected keys.
    """
    # Create a dummy frame (black image) 640x480
    frame = np.zeros((480, 640, 3), dtype=np.uint8)

    detections = object_detector.detect_objects(frame)
    assert isinstance(detections, list), "Expected a list of detections"
    assert len(detections) > 0, "Expected at least one stub detection"

    # Check that each detection has required keys
    for det in detections:
        assert "label" in det, "Detection missing 'label'"
        assert "bbox" in det, "Detection missing 'bbox'"
        assert "confidence" in det, "Detection missing 'confidence'"

        # Further checks if needed
        # e.g., check that 'bbox' is a 4-tuple, confidence is float, etc.
