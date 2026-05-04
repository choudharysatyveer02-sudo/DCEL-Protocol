import socket
import json
import hashlib

class DCEL_Agent:
    def __init__(self, name):
        self.name = name
        # Generates the 8-character ID for payment tracking
        self.sig = hashlib.sha256(name.encode()).hexdigest()[:8]

    def connect_to_network(self, mission="HANDSHAKE"):
        packet = {
            "header": {"sig": self.sig, "v": "1.0-GENESIS"},
            "payload": {"agent": self.name, "action": mission}
        }
        
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Use 'localhost' for Wednesday test. 
            client.connect(('localhost', 9999))
            client.send(json.dumps(packet).encode('utf-8'))
            
            response = json.loads(client.recv(1024).decode('utf-8'))
            
            print("\n" + "="*45)
            if response["auth"]:
               print(f"🚀 SUCCESS: {response['msg']}")
            else:
             print(f"⛔ ACCESS DENIED: {response['msg']}")  
            print("="*45 + "\n")
            client.close()
        except ConnectionRefusedError:
            print("\n🛑 OFFLINE: DCEL Network unreachable. Ensure Gateway is active.")

if __name__ == "__main__":
    print("=== DCEL AGENT TERMINAL v1.0 ===")
    agent_name = input("Enter Agent Name: ")
    user = DCEL_Agent(agent_name)
    print(f"Your Unique Agent Signature: {user.sig}")
    print("--------------------------------------------------")
    print(f"Instructions: Send ₹500 to DCEL UPI with the note: {user.sig}")
    print("--------------------------------------------------")
    user.connect_to_network()
