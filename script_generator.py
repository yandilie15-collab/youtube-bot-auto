import openai
from groq import Groq
import config_chatgpt as config

def generate_script_openai(topic):
    """Generate video script using OpenAI"""
    openai.api_key = config.OPENAI_API_KEY
    
    prompt = f"""Buat script video YouTube singkat (60 detik) dalam Bahasa Indonesia tentang: {topic}

Format:
- Judul menarik
- Hook pembuka (5 detik)
- 3 poin utama (masing-masing 15 detik)
- Penutup dengan call-to-action (10 detik)

Gunakan bahasa yang conversational dan engaging."""

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Kamu adalah content creator YouTube yang ahli membuat script viral."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI Error: {e}")
        return None

def generate_script_groq(topic):
    """Generate video script using Groq"""
    client = Groq(api_key=config.GROQ_API_KEY)
    
    prompt = f"""Buat script video YouTube singkat (60 detik) dalam Bahasa Indonesia tentang: {topic}

Format:
- Judul menarik
- Hook pembuka (5 detik)
- 3 poin utama (masing-masing 15 detik)
- Penutup dengan call-to-action (10 detik)

Gunakan bahasa yang conversational dan engaging."""

    try:
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "system", "content": "Kamu adalah content creator YouTube yang ahli membuat script viral."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Groq Error: {e}")
        return None

def generate_script(topic, use_openai=True):
    """Generate script with fallback"""
    if use_openai and config.OPENAI_API_KEY:
        script = generate_script_openai(topic)
        if script:
            return script
    
    if config.GROQ_API_KEY:
        return generate_script_groq(topic)
    
    return None

def generate_metadata(script):
    """Generate title, description, and tags from script"""
    client = Groq(api_key=config.GROQ_API_KEY) if config.GROQ_API_KEY else None
    
    if not client:
        openai.api_key = config.OPENAI_API_KEY
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Buat metadata YouTube dari script."},
                {"role": "user", "content": f"Script: {script}\n\nBuat:\n1. Title (maks 60 karakter)\n2. Description (maks 200 karakter)\n3. Tags (10 tags, comma-separated)"}
            ],
            max_tokens=200
        )
        content = response.choices[0].message.content
    else:
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "system", "content": "Buat metadata YouTube dari script."},
                {"role": "user", "content": f"Script: {script}\n\nBuat:\n1. Title (maks 60 karakter)\n2. Description (maks 200 karakter)\n3. Tags (10 tags, comma-separated)"}
            ],
            max_tokens=200
        )
        content = response.choices[0].message.content
    
    lines = content.strip().split('\n')
    title = ""
    description = ""
    tags = []
    
    for line in lines:
        if "title" in line.lower() and not title:
            title = line.split(':', 1)[-1].strip().strip('"')
        elif "description" in line.lower() and not description:
            description = line.split(':', 1)[-1].strip().strip('"')
        elif "tags" in line.lower() and not tags:
            tag_str = line.split(':', 1)[-1].strip()
            tags = [t.strip() for t in tag_str.split(',')]
    
    return {
        "title": title[:60] if title else "Video Menarik",
        "description": description[:200] if description else "Konten edukatif dan menghibur",
        "tags": tags[:10] if tags else ["video", "indonesia"]
    }
