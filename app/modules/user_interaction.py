# app/modules/user_interaction.py

class UserInteraction:
    """
    Manages user interaction for the HUMAN / AR-glasses mode.
    Responsibilities include:
      - Capturing frames from the AR device camera.
      - Running object detection on those frames.
      - Mapping detections to 3D positions via ObjectRecognition.
      - Handling voice commands (like "What am I looking at?" or "Navigate to the fridge").
      - Using SpatialAudioEngine to provide audio cues or other feedback.
    """

    def __init__(
            self,
            glasses_integration,
            audio_engine,
            object_detector,
            object_recognizer,
            nav,
            llm
        ):
        """
        :param glasses_integration: An instance of GlassesIntegration for camera, orientation, voice commands
        :param audio_engine: An instance of SpatialAudioEngine for playing directional or TTS-like cues
        :param object_detector: An instance of ObjectDetection to find objects in camera frames
        :param object_recognizer: An instance of ObjectRecognition to map detections to 3D
        :param nav: An instance of NavigationAssistance for guiding the user
        :param llm: An instance of LLMIntegration for answering environment-related queries
        """
        self.glasses = glasses_integration
        self.audio = audio_engine
        self.detector = object_detector
        self.recognizer = object_recognizer
        self.navigation = nav
        self.llm = llm

        # Keep track of currently detected objects in view
        self.detected_objects = []

    def process_input(self):
        """
        1. Retrieve a camera frame from glasses_integration (if available).
        2. Run object detection -> create or update self.detected_objects.
        3. For each recognized object, play a short or continuous spatial cue (optional).
        4. Poll for voice commands -> handle them appropriately (LLM queries, navigation).
        """
        # 1. Get camera frame
        frame = self.glasses.get_camera_frame()
        if frame is not None:
            # 2. Detect objects
            detections = self.detector.detect_objects(frame)

            # Convert 2D detections to 3D + retrieve furniture DB info
            new_objects = []
            head_orientation = self.glasses.get_head_orientation()  # e.g. (pitch, yaw, roll)

            for d in detections:
                # Associate detection with recognized object data + 3D position
                recognized_obj = self.recognizer.associate_detection(d, head_orientation)
                new_objects.append(recognized_obj)

                # Example: play a short beep or TTS once for each newly recognized object
                label = recognized_obj["name"]
                position = recognized_obj["position"]
                self.audio.play_spatial_cue(label, position)

            # Update internal list
            self.detected_objects = new_objects

        # 2. Check for voice commands
        command = self.glasses.capture_voice_command()
        if command:
            self.handle_voice_command(command)

    def handle_voice_command(self, command):
        """
        Interpret and execute the user's voice command, such as:
          - "What am I looking at?"
          - "Navigate to the fridge."
          - "Where is the table?"
        """
        print(f"[UserInteraction] Voice command received: {command}")
        cmd_lower = command.strip().lower()

        # Basic pattern matching:
        if "navigate" in cmd_lower:
            # E.g. "navigate to the fridge"
            # Extract the destination object name
            target = cmd_lower.replace("navigate to", "").strip()
            self.navigation.start_navigation(target)

        elif "what am i looking at" in cmd_lower or "what is around" in cmd_lower:
            # Ask LLM about recognized objects
            response = self.llm.query_environment(
                command,
                self.detected_objects,
                self.recognizer.building_model
            )
            # For demonstration, just print the LLM response to console
            print(f"[LLM] {response}")

            # Optionally, you can speak it via TTS if your audio engine supports that:
            # self.audio.play_text(response)

        elif "where is" in cmd_lower:
            # e.g. "where is the table?"
            # Could look up the object in self.detected_objects or building model
            # Then respond with direction or distance
            object_name = cmd_lower.replace("where is", "").strip()
            matched = [obj for obj in self.detected_objects if object_name in obj['name'].lower()]
            if matched:
                # For simplicity, pick the first matched object
                obj_info = matched[0]
                position = obj_info["position"]
                answer = f"The {obj_info['name']} is at approximate 3D position {position}."
                print(f"[UserInteraction] {answer}")
                # Optional TTS:
                # self.audio.play_text(answer)
            else:
                print("[UserInteraction] Not currently detected or unknown object.")
        else:
            # Unrecognized command
            print("[UserInteraction] Command not recognized or not supported.")
