import subprocess
import time
import os
import sys
from moviepy.editor import VideoFileClip

def condense_with_moviepy(input_path, remove_sound=False):
    """Original moviepy method"""
    start_time = time.time()
    
    video = VideoFileClip(input_path)
    speed_multiplier = video.duration / 60
    final_clip = video.speedx(speed_multiplier)
    
    if remove_sound:
        final_clip = final_clip.without_audio()
    
    output_path = f"{os.path.splitext(input_path)[0]}_1min_moviepy{os.path.splitext(input_path)[1]}"
    final_clip.write_videofile(output_path)
    
    final_clip.close()
    video.close()
    
    return time.time() - start_time

def condense_with_ffmpeg_ultrafast(input_path, remove_sound=False):
    """Ultra-fast ffmpeg method prioritizing speed over quality"""
    start_time = time.time()
    
    # Get video duration using ffprobe
    duration_cmd = [
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', input_path
    ]
    duration = float(subprocess.check_output(duration_cmd).decode().strip())
    
    speed_multiplier = duration / 60
    output_path = f"{os.path.splitext(input_path)[0]}_1min_ffmpeg_fast{os.path.splitext(input_path)[1]}"
    
    # More stable hardware-accelerated encoding settings
    ffmpeg_cmd = [
        'ffmpeg',
        '-hwaccel', 'videotoolbox',
        '-i', input_path,
        # Scale down video for faster processing while maintaining aspect ratio
        '-filter_complex', 
        f'[0:v]scale=-2:720,setpts={1/speed_multiplier}*PTS[v]',
        '-c:v', 'h264_videotoolbox',
        '-b:v', '4M',            # Increased bitrate for better quality
        '-maxrate', '5M',
        '-bufsize', '5M',
        '-profile:v', 'main',    # More compatible profile
        '-threads', '0',
        '-movflags', '+faststart'
    ]
    
    if remove_sound:
        ffmpeg_cmd.extend(['-an'])
    else:
        # Simplified audio processing
        ffmpeg_cmd.extend([
            '-filter_complex', f'[0:a]atempo={min(2.0, speed_multiplier)}[a]',
            '-map', '[a]',
            '-c:a', 'aac',
            '-b:a', '128k'
        ])
    
    ffmpeg_cmd.extend([
        '-map', '[v]',
        '-y',
        output_path
    ])
    
    # Run ffmpeg and capture output
    process = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Print FFmpeg output for debugging
    print("\nFFmpeg output:")
    print(process.stderr.decode())
    
    return time.time() - start_time

def compare_methods(input_path, remove_sound=False):
    """Compare methods and print results"""
    print(f"\nTesting with video: {input_path}")
    print("Remove sound:", remove_sound)
    
    print("\nProcessing with FFmpeg (Ultra-fast)...")
    ffmpeg_ultrafast_time = condense_with_ffmpeg_ultrafast(input_path, remove_sound)
    print(f"\nFFmpeg Ultra-fast processing time: {ffmpeg_ultrafast_time:.2f} seconds")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Compare video condensing methods')
    parser.add_argument('input_path', help='Path to the input video file')
    parser.add_argument('--no-sound', action='store_true', help='Remove sound from the output video')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_path):
        print(f"Error: The file '{args.input_path}' does not exist.")
        sys.exit(1)
    
    compare_methods(args.input_path, args.no_sound) 
