"""
Test Cases for Account Model
"""
import json
from random import randrange
import pytest
from models import db
from models.account import Account, DataValidationError

ACCOUNT_DATA = {}

@pytest.fixture(scope="module", autouse=True)
def load_account_data():
    """ Load data needed by tests """
    global ACCOUNT_DATA
    with open('tests/fixtures/account_data.json') as json_data:
        ACCOUNT_DATA = json.load(json_data)

    # Set up the database tables
    db.create_all()
    yield
    db.session.close()

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    """ Truncate the tables and set up for each test """
    db.session.query(Account).delete()
    db.session.commit()
    yield
    db.session.remove()

######################################################################
#  E X A M P L E   T E S T   C A S E
######################################################################

# ===========================
# Test Group: Role Management
# ===========================

# ===========================
# Test: Account Role Assignment
# Author: John Businge
# Date: 2025-01-30
# Description: Ensure roles can be assigned and checked.
# ===========================

# def test_account_role_assignment():
#     """Test assigning roles to an account"""
#     account = Account(name="John Doe", email="johndoe@example.com", role="user")

#     # Assign initial role
#     assert account.role == "user"

#     # Change role and verify
#     account.change_role("admin")
#     assert account.role == "admin"

# ===========================
# Test: Invalid Role Assignment
# Author: John Businge
# Date: 2025-01-30
# Description: Ensure invalid roles raise a DataValidationError.
# ===========================

def test_invalid_role_assignment():
    """Test assigning an invalid role"""
    account = Account(role="user")

    # Attempt to assign an invalid role
    with pytest.raises(DataValidationError):
        account.change_role("moderator")  # Invalid role should raise an error


######################################################################
#  T O D O   T E S T S  (To Be Completed by Students)
######################################################################

"""
Each student in the team should implement **one test case** from the list below.
The team should coordinate to **avoid duplicate work**.

Each test should include:
- A descriptive **docstring** explaining what is being tested.
- **Assertions** to verify expected behavior.
- A meaningful **commit message** when submitting their PR.
"""

# TODO 1: Test Default Values
# - Ensure that new accounts have the correct default values (e.g., `disabled=False`).
# - Check if an account has no assigned role, it defaults to "user".

# TODO 2: Test Updating Account Email
# - Ensure an account’s email can be successfully updated.
# - Verify that the updated email is stored in the database.

# TODO 3: Test Finding an Account by ID
# - Create an account and retrieve it using its ID.
# - Ensure the retrieved account matches the created one.

# TODO 4: Test Invalid Email Handling
# ===========================
# Test: Invalid Email Handling
# Author: Alan Reisenauer
# Date: 2025-01-31
# Description: Ensure invalid Emails are handled properly
# ===========================
def test_invalid_email_handling():
    """Test invalid email input"""
    #Check that invalid emails (e.g., "not-an-email") raise a validation error.
    account = Account(email="not-an-email")
    with pytest.raises(DataValidationError):
        account.validate_email()
    #Esnure accounts without an email cannot be created
    account = Account(name="John Doe", role="user")

# TODO 5: Test Password Hashing
# - Ensure that passwords are stored as **hashed values**.
# - Verify that plaintext passwords are never stored in the database.

# TODO 6: Test Account Persistence
# - Create an account, commit the session, and restart the session.
# - Ensure the account still exists in the database.

# TODO 7: Test Searching by Name
# - Ensure accounts can be searched by their **name**.
# - Verify that partial name searches return relevant accounts.

# TODO 8: Test Bulk Insertion
# - Create and insert multiple accounts at once.
# - Verify that all accounts are successfully stored in the database.

# TODO 9: Test Phone Number Validation
# - Ensure only valid phone numbers can be stored.
# - Check that phone numbers must be a valid format (e.g., `123-456-7890`).

# TODO 10: Test Searching by Filters
# - Implement a search function that filters accounts by attributes (e.g., `email`, `role`).
# - Ensure it correctly returns accounts that match the search criteria.

# TODO 11: Test Role-Based Access
# - Ensure users with different roles ('admin', 'user', 'guest') have appropriate permissions.
# - Verify that role changes are correctly reflected in the database.
# ===========================
# Test: Test role assignment (Student 9)
# Author: Harrison Atherton
# Date: 2025-01-31
# Description: Ensure roles can be assigned and checked.
# ===========================
def test_account_role_assignment():
    """Test assigning roles to an account"""
    account = Account(name="John Doe", email="johndoe@example.com", role="user")
    db.session.add(account)
    db.session.commit()

    # Retrieve from database
    retrieved_account = Account.query.filter_by(email="johndoe@example.com").first()
    assert retrieved_account.role == "user"

    # Change role and verify
    retrieved_account.change_role("admin")
    db.session.commit()

    updated_account = Account.query.filter_by(email="johndoe@example.com").first()
    assert updated_account.role == "admin"