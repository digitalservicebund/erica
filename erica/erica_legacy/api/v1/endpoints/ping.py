from fastapi import APIRouter

router = APIRouter()


@router.get('/')
def ping():
    """Simple route that can be used to check if the app has started.
    """
    return 'pong'
