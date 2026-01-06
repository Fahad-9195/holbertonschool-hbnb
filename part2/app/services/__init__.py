from .facade import HBnBFacade

# Create a shared facade instance with a shared repository
_shared_facade = None
_shared_repo = None

def get_facade():
    """Get or create a shared facade instance."""
    global _shared_facade, _shared_repo
    if _shared_facade is None:
        from app.persistence.repository import InMemoryRepository
        _shared_repo = InMemoryRepository()
        _shared_facade = HBnBFacade(_shared_repo)
    return _shared_facade

# Create the shared facade instance
facade = get_facade()