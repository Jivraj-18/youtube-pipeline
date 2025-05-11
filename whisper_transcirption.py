# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "faster-whisper"
# ]
# ///

from faster_whisper import WhisperModel

# Load the medium model
model = WhisperModel("medium", device="cuda" , compute_type="float16")

# Transcribe the video file
segments, info = model.transcribe("fork_demo.mp4", language="en")
print(segments)
# Print segments
for segment in segments:
    print(f"[{segment.start:.2f}s --> {segment.end:.2f}s] {segment.text}")

