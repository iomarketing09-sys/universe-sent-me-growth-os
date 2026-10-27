"""Model Router para OmniRoute."""

from __future__ import annotations

from typing import Dict, Any


def get_model_alias(task: str) -> str:
    """Alias de modelo para OmniRoute según la tarea."""
    aliases = {
        "copywriting": "groq/openai/gpt-oss-120b",
        "copywriting_fast": "groq/openai/gpt-oss-20b",
        "tone_analysis": "morph-v3-fast",
        "research": "gemini/gemini-3.5-flash",
        "compliance": "groq/openai/gpt-oss-20b",
        "ab_testing": "groq/openai/gpt-oss-120b",
    }
    return aliases.get(task, "groq/openai/gpt-oss-120b")


def get_generation_params(task: str) -> Dict[str, Any]:
    """Parámetros de generación por tarea."""
    return {
        "copywriting": {"temperature": 0.7, "reasoning_effort": "low", "max_tokens": 2200},
        "copywriting_fast": {"temperature": 0.7, "reasoning_effort": "low", "max_tokens": 2200},
        "tone_analysis": {"temperature": 0.3, "reasoning_effort": "low", "max_tokens": 800},
        "research": {"temperature": 0.5, "reasoning_effort": "low", "max_tokens": 3000},
        "compliance": {"temperature": 0.1, "reasoning_effort": "low", "max_tokens": 1000},
        "ab_testing": {"temperature": 0.8, "reasoning_effort": "low", "max_tokens": 2200},
    }.get(task, {"temperature": 0.7, "reasoning_effort": "low", "max_tokens": 2200})


class ModelRouter:
    """Router simple de modelos."""
    
    def list_models(self) -> Dict[str, str]:
        return {
            "copywriting": get_model_alias("copywriting"),
            "copywriting_fast": get_model_alias("copywriting_fast"),
            "tone_analysis": get_model_alias("tone_analysis"),
            "research": get_model_alias("research"),
            "compliance": get_model_alias("compliance"),
            "ab_testing": get_model_alias("ab_testing"),
        }
