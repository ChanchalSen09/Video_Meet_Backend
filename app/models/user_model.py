from typing import Dict, Any

def user_document(name: str, email: str, picture: str) -> Dict[str, Any]:
    """
    Prepare the user document to be saved in MongoDB.
    """
    return {
        "name": name,
        "email": email,
        "picture": picture
    }
