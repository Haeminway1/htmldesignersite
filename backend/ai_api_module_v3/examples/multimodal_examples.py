# examples/multimodal_examples.py
"""
Multimodal capabilities examples
"""
from ai_api_module import AI
from pathlib import Path

def main():
    """Run multimodal examples"""
    print("🎨 AI API Module - Multimodal Examples\n")
    
    ai = AI()
    
    print("=== Image Generation ===")
    try:
        image_response = ai.generate_image(
            "A futuristic cityscape at sunset with flying cars",
            style="photorealistic",
            size="1024x1024"
        )
        
        if image_response.images:
            # Save the generated image
            image_response.images[0].save("generated_city.png")
            print(f"Generated image saved as 'generated_city.png'")
            print(f"Cost: ${image_response.cost:.4f}")
        
    except Exception as e:
        print(f"Image generation error: {e}")
    
    print("\n=== Image Analysis ===")
    # Create a simple test image if it doesn't exist
    test_image_path = Path("test_image.txt")
    if not test_image_path.exists():
        print("Creating test description for image analysis demo...")
        with open(test_image_path, 'w') as f:
            f.write("This is a placeholder for image analysis demo")
    
    try:
        response = ai.analyze_image(
            "test_image.txt",  # In real use, this would be an image file
            "Describe what you see in detail"
        )
        print(f"Analysis: {response.text}")
    except Exception as e:
        print(f"Image analysis error: {e}")
    
    print("\n=== Multiple Images Analysis ===")
    try:
        # In practice, these would be actual image files
        image_files = ["image1.jpg", "image2.jpg"] 
        response = ai.analyze_images(
            image_files,
            "Compare these two images and describe the differences"
        )
        print(f"Multi-image analysis: {response.text}")
    except Exception as e:
        print(f"Multi-image analysis not available: {e}")
    
    print("\n=== Document Processing ===")
    # Create a test document
    test_doc = Path("test_document.txt")
    with open(test_doc, 'w') as f:
        f.write("""
        AI API Module Documentation
        
        This is a comprehensive AI API module that provides a unified interface
        for multiple AI providers including OpenAI, Anthropic, Google, and xAI.
        
        Key features:
        - Unified API across providers
        - Cost tracking and budget management
        - Conversation management
        - Multimodal capabilities
        - Async support
        """)
    
    try:
        response = ai.analyze_document(
            test_doc,
            "Summarize the key points from this document"
        )
        print(f"Document summary: {response.text}")
    except Exception as e:
        print(f"Document analysis error: {e}")
    
    print("\n=== Audio Processing ===")
    try:
        # Text to speech
        audio_response = ai.generate_speech(
            "Hello, this is a test of the AI API module's text to speech capabilities.",
            voice="natural",
            speed=1.0
        )
        
        if audio_response.audio:
            audio_response.audio.save("test_speech.mp3")
            print("Generated speech saved as 'test_speech.mp3'")
            print(f"Cost: ${audio_response.cost:.4f}")
    
    except Exception as e:
        print(f"Text-to-speech error: {e}")
    
    try:
        # Speech to text (would need an actual audio file)
        # text = ai.transcribe_audio("audio_file.mp3")
        # print(f"Transcription: {text}")
        print("Audio transcription requires an actual audio file")
    except Exception as e:
        print(f"Speech-to-text error: {e}")
    
    print("\n=== Mixed Multimodal Conversation ===")
    conversation = ai.start_conversation(
        name="Multimodal Chat",
        system="You are a helpful assistant that can work with text, images, and other media"
    )
    
    # Text message
    conversation.add_user_message("Hello! I'd like to work with different types of content.")
    response1 = conversation.send()
    print(f"AI: {response1.text}")
    
    # Message with image (simulated)
    try:
        response2 = conversation.send(
            "I'll send you an image to analyze",
            # image="path/to/image.jpg"  # Would include actual image
        )
        print(f"AI: {response2.text}")
    except Exception as e:
        print(f"Mixed conversation error: {e}")
    
    # Clean up test files
    for file in [test_image_path, test_doc]:
        if file.exists():
            file.unlink()
    
    print(f"\nConversation cost: ${conversation.total_cost:.4f}")


if __name__ == "__main__":
    main()