# ai_api_module/cli.py
"""
Command Line Interface for AI API Module
"""
import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Optional

from .core.ai import AI
from .core.conversation import Conversation
from .core.exceptions import AIError


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="AI API Module - Unified interface for multiple AI providers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ai-api-module chat "What is machine learning?"
  ai-api-module chat "Explain quantum computing" --model claude --provider anthropic
  ai-api-module image "A sunset over mountains" --output sunset.png
  ai-api-module conversation start --name "Project Planning"
  ai-api-module stats
  ai-api-module providers
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Chat command
    chat_parser = subparsers.add_parser('chat', help='Send chat message')
    chat_parser.add_argument('message', help='Message to send')
    chat_parser.add_argument('--model', '-m', help='Model to use (e.g., gpt, claude, smart, fast)')
    chat_parser.add_argument('--provider', '-p', help='Provider to use (openai, anthropic, google, xai)')
    chat_parser.add_argument('--system', '-s', help='System prompt')
    chat_parser.add_argument('--temperature', '-t', type=float, help='Temperature (0-2)')
    chat_parser.add_argument('--max-tokens', type=int, help='Maximum output tokens')
    chat_parser.add_argument('--stream', action='store_true', help='Stream response')
    chat_parser.add_argument('--image', help='Image file to include')
    chat_parser.add_argument('--web-search', action='store_true', help='Enable web search')
    chat_parser.add_argument('--output', '-o', help='Save response to file')
    
    # Image generation command
    image_parser = subparsers.add_parser('image', help='Generate image')
    image_parser.add_argument('prompt', help='Image generation prompt')
    image_parser.add_argument('--model', help='Image model to use')
    image_parser.add_argument('--provider', help='Provider for image generation')
    image_parser.add_argument('--size', default='1024x1024', help='Image size')
    image_parser.add_argument('--style', default='natural', help='Image style')
    image_parser.add_argument('--output', '-o', default='generated_image.png', help='Output file')
    
    # Conversation management
    conv_parser = subparsers.add_parser('conversation', help='Manage conversations')
    conv_subparsers = conv_parser.add_subparsers(dest='conv_action')
    
    # Start conversation
    start_parser = conv_subparsers.add_parser('start', help='Start new conversation')
    start_parser.add_argument('--name', help='Conversation name')
    start_parser.add_argument('--system', help='System prompt')
    start_parser.add_argument('--model', help='Model to use')
    
    # Continue conversation
    continue_parser = conv_subparsers.add_parser('continue', help='Continue conversation')
    continue_parser.add_argument('file', help='Conversation file')
    continue_parser.add_argument('message', help='Message to send')
    
    # List conversations
    conv_subparsers.add_parser('list', help='List saved conversations')
    
    # Audio commands
    audio_parser = subparsers.add_parser('audio', help='Audio processing')
    audio_subparsers = audio_parser.add_subparsers(dest='audio_action')
    
    # Text to speech
    tts_parser = audio_subparsers.add_parser('speak', help='Text to speech')
    tts_parser.add_argument('text', help='Text to convert to speech')
    tts_parser.add_argument('--voice', default='natural', help='Voice to use')
    tts_parser.add_argument('--output', '-o', default='speech.mp3', help='Output file')
    
    # Speech to text
    stt_parser = audio_subparsers.add_parser('transcribe', help='Speech to text')
    stt_parser.add_argument('audio_file', help='Audio file to transcribe')
    
    # Utility commands
    subparsers.add_parser('providers', help='List available providers')
    subparsers.add_parser('models', help='List available models')
    subparsers.add_parser('stats', help='Show usage statistics')
    subparsers.add_parser('config', help='Show configuration')
    
    # Cost estimation
    cost_parser = subparsers.add_parser('estimate', help='Estimate cost')
    cost_parser.add_argument('message', help='Message to estimate cost for')
    cost_parser.add_argument('--model', help='Model to estimate for')
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        asyncio.run(run_command(args))
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(1)
    except AIError as e:
        print(f"AI Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


async def run_command(args):
    """Execute CLI command"""
    ai = AI()
    
    if args.command == 'chat':
        await handle_chat(ai, args)
    elif args.command == 'image':
        await handle_image(ai, args)
    elif args.command == 'conversation':
        await handle_conversation(ai, args)
    elif args.command == 'audio':
        await handle_audio(ai, args)
    elif args.command == 'providers':
        handle_providers(ai)
    elif args.command == 'models':
        handle_models(ai)
    elif args.command == 'stats':
        handle_stats(ai)
    elif args.command == 'config':
        handle_config(ai)
    elif args.command == 'estimate':
        handle_estimate(ai, args)


async def handle_chat(ai: AI, args):
    """Handle chat command"""
    kwargs = {
        'model': args.model,
        'provider': args.provider,
        'system': args.system,
        'temperature': args.temperature,
        'max_tokens': args.max_tokens,
        'image': args.image,
        'web_search': args.web_search
    }
    
    # Remove None values
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    
    if args.stream:
        print("Response (streaming):")
        print("-" * 40)
        
        full_response = ""
        async for chunk in ai.stream_chat(args.message, **kwargs):
            print(chunk, end="", flush=True)
            full_response += chunk
        print("\n" + "-" * 40)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(full_response)
            print(f"Response saved to {args.output}")
    else:
        response = ai.chat(args.message, **kwargs)
        
        print("Response:")
        print("-" * 40)
        print(response.text)
        print("-" * 40)
        print(f"Model: {response.model}")
        print(f"Provider: {response.provider}")
        print(f"Cost: ${response.cost:.4f}")
        print(f"Tokens: {response.usage.total_tokens}")
        
        if response.tool_calls:
            print(f"Tools used: {len(response.tool_calls)}")
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(response.text)
            print(f"Response saved to {args.output}")


async def handle_image(ai: AI, args):
    """Handle image generation command"""
    print(f"Generating image: {args.prompt}")
    
    response = ai.generate_image(
        args.prompt,
        model=args.model,
        provider=args.provider,
        size=args.size,
        style=args.style
    )
    
    if response.images:
        output_path = Path(args.output)
        response.images[0].save(output_path)
        print(f"Image saved to {output_path}")
        print(f"Cost: ${response.cost:.4f}")
    else:
        print("No image generated")


async def handle_conversation(ai: AI, args):
    """Handle conversation management"""
    if args.conv_action == 'start':
        conv = ai.start_conversation(
            name=args.name,
            system=args.system
        )
        if args.model:
            conv.switch_model(args.model)
        
        print(f"Started conversation: {conv.name}")
        print("Type 'exit' to end conversation")
        
        while True:
            try:
                user_input = input("\nYou: ")
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    break
                
                response = conv.send(user_input)
                print(f"AI: {response.text}")
                print(f"Cost: ${response.cost:.4f}")
                
            except EOFError:
                break
        
        # Save conversation
        save_path = conv.save()
        print(f"Conversation saved to {save_path}")
        
    elif args.conv_action == 'continue':
        conv = ai.load_conversation(Path(args.file))
        print(f"Loaded conversation: {conv.name}")
        
        response = conv.send(args.message)
        print(f"AI: {response.text}")
        print(f"Cost: ${response.cost:.4f}")
        
        # Save updated conversation
        conv.save()
        
    elif args.conv_action == 'list':
        conv_files = list(Path.cwd().glob("*.json"))
        if conv_files:
            print("Saved conversations:")
            for file in conv_files:
                print(f"  {file.name}")
        else:
            print("No saved conversations found")


async def handle_audio(ai: AI, args):
    """Handle audio processing"""
    if args.audio_action == 'speak':
        print(f"Generating speech: {args.text[:50]}...")
        
        response = ai.generate_speech(
            args.text,
            voice=args.voice
        )
        
        if response.audio:
            response.audio.save(args.output)
            print(f"Speech saved to {args.output}")
            print(f"Cost: ${response.cost:.4f}")
        
    elif args.audio_action == 'transcribe':
        print(f"Transcribing: {args.audio_file}")
        
        text = ai.transcribe_audio(args.audio_file)
        print("Transcription:")
        print("-" * 40)
        print(text)
        print("-" * 40)


def handle_providers(ai: AI):
    """Handle providers command"""
    providers = ai.provider_router.get_available_providers()
    
    print("Available providers:")
    for provider in providers:
        print(f"  ✓ {provider}")
    
    if not providers:
        print("  No providers configured")
        print("  Set API keys as environment variables:")
        print("    OPENAI_API_KEY=your-key")
        print("    ANTHROPIC_API_KEY=your-key")
        print("    GOOGLE_API_KEY=your-key")
        print("    XAI_API_KEY=your-key")


def handle_models(ai: AI):
    """Handle models command"""
    print("Model aliases:")
    for alias, model in ai.model_registry.aliases.items():
        print(f"  {alias:15} → {model}")
    
    print("\nModel categories:")
    print("  smart     - Best reasoning models")
    print("  fast      - Fastest response")
    print("  cheap     - Most cost-effective")
    print("  creative  - Best for creative tasks")
    print("  coding    - Best for programming")
    print("  vision    - Best for image analysis")


def handle_stats(ai: AI):
    """Handle stats command"""
    stats = ai.get_usage_stats()
    
    print("Usage Statistics:")
    print(f"  Total requests: {stats['request_count']}")
    print(f"  Total cost: ${stats['total_cost']:.4f}")
    
    if stats['request_count'] > 0:
        avg_cost = stats['total_cost'] / stats['request_count']
        print(f"  Average cost per request: ${avg_cost:.4f}")
    
    # Memory stats
    memory_stats = ai.memory.get_usage_stats(days=7)
    print(f"\nLast 7 days:")
    print(f"  Requests: {memory_stats['total_requests']}")
    print(f"  Cost: ${memory_stats['total_cost']:.4f}")
    print(f"  Tokens: {memory_stats['total_tokens']:,}")
    
    if memory_stats['model_usage']:
        print("\nTop models:")
        for model in memory_stats['model_usage'][:3]:
            print(f"  {model['model']:20} {model['requests']:3} requests  ${model['cost']:.4f}")


def handle_config(ai: AI):
    """Handle config command"""
    config_dict = ai.config.to_dict()
    
    print("Configuration:")
    for key, value in config_dict.items():
        if 'key' in key.lower():
            # Hide API keys for security
            value = "***" if value else "Not set"
        print(f"  {key:25} {value}")


def handle_estimate(ai: AI, args):
    """Handle cost estimation"""
    cost = ai.estimate_cost(args.message, model=args.model)
    
    print(f"Cost estimate: ${cost:.4f}")
    print(f"Message length: {len(args.message)} characters")
    
    if args.model:
        print(f"Model: {args.model}")
