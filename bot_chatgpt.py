#!/usr/bin/env python3
import schedule
import time
import random
import os
from datetime import datetime
import config_chatgpt as config
import database_chatgpt as db
import script_generator
import video_generator_chatgpt as video_gen
import youtube_uploader_chatgpt as uploader

def create_and_upload_video():
    """Main function to create and upload video"""
    print(f"\n{'='*50}")
    print(f"🚀 Starting video creation - {datetime.now()}")
    print(f"{'='*50}\n")
    
    # Initialize database
    db.init_db()
    
    # Get unused topic
    used_topics = db.get_used_topics()
    available_topics = [t for t in config.TOPICS if t not in used_topics]
    
    if not available_topics:
        print("⚠️  All topics used, resetting...")
        available_topics = config.TOPICS
    
    topic = random.choice(available_topics)
    print(f"📝 Topic: {topic}")
    
    # Generate script
    print("🤖 Generating script...")
    script = script_generator.generate_script(topic, use_openai=bool(config.OPENAI_API_KEY))
    
    if not script:
        print("❌ Failed to generate script")
        return
    
    print(f"✅ Script generated ({len(script)} chars)")
    
    # Generate metadata
    print("🏷️  Generating metadata...")
    metadata = script_generator.generate_metadata(script)
    title = metadata['title']
    description = metadata['description']
    tags = metadata['tags']
    
    print(f"   Title: {title}")
    print(f"   Tags: {', '.join(tags[:3])}...")
    
    # Generate video
    print("🎬 Generating video...")
    video_filename = f"video_{int(time.time())}.mp4"
    video_path = video_gen.generate_video(script, video_filename)
    
    # Add to database
    video_id = db.add_video(topic, title, video_path)
    print(f"💾 Saved to database (ID: {video_id})")
    
    # Upload to YouTube
    try:
        print("📤 Uploading to YouTube...")
        youtube_id = uploader.upload_video(
            video_path=video_path,
            title=title,
            description=description,
            tags=tags
        )
        
        db.update_video_status(video_id, 'uploaded', youtube_id)
        print(f"✅ Upload complete!")
        
        # Clean up video file
        if os.path.exists(video_path):
            os.remove(video_path)
            print(f"🗑️  Cleaned up: {video_path}")
        
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        db.update_video_status(video_id, 'failed')
    
    print(f"\n{'='*50}")
    print(f"✅ Process complete - {datetime.now()}")
    print(f"{'='*50}\n")

def main():
    """Main bot loop"""
    print("🤖 YouTube Bot Started!")
    print(f"   Schedule: {config.UPLOAD_SCHEDULE} at {config.UPLOAD_TIME}")
    print(f"   Language: {config.LANGUAGE}")
    print(f"   Topics: {len(config.TOPICS)} available")
    print(f"   API: {'OpenAI' if config.OPENAI_API_KEY else 'Groq'}")
    print()
    
    # Verify API keys
    if not config.OPENAI_API_KEY and not config.GROQ_API_KEY:
        print("❌ ERROR: No API keys found!")
        print("   Set OPENAI_API_KEY or GROQ_API_KEY in .env")
        return
    
    # Verify client secrets
    if not os.path.exists(config.CLIENT_SECRETS_FILE):
        print(f"❌ ERROR: {config.CLIENT_SECRETS_FILE} not found!")
        return
    
    # Schedule upload
    if config.UPLOAD_SCHEDULE == "daily":
        schedule.every().day.at(config.UPLOAD_TIME).do(create_and_upload_video)
        print(f"⏰ Scheduled daily upload at {config.UPLOAD_TIME}")
    
    # Uncomment to test immediately:
    # create_and_upload_video()
    
    # Keep bot running
    print("✅ Bot running! Press Ctrl+C to stop\n")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
