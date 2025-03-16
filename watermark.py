import os
import subprocess
import argparse
from pathlib import Path
import sys

## Text watermark settings
WATERMARK_OPACITY = '0.8'
TEXT_TOP_MARGIN = 0.02
TEXT_COLOUR = f'rgba(255,255,0,{WATERMARK_OPACITY})'


## Image watermark settings

IMAGE_SCALE = 0.2

def get_logo_path(args):
    logo_path = os.path.join(args.logo, 'logo.png')
    if not os.path.isfile(logo_path):
        raise FileNotFoundError(f"Logo file not found: {logo_path}")
    return logo_path

def print_settings(args):
    source_path = Path(args.input)
    dest_path = Path(args.output)
    print("Settings:")
    print(f"Source directory: {source_path}")
    print(f"Destination directory: {dest_path}")
    print(f"Text watermark colour: {TEXT_COLOUR}")
    print(f"Text watermark top margin: {TEXT_TOP_MARGIN}")
    print(f"Image watermark path: {LOGO_PATH}")
    print(f"Image watermark scale: {IMAGE_SCALE}")
    print(f"Resize option: {args.resize}")

def add_watermark(source_path, dest_path, watermark_text, resize_option):
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    # Get image dimensions to adjust point size and logo size dynamically
    identify_cmd = ['magick', 'identify', '-format', '%w %h', str(source_path)]
    result = subprocess.run(identify_cmd, capture_output=True, text=True, check=True)
    width, height = map(int, result.stdout.strip().split())
    point_size = int(min(width, height) * 0.05)  # Set point size to 5% of the smallest dimension
    logo_width = int(width * IMAGE_SCALE)
    logo_height = int(height * IMAGE_SCALE)

    command = [
        'magick', str(source_path),
        '-gravity', 'north',
        '-pointsize', str(point_size),
        '-fill', TEXT_COLOUR,
        '-annotate', f'+0+{int(height * TEXT_TOP_MARGIN)}', watermark_text,
        '(', str(LOGO_PATH),
        '-resize', f'{logo_width}x{logo_height}',
        '-alpha', 'set', '-fuzz', '10%', '-transparent', 'white', ')',
        '-gravity', 'southeast', '-geometry', '+10+10', '-composite',
        str(dest_path)
    ]
    subprocess.run(command, check=True)

    if resize_option == "facebook":
        resize_cmd = [
            'magick', str(dest_path),
            '-resize', '2047x2047>',
            str(dest_path)
        ]
        subprocess.run(resize_cmd, check=True)

def process_images(source_dir, dest_dir, resize_option):
    total_files = 0
    processed_files = 0

    for root, _, files in os.walk(source_dir):
        for file in files:
            total_files += 1
            source_file = Path(root) / file
            relative_path = source_file.relative_to(source_dir)
            dest_file = dest_dir / relative_path
            watermark_text = str(relative_path)

            try:
                add_watermark(source_file, dest_file, watermark_text, resize_option)
                processed_files += 1
                print(f"\033[92mProcessed:\033[0m \033[1;37m{relative_path}\033[0m")
            except subprocess.CalledProcessError as e:
                print(f"\033[91mFailed to process\033[0m \033[1;37m{relative_path}\033[0m: {e}")

    sys.stdout.flush()
    print(f"\nSummary: {processed_files}/{total_files} files processed successfully.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Watermark images with their relative paths.')
    parser.add_argument('--input', required=True, help='Input directory containing source images.')
    parser.add_argument('--logo', required=True, help='Input directory containing watermark logos.')
    parser.add_argument('--output', required=True, help='Output directory to save watermarked images.')
    parser.add_argument('--resize', choices=['none', 'facebook'], default='none', help='Resize option for the output images.')
    args = parser.parse_args()
    LOGO_PATH = get_logo_path(args)

    print_settings(args)

    process_images(Path(args.input), Path(args.output), args.resize)
