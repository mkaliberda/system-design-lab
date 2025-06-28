import os
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from ...core.db import get_db
from ...models import URL

router = APIRouter(tags=["service_redirect"])


@router.get("/{alias}", response_class=RedirectResponse)
def redirect_to_original_url(
    alias: str,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Redirects to the original URL based on the provided alias.
    """
    # TODO check if alias in redis cache
    # If not found in cache, query the database
    url_obj = db.query(URL).filter(URL.alias == alias).first()
    if not url_obj:
        raise HTTPException(status_code=404, detail="URL not found")

    reddirect_url = url_obj.url
    if not reddirect_url.startswith(("http://", "https://")):
        reddirect_url = f"http://{reddirect_url}"
    return RedirectResponse(url=reddirect_url, status_code=status.HTTP_302_FOUND)
