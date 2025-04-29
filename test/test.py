import os
import argparse
import requests
from pathlib import Path

def test_endpoint(api_url, audio_path, source_lang, target_lang, output_dir):
    """Test medical translation endpoint with full validation"""
    
    # Validate inputs
    if not Path(audio_path).is_file():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # 1. Send request to endpoint
        with open(audio_path, 'rb') as audio_file:
            files = {'audio_file': audio_file}
            data = {
                'source_lang': source_lang,
                'target_lang': target_lang
            }
            
            response = requests.post(
                f"{api_url}/api/v1/medical-translate",
                files=files,
                data=data
            )
        
        # 2. Validate response
        response.raise_for_status()
        json_response = response.json()
        
        required_keys = ['source_transcription', 'translated_text', 'tts_audio_url']
        if not all(key in json_response for key in required_keys):
            raise ValueError("Missing required keys in response")
        
        # 3. Save text outputs
        with open(output_dir/'source_transcription.txt', 'w') as f:
            f.write(json_response['source_transcription'])
            
        with open(output_dir/'translated_text.txt', 'w', encoding='utf-8') as f:
            f.write(json_response['translated_text'])
        
        # 4. Download audio file
        tts_url = f"{api_url}{json_response['tts_audio_url']}"
        audio_response = requests.get(tts_url)
        audio_response.raise_for_status()
        
        with open(output_dir/'translated_audio.mp3', 'wb') as f:
            f.write(audio_response.content)
            
        print("Test succeeded!")
        print(f"Outputs saved to: {output_dir.resolve()}")
        
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        exit(1)
    except Exception as e:
        print(f"Test failed: {str(e)}")
        exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Test Medical Translation API Endpoint",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '--api-url',
        default='http://localhost:2000',
        help='Base URL of the API'
    )
    parser.add_argument(
        '--audio-path',
         default='zzz_static_response_audio.mp3',
        help='Path to input audio file'
    )
    parser.add_argument(
        '--source-lang',
        default='en-US',
        help='Source language code'
    )
    parser.add_argument(
        '--target-lang',
        default='hi-IN',
        help='Target language code'
    )
    parser.add_argument(
        '--output-dir',
        default='test',
        help='Directory to save outputs'
    )
    
    args = parser.parse_args()
    
    test_endpoint(
        api_url=args.api_url,
        audio_path=args.audio_url,
        source_lang=args.source_lang,
        target_lang=args.target_lang,
        output_dir=args.output_dir
    )