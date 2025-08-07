from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging

from llm_providers import llm_manager, LLMProvider

router = APIRouter(prefix="/api")

logger = logging.getLogger(__name__)


class FeedbackRequest(BaseModel):
    prompt: str
    llm_provider: LLMProvider = LLMProvider.OPENAI


class FeedbackResponse(BaseModel):
    feedback: str


@router.post("/feedback", response_model=FeedbackResponse)
async def generate_feedback(request: FeedbackRequest) -> FeedbackResponse:
    """Evaluate a user prompt and provide improvement suggestions."""
    evaluation_prompt = (
        "You are a helpful prompt engineer. Given the following prompt, "
        "provide suggestions and improvement tips to make it clearer and more effective.\n\n"
        f"Prompt:\n{request.prompt}"
    )

    try:
        response = await llm_manager.generate_response(
            provider_type=request.llm_provider,
            prompt=evaluation_prompt,
            max_tokens=300,
            temperature=0.5,
        )
    except Exception as e:
        logger.error(
            "LLM response generation failed",
            extra={"error": str(e), "request": request.dict()},
        )
        raise HTTPException(status_code=500, detail="LLM failed to generate feedback.") from e

    feedback_text = response.get("response", "").strip()
    if not feedback_text:
        logger.warning(
            "Empty feedback response from LLM", extra={"request": request.dict()}
        )
        raise HTTPException(status_code=502, detail="Received empty feedback from LLM.")

    return FeedbackResponse(feedback=feedback_text)
