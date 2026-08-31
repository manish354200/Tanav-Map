"""
Multilingual NLP Models for Indian Languages
Setup and download models for Hindi, Tamil, Telugu, etc.
"""

import os
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Model cache directory
MODEL_CACHE_DIR = Path(__file__).parent / "models" / "multilingual"
MODEL_CACHE_DIR.mkdir(parents=True, exist_ok=True)

class MultilingualModelLoader:
    """Load and manage multilingual NLP models"""
    
    # Available models for different languages
    MODELS = {
        'hindi': {
            'sentiment': 'nlptown/bert-base-multilingual-uncased-sentiment',
            'ner': 'xlm-roberta-base',
        },
        'tamil': {
            'sentiment': 'xlm-roberta-base',
            'ner': 'xlm-roberta-base',
        },
        'telugu': {
            'sentiment': 'xlm-roberta-base',
            'ner': 'xlm-roberta-base',
        },
        'bengali': {
            'sentiment': 'nlptown/bert-base-multilingual-uncased-sentiment',
            'ner': 'xlm-roberta-base',
        },
        'marathi': {
            'sentiment': 'xlm-roberta-base',
            'ner': 'xlm-roberta-base',
        },
        'english': {
            'sentiment': 'twitter-roberta-base-sentiment',
            'ner': 'dslim/bert-base-uncased-ner',
        }
    }
    
    @staticmethod
    def download_models():
        """Download all required multilingual models"""
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        
        logger.info("Downloading multilingual models...")
        
        for lang, models in MultilingualModelLoader.MODELS.items():
            logger.info(f"Downloading models for {lang}...")
            
            for task, model_name in models.items():
                try:
                    logger.info(f"  - {task}: {model_name}")
                    
                    # Download tokenizer
                    tokenizer = AutoTokenizer.from_pretrained(model_name)
                    
                    # Download model
                    model = AutoModelForSequenceClassification.from_pretrained(model_name)
                    
                    logger.info(f"    ✓ Successfully downloaded")
                
                except Exception as e:
                    logger.error(f"    ✗ Error downloading {model_name}: {str(e)}")
    
    @staticmethod
    def get_sentiment_model(language='english'):
        """Get sentiment analysis model for language"""
        from transformers import pipeline
        
        model_name = MultilingualModelLoader.MODELS.get(
            language, MultilingualModelLoader.MODELS['english']
        )['sentiment']
        
        return pipeline(
            'sentiment-analysis',
            model=model_name,
            cache_dir=str(MODEL_CACHE_DIR)
        )
    
    @staticmethod
    def translate_text(text, source_lang, target_lang='english'):
        """Translate text to target language"""
        from googletrans import Translator
        
        translator = Translator()
        
        if source_lang != target_lang:
            result = translator.translate(text, src_lang=source_lang, dest_lang=target_lang)
            return result['text']
        
        return text


def download_all_models():
    """Download all models (run once during setup)"""
    MultilingualModelLoader.download_models()
    logger.info("All models downloaded successfully!")


if __name__ == "__main__":
    download_all_models()
