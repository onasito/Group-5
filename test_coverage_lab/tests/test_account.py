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

def test_account_role_assignment():
    """Test assigning roles to an account"""
    account = Account(name="John Doe", email="johndoe@example.com", role="user")

    # Assign initial role
    assert account.role == "user"

    # Change role and verify
    account.change_role("admin")
    assert account.role == "admin"

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

# TODO 1: Test Account Serialization
# - Ensure `to_dict()` correctly converts an account to a dictionary format.
# - Verify that all expected fields are included in the dictionary.

# TODO 2: Test Invalid Email Input
# - Check that invalid emails (e.g., "not-an-email") raise a validation error.
# - Ensure accounts without an email cannot be created.

# TODO 3: Test Missing Required Fields
# - Ensure that creating an `Account()` without required fields raises an error.
# - Validate that missing fields trigger the correct exception.

# ===========================
# Test: Test Missing Required Fields
# Author: Riley Ramos
# Date: 2025-02-04
# Description: Ensure accounts missing required fields raise exceptions.
# ===========================
def test_missing_required_fields():
    """Test creating an account that's missing required fields"""
    # Attempt to create an account with missing name
    account = Account(name=None, email="ramos@example.com")
    
    # Account with missing name should raise an exception
    with pytest.raises(Exception) as exception:
        db.session.add(account)
        db.session.commit() 
    
    # Verify correct 'null name' exception was raised
    db.session.rollback()
    exception_str = str(exception) 
    assert "NOT NULL constraint failed: account.name" in exception_str 
    
    # Attempt to create an account with missing email
    account = Account(name="Riley", email=None)
    
    # Account with missing email should raise an error
    with pytest.raises(Exception) as exception:
        
        db.session.commit() 
    
    # Verify correct 'null email' exception was raised
    db.session.rollback()
    exception_str = str(exception) 
    assert "NOT NULL constraint failed: account.email" in exception_str 

def test_invalid_email_handling():
    """Test invalid email input"""
    #Check that invalid emails (e.g., "not-an-email") raise a validation error.
    account = Account(email="not-an-email")
    with pytest.raises(DataValidationError):
        account.validate_email()
    #Esnure accounts without an email cannot be created
    account = Account(name="John Doe", role="user")

# TODO 3: Test Missing Required Fields
# - Ensure that creating an `Account()` without required fields raises an error.
# - Validate that missing fields trigger the correct exception.


# TODO 4: Test Positive Deposit
# - Ensure `deposit()` correctly increases the account balance.
# - Verify that depositing a positive amount updates the balance correctly.
# ===========================
# Test: Test Positive Deposit
# Author: Stella Heo
# Date: 2025-02-05
# Description: Ensure `deposit()` correctly increases the account balance.
#              Verify that depositing a positive amount updates the balance correctly.
# ===========================
def test_positive_deposit():
    # Test the deposit amount correctly increases the balance
    # Create a test user
    account = Account(name="User Test", email="test@gmail.com", balance=0)
    # Deposit a positive amount ($100)
    account.deposit(100)

    # Test that depositing a positive amount updates the balance correctly
    assert account.balance == 100
        

# TODO 5: Test Deposit with Zero/Negative Values
# - Ensure `deposit()` raises an error for zero or negative amounts.
# - Verify that balance remains unchanged after an invalid deposit attempt.

# TODO 6: Test Valid Withdrawal
# - Ensure `withdraw()` correctly decreases the account balance.
# - Verify that withdrawals within available balance succeed.

# ===========================
# Test: Test Valid Withdrawl
# Author: Joel Mendoza
# Date: 2025-02-06
# Description: Validate withdraw function alters balance and doesn't over withdraw
# ===========================
def test_valid_withdraw():
    """Test successful withdrawal that decreases the account balance"""
    account = Account(name="Test", email="test@example.com", balance=100.0)
    db.session.add(account)
    db.session.commit()

    # Withdraw a VALID amount
    account.withdraw(50.0)

    # Check if the balance was updated directly after withdrawal
    assert account.balance == 50.0, f"Expected balance to be 50.0, but got {account.balance}"

def test_withdraw_insufficient_balance():
    """Test withdrawal that exceeds available balance raises DataValidationError"""
    # Create a new account with an initial balance
    account = Account(name="Test", email="test@example.com", balance=10.0)
    db.session.add(account)
    db.session.commit()

    # Try to over-withdraw
    with pytest.raises(DataValidationError):
        account.withdraw(100.0)

# TODO 7: Test Withdrawal with Insufficient Funds
# - Ensure `withdraw()` raises an error when attempting to withdraw more than available balance.
# - Verify that the balance remains unchanged after a failed withdrawal.

# TODO 8: Test Password Hashing
# - Ensure that passwords are stored as **hashed values**.
# - Verify that plaintext passwords are never stored in the database.
# - Test password verification with `set_password()` and `check_password()`.

# TODO 9: Test Role Assignment
# - Ensure that `change_role()` correctly updates an account’s role.
# - Verify that the updated role is stored in the database.

# TODO 10: Test Invalid Role Assignment
# - Ensure that assigning an invalid role raises an appropriate error.
# - Verify that only allowed roles (`admin`, `user`, etc.) can be set.

# TODO 11: Test Deleting an Account
# - Ensure that `delete()` removes an account from the database.
# - Verify that attempting to retrieve a deleted account returns `None` or raises an error.


# TODO 5: Test Deposit with Zero/Negative Values
# ===========================
# Test: Zero/Negative Values for Deposit
# Author: Austin Kim
# Date: 2025-02-03
# Description: Ensure `deposit()` raises an error for zero or negative amounts.
#              Verify that balance remains unchanged after an invalid deposit attempt.
# ===========================
def test_zero_or_negative_deposits(): 
    account = Account(name="Test User", email="test@gmail.com", balance = 100.0)
    acct_init_balance = account.balance 
  
    # Test w/ deposit amount 0 & validate the account balance hasn't changed 
    with pytest.raises(DataValidationError):
        account.deposit(0)
    assert account.balance == acct_init_balance

    # Test w/ negative deposit amount & validate the account balance hasn't changed 
    with pytest.raises(DataValidationError): 
        account.deposit(-10)
    assert account.balance == acct_init_balance


# TODO 7: Test Withdrawal with Insufficient Funds
# - Ensure `withdraw()` raises an error when attempting to withdraw more than available balance.
# - Verify that the balance remains unchanged after a failed withdrawal.

# TODO 8: Test Password Hashing
# - Ensure that passwords are stored as **hashed values**.
# - Verify that plaintext passwords are never stored in the database.
# - Test password verification with `set_password()` and `check_password()`.

# TODO 9: Test Role Assignment
# - Ensure that `change_role()` correctly updates an account’s role.
# - Verify that the updated role is stored in the database.

# TODO 10: Test Invalid Role Assignment
# - Ensure that assigning an invalid role raises an appropriate error.
# - Verify that only allowed roles (`admin`, `user`, etc.) can be set.


# TODO 11: Test Deleting an Account
# - Ensure that `delete()` removes an account from the database.
# - Verify that attempting to retrieve a deleted account returns `None` or raises an error.
