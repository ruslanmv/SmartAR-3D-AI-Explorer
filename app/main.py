# app/main.py

import argparse
from modules.ingestion import ModelIngestion
from modules.spatial_audio import SpatialAudioEngine
from modules.user_interaction import UserInteraction
from modules.object_detection import ObjectDetection
from modules.object_recognition import ObjectRecognition
from modules.ml_model_manager import MLModelManager
from modules.llm_integration import LLMIntegration
from modules.navigation import NavigationAssistance
from modules.glasses_integration import GlassesIntegration
from modules.robot_integration import RobotIntegration
from modules.robot_navigation import RobotNavigation


def main():
    """
    Main entry point for the SmartAR-3D-Robot-Explorer framework.
    
    Usage Examples:
      python app/main.py --model examples/example_3d_model.obj --furniture_db examples/test_furniture_db.json --mode human
      python app/main.py --model examples/example_3d_model.obj --furniture_db examples/test_furniture_db.json --mode robot

    The '--mode' argument determines whether we run the system in:
      - 'human' mode (AR glasses, spatial audio, voice commands).
      - 'robot' mode (autonomous robot integration, camera feed, path planning).
    """

    # 1. Parse command-line arguments
    parser = argparse.ArgumentParser(description="SmartAR-3D-Robot-Explorer")
    parser.add_argument("--model", type=str, required=True,
                        help="Path to the 3D building model file (e.g., OBJ, IFC).")
    parser.add_argument("--furniture_db", type=str, required=True,
                        help="Path to the furniture/object database (JSON).")
    parser.add_argument("--mode", type=str, choices=["human", "robot"], default="human",
                        help="Run mode: 'human' for AR usage, 'robot' for autonomous robot.")
    args = parser.parse_args()

    # 2. Ingest the 3D model
    ingestion_module = ModelIngestion()
    building_model = ingestion_module.load_model(args.model)

    # 3. Initialize spatial audio engine (useful for human mode; safe to init anyway)
    audio_engine = SpatialAudioEngine()
    audio_engine.initialize()

    # 4. Load machine learning models (object detection + LLM)
    ml_manager = MLModelManager()
    detection_model = ml_manager.load_detection_model()  # e.g., YOLO
    llm_model = ml_manager.load_llm()                    # e.g., GPT-based or local model

    # 5. Prepare object detection & recognition
    detector = ObjectDetection(detection_model)
    object_recognizer = ObjectRecognition(building_model, args.furniture_db)

    # 6. Prepare LLM integration
    llm_integration = LLMIntegration(llm_model)

    # 7. Shared navigation references (building structure, etc.)
    nav_assistance = NavigationAssistance(building_model)

    # 8. Branch logic: Human vs. Robot mode
    if args.mode == "human":
        # Setup AR glasses hardware integration
        glasses = GlassesIntegration()
        glasses.connect_hardware()

        # Create user interaction module (for voice commands, etc.)
        user_interact = UserInteraction(
            glasses_integration=glasses,
            audio_engine=audio_engine,
            object_detector=detector,
            object_recognizer=object_recognizer,
            nav=nav_assistance,
            llm=llm_integration
        )

        print("[Main] Running in HUMAN (AR) mode. Press Ctrl+C to exit.")
        try:
            while True:
                # Continually poll for camera frames, voice commands, etc.
                user_interact.process_input()

                # Update spatial audio environment
                audio_engine.update()
        except KeyboardInterrupt:
            print("\n[Main] Exiting HUMAN mode cleanly.")

    else:
        # Setup robot hardware integration
        robot_integration = RobotIntegration()
        robot_integration.connect_robot_hardware()

        # Create specialized robot navigation
        robot_nav = RobotNavigation(building_model, robot_integration)

        print("[Main] Running in ROBOT mode. Press Ctrl+C to exit.")
        try:
            while True:
                # 1. Retrieve camera frame from the robot (or LiDAR data)
                frame = robot_integration.get_robot_camera_frame()
                if frame is not None:
                    # 2. Detect objects
                    detections = detector.detect_objects(frame)

                    # 3. Associate detections with 3D environment
                    recognized_objects = []
                    for d in detections:
                        recognized_obj = object_recognizer.associate_detection(
                            d, camera_pose=robot_integration.get_robot_pose()
                        )
                        recognized_objects.append(recognized_obj)
                        # In a more advanced version, you might log or display these

                # 4. Update robot navigation logic (autonomous movement, obstacle avoidance, etc.)
                robot_nav.update_navigation()

        except KeyboardInterrupt:
            print("\n[Main] Exiting ROBOT mode cleanly.")


if __name__ == "__main__":
    main()
