#!/usr/bin/env bash

# --------------------------------------------------------------
# demo_run.sh
#
# A simple shell script to launch the HUMAN (AR) mode of the
# SmartAR-3D-Robot-Explorer application using a sample 3D model
# and furniture DB. 
# 
# Usage:
#   ./demo_run.sh
# 
# Make sure this script has execute permissions:
#   chmod +x demo_run.sh
# --------------------------------------------------------------

# 1) Path to the Python interpreter. 
#    If you're using a virtual environment, adjust accordingly:
PYTHON="python"

# 2) The main Python script:
MAIN_SCRIPT="app/main.py"

# 3) Sample 3D model (OBJ) and furniture DB (JSON):
MODEL_FILE="examples/example_3d_model.obj"
FURNITURE_DB="examples/test_furniture_db.json"

# 4) Desired run mode: human
MODE="human"

echo "Running in HUMAN mode with model: $MODEL_FILE"
echo "Using furniture DB: $FURNITURE_DB"

# Execute the command:
$PYTHON $MAIN_SCRIPT \
  --model "$MODEL_FILE" \
  --furniture_db "$FURNITURE_DB" \
  --mode "$MODE"

