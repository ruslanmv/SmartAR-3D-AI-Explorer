# SmartAR-3D-AI-Explorer

A **Python-based** framework for **3D environment exploration**, combining:

1. **AR Glasses** support for humans (spatial audio, head-tracking, real-time object detection).  
2. **Autonomous Robot** integration (camera-based or LiDAR-based mapping, object detection, path planning).  
3. **Large Language Model (LLM) Integration** for querying the environment, recognized objects, and building layout.

This framework allows both **people** and **robots** to share a common perception of the environment, enabling collaboration and richer interactions.

---

## Table of Contents

1. [Overview](#overview)  
2. [Key Features](#key-features)  
3. [Installation](#installation)  
4. [Project Structure](#project-structure)  
5. [Usage Scenarios](#usage-scenarios)  
   - [Human AR Glasses Mode](#human-ar-glasses-mode)  
   - [Robot Mode](#robot-mode)  
6. [Architecture and Modules](#architecture-and-modules)  
7. [Extending the Framework](#extending-the-framework)  
8. [Acknowledgments and References](#acknowledgments-and-references)  
9. [License](#license)  

---

## Overview

**SmartAR-3D-AI-Explorer** is designed to help **two main entities** explore and understand a building or environment:

1. **People**:  
   - Wear AR smart glasses (like Meta Quest 3 or other AR-capable devices).  
   - Get real-time object detection (e.g., chairs, tables, appliances).  
   - Experience **spatialized audio** or visual overlays that indicate where objects are.  
   - Ask questions such as *“Which furniture is in front of me?”* or *“How do I get to the refrigerator?”*  
   - Receive answers or directions from an integrated **Large Language Model (LLM)**.

2. **Robots**:  
   - Use onboard cameras or LiDAR to detect objects.  
   - Rely on the same 3D building model for navigation.  
   - Drive autonomously to target locations (e.g., “Move to the living room”).  
   - Answer queries about the environment or the objects the robot has detected.  

By sharing the **same** data structures for 3D building information and recognized objects, humans and robots can coordinate and exchange high-level understanding of the world.

---

## Key Features

- **3D Model Ingestion**  
  Parse architectural models (OBJ, IFC, glTF) for building structures (walls, doors, etc.).

- **Object Detection**  
  A simplified YOLO-like approach to identify objects in real time from camera frames.  
  - Humans: AR glasses camera.  
  - Robots: Onboard camera or sensor feed.

- **Spatial Audio / Visual Overlays**  
  For human users, plays directional audio or shows AR labels to convey where an object is located.

- **Robot Navigation**  
  Robot can autonomously move using path planning modules (e.g., A* or custom solutions).  
  - Motor commands for linear/angular velocity.  
  - Pose updates from odometry or SLAM.

- **LLM Integration**  
  Voice or text-based Q&A about the environment. The LLM has context from recognized objects, building layout, or user queries.

- **Two Modes**  
  1. **`human`**: Focuses on AR glasses integration, voice commands.  
  2. **`robot`**: Focuses on robot hardware (motors, camera, LiDAR, etc.).

---

## Installation

**Prerequisites**:

- Python 3.8+  
- (Optional) A working AR device or standard webcam for testing.  
- (Optional) A mobile robot setup or simulation environment (e.g., ROS or other frameworks).  

### 1. Clone the Repository

```bash
git clone https://github.com/ruslanmv/SmartAR-3D-AI-Explorer.git
cd SmartAR-3D-AI-Explorer
```

### 2. (Recommended) Create a Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate        # Linux/Mac
# or: venv\Scripts\activate.bat # on Windows
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

*(Note: `requirements.txt` should contain libraries like `opencv-python`, `torch` or `onnxruntime` (if using YOLO), `pywavefront`, `SpeechRecognition`, plus any robot/AR-specific dependencies.)*

---

## Project Structure

Below is the **full directory tree** to highlight each component:

```
SmartAR-3D-Robot-Explorer/
├── .gitignore                # Git ignore patterns (venv, pycache, etc.)
├── README.md                 # This file: project documentation
├── requirements.txt          # Python dependencies
├── LICENSE                   # Open-source license (e.g., MIT)
├── docs/
│   ├── architecture_diagram.md
│   ├── detection_pipeline.md
│   └── robot_integration_diagram.md
├── examples/
│   ├── example_3d_model.obj           # Sample 3D model for testing
│   ├── test_furniture_db.json         # Example object/furniture DB
│   ├── demo_run.sh                    # Simple script to run in human mode
│   └── robot_demo_run.sh              # Simple script to run in robot mode
├── app/
│   ├── main.py                        # Main entry point
│   └── modules/
│       ├── __init__.py
│       ├── ingestion.py               # 3D model loader (OBJ, IFC, etc.)
│       ├── spatial_audio.py           # Binaural audio & HRTF rendering
│       ├── user_interaction.py        # Voice commands, user I/O for AR
│       ├── object_detection.py        # YOLO-like detection
│       ├── object_recognition.py      # Maps detections to known objects + 3D coords
│       ├── ml_model_manager.py        # Manages ML models (YOLO, LLM, etc.)
│       ├── llm_integration.py         # Q&A with LLM given environment data
│       ├── navigation.py              # Basic navigation for human guidance
│       ├── glasses_integration.py     # Connect with AR glasses (camera, orientation)
│       ├── robot_integration.py       # Connect with robot hardware (motors, sensors)
│       └── robot_navigation.py        # Robot-specific path planning, movement
└── tests/
    ├── test_ingestion.py
    ├── test_detection.py
    ├── test_robot_integration.py
    ├── test_navigation.py
    └── ...
```

### High-Level Explanation

1. **`app/main.py`**  
   - The primary script. Parses arguments (`--mode human` or `--mode robot`), loads the environment, sets up modules, and enters the main loop.

2. **`modules/ingestion.py`**  
   - Loads/Parses building models. Could use `pywavefront` (OBJ), `ifcopenshell` (IFC), or others.

3. **`modules/spatial_audio.py`**  
   - Implements 3D audio rendering (HRTFs/binaural cues). Primarily relevant for visually impaired or AR usage.

4. **`modules/user_interaction.py`**  
   - Gathers user input (voice commands, gestures) in **human** mode. Plays audio or overlays for feedback.

5. **`modules/object_detection.py`**  
   - A minimal YOLO-like approach to detect bounding boxes in camera frames.

6. **`modules/object_recognition.py`**  
   - Converts bounding boxes → 3D positions. Associates them with known furniture from a DB (`test_furniture_db.json`).

7. **`modules/ml_model_manager.py`**  
   - Loads the detection model and the LLM. Could be local or remote (e.g., OpenAI, Hugging Face).

8. **`modules/llm_integration.py`**  
   - Handles environment queries. If user asks “What am I looking at?” it forms a prompt with the recognized objects and calls the LLM.

9. **`modules/navigation.py`**  
   - Basic pathfinding or instructions for human users. E.g., “turn left, walk straight” or beep cues.

10. **`modules/glasses_integration.py`**  
    - Connects to AR glasses (camera feed, sensor data, orientation). For simpler tests, this might just read from a webcam.

11. **`modules/robot_integration.py`**  
    - Low-level robot hardware. Could integrate with ROS, or send motor commands directly over serial.

12. **`modules/robot_navigation.py`**  
    - Robot path planning. Could implement or wrap more advanced algorithms for obstacle avoidance, SLAM, etc.

---

## Usage Scenarios

### 1. Human AR Glasses Mode

1. **Launch**  
   ```bash
   python app/main.py --model examples/example_3d_model.obj \
                      --furniture_db examples/test_furniture_db.json \
                      --mode human
   ```

2. **System Flow**  
   - Loads the 3D model of a building (from `example_3d_model.obj`).  
   - Initializes **spatial audio** and user input modules.  
   - Camera frames from AR glasses → `object_detection.py` → recognized objects.  
   - For each recognized object, **spatial audio** or an AR overlay is rendered.  
   - The user can speak commands like: “What am I looking at?” or “Navigate to the chair.”  
     - The system consults the LLM with environment data and returns an answer or starts path guidance.

3. **For Visually Impaired Users**  
   - The system plays short beep or musical icons for each recognized object. 
   - Real-time **binaural** updates if the user moves their head (head tracking).

4. **Exit**  
   - Press `Ctrl + C` in the terminal to stop.

---

### 2. Robot Mode

1. **Launch**  
   ```bash
   python app/main.py --model examples/example_3d_model.obj \
                      --furniture_db examples/test_furniture_db.json \
                      --mode robot
   ```
2. **System Flow**  
   - Loads the same 3D model.  
   - Initializes robot drivers (`robot_integration.py`) to connect with motors and sensors.  
   - Receives camera or LiDAR frames, passes them to `object_detection.py`.  
   - Detected objects are mapped into the robot’s coordinate frame.  
   - The robot can either:
     - **Autonomously navigate** to a set goal.  
     - **Answer queries** from an operator or an LLM (e.g., “Do you see a table?”).

3. **Extend with SLAM**  
   - For unknown or partially known environments, integrate a SLAM library.  
   - This ensures the robot knows its position in real time and can plan around obstacles not in the original 3D model.

4. **Exit**  
   - Press `Ctrl + C` in the terminal.

---

## Architecture and Modules

Below is a simplified summary of how everything interacts:

1. **3D Model + Furniture DB**  
   - `ingestion.py` loads geometry.  
   - `object_recognition.py` references a furniture database (a JSON with known items, e.g. “chair,” “table,” etc.).

2. **Camera / Sensor Input**  
   - **Human**: from AR glasses or a standard webcam.  
   - **Robot**: from the robot’s onboard camera or LiDAR.

3. **Object Detection (YOLO)**  
   - Takes each frame, returns bounding boxes.  
   - Could run on CPU or GPU, depending on your hardware.

4. **Object Recognition + 3D Mapping**  
   - Projects bounding boxes into a 3D coordinate system.  
   - Matches recognized labels with known objects in `test_furniture_db.json`.

5. **Navigation**  
   - **Human**: “navigation.py” provides instructions or sound cues.  
   - **Robot**: “robot_navigation.py” sends motor commands, updates odometry/pose.

6. **LLM Integration**  
   - Queries about environment → data fused → LLM responds with a textual answer.  
   - For humans, the answer can be read aloud (TTS) or displayed in the AR interface.  
   - For robots, the answer might be used internally or displayed in a console.

---

## Extending the Framework

1. **Add Real YOLO**  
   - Replace the stub in `object_detection.py` with a PyTorch YOLO or ONNX-based solution.  
   - Optimize for real-time performance if needed.

2. **Personalize Spatial Audio**  
   - Use personalized HRTFs or add more advanced reverberation/echo modeling.

3. **Robot SLAM**  
   - Integrate with ROS (Robot Operating System) for advanced mapping and localization.  
   - Subscribe to `/odom` for pose, publish to `/cmd_vel` for movement.

4. **Advanced LLM Prompts**  
   - Provide more contextual data: building layout, distances, object shapes, etc.  
   - Use prompting techniques so the LLM can give more dynamic or instructive answers (e.g., “Please generate a route to the chair”).

5. **Real AR Overlays**  
   - For devices like the Meta Quest 3 or Microsoft HoloLens, use their respective SDKs to display bounding boxes or object labels in the user’s field of view.

---

## Acknowledgments and References

1. **Spatial Audio Research**  
   - Begault, D.R. *3D sound for virtual reality and multimedia* (1994).  
   - Wightman, F.L., Kistler, D.J. “Headphone simulation of free-field listening. I. Stimulus synthesis.” *J. Acoust. Soc. Am.* (1989).

2. **Object Detection**  
   - Redmon, J. et al. *YOLO: You Only Look Once*.  
   - Huang, J. et al. *Speed/accuracy trade-offs for modern convolutional object detectors*.

3. **Robot Navigation**  
   - Thrun, S. *Probabilistic robotics*. MIT Press, 2005.  
   - Quigley, M. et al. *ROS: an open-source Robot Operating System*.

4. **LLM Integration**  
   - Wolf, T., et al. *Transformers: State-of-the-art natural language processing*.  
   - Brown, T., et al. *Language Models are Few-Shot Learners* (GPT-3).

---

## License

This project is distributed under the terms of the **MIT License** (see the [LICENSE](LICENSE) file). 

**Disclaimer**: This is a **prototype reference** framework. It’s intended for experimentation and research. Real-world deployment, especially for visually impaired navigation or autonomous robots, **requires extensive testing** and safety measures.

