#!/bin/bash
set -euo pipefail

# Start the backend server in the background
uvicorn backend.main:app --host 0.0.0.0 --port 8000 &

# Start the frontend development server
cd frontend
npm run dev

# Wait for background processes to finish
wait