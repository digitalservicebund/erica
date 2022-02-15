from fastapi import APIRouter
from fastapi_versioning import version

router = APIRouter()


@router.get('/')
@version(2)
def ping():
    """Simple route that can be used to check if the app has started.
    """
    return 'pong'
