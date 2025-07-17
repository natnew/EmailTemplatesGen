"""EmailTemplatesGen - AI-powered email template generation."""

__version__ = "0.1.0"
__author__ = "EmailTemplatesGen Team"
__description__ = "AI-powered email template generation with Outlook and SharePoint integration"

from email_templates_gen.email_generator import generator
from email_templates_gen.integrations import outlook, sharepoint
from email_templates_gen.learnbot import chatbot, rag_pipeline

__all__ = [
    "generator",
    "outlook", 
    "sharepoint",
    "chatbot",
    "rag_pipeline",
]
