from fastapi import APIRouter, status

router = APIRouter()


@router.get("/health/")
async def health_check_router():
    """
    Health check endpoint to verify the service is running.
    """
    return status.HTTP_200_OK
