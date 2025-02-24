from moviepy.editor import VideoFileClip
import sys
import os
import argparse

def condense_to_minute(input_path, remove_sound=False):
    """
    Condenses a video to exactly one minute by adjusting its speed.
    
    Args:
        input_path (str): Path to the input video file
        remove_sound (bool): Whether to remove sound from the output video
    """
    try:
        # Load the video
        video = VideoFileClip(input_path)
        
        # Calculate the speed multiplier needed to make it exactly 1 minute
        original_duration = video.duration
        target_duration = 60  # 1 minute in seconds
        speed_multiplier = original_duration / target_duration
        
        # Create the output filename
        filename, ext = os.path.splitext(input_path)
        output_path = f"{filename}_1min{ext}"
        
        # Apply the speed change
        final_clip = video.speedx(speed_multiplier)
        
        # Remove audio if specified
        if remove_sound:
            final_clip = final_clip.without_audio()
        
        # Write the output file
        final_clip.write_videofile(output_path)
        
        # Close the clips to free up system resources
        final_clip.close()
        video.close()
        
        print(f"\nSuccess! Video has been condensed to 1 minute.")
        print(f"Original duration: {original_duration:.2f} seconds")
        print(f"Speed multiplier: {speed_multiplier:.2f}x")
        print(f"Audio: {'Removed' if remove_sound else 'Preserved'}")
        print(f"Output saved as: {output_path}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Condense a video to exactly one minute.')
    parser.add_argument('input_path', help='Path to the input video file')
    parser.add_argument('--no-sound', action='store_true', help='Remove sound from the output video')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_path):
        print(f"Error: The file '{args.input_path}' does not exist.")
        sys.exit(1)
        
    print("Processing video... This may take a while depending on the video size.")
    condense_to_minute(args.input_path, remove_sound=args.no_sound)

if __name__ == "__main__":
    main()
