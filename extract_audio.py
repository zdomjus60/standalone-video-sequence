import os
import subprocess

print("Starting audio extraction...")
# Automatically extract audio from all .mp4 files
for file in os.listdir('.'):
    if file.endswith('.mp4'):
        wav_file = file.replace('.mp4', '.mp3')
        if not os.path.exists(wav_file):
            print(f"Attempting to extract audio from {file} to MP3...")
            
            # Run ffmpeg and capture output, using libmp3lame for compression
            result = subprocess.run([
                'ffmpeg', '-i', file, '-vn', '-acodec', 'libmp3lame', '-q:a', '2', wav_file, '-y'
            ], capture_output=True, text=True)

            # Check if ffmpeg succeeded
            if result.returncode == 0:
                print(f"Successfully extracted audio to {wav_file}")
            else:
                # If ffmpeg failed, it's likely because there's no audio stream.
                # Print a warning and delete the empty/corrupt .wav file ffmpeg might have created.
                print(f"Warning: Could not extract audio from {file}. It may not have an audio track.")
                if os.path.exists(wav_file):
                    os.remove(wav_file)
        else:
            print(f"Audio already exists: {wav_file}")

print("Audio extraction complete!")