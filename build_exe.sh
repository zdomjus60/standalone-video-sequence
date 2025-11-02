#!/bin/bash
# Exit immediately if a command exits with a non-zero status.
set -e

echo "Cleaning up old builds..."
rm -rf dist build standalone_video_with_audio.spec

# Base command
PYINSTALLER_CMD="pyinstaller --onefile --windowed standalone_video_with_audio.py"

# Add data files
PYINSTALLER_CMD="$PYINSTALLER_CMD --add-data \"videolist.txt:.\""

# Add all .mp4, .mp3 files found in the directory
for f in *.mp4; do
  if [ -f "$f" ]; then
    PYINSTALLER_CMD="$PYINSTALLER_CMD --add-data \"$f:.\""
  fi
done
for f in *.mp3; do
  if [ -f "$f" ]; then
    PYINSTALLER_CMD="$PYINSTALLER_CMD --add-data \"$f:.\""
  fi
done

echo "------------------------------------------------"
echo "Building with the following command:"
echo "$PYINSTALLER_CMD"
echo "------------------------------------------------"

# Execute the command and capture the real error
if eval $PYINSTALLER_CMD; then
    echo "PyInstaller completed successfully."
else
    echo "--- PYINSTALLER FAILED ---"
    exit 1
fi

echo "------------------------------------------------"
echo "Making the executable statically linked with staticx..."
echo "------------------------------------------------"
staticx dist/standalone_video_with_audio dist/standalone_video_with_audio_static
echo "Static build complete! The true standalone executable is dist/standalone_video_with_audio_static"
