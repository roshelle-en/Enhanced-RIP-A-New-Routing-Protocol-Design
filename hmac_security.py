import hmac
import hashlib


# ------------------ HMAC Functions ------------------ #
def generate_hmac(key: bytes, message: str) -> str:
    """
    Generate an HMAC-SHA1 for a given message.

    Args:
        key (bytes): Shared secret key
        message (str): Message to authenticate

    Returns:
        str: Hexadecimal HMAC digest
    """
    return hmac.new(key, message.encode(), hashlib.sha1).hexdigest()


def verify_hmac(key: bytes, message: str, hmac_value: str) -> bool:
    """
    Verify an HMAC-SHA1 for a given message.

    Args:
        key (bytes): Shared secret key
        message (str): Original message
        hmac_value (str): Received HMAC to verify

    Returns:
        bool: True if valid, False otherwise
    """
    expected = generate_hmac(key, message)
    return hmac.compare_digest(expected, hmac_value)


# ------------------ Example Usage ------------------ #
if __name__ == "__main__":
    SECRET_KEY = b"shared_secret_key"
    msg = "Test packet"

    # Generate HMAC
    hmac_val = generate_hmac(SECRET_KEY, msg)
    print(f"Generated HMAC: {hmac_val}")

    # Verify (valid case)
    print("Verification (valid):", verify_hmac(SECRET_KEY, msg, hmac_val))

    # Verify (tampered case)
    print("Verification (invalid):", verify_hmac(SECRET_KEY, msg, "deadbeef"))
