from sage.all import *
from pwn import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from hashlib import sha256
import json

context.log_level = "info" # switch to "debug" for verbose output

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        exit()
    
io = start()

# Obtaining the values from the server
io.recvuntil("[ ALICE ] :")
alice_json = json.loads(io.recvlineS().strip())
p, a, b, Gx, Gy, Ax, Ay = dict(alice_json).values()

io.recvuntil("[  BOB  ] :")
bob_json = json.loads(io.recvlineS().strip())
Bx, By = dict(bob_json).values()

io.recvuntil("[ ALICE ] :")
enc_json = json.loads(io.recvlineS().strip())
iv, enc = bytes.fromhex(enc_json["iv"]), bytes.fromhex(enc_json["encrypted"])

info(f"Alice : {(Ax, Ay)}")
info(f"Bob   : {(Bx, By)}")
info(f"IV    : {iv.hex()}")
info(f"MSG   : {enc.hex()}")

# Actually solving
def movAttack(G, Q, p, a, b):
    # finding the embdedding degree
    k = 1
    while (p**k - 1) % E.order():
        k += 1

    Ee = EllipticCurve(GF(p**k, 'y'), [a, b])

    Ge = Ee(G)
    Qe = Ee(Q)

    R = Ee.random_point()
    m = R.order()
    d = gcd(m, G.order())
    B = (m // d) * R

    assert G.order() / B.order() in ZZ
    assert G.order() == B.order()

    n = G.order()
    alpha = Ge.weil_pairing(B, n)
    beta = Qe.weil_pairing(B, n)

    loading = log.progress('Computing log...')
    nQ = beta.log(alpha)
    loading.success(f"Scalar: {nQ}")
    return nQ

# see `source.py`
def decrypt(secret: int, ciphertext: bytes):
    hash = sha256(str(secret).encode()).digest()
    iv, key = hash[:16], hash[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(ciphertext)
    return decrypted

E = EllipticCurve(GF(p), [a, b])
G = E(Gx, Gy)
A = E(Ax, Ay)
B = E(Bx, By)

alice_secret = movAttack(G, A, p, a, b)
shared_secret = B * alice_secret
info(f"shared: {shared_secret[0]} {shared_secret[1]}")
flag = unpad(decrypt(shared_secret[0], enc), 16)
success(f"{flag.decode()}")
