# app/modules/object_recognition.py

import json

class ObjectRecognition:
    """
    Converts 2D bounding boxes into 3D positions and associates them
    with known furniture or object types.

    In a real system, you might:
      - Use camera intrinsics and possibly a depth sensor to accurately
        compute 3D coordinates from 2D bounding boxes.
      - Or rely on AR device tracking (SLAM) to know where a detection is
        in the environment relative to the user.
    """

    def __init__(self, building_model, furniture_db_path):
        """
        :param building_model: A data structure containing the loaded 3D model
                               of the building/environment.
        :param furniture_db_path: Path to a JSON file with a 'furniture DB'.
                                  For example, keys could be object names
                                  ("chair", "table") with relevant metadata.
        """
        self.building_model = building_model

        # Load furniture DB
        try:
            with open(furniture_db_path, "r") as f:
                self.furniture_db = json.load(f)
            print(f"[ObjectRecognition] Loaded furniture DB from {furniture_db_path}")
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"[ObjectRecognition] Could not load furniture DB from {furniture_db_path}; using empty dict.")
            self.furniture_db = {}

    def map_2D_to_3D(self, bbox, camera_pose):
        """
        Convert a 2D bounding box (x1, y1, x2, y2) into a rough 3D position.

        :param bbox: (x1, y1, x2, y2) in image pixel coordinates.
        :param camera_pose: For AR glasses or a robot, might be (x, y, z, orientation) 
                            or (yaw, pitch, roll). This example just has a stub (0, 0, 0).
        :return: A tuple (X, Y, Z) in some global coordinate frame.

        In real usage:
          - Use camera intrinsics (focal length, principal point).
          - Possibly use depth data or triangulation from multiple frames.
          - If the device is doing SLAM, you might directly query the 3D position 
            of the bounding box from its tracking data.

        For demonstration, we will return a hardcoded or approximate position.
        """
        (x1, y1, x2, y2) = bbox

        # Let's say we just approximate that the object is 2 meters in front
        # of the camera (Z=2.0) and we offset X based on the bounding box center.
        box_center_x = (x1 + x2) / 2.0
        # For demonstration, let’s assume image width ~ 640, so we shift X from -1.0 to +1.0
        # if box_center_x is 320 => X=0.0, if box_center_x is 0 => X=-1.0, if box_center_x is 640 => X=+1.0
        # This is a *very* rough approximation.
        approximate_image_width = 640.0  # purely for the demonstration
        x_norm = (box_center_x - approximate_image_width / 2.0) / (approximate_image_width / 2.0)

        # We'll treat x_norm ~ -1..+1 as ~ -1..+1 meters in the real world (purely fictitious).
        approximate_x = x_norm * 1.0
        approximate_y = 0.0  # We won't offset vertical for now
        approximate_z = 2.0  # Assume everything is 2m away

        # If camera_pose had actual orientation/translation, 
        # you could transform (approximate_x, approximate_y, approximate_z)
        # into the building's coordinate frame. We'll just return as is.
        return (approximate_x, approximate_y, approximate_z)

    def recognize_object(self, detection_label):
        """
        Match the detection label (e.g. "chair", "table") with known info from
        furniture_db. That might include synonyms, additional metadata, etc.
        
        :param detection_label: The label from the detection step.
        :return: A dictionary containing recognized info, e.g.:
                 {
                   "name": "chair",
                   "type": "furniture",
                   "description": "...",
                   ...
                 }
        """
        label_lower = detection_label.lower()
        if label_lower in self.furniture_db:
            # Return the entire dictionary for this label
            return self.furniture_db[label_lower]
        else:
            # Fallback if not found
            return {
                "name": detection_label,
                "type": "unknown",
                "description": "No entry in furniture DB."
            }

    def associate_detection(self, detection, camera_pose):
        """
        Takes a detection dictionary and a camera pose, 
        maps it to a 3D position, and merges with furniture DB info.

        :param detection: dict with keys like "label", "bbox", "confidence".
        :param camera_pose: e.g. (0.0, 0.0, 0.0) or some orientation data.
        :return: A structured object info dictionary, e.g.:
                 {
                   "name": "chair",
                   "type": "furniture",
                   "position": (x, y, z),
                   "confidence": 0.94
                 }
        """
        # 1. Map 2D bounding box -> approximate 3D position
        position_3d = self.map_2D_to_3D(detection["bbox"], camera_pose)

        # 2. Get more info from furniture DB
        recognized_info = self.recognize_object(detection["label"])

        # 3. Construct final dictionary
        object_info = {
            "name": recognized_info.get("name", detection["label"]),
            "type": recognized_info.get("type", "furniture"),
            "description": recognized_info.get("description", ""),
            "position": position_3d,
            "confidence": detection["confidence"]
        }

        return object_info
