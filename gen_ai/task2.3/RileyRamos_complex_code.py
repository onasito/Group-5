import pytest
from sqlalchemy.exc import IntegrityError

def create_account(name, email):
    """Helper function to create an account."""
    account = Account(name=name, email=email)
    db.session.add(account)
    db.session.commit()

def test_missing_required_fields():
    """Test creating an account with missing required fields (name or email)."""
    # Test account creation with missing name
    with pytest.raises(IntegrityError) as exc_info:
        create_account(name=None, email="ramos@example.com")
    db.session.rollback()
    # Check if the exception message refers to the 'name' field violation
    assert "NOT NULL constraint failed: account.name" in str(exc_info.value)

    # Test account creation with missing email
    with pytest.raises(IntegrityError) as exc_info:
        create_account(name="Riley", email=None)
    db.session.rollback()
    # Check if the exception message refers to the 'email' field violation
    assert "NOT NULL constraint failed: account.email" in str(exc_info.value)
