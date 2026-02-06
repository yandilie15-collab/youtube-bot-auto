from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import os
import random
import config_chatgpt as config

def create_text_image(text, size=(1920, 1080), bg_color=(30, 30, 30), text_color=(255, 255, 255)):
    """Create an image with text overlay"""
    img = Image.new('RGB', size, color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a system font, fallback to default
    try:
        font = ImageFont.truetype("arial.ttf", 80)
    except:
        font = ImageFont.load_default()
    
    # Calculate text position (centered)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)
    draw.text(position, text, fill=text_color, font=font)
    
    return img

def generate_video(script, output_path="output.mp4"):
    """Generate video from script"""
    print(f"Generating video: {output_path}")
    
    # Parse script into segments
    lines = [l.strip() for l in script.split('\n') if l.strip()]
    
    # Create clips
    clips = []
    duration_per_clip = config.VIDEO_DURATION / max(len(lines), 4)
    
    # Background colors for variety
    bg_colors = [
        (30, 30, 30),    # Dark gray
        (20, 40, 60),    # Dark blue
        (40, 20, 50),    # Dark purple
        (20, 50, 30),    # Dark green
    ]
    
    for i, line in enumerate(lines[:4]):  # Limit to 4 segments
        # Skip empty or very short lines
        if len(line) < 10:
            continue
        
        # Truncate long lines
        if len(line) > 100:
            line = line[:97] + "..."
        
        # Create text image
        bg_color = bg_colors[i % len(bg_colors)]
        img = create_text_image(line, bg_color=bg_color)
        
        # Save temp image
        temp_img_path = f"temp_frame_{i}.png"
        img.save(temp_img_path)
        
        # Create clip
        clip = ImageClip(temp_img_path).set_duration(duration_per_clip)
        clips.append(clip)
        
        # Clean up temp image
        try:
            os.remove(temp_img_path)
        except:
            pass
    
    # If no clips created, create a default one
    if not clips:
        img = create_text_image("Video Content", bg_color=(30, 30, 30))
        temp_img_path = "temp_frame_default.png"
        img.save(temp_img_path)
        clips.append(ImageClip(temp_img_path).set_duration(config.VIDEO_DURATION))
        try:
            os.remove(temp_img_path)
        except:
            pass
    
    # Concatenate clips
    final_clip = concatenate_videoclips(clips, method="compose")
    
    # Ensure proper duration
    if final_clip.duration < config.VIDEO_DURATION:
        final_clip = final_clip.loop(duration=config.VIDEO_DURATION)
    elif final_clip.duration > config.VIDEO_DURATION:
        final_clip = final_clip.subclip(0, config.VIDEO_DURATION)
    
    # Write video file
    final_clip.write_videofile(
        output_path,
        fps=config.VIDEO_FPS,
        codec='libx264',
        audio=False,
        preset='ultrafast',
        threads=4
    )
    
    # Clean up
    final_clip.close()
    
    print(f"✅ Video created: {output_path}")
    return output_path
