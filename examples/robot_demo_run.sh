#!/usr/bin/env bash

# ------------------------------------------------------------------
# robot_demo_run.sh
#
# A simple shell script to launch the ROBOT mode of the 
# SmartAR-3D-Robot-Explorer application using a sample 3D model 
# and furniture DB.
#
# Usage:
#   ./robot_demo_run.sh
#
# Make this script executable:
#   chmod +x robot_demo_run.sh
# ------------------------------------------------------------------

# 1) Path to your Python interpreter or venv Python
PYTHON="python"

# 2) Main Python script 
MAIN_SCRIPT="app/main.py"

# 3) Sample 3D model (OBJ or IFC) and furniture DB (JSON)
MODEL_FILE="examples/example_3d_model.obj"
FURNITURE_DB="examples/test_furniture_db.json"

# 4) Desired run mode: robot
MODE="robot"

echo "Running in ROBOT mode with model: $MODEL_FILE"
echo "Using furniture DB: $FURNITURE_DB"

# Execute the command:
$PYTHON $MAIN_SCRIPT \
  --model "$MODEL_FILE" \
  --furniture_db "$FURNITURE_DB" \
  --mode "$MODE"
