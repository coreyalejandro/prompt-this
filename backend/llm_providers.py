import os
import logging
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod
from enum import Enum

logger = logging.getLogger(__name__)

try:
    import openai
except ImportError:
    openai = None  # type: ignore[assignment]
    logger.warning(
        "openai package not installed. OpenAI provider will be unavailable."
    )

try:
    import anthropic
except ImportError:
    anthropic = None  # type: ignore[assignment]
    logger.warning(
        "anthropic package not installed. Anthropic provider will be unavailable."
    )

class LLMProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    LOCAL = "local"

class BaseLLMProvider(ABC):
    """Base class for LLM providers"""
    
    def __init__(self, provider_type: LLMProvider):
        self.provider_type = provider_type
        self.initialized = False
    
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the provider with API keys and configuration"""
        pass
    
    @abstractmethod
    async def generate_response(
        self, 
        prompt: str, 
        max_tokens: int = 1000,
        temperature: float = 0.7,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate a response from the LLM"""
        pass
    
    @abstractmethod
    async def generate_with_cache(
        self,
        prompt: str,
        cache_key: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate response with caching support"""
        pass

class OpenAIProvider(BaseLLMProvider):
    """OpenAI API provider"""
    
    def __init__(self):
        super().__init__(LLMProvider.OPENAI)
        self.client = None
        self.model = "gpt-4o-mini"  # Default model
        self.cache = {}  # Simple in-memory cache
    
    async def initialize(self) -> bool:
        """Initialize OpenAI client"""
        try:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                logger.error("OPENAI_API_KEY not found in environment variables")
                return False
            
            self.client = openai.AsyncOpenAI(api_key=api_key)
            
            # Test the connection
            await self.client.models.list()
            self.initialized = True
            logger.info("OpenAI provider initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI provider: {str(e)}")
            return False
    
    async def generate_response(
        self, 
        prompt: str, 
        max_tokens: int = 1000,
        temperature: float = 0.7,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate response using OpenAI API"""
        if not self.initialized:
            raise RuntimeError("OpenAI provider not initialized")
        
        try:
            model = kwargs.get("model", self.model)
            
            response = await self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return {
                "response": response.choices[0].message.content,
                "model": model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                },
                "provider": "openai"
            }
            
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise e
    
    async def generate_with_cache(
        self,
        prompt: str,
        cache_key: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate response with caching"""
        if cache_key and cache_key in self.cache:
            logger.info(f"Cache hit for key: {cache_key}")
            return self.cache[cache_key]
        
        response = await self.generate_response(prompt, **kwargs)
        
        if cache_key:
            self.cache[cache_key] = response
            logger.info(f"Cached response for key: {cache_key}")
        
        return response

class AnthropicProvider(BaseLLMProvider):
    """Anthropic Claude API provider"""
    
    def __init__(self):
        super().__init__(LLMProvider.ANTHROPIC)
        self.client = None
        self.model = "claude-3-haiku-20240307"  # Default model
        self.cache = {}  # Simple in-memory cache
    
    async def initialize(self) -> bool:
        """Initialize Anthropic client"""
        try:
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                logger.error("ANTHROPIC_API_KEY not found in environment variables")
                return False
            
            self.client = anthropic.AsyncAnthropic(api_key=api_key)
            self.initialized = True
            logger.info("Anthropic provider initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Anthropic provider: {str(e)}")
            return False
    
    async def generate_response(
        self, 
        prompt: str, 
        max_tokens: int = 1000,
        temperature: float = 0.7,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate response using Anthropic API"""
        if not self.initialized:
            raise RuntimeError("Anthropic provider not initialized")
        
        try:
            model = kwargs.get("model", self.model)
            
            response = await self.client.messages.create(
                model=model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return {
                "response": response.content[0].text,
                "model": model,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens,
                    "total_tokens": response.usage.input_tokens + response.usage.output_tokens
                },
                "provider": "anthropic"
            }
            
        except Exception as e:
            logger.error(f"Anthropic API error: {str(e)}")
            raise e
    
    async def generate_with_cache(
        self,
        prompt: str,
        cache_key: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate response with caching"""
        if cache_key and cache_key in self.cache:
            logger.info(f"Cache hit for key: {cache_key}")
            return self.cache[cache_key]
        
        response = await self.generate_response(prompt, **kwargs)
        
        if cache_key:
            self.cache[cache_key] = response
            logger.info(f"Cached response for key: {cache_key}")
        
        return response

class LocalProvider(BaseLLMProvider):
    """Local LLM provider (placeholder for future implementation)"""
    
    def __init__(self):
        super().__init__(LLMProvider.LOCAL)
    
    async def initialize(self) -> bool:
        """Initialize local provider"""
        # Placeholder for local model initialization
        logger.info("Local provider initialized (placeholder)")
        self.initialized = True
        return True
    
    async def generate_response(
        self, 
        prompt: str, 
        max_tokens: int = 1000,
        temperature: float = 0.7,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate response using local model"""
        # Placeholder implementation
        response = f"[LOCAL MODEL RESPONSE] {prompt[:100]}..."
        
        return {
            "response": response,
            "model": "local",
            "usage": {
                "prompt_tokens": len(prompt.split()),
                "completion_tokens": len(response.split()),
                "total_tokens": len(prompt.split()) + len(response.split())
            },
            "provider": "local"
        }
    
    async def generate_with_cache(
        self,
        prompt: str,
        cache_key: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate response with caching"""
        return await self.generate_response(prompt, **kwargs)

class LLMProviderManager:
    """Manager for all LLM providers"""
    
    def __init__(self):
        self.providers: Dict[LLMProvider, BaseLLMProvider] = {}
        self.initialized = False
    
    async def initialize_all_providers(self) -> Dict[LLMProvider, bool]:
        """Initialize all available providers"""
        results: Dict[LLMProvider, bool] = {}

        # Initialize OpenAI if available
        if openai is not None:
            openai_provider = OpenAIProvider()
            initialized = await openai_provider.initialize()
            results[LLMProvider.OPENAI] = initialized
            if initialized:
                self.providers[LLMProvider.OPENAI] = openai_provider
        else:
            logger.warning("OpenAI provider skipped due to missing openai package")

        # Initialize Anthropic if available
        if anthropic is not None:
            anthropic_provider = AnthropicProvider()
            initialized = await anthropic_provider.initialize()
            results[LLMProvider.ANTHROPIC] = initialized
            if initialized:
                self.providers[LLMProvider.ANTHROPIC] = anthropic_provider
        else:
            logger.warning(
                "Anthropic provider skipped due to missing anthropic package"
            )

        # Initialize Local (always available as fallback)
        local_provider = LocalProvider()
        initialized = await local_provider.initialize()
        results[LLMProvider.LOCAL] = initialized
        if initialized:
            self.providers[LLMProvider.LOCAL] = local_provider

        self.initialized = True
        logger.info(
            f"LLM Provider Manager initialized. Available providers: {list(self.providers.keys())}"
        )
        return results
    
    def get_provider(self, provider_type: LLMProvider) -> Optional[BaseLLMProvider]:
        """Get a specific provider"""
        return self.providers.get(provider_type)
    
    def get_available_providers(self) -> List[LLMProvider]:
        """Get list of available providers"""
        return list(self.providers.keys())
    
    async def generate_response(
        self,
        provider_type: LLMProvider,
        prompt: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate response using specified provider"""
        provider = self.get_provider(provider_type)
        if not provider:
            raise ValueError(f"Provider {provider_type} not available")
        
        return await provider.generate_response(prompt, **kwargs)

# Global provider manager instance
llm_manager = LLMProviderManager()
