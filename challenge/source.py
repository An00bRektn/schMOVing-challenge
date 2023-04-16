from ecdsa import ellipticcurve as ecc
from flag import FLAG
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from hashlib import sha256
import time
import json
import random

a = -35
b = 98
p = 434252269029337012720086440207
Gx = 16378704336066569231287640165
Gy = 377857010369614774097663166640
ec_order = 434252269029337012720086440208

E = ecc.CurveFp(p, a, b)
G = ecc.Point(E, Gx, Gy, ec_order)

# credit to HackTheBox for this and the parameters
def intercepting():
    log_msgs = \
        """
[\033[92mOK\033[0m] Locating targets...      
[\033[92mOK\033[0m] Calibrating listening frequency...
[\033[92mOK\033[0m] Correcting interference...
[\033[92mOK\033[0m] Identifying parties...
[\033[92mOK\033[0m] Streams absorbed

Eavesdropping activated ...
    """.split('\n')
    for m in log_msgs:
        print(m)
        time.sleep(random.random())

def exchange():
    alice_secret, bob_secret = random.randint(1,pow(2,64)), random.randint(1,pow(2,64))
    aG = G * alice_secret
    alice_msg = json.dumps({"p": p, "a": a, "b": b, "Gx": Gx, "Gy": Gy, "Ax": int(aG.x()), "Ay": int(aG.y())})
    time.sleep(random.random())
    print(f"[ ALICE ] : {alice_msg}")

    bG = G * bob_secret
    bob_msg = json.dumps({"Bx": int(bG.x()), "By": int(bG.y())})
    time.sleep(random.random())
    print(f"[  BOB  ] : {bob_msg}")

    shared_secret = aG * bob_secret
    return shared_secret

def encrypt(shared_secret: int):
    hash = sha256(str(shared_secret).encode()).digest()
    iv, key = hash[:16], hash[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(FLAG, 16))
    return json.dumps({"iv": iv.hex(), "encrypted": encrypted.hex()})


if __name__ == "__main__":
    intercepting()
    s = exchange()
    #print(f"[ DEBUG ] : {s}")
    final_msg = encrypt(int(s.x()))

    time.sleep(random.random())
    print(f"[ ALICE ] : {final_msg}")
    print(f"[\033[93m??\033[0m] Signal Lost")
    input()
    print("[\033[91m!!\033[0m] Channel collapsing...")
    time.sleep(random.random())
    print("[\033[91m!!\033[0m] Targets not found...")
    time.sleep(random.random())
    print("[\033[91m!!\033[0m] Exiting...")
    exit()