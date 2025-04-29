from app.config.settings import settings
from groq import Groq

class TranslationService:
    def __init__(self):
        self.client = Groq(api_key=settings.groq_api_key)
    
    async def medical_translate(self, text: str, source_lang: str, target_lang: str) -> str:
        system_prompt = """You are a highly specialized medical translator. Your task is to translate medical texts accurately while adhering to strict guidelines. Follow these rules:

1. **Preserve Medical Terminology**: Do not simplify or change medical terms.
2. **Retain Numerical Values & Units**: Keep all numbers, dosages, and measurements unchanged.
3. **Ensure Clinical Context Consistency**: Maintain the intent and medical meaning.
4. **Do Not Localize Measurement Units**: Keep mg/dL, IU/L, etc., unchanged.
5. **Preserve Drug Names**: Do not substitute with generic alternatives.
6. **Maintain Alphanumeric Values**: Numbers, codes, and percentages must remain the same.
7. **Keep Standardized Codes Untranslated**: Retain ICD-10, LOINC, BI-RADS, etc.

### **Output Format**
Your response must strictly follow this structure:

  
**Target Language:**  {translated_text}  

Ensure high accuracy and clinical correctness in your translation."""

        prompt = f"""Translate the following medical text from {source_lang} to {target_lang} while adhering to strict medical translation guidelines.

        **Text:** {text}
        """


        
        result = self.client.chat.completions.create(
            model=settings.llm_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                "role": "user", 
                "content": prompt
                }],
            temperature=0.1,
            max_tokens=4000
        )
        response= result.choices[0].message.content
        response=response.lower()
        response=response.strip()
        response=response.replace("**target language:**:","")
        response=response.replace("target language:","")
        response=response.replace("target language","")
        response=response.replace("*","")




        return response