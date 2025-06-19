import string
import random

from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from ...core.db import get_db
from ...models import URL

from .alias_generator import get_alias_generator


class URLCreateRequest(BaseModel):
    url: str = Field(
        required=True, description="The original long URL to be shortened."
    )
    alias: str = Field(
        default=None, description="Optional alias for the shortened URL."
    )

    def _validate_url(self):
        """Validate the URL format."""
        if not self.url.startswith(("http://", "https://")):
            raise ValueError("Invalid URL format. Must start with http:// or https://")


class URLCreateResponse(BaseModel):
    url: str
    short_url: str


router = APIRouter(tags=["service_shortener"])


@router.post("/")
def create_shortener(
    request: Request, request_data: URLCreateRequest, db: Session = Depends(get_db)
):
    """
    Endpoint to create a new URL shortener service.
    """
    # Check if the URL already exists in the
    # TODO add validation at cache and model
    alias = None
    if request_data.alias:
        existing_url = db.query(URL).filter(URL.alias == request_data.alias).first()
        if existing_url:
            raise HTTPException(
                status_code=400,
                detail="Alias already exists. Please choose a different alias.",
            )
        alias = request_data.alias

    else:
        try:
            alias = get_alias_generator().generate_alias(db=db)
        except RuntimeError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Alias generation failed after multiple retries. Please try again later.",
            )

    url_obj = URL(
        alias=alias,
        url=request_data.url,
    )
    db.add(url_obj)
    db.commit()
    db.refresh(url_obj)

    return URLCreateResponse(
        url=request_data.url,
        short_url=f"{request.base_url}{url_obj.alias}",
    )
