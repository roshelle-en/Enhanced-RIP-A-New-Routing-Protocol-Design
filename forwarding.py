import time
import hmac
import hashlib

# ------------------ Packet Structure ------------------ #
class Packet:
    def __init__(self, src, dest, data, failed_links=None, hmac_value=None):
        self.src = src
        self.dest = dest
        self.data = data
        self.failed_links = failed_links if failed_links else []
        self.hmac_value = hmac_value


# ------------------ HMAC Utility ------------------ #
def generate_hmac(key, message):
    return hmac.new(key, message.encode(), hashlib.sha1).hexdigest()


def verify_hmac(key, message, hmac_value):
    expected = generate_hmac(key, message)
    return hmac.compare_digest(expected, hmac_value)


# ------------------ Forwarding Logic ------------------ #
def forward_packet(packet, current_node, routing_table, secret_key, verbose=False):
    """
    Forward a packet based on primary/secondary next hops.
    Adds failure data to the packet header and validates HMAC.

    Args:
        packet (Packet): The packet to forward
        current_node (str): The router handling the packet
        routing_table (dict): Routing table for this node
        secret_key (bytes): Shared HMAC key
        verbose (bool): Print debug info

    Returns:
        next_hop (str or None): Next router or None if dropped
    """
    # Verify HMAC
    if not verify_hmac(secret_key, packet.data, packet.hmac_value):
        if verbose:
            print(f"[SECURITY] Packet dropped at {current_node}: HMAC verification failed.")
        return None

    # If destination is current node -> deliver
    if current_node == packet.dest:
        if verbose:
            print(f"[DELIVERED] Packet reached {packet.dest} with data: {packet.data}")
        return None

    if packet.dest not in routing_table[current_node]:
        if verbose:
            print(f"[DROP] No route from {current_node} to {packet.dest}")
        return None

    entry = routing_table[current_node][packet.dest]

    # Try primary route first
    if entry["primary"]:
        primary_cost, primary_next = entry["primary"]
        if (current_node, primary_next) not in packet.failed_links:
            if verbose:
                print(f"[FORWARD] {current_node} -> {primary_next} (primary)")
            return primary_next

    # Try secondary routes
    for sec in entry["secondary"]:
        sec_cost, sec_next = sec
        if (current_node, sec_next) not in packet.failed_links:
            if verbose:
                print(f"[FORWARD] {current_node} -> {sec_next} (secondary)")
            return sec_next

    # If all fail -> drop
    if verbose:
        print(f"[DROP] No available path from {current_node} to {packet.dest}")
    return None


# ------------------ Failure Handling ------------------ #
def mark_link_failure(packet, u, v):
    """
    Mark a failed link in the packet header so downstream routers avoid it.
    """
    packet.failed_links.append((u, v))


# ------------------ Example Run ------------------ #
if __name__ == "__main__":
    # Example secret key
    SECRET_KEY = b"shared_secret_key"

    # Example routing table (simplified)
    routing_table = {
        "A": {"B": {"primary": (1, "B"), "secondary": []}},
        "B": {"C": {"primary": (1, "C"), "secondary": []}},
        "C": {}
    }

    # Create packet
    data = "Hello World"
    hmac_value = generate_hmac(SECRET_KEY, data)
    packet = Packet("A", "C", data, hmac_value=hmac_value)

    # Forward through network
    current = "A"
    while current:
        next_hop = forward_packet(packet, current, routing_table, SECRET_KEY, verbose=True)
        if not next_hop:
            break
        current = next_hop
