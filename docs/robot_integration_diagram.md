# Robot Integration Diagram

Below is a Mermaid diagram showing the flow of data and control between
the **robot hardware**, **RobotIntegration**, and other modules in 
**SmartAR-3D-Robot-Explorer**.

```mermaid
flowchart TB

    subgraph Robot Hardware & Sensors
        A(Physical Robot<br>Motors, Sensors,<br>Camera, etc.)
    end

    subgraph Framework
        B(RobotIntegration<br>(robot_integration.py))
        C(ObjectDetection<br>(object_detection.py))
        D(ObjectRecognition<br>(object_recognition.py))
        E(RobotNavigation<br>(robot_navigation.py))
        F(LLMIntegration<br>(llm_integration.py))
        G(Building Model<br>(ingestion.py))
    end

    A -->|sensor data| B
    B -->|camera frames| C
    C -->|detections| D
    D -->|3D objects| E
    E -->|motor commands| B
    B -->|queries| F

    D -->|reference geometry| G
    E -->|reference layout| G
```