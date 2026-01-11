#!/bin/bash
# Add project to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
echo "Environment configured. PYTHONPATH includes: $(pwd)"
