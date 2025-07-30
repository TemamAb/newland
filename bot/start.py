from zkproof import verify_proof
import requests
session = requests.session()
session.proxies = {'http': 'socks5h://localhost:9050'}
if not verify_proof(user_proof):
    exit('Invalid ZK Proof')
