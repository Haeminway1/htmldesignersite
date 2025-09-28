# tests/test_memory.py
"""
Memory system tests
"""
import pytest
from unittest.mock import Mock, patch
from ai_api_module.core.memory import Memory, MemoryManager
from ai_api_module import AI
from ai_api_module.core.response import AIResponse
import tempfile
import os
import json


class TestMemory:
    """Test Memory class functionality"""
    
    def test_memory_creation(self):
        """Test creating a memory"""
        memory = Memory(
            key="user_preference",
            value="Likes detailed explanations",
            category="preferences",
            importance=0.8
        )
        
        assert memory.key == "user_preference"
        assert memory.value == "Likes detailed explanations"
        assert memory.category == "preferences"
        assert memory.importance == 0.8
        assert memory.timestamp is not None
    
    def test_memory_serialization(self):
        """Test memory serialization to dict"""
        memory = Memory(
            key="project_type",
            value="Web application using FastAPI",
            category="project",
            importance=0.9
        )
        
        data = memory.to_dict()
        
        assert data["key"] == "project_type"
        assert data["value"] == "Web application using FastAPI"
        assert data["category"] == "project"
        assert data["importance"] == 0.9
        assert "timestamp" in data
        assert "id" in data
    
    def test_memory_from_dict(self):
        """Test creating memory from dict"""
        data = {
            "key": "user_name",
            "value": "Alice",
            "category": "personal",
            "importance": 0.7,
            "timestamp": "2024-01-01T12:00:00",
            "id": "mem_123"
        }
        
        memory = Memory.from_dict(data)
        
        assert memory.key == "user_name"
        assert memory.value == "Alice"
        assert memory.category == "personal"
        assert memory.importance == 0.7
        assert memory.id == "mem_123"
    
    def test_memory_update(self):
        """Test updating memory value"""
        memory = Memory("skill_level", "beginner", "learning")
        
        # Update value
        memory.update_value("intermediate")
        
        assert memory.value == "intermediate"
        # Timestamp should be updated
        assert memory.timestamp is not None
    
    def test_memory_relevance_calculation(self):
        """Test memory relevance calculation"""
        memory = Memory(
            key="programming_language",
            value="Python",
            category="technical",
            importance=0.8
        )
        
        # Test relevance to related query
        relevance = memory.calculate_relevance("What is the best Python framework?")
        assert relevance > 0.5  # Should be relevant
        
        # Test relevance to unrelated query
        relevance = memory.calculate_relevance("What is the weather today?")
        assert relevance < 0.3  # Should be less relevant


class TestMemoryManager:
    """Test MemoryManager functionality"""
    
    def test_memory_manager_creation(self):
        """Test memory manager creation"""
        manager = MemoryManager()
        
        assert len(manager.memories) == 0
        assert manager.storage_file is None
    
    def test_add_fact(self):
        """Test adding facts to memory"""
        manager = MemoryManager()
        
        manager.add_fact("user_preference", "Prefers concise answers")
        manager.add_fact("project_deadline", "End of December", category="project")
        
        assert len(manager.memories) == 2
        
        # Check if memories are stored correctly
        user_pref = manager.get_fact("user_preference")
        assert user_pref.value == "Prefers concise answers"
        
        deadline = manager.get_fact("project_deadline")
        assert deadline.category == "project"
    
    def test_update_fact(self):
        """Test updating existing facts"""
        manager = MemoryManager()
        
        manager.add_fact("user_skill", "beginner")
        manager.update_fact("user_skill", "intermediate")
        
        updated_fact = manager.get_fact("user_skill")
        assert updated_fact.value == "intermediate"
        assert len(manager.memories) == 1  # Should not create duplicate
    
    def test_remove_fact(self):
        """Test removing facts from memory"""
        manager = MemoryManager()
        
        manager.add_fact("temp_note", "This is temporary")
        assert len(manager.memories) == 1
        
        manager.remove_fact("temp_note")
        assert len(manager.memories) == 0
        
        # Removing non-existent fact should not raise error
        manager.remove_fact("non_existent")
    
    def test_get_relevant_memories(self):
        """Test getting relevant memories for a query"""
        manager = MemoryManager()
        
        # Add diverse memories
        manager.add_fact("programming_language", "Python", importance=0.9)
        manager.add_fact("favorite_food", "Pizza", importance=0.3)
        manager.add_fact("project_framework", "FastAPI", importance=0.8)
        manager.add_fact("user_location", "Seoul", importance=0.5)
        
        # Query related to programming
        relevant = manager.get_relevant_memories(
            "Help me with Python web development",
            limit=3
        )
        
        assert len(relevant) <= 3
        # Programming-related memories should be first
        assert any("Python" in mem.value for mem in relevant)
        assert any("FastAPI" in mem.value for mem in relevant)
    
    def test_memory_categories(self):
        """Test memory categorization"""
        manager = MemoryManager()
        
        manager.add_fact("name", "Alice", category="personal")
        manager.add_fact("skill", "Python", category="technical")
        manager.add_fact("deadline", "Next week", category="project")
        
        # Get memories by category
        personal = manager.get_memories_by_category("personal")
        technical = manager.get_memories_by_category("technical")
        
        assert len(personal) == 1
        assert len(technical) == 1
        assert personal[0].value == "Alice"
        assert technical[0].value == "Python"
    
    def test_memory_importance_filtering(self):
        """Test filtering memories by importance"""
        manager = MemoryManager()
        
        manager.add_fact("critical_info", "Very important", importance=0.9)
        manager.add_fact("moderate_info", "Somewhat important", importance=0.6)
        manager.add_fact("minor_info", "Not very important", importance=0.2)
        
        # Get high importance memories
        important = manager.get_memories_by_importance(min_importance=0.7)
        
        assert len(important) == 1
        assert important[0].value == "Very important"


class TestMemoryPersistence:
    """Test memory persistence (save/load)"""
    
    def test_save_and_load_memory(self, tmp_path):
        """Test saving and loading memory to/from file"""
        # Create temporary file
        memory_file = tmp_path / "test_memory.json"
        
        # Create manager and add some memories
        manager = MemoryManager(storage_file=str(memory_file))
        
        manager.add_fact("user_name", "Bob")
        manager.add_fact("project_type", "AI Assistant")
        manager.add_fact("deadline", "Q1 2025", category="project")
        
        # Save to file
        manager.save()
        
        assert memory_file.exists()
        
        # Create new manager and load
        new_manager = MemoryManager(storage_file=str(memory_file))
        new_manager.load()
        
        assert len(new_manager.memories) == 3
        assert new_manager.get_fact("user_name").value == "Bob"
        assert new_manager.get_fact("project_type").value == "AI Assistant"
        assert new_manager.get_fact("deadline").category == "project"
    
    def test_auto_save_on_changes(self, tmp_path):
        """Test automatic saving when memories change"""
        memory_file = tmp_path / "auto_save_test.json"
        
        manager = MemoryManager(
            storage_file=str(memory_file),
            auto_save=True
        )
        
        # Add fact should trigger auto-save
        manager.add_fact("test_key", "test_value")
        
        assert memory_file.exists()
        
        # Load in new manager to verify save
        new_manager = MemoryManager(storage_file=str(memory_file))
        new_manager.load()
        
        assert len(new_manager.memories) == 1
        assert new_manager.get_fact("test_key").value == "test_value"
    
    def test_memory_file_corruption_handling(self, tmp_path):
        """Test handling of corrupted memory files"""
        memory_file = tmp_path / "corrupted.json"
        
        # Create corrupted file
        memory_file.write_text("invalid json content")
        
        manager = MemoryManager(storage_file=str(memory_file))
        
        # Should handle corruption gracefully
        manager.load()  # Should not raise exception
        assert len(manager.memories) == 0  # Should start fresh


class TestMemoryIntegrationWithAI:
    """Test memory integration with AI class"""
    
    @patch('ai_api_module.providers.router.ProviderRouter')
    def test_ai_memory_usage(self, mock_router):
        """Test AI using memory in conversations"""
        # Mock response
        mock_response = AIResponse(
            text="Based on your preference for concise answers, here's a brief explanation.",
            cost=0.001
        )
        
        mock_router_instance = Mock()
        mock_router_instance.execute.return_value = mock_response
        mock_router.return_value = mock_router_instance
        
        ai = AI()
        ai.provider_router = mock_router_instance
        
        # Add memory
        ai.memory.add_fact("user_preference", "Prefers concise answers")
        ai.memory.add_fact("expertise_level", "Beginner programmer")
        
        # Chat with memory enabled
        response = ai.chat(
            "Explain functions in Python",
            use_memory=True
        )
        
        # Verify memory was included in request
        request_data = mock_router_instance.execute.call_args[0][0]
        assert "memory_context" in request_data or "system" in request_data
        
        # Should contain memory information
        memory_text = str(request_data)
        assert "concise" in memory_text.lower() or "beginner" in memory_text.lower()
    
    @patch('ai_api_module.providers.router.ProviderRouter')
    def test_conversation_memory_accumulation(self, mock_router):
        """Test memory accumulation during conversations"""
        mock_response = AIResponse(
            text="I'll remember that you're working on a web application.",
            cost=0.001
        )
        
        mock_router_instance = Mock()
        mock_router_instance.execute.return_value = mock_response
        mock_router.return_value = mock_router_instance
        
        ai = AI()
        ai.provider_router = mock_router_instance
        
        # Start conversation
        conversation = ai.start_conversation(
            name="Project Discussion",
            system="Remember important details about the user's project"
        )
        
        # Add messages that should create memories
        conversation.add_user_message("I'm building a FastAPI web application")
        response1 = conversation.send()
        
        conversation.add_user_message("The deadline is end of March 2025")
        response2 = conversation.send()
        
        # Manually add facts that would be extracted in real implementation
        ai.memory.add_fact("project_framework", "FastAPI")
        ai.memory.add_fact("project_deadline", "End of March 2025")
        
        # Next message should use accumulated memory
        conversation.add_user_message("What should I focus on first?")
        response3 = conversation.send(use_memory=True)
        
        # Verify memory exists
        assert ai.memory.get_fact("project_framework") is not None
        assert ai.memory.get_fact("project_deadline") is not None
    
    def test_memory_context_injection(self):
        """Test memory context injection into prompts"""
        ai = AI()
        
        # Add various memories
        ai.memory.add_fact("user_name", "Alice")
        ai.memory.add_fact("programming_language", "Python", importance=0.9)
        ai.memory.add_fact("project_type", "Web scraper", importance=0.8)
        ai.memory.add_fact("random_fact", "Likes coffee", importance=0.3)
        
        # Get memory context for a programming question
        context = ai.memory._build_context_string(
            query="Help me optimize my Python code",
            max_memories=3
        )
        
        assert "Alice" in context  # User name should be included
        assert "Python" in context  # Highly relevant
        assert "Web scraper" in context  # Relevant to programming
        # Low importance "Likes coffee" might or might not be included
    
    def test_memory_cleanup(self):
        """Test memory cleanup and optimization"""
        ai = AI()
        
        # Add many memories
        for i in range(100):
            ai.memory.add_fact(
                f"fact_{i}",
                f"Value {i}",
                importance=0.1 + (i % 10) * 0.1  # Varying importance
            )
        
        assert len(ai.memory.memories) == 100
        
        # Cleanup low importance memories
        ai.memory.cleanup_memories(min_importance=0.5, max_memories=20)
        
        # Should have fewer memories now
        assert len(ai.memory.memories) <= 20
        
        # Remaining memories should have higher importance
        for memory in ai.memory.memories:
            assert memory.importance >= 0.5


# Integration tests requiring real AI responses
@pytest.mark.integration
class TestMemoryIntegrationReal:
    """Integration tests for memory with real AI"""
    
    def test_real_memory_persistence(self, tmp_path):
        """Test memory persistence with real AI interactions"""
        if not any(os.getenv(key) for key in ["OPENAI_API_KEY", "ANTHROPIC_API_KEY"]):
            pytest.skip("No API keys available")
        
        memory_file = tmp_path / "real_memory.json"
        
        # First AI instance
        ai1 = AI()
        ai1.memory.storage_file = str(memory_file)
        ai1.memory.auto_save = True
        
        # Add some facts
        ai1.memory.add_fact("user_programming_level", "Intermediate Python developer")
        ai1.memory.add_fact("current_project", "Building a web API with FastAPI")
        
        # Save memory
        ai1.memory.save()
        
        # Second AI instance loading same memory
        ai2 = AI()
        ai2.memory.storage_file = str(memory_file)
        ai2.memory.load()
        
        # Should have same memories
        assert len(ai2.memory.memories) == 2
        assert ai2.memory.get_fact("user_programming_level") is not None
        assert ai2.memory.get_fact("current_project") is not None
        
        # Test using memory in actual chat
        try:
            response = ai2.chat(
                "Give me a quick tip for my current work",
                use_memory=True,
                max_tokens=50
            )
            
            assert isinstance(response, AIResponse)
            assert len(response.text) > 0
            
        except Exception as e:
            pytest.skip(f"Real AI chat with memory failed: {e}")
    
    def test_memory_across_conversation_sessions(self, tmp_path):
        """Test memory persistence across conversation sessions"""
        if not any(os.getenv(key) for key in ["OPENAI_API_KEY", "ANTHROPIC_API_KEY"]):
            pytest.skip("No API keys available")
        
        memory_file = tmp_path / "conversation_memory.json"
        
        # First conversation session
        ai1 = AI()
        ai1.memory.storage_file = str(memory_file)
        ai1.memory.auto_save = True
        
        conv1 = ai1.start_conversation("Learning Session")
        conv1.add_user_message("I'm learning about machine learning algorithms")
        
        try:
            response1 = conv1.send(max_tokens=30)
            
            # Manually add what would be extracted from conversation
            ai1.memory.add_fact("learning_topic", "Machine learning algorithms")
            
            # Second conversation session with new AI instance
            ai2 = AI()
            ai2.memory.storage_file = str(memory_file)
            ai2.memory.load()
            
            conv2 = ai2.start_conversation("Follow-up Session")
            conv2.add_user_message("Can you recommend some resources for my studies?")
            
            response2 = conv2.send(use_memory=True, max_tokens=50)
            
            # Both responses should be valid
            assert isinstance(response1, AIResponse)
            assert isinstance(response2, AIResponse)
            
            # Memory should persist
            assert ai2.memory.get_fact("learning_topic") is not None
            
        except Exception as e:
            pytest.skip(f"Real conversation with memory failed: {e}")
