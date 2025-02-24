# Minute Condenser

A Python application that condenses any video to exactly one minute by adjusting its playback speed.

## Installation

1. Make sure you have Python 3.6 or higher installed
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```
3. For the faster FFmpeg method, ensure FFmpeg is installed on your system:
   - macOS: `brew install ffmpeg`
   - Ubuntu/Debian: `sudo apt-get install ffmpeg`
   - Windows: Download from [FFmpeg website](https://ffmpeg.org/download.html)

## Usage

### Standard Method (MoviePy)
Run the script from the command line by providing the path to your video file:

```bash
python minute_condenser.py path/to/your/video.mp4
```

To remove sound from the output video, add the `--no-sound` flag:

```bash
python minute_condenser.py path/to/your/video.mp4 --no-sound
```

### Faster Method (FFmpeg)
For faster processing, use the test script which implements both methods:

```bash
python speed_test.py path/to/your/video.mp4
```

The script will:
1. Calculate the necessary speed adjustment to make the video exactly 1 minute long
2. Process the video using both methods for comparison
3. Remove audio if the `--no-sound` flag is used
4. Display information about the processing time for each method

## Features

- Automatically calculates the required speed multiplier
- Preserves the original video file
- Creates a new condensed video file
- Optional audio removal with `--no-sound` flag
- Handles various video formats supported by moviepy/FFmpeg
- Provides clear feedback about the processing
- Two implementation methods:
  - MoviePy: More Python-friendly, easier to modify
  - FFmpeg: Significantly faster processing

## Notes

- Processing time depends on the size and length of the input video
- The output video will maintain the original aspect ratio and resolution
- For very long videos, the speed increase might make the content hard to follow
- For very short videos, the speed decrease might make the content appear too slow
- The FFmpeg method is generally 2-5x faster than the MoviePy method 