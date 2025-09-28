# ai_api_module/core/conversation.py
"""
Conversation management system
"""
import json
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional, TYPE_CHECKING
from pathlib import Path

if TYPE_CHECKING:
    from .ai import AI

from .response import AIResponse
from .memory import Message


class Conversation:
    """Manages conversation context and history"""
    
    def __init__(
        self,
        ai_instance: "AI",
        name: Optional[str] = None,
        system: Optional[str] = None,
        conversation_id: Optional[str] = None
    ):
        self.ai = ai_instance
        self.conversation_id = conversation_id or str(uuid.uuid4())
        self.name = name or f"Conversation_{self.conversation_id[:8]}"
        self.system = system
        
        self.messages: List[Message] = []
        self.responses: List[AIResponse] = []
        self.total_cost = 0.0
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        
        # Current model (can be changed mid-conversation)
        self.current_model = None
        self.current_provider = None
        
        # Settings
        self.track_costs = True
        self.auto_summarize = False
        self.max_context_tokens = 8000
        
        # Add system message if provided
        if system:
            self.messages.append(Message(
                role="system",
                content=system,
                timestamp=datetime.now()
            ))
    
    def add_user_message(self, content: str, **kwargs) -> "Conversation":
        """Add user message to conversation"""
        message = Message(
            role="user",
            content=content,
            timestamp=datetime.now(),
            metadata=kwargs
        )
        self.messages.append(message)
        self.updated_at = datetime.now()
        return self
    
    def add_assistant_message(self, content: str, **kwargs) -> "Conversation":
        """Add assistant message to conversation"""
        message = Message(
            role="assistant", 
            content=content,
            timestamp=datetime.now(),
            metadata=kwargs
        )
        self.messages.append(message)
        self.updated_at = datetime.now()
        return self
    
    def send(self, message: Optional[str] = None, **kwargs) -> AIResponse:
        """Send message and get response"""
        if message:
            self.add_user_message(message)
        
        # Check if we need to summarize for context length
        if self.auto_summarize and self._estimate_tokens() > self.max_context_tokens:
            self._auto_summarize()
        
        # Prepare request
        request_kwargs = {
            "conversation_id": self.conversation_id,
            "model": self.current_model,
            "provider": self.current_provider,
            **kwargs
        }
        
        # Get conversation history as messages
        conversation_messages = self._build_message_history()
        
        # Send to AI
        if conversation_messages:
            last_message = conversation_messages[-1]
            if last_message["role"] == "user":
                response = self.ai.chat(
                    message=last_message["content"],
                    system=self.system,
                    **request_kwargs
                )
            else:
                # Continue conversation
                response = self.ai.chat(
                    message="",  # Empty message, will use history
                    system=self.system, 
                    **request_kwargs
                )
        else:
            raise ValueError("No messages to send")
        
        # Add response to conversation
        self.add_assistant_message(response.text)
        self.responses.append(response)
        
        # Track costs
        if self.track_costs:
            self.total_cost += response.cost
        
        self.updated_at = datetime.now()
        
        return response
    
    async def async_send(self, message: Optional[str] = None, **kwargs) -> AIResponse:
        """Async version of send"""
        if message:
            self.add_user_message(message)
        
        request_kwargs = {
            "conversation_id": self.conversation_id,
            "model": self.current_model,
            "provider": self.current_provider,
            **kwargs
        }
        
        conversation_messages = self._build_message_history()
        
        if conversation_messages:
            last_message = conversation_messages[-1]
            response = await self.ai.async_chat(
                message=last_message["content"],
                system=self.system,
                **request_kwargs
            )
        else:
            raise ValueError("No messages to send")
        
        self.add_assistant_message(response.text)
        self.responses.append(response)
        
        if self.track_costs:
            self.total_cost += response.cost
        
        self.updated_at = datetime.now()
        
        return response
    
    def switch_model(self, model: str, provider: Optional[str] = None) -> "Conversation":
        """Switch to different model mid-conversation"""
        self.current_model = model
        self.current_provider = provider
        
        # Add system message about model switch
        self.messages.append(Message(
            role="system",
            content=f"[Model switched to {model}]",
            timestamp=datetime.now(),
            metadata={"model_switch": True}
        ))
        
        return self
    
    def clear_history(self, keep_system: bool = True) -> "Conversation":
        """Clear conversation history"""
        if keep_system and self.system:
            system_messages = [m for m in self.messages if m.role == "system" and not m.metadata.get("model_switch")]
            self.messages = system_messages
        else:
            self.messages = []
        
        self.responses = []
        self.total_cost = 0.0
        self.updated_at = datetime.now()
        
        return self
    
    def get_summary(self) -> str:
        """Get conversation summary"""
        if not self.messages:
            return "Empty conversation"
        
        user_messages = len([m for m in self.messages if m.role == "user"])
        assistant_messages = len([m for m in self.messages if m.role == "assistant"])
        
        return f"""
Conversation: {self.name}
Created: {self.created_at.strftime('%Y-%m-%d %H:%M')}
Updated: {self.updated_at.strftime('%Y-%m-%d %H:%M')}
Messages: {user_messages} user, {assistant_messages} assistant
Total Cost: ${self.total_cost:.4f}
Current Model: {self.current_model or 'default'}
        """.strip()
    
    def save(self, file_path: Optional[Path] = None) -> Path:
        """Save conversation to file"""
        if not file_path:
            file_path = Path(f"{self.name}_{self.conversation_id[:8]}.json")
        
        data = {
            "conversation_id": self.conversation_id,
            "name": self.name,
            "system": self.system,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "current_model": self.current_model,
            "current_provider": self.current_provider,
            "total_cost": self.total_cost,
            "messages": [
                {
                    "role": m.role,
                    "content": m.content,
                    "timestamp": m.timestamp.isoformat(),
                    "metadata": m.metadata
                }
                for m in self.messages
            ],
            "responses": [r.to_dict() for r in self.responses],
            "settings": {
                "track_costs": self.track_costs,
                "auto_summarize": self.auto_summarize,
                "max_context_tokens": self.max_context_tokens
            }
        }
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        return file_path
    
    @classmethod
    def load(cls, file_path: Path, ai_instance: "AI") -> "Conversation":
        """Load conversation from file"""
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        conv = cls(
            ai_instance=ai_instance,
            name=data["name"],
            system=data["system"],
            conversation_id=data["conversation_id"]
        )
        
        conv.created_at = datetime.fromisoformat(data["created_at"])
        conv.updated_at = datetime.fromisoformat(data["updated_at"])
        conv.current_model = data.get("current_model")
        conv.current_provider = data.get("current_provider")
        conv.total_cost = data.get("total_cost", 0.0)
        
        # Load messages
        conv.messages = [
            Message(
                role=m["role"],
                content=m["content"],
                timestamp=datetime.fromisoformat(m["timestamp"]),
                metadata=m.get("metadata", {})
            )
            for m in data["messages"]
        ]
        
        # Load settings
        settings = data.get("settings", {})
        conv.track_costs = settings.get("track_costs", True)
        conv.auto_summarize = settings.get("auto_summarize", False)
        conv.max_context_tokens = settings.get("max_context_tokens", 8000)
        
        return conv
    
    def _build_message_history(self) -> List[Dict[str, str]]:
        """Build message history for API"""
        return [
            {
                "role": m.role,
                "content": m.content
            }
            for m in self.messages
            if not m.metadata.get("model_switch")  # Exclude model switch messages
        ]
    
    def _estimate_tokens(self) -> int:
        """Estimate token count for conversation"""
        total_chars = sum(len(m.content) for m in self.messages)
        return total_chars // 4  # Rough estimate: 4 chars = 1 token
    
    def _auto_summarize(self):
        """Auto-summarize old messages to maintain context window"""
        if len(self.messages) <= 3:  # Keep at least system + 1 exchange
            return
        
        # Keep system messages and last few exchanges
        system_messages = [m for m in self.messages if m.role == "system"]
        recent_messages = self.messages[-4:]  # Last 2 exchanges
        
        # Messages to summarize (middle section)
        to_summarize = self.messages[len(system_messages):-4]
        
        if not to_summarize:
            return
        
        # Create summary
        summary_text = "\n".join([f"{m.role}: {m.content}" for m in to_summarize])
        
        try:
            summary_response = self.ai.chat(
                f"Summarize this conversation history concisely:\n\n{summary_text}",
                model="fast"  # Use fast model for summarization
            )
            
            summary_message = Message(
                role="system",
                content=f"[Previous conversation summary: {summary_response.text}]",
                timestamp=datetime.now(),
                metadata={"summary": True}
            )
            
            # Replace messages with summary
            self.messages = system_messages + [summary_message] + recent_messages
            
        except Exception:
            # If summarization fails, just truncate
            self.messages = system_messages + recent_messages