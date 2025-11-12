import requests
from bs4 import BeautifulSoup
import uuid
import os
from keybert import KeyBERT

def extract_keywords(text, num_keywords=10):
    """Extract keywords from text using KeyBERT"""
    try:
        kw_model = KeyBERT()
        keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), 
                                            stop_words='english', 
                                            top_n=num_keywords)
        return [kw[0] for kw in keywords]
    except Exception as e:
        print(f"Error extracting keywords: {e}")
        # Fallback to simple word extraction
        words = text.split()
        return list(set([w for w in words if len(w) > 5]))[:num_keywords]

def google_search_image(search_term, api_key, cse_id, num=3):
    """Search for images using Google Custom Search API"""
    try:
        search_url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "q": search_term,
            "cx": cse_id,
            "key": api_key,
            "searchType": "image",
            "num": num
        }
        response = requests.get(search_url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Google search failed for '{search_term}': {e}")
        # Fallback to direct image search
        return fallback_image_search(search_term, num)

def fallback_image_search(search_term, num=3):
    """Fallback method to search images without API"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        search_url = f"https://www.google.com/search?q={search_term}+medical+imaging&tbm=isch"
        response = requests.get(search_url, headers=headers, timeout=10)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img', limit=num+5)
        
        results = {'items': []}
        for img in img_tags[1:num+1]:  # Skip first (Google logo)
            if img.get('src'):
                results['items'].append({'link': img['src']})
        
        return results
    except Exception as e:
        print(f"Fallback search failed for '{search_term}': {e}")
        return {'items': []}

def download_images(response_json, save_folder='images'):
    """Download images from search results"""
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    
    items = response_json.get('items', [])
    if not items:
        print("No images found.")
        return []
    
    image_paths = []
    
    for idx, item in enumerate(items):
        image_url = item.get('link')
        if not image_url:
            continue
        
        try:
            # Handle data URLs (base64 images)
            if image_url.startswith('data:image'):
                continue  # Skip base64 images for now
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            img_data = requests.get(image_url, headers=headers, timeout=10).content
            
            # Determine file extension
            file_ext = image_url.split('.')[-1].split('?')[0][:4]
            if file_ext not in ['jpg', 'jpeg', 'png', 'webp', 'gif']:
                file_ext = 'jpg'
            
            # Generate unique filename
            unique_id = str(uuid.uuid4())[:8]
            filename = f"image_{unique_id}.{file_ext}"
            filepath = os.path.join(save_folder, filename)
            
            with open(filepath, 'wb') as f:
                f.write(img_data)
            
            image_paths.append(filepath)
            print(f"Downloaded: {filepath}")
            
        except Exception as e:
            print(f"Failed to download image from {image_url}: {e}")
            continue
    
    return image_paths

def create_placeholder_images(keywords, save_folder='images', count=10):
    """Create placeholder images if download fails"""
    from PIL import Image, ImageDraw, ImageFont
    import random
    
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    
    colors = [(52, 152, 219), (46, 204, 113), (155, 89, 182), 
              (241, 196, 15), (231, 76, 60), (26, 188, 156)]
    
    image_paths = []
    
    for i in range(min(count, max(len(keywords) * 3, 10))):
        # Create image
        img = Image.new('RGB', (1280, 720), color=random.choice(colors))
        draw = ImageDraw.Draw(img)
        
        # Add text
        keyword = keywords[i % len(keywords)] if keywords else "Medical Image"
        text = keyword.upper()[:30]  # Limit text length
        
        # Draw text in center (approximate position)
        text_position = (400, 320)
        draw.text(text_position, text, fill=(255, 255, 255))
        
        # Save image
        filename = f"placeholder_{i}.jpg"
        filepath = os.path.join(save_folder, filename)
        img.save(filepath)
        image_paths.append(filepath)
        print(f"Created placeholder: {filepath}")
    
    return image_paths
