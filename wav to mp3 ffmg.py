import os
import subprocess

# Input and output folder
input_folder = "input_audio"
output_folder = "output_audio"
replacing = False 

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# FFmpeg conversion settings
def convert_to_mp3(input_file, output_file):
    command = [
        "ffmpeg",
        "-i", input_file,
        "-ac", "2",
        "-codec:a", "libmp3lame",
        "-b:a", "48k",
        "-ar", "16000",
        "-write_xing", "0",
        output_file
    ]
    subprocess.run(command, check=True)

# Process all audio files in the input folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith((".wav", ".mp3", ".flac", ".m4a", ".aac", ".ogg")):
        input_path = os.path.join(input_folder, filename)
        output_filename = os.path.splitext(filename.lower())[0] + ".mp3"
        output_path = os.path.join(output_folder, output_filename)

        if os.path.exists(output_path):
          os.remove(output_path)
          replacing = True

        if replacing:
          print(f"Replacing-Converting: {filename} → {output_filename}")
        else:
          print(f"Converting: {filename} → {output_filename}")
        try:
            convert_to_mp3(input_path, output_path)
        except subprocess.CalledProcessError as e:
            print(f"Error converting {filename}: {e}")

print("✅ Bulk conversion complete.")