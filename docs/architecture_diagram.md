# System Architecture Diagram

Below is a Mermaid diagram representing the high-level flow of data and control
across the **SmartAR-3D-Robot-Explorer** framework. It shows how the system
initializes, loads the 3D building model, sets up machine learning models, and
then branches into **human** or **robot** mode.

```mermaid
flowchart TB
    subgraph Setup [Initial Setup]
        A[Ingestion<br>ingestion.py] --> B[ML Model Manager<br>ml_model_manager.py]
    end

    B --> C[main.py]

    C --> D{Run Mode<br>human or robot?}

    D -->|human| E[GlassesIntegration<br>glasses_integration.py]
    D -->|robot| F[RobotIntegration<br>robot_integration.py]

    %% HUMAN Mode Sub-flow
    E --> G[UserInteraction<br>user_interaction.py]
    G --> H[ObjectDetection<br>object_detection.py]
    H --> I[ObjectRecognition<br>object_recognition.py]
    I --> J[LLMIntegration<br>llm_integration.py]
    G --> K[SpatialAudioEngine<br>spatial_audio.py]
    G --> L[NavigationAssistance<br>navigation.py]

    %% ROBOT Mode Sub-flow
    F --> M[ObjectDetection<br>object_detection.py]
    M --> N[ObjectRecognition<br>object_recognition.py]
    N --> O[RobotNavigation<br>robot_navigation.py]
    N --> P[LLMIntegration<br>llm_integration.py]

    %% Example references to building_model
    A --> Q[Building Model Data]
    Q -.-> L
    Q -.-> O

```
