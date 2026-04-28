```python
import os
import json
import pandas as pd
from fpdf import FPDF
import google.generativeai as genai
from datetime import datetime, timedelta

# --- CONFIGURATION ---
# The API key is handled by the environment or provided via environment variable
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
genai.configure(api_key=GEMINI_API_KEY)

class AISMMManager:
    """A comprehensive Python automation suite for Social Media Management."""
    
    def __init__(self, niche, audience):
        self.niche = niche
        self.audience = audience
        self.model = genai.GenerativeModel('gemini-2.5-flash-preview-09-2025')
        self.strategy_data = []

    def generate_30_day_strategy(self):
        """Uses Gemini API to generate a structured 30-day content plan."""
        print(f"🚀 Generating 30-day strategy for {self.niche}...")
        
        prompt = f"""
        Act as a Senior Social Media Strategist. Create a 30-day content calendar for a business in the {self.niche} niche, 
        targeting {self.audience}.
        
        For each day, provide:
        1. Topic/Theme
        2. Caption (Engaging and viral-ready)
        3. 5-10 trending hashtags
        4. AI Image Generation Prompt (for Midjourney/DALL-E)
        5. Optimal Posting Time (based on engagement trends)

        Return the data strictly as a JSON list of objects with keys: 
        'day', 'topic', 'caption', 'hashtags', 'image_prompt', 'posting_time'.
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Basic cleaning of markdown if AI includes it
            raw_text = response.text.strip().replace('```json', '').replace('```', '')
            self.strategy_data = json.loads(raw_text)
            return self.strategy_data
        except Exception as e:
            print(f"❌ Error generating strategy: {e}")
            return None

    def export_to_csv(self, filename="content_plan.csv"):
        """Exports the strategy to a CSV file."""
        if not self.strategy_data:
            print("⚠️ No data to export.")
            return
        df = pd.DataFrame(self.strategy_data)
        df.to_csv(filename, index=False)
        print(f"✅ Strategy exported to {filename}")

    def export_to_pdf(self, filename="content_plan.pdf"):
        """Exports the strategy to a beautifully formatted PDF."""
        if not self.strategy_data:
            print("⚠️ No data to export.")
            return

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        for item in self.strategy_data:
            pdf.add_page()
            
            # Header
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt=f"Day {item['day']}: {item['topic']}", ln=True, align='C')
            pdf.ln(10)
            
            # Posting Info
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, txt=f"Optimal Posting Time: {item['posting_time']}", ln=True)
            pdf.ln(5)
            
            # Caption
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, txt="Caption:", ln=True)
            pdf.set_font("Arial", '', 11)
            pdf.multi_cell(0, 7, txt=item['caption'])
            pdf.ln(5)
            
            # Hashtags
            pdf.set_font("Arial", 'I', 10)
            pdf.multi_cell(0, 7, txt=f"Hashtags: {item['hashtags']}")
            pdf.ln(5)
            
            # AI Image Prompt
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, txt="AI Image Prompt:", ln=True)
            pdf.set_font("Courier", '', 10)
            pdf.set_fill_color(240, 240, 240)
            pdf.multi_cell(0, 7, txt=item['image_prompt'], fill=True)

        pdf.output(filename)
        print(f"✅ Strategy exported to {filename}")

def main():
    print("--- AI SMM Manager Pro ---")
    niche = input("Enter Business Niche (e.g., Sustainable Fashion): ")
    audience = input("Enter Target Audience (e.g., Gen Z Eco-conscious): ")
    
    manager = AISMMManager(niche, audience)
    strategy = manager.generate_30_day_strategy()
    
    if strategy:
        manager.export_to_csv()
        manager.export_to_pdf()
        print("\n🎉 Milestone Special: 30-Day Content Plan is Ready!")

if __name__ == "__main__":
    main()

```
      
