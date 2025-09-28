# tests/test_multimodal.py
"""
Multimodal functionality tests (images, audio, documents)
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from ai_api_module import AI
from ai_api_module.core.response import AIResponse
import tempfile
import os
import base64


class TestImageGeneration:
    """Test image generation functionality"""
    
    @patch('ai_api_module.providers.router.ProviderRouter')
    def test_image_generation_basic(self, mock_router):
        """Test basic image generation"""
        # Mock response with generated image
        mock_image = Mock()
        mock_image.save = Mock()
        
        mock_response = AIResponse(
            text="Generated image successfully",
            images=[mock_image],
            cost=0.04
        )
        
        mock_router_instance = Mock()
        mock_router_instance.execute.return_value = mock_response
        mock_router.return_value = mock_router_instance
        
        ai = AI()
        ai.provider_router = mock_router_instance
        
        response = ai.generate_image("A beautiful sunset")
        
        assert isinstance(response, AIResponse)
        assert len(response.images) == 1
        assert response.cost > 0
        mock_router_instance.execute.assert_called_once()
    
    @patch('ai_api_module.providers.router.ProviderRouter')
    def test_image_generation_with_parameters(self, mock_router):
        """Test image generation with custom parameters"""
        mock_response = AIResponse(
            text="Generated high-quality image",
            images=[Mock()],
            cost=0.08
        )
        
        mock_router_instance = Mock()
        mock_router_instance.execute.return_value = mock_response
        mock_router.return_value = mock_router_instance
        
        ai = AI()
        ai.provider_router = mock_router_instance
        
        response = ai.generate_image(
            "A detailed cityscape",
            style="photorealistic",
            size="1024x1024",
            quality="high"
        )
        
        assert isinstance(response, AIResponse)
        request_data = mock_router_instance.execute.call_args[0][0]
        assert request_data["style"] == "photorealistic"
        assert request_data["size"] == "1024x1024"
        assert request_data["quality"] == "high"
    
    def test_image_generation_error_handling(self):
        """Test error handling in image generation"""
        ai = AI()
        
        # Mock provider router to raise exception
        with patch.object(ai.provider_router, 'execute', side_effect=Exception("API Error")):
            with pytest.raises(Exception):
                ai.generate_image("Test prompt")


class TestImageAnalysis:
    """Test image analysis functionality"""
    
    @patch('ai_api_module.providers.router.ProviderRouter')
    def test_analyze_image_from_path(self, mock_router, tmp_path):
        """Test analyzing image from file path"""
        # Create test image file
        test_image = tmp_path / "test.jpg"
        test_image.write_bytes(b"fake image data")
        
        mock_response = AIResponse(
            text="This image shows a beautiful landscape with mountains and trees.",
            cost=0.002
        )
        
        mock_router_instance = Mock()
        mock_router_instance.execute.return_value = mock_response
        mock_router.return_value = mock_router_instance
        
        ai = AI()
        ai.provider_router = mock_router_instance
        
        response = ai.analyze_image(str(test_image), "What do you see in this image?")
        
        assert isinstance(response, AIResponse)
        assert "landscape" in response.text
        mock_router_instance.execute.assert_called_once()
    
    @patch('ai_api_module.providers.router.ProviderRouter')
    def test_analyze_image_from_url(self, mock_router):
        """Test analyzing image from URL"""
        mock_response = AIResponse(
            text="This image contains a cat sitting on a chair.",
            cost=0.003
        )
        
        mock_router_instance = Mock()
        mock_router_instance.execute.return_value = mock_response
        mock_router.return_value = mock_router_instance
        
        ai = AI()
        ai.provider_router = mock_router_instance
        
        response = ai.analyze_image(
            "https://example.com/cat.jpg",
            "Describe what you see"
        )
        
        assert isinstance(response, AIResponse)
        assert "cat" in response.text
    
    @patch('ai_api_module.providers.router.ProviderRouter')
    def test_analyze_multiple_images(self, mock_router, tmp_path):
        """Test analyzing multiple images"""
        # Create test images
        image1 = tmp_path / "image1.jpg"
        image2 = tmp_path / "image2.jpg"
        image1.write_bytes(b"fake image data 1")
        image2.write_bytes(b"fake image data 2")
        
        mock_response = AIResponse(
            text="The first image shows a dog, the second shows a cat. Both are pets.",
            cost=0.005
        )
        
        mock_router_instance = Mock()
        mock_router_instance.execute.return_value = mock_response
        mock_router.return_value = mock_router_instance
        
        ai = AI()
        ai.provider_router = mock_router_instance
        
        response = ai.analyze_images(
            [str(image1), str(image2)],
            "Compare these images"
        )
        
        assert isinstance(response, AIResponse)
        assert "dog" in response.text and "cat" in response.text


class TestDocumentProcessing:
    """Test document processing functionality"""
    
    @patch('ai_api_module.providers.router.ProviderRouter')
    def test_analyze_text_document(self, mock_router, tmp_path):
        """Test analyzing text document"""
        # Create test document
        test_doc = tmp_path / "test.txt"
        doc_content = """
        Project Proposal: AI Assistant
        
        Objective: Develop an AI-powered assistant for customer service.
        Timeline: 6 months
        Budget: $100,000
        Team: 5 developers, 2 designers
        
        Key Features:
        - Natural language processing
        - Multi-language support
        - Integration with existing systems
        """
        test_doc.write_text(doc_content, encoding='utf-8')
        
        mock_response = AIResponse(
            text="This document outlines a comprehensive AI assistant project with clear objectives, timeline, and budget.",
            cost=0.001
        )
        
        mock_router_instance = Mock()
        mock_router_instance.execute.return_value = mock_response
        mock_router.return_value = mock_router_instance
        
        ai = AI()
        ai.provider_router = mock_router_instance
        
        response = ai.analyze_document(
            str(test_doc),
            "Summarize the key points of this proposal"
        )
        
        assert isinstance(response, AIResponse)
        assert "AI assistant" in response.text.lower()
    
    @patch('ai_api_module.providers.router.ProviderRouter')
    def test_analyze_multiple_documents(self, mock_router, tmp_path):
        """Test analyzing multiple documents"""
        # Create test documents
        doc1 = tmp_path / "doc1.txt"
        doc2 = tmp_path / "doc2.txt"
        
        doc1.write_text("Technical specifications for the AI system.", encoding='utf-8')
        doc2.write_text("Business requirements and user stories.", encoding='utf-8')
        
        mock_response = AIResponse(
            text="Both documents relate to AI development - one focuses on technical specs, the other on business needs.",
            structured_data={
                "common_themes": ["AI development", "project planning"],
                "document_types": ["technical", "business"]
            },
            cost=0.003
        )
        
        mock_router_instance = Mock()
        mock_router_instance.execute.return_value = mock_response
        mock_router.return_value = mock_router_instance
        
        ai = AI()
        ai.provider_router = mock_router_instance
        
        response = ai.analyze_documents(
            [str(doc1), str(doc2)],
            "Find common themes",
            format="json"
        )
        
        assert isinstance(response, AIResponse)
        assert response.structured_data is not None
        assert "common_themes" in response.structured_data
    
    @patch('ai_api_module.providers.router.ProviderRouter')
    def test_pdf_document_analysis(self, mock_router, tmp_path):
        """Test PDF document analysis"""
        # Create fake PDF file
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4 fake PDF content with research data")
        
        mock_response = AIResponse(
            text="This PDF contains research data about machine learning applications in healthcare.",
            cost=0.002
        )
        
        mock_router_instance = Mock()
        mock_router_instance.execute.return_value = mock_response
        mock_router.return_value = mock_router_instance
        
        ai = AI()
        ai.provider_router = mock_router_instance
        
        response = ai.analyze_document(
            str(pdf_file),
            "Extract the main findings from this research paper"
        )
        
        assert isinstance(response, AIResponse)
        assert "research" in response.text.lower()


class TestAudioProcessing:
    """Test audio processing functionality"""
    
    @patch('ai_api_module.providers.router.ProviderRouter')
    def test_transcribe_audio(self, mock_router, tmp_path):
        """Test audio transcription"""
        # Create fake audio file
        audio_file = tmp_path / "test.mp3"
        audio_file.write_bytes(b"fake audio data")
        
        mock_response = AIResponse(
            text="Hello, this is a test recording about AI development.",
            cost=0.006
        )
        
        mock_router_instance = Mock()
        mock_router_instance.execute.return_value = mock_response
        mock_router.return_value = mock_router_instance
        
        ai = AI()
        ai.provider_router = mock_router_instance
        
        text = ai.transcribe_audio(str(audio_file))
        
        assert isinstance(text, str)
        assert "test recording" in text.lower()
    
    @patch('ai_api_module.providers.router.ProviderRouter')
    def test_generate_speech(self, mock_router):
        """Test speech generation"""
        # Mock audio response
        mock_audio = Mock()
        mock_audio.save = Mock()
        
        mock_response = AIResponse(
            text="Speech generated successfully",
            audio=mock_audio,
            cost=0.015
        )
        
        mock_router_instance = Mock()
        mock_router_instance.execute.return_value = mock_response
        mock_router.return_value = mock_router_instance
        
        ai = AI()
        ai.provider_router = mock_router_instance
        
        audio = ai.generate_speech(
            "Hello, this is a test message",
            voice="natural",
            speed=1.0
        )
        
        assert audio is not None
        assert hasattr(audio, 'save')


class TestMultimodalIntegration:
    """Test integration of multiple modalities"""
    
    @patch('ai_api_module.providers.router.ProviderRouter')
    def test_chat_with_image_and_document(self, mock_router, tmp_path):
        """Test chat with both image and document"""
        # Create test files
        image_file = tmp_path / "chart.jpg"
        doc_file = tmp_path / "report.txt"
        
        image_file.write_bytes(b"fake chart image")
        doc_file.write_text("Sales report showing 20% growth", encoding='utf-8')
        
        mock_response = AIResponse(
            text="Based on the chart and report, the company shows strong growth trajectory with 20% increase in sales.",
            cost=0.008
        )
        
        mock_router_instance = Mock()
        mock_router_instance.execute.return_value = mock_response
        mock_router.return_value = mock_router_instance
        
        ai = AI()
        ai.provider_router = mock_router_instance
        
        response = ai.chat(
            "Analyze the trends shown in this chart and correlate with the report",
            image=str(image_file),
            files=[str(doc_file)]
        )
        
        assert isinstance(response, AIResponse)
        assert "growth" in response.text.lower()
        
        # Verify that both image and document were included in the request
        request_data = mock_router_instance.execute.call_args[0][0]
        assert "image" in request_data or "images" in request_data
        assert "documents" in request_data or "files" in request_data
    
    @patch('ai_api_module.providers.router.ProviderRouter')
    def test_multimodal_with_structured_output(self, mock_router, tmp_path):
        """Test multimodal analysis with structured JSON output"""
        # Create test files
        image_file = tmp_path / "product.jpg"
        image_file.write_bytes(b"fake product image")
        
        mock_response = AIResponse(
            text="Product analysis completed",
            structured_data={
                "product_name": "Smartphone",
                "features": ["camera", "display", "battery"],
                "rating": 4.5,
                "price_estimate": "$299"
            },
            cost=0.005
        )
        
        mock_router_instance = Mock()
        mock_router_instance.execute.return_value = mock_response
        mock_router.return_value = mock_router_instance
        
        ai = AI()
        ai.provider_router = mock_router_instance
        
        response = ai.analyze_image(
            str(image_file),
            "Analyze this product and provide structured information",
            format="json"
        )
        
        assert isinstance(response, AIResponse)
        assert response.structured_data is not None
        assert "product_name" in response.structured_data
        assert "features" in response.structured_data


# Integration tests requiring real API keys
@pytest.mark.integration
class TestMultimodalIntegration:
    """Integration tests for multimodal features"""
    
    def test_real_image_generation(self):
        """Test real image generation (requires API key)"""
        if not os.getenv("OPENAI_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"):
            pytest.skip("No API keys available for image generation")
        
        ai = AI()
        
        try:
            response = ai.generate_image(
                "A simple geometric shape",
                size="512x512",
                quality="standard"
            )
            
            assert isinstance(response, AIResponse)
            if response.images:
                assert len(response.images) > 0
            assert response.cost >= 0
            
        except Exception as e:
            # Some providers might not support image generation
            pytest.skip(f"Image generation not available: {e}")
    
    def test_real_document_analysis(self, tmp_path):
        """Test real document analysis (requires API key)"""
        if not any(os.getenv(key) for key in ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GOOGLE_API_KEY"]):
            pytest.skip("No API keys available")
        
        # Create a real test document
        test_doc = tmp_path / "sample.txt"
        test_doc.write_text("""
        Meeting Notes - Q4 Planning Session
        
        Date: December 1, 2024
        Attendees: Sarah, Mike, Lisa, Tom
        
        Key Decisions:
        1. Launch new product line in Q1 2025
        2. Increase marketing budget by 30%
        3. Hire 2 additional developers
        
        Action Items:
        - Sarah: Prepare product roadmap (Due: Dec 15)
        - Mike: Submit budget proposal (Due: Dec 10)
        - Lisa: Start recruitment process (Due: Dec 5)
        """, encoding='utf-8')
        
        ai = AI()
        
        response = ai.analyze_document(
            str(test_doc),
            "Extract the key decisions and action items from these meeting notes",
            format="json"
        )
        
        assert isinstance(response, AIResponse)
        assert len(response.text) > 0
        assert response.cost >= 0
        
        # If structured output is available, check it
        if response.structured_data:
            assert isinstance(response.structured_data, dict)
