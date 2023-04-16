# schMOVing-challenge

For an Abstract Algebra class, I chose to do a small presentation on Elliptic Curves, and wanted to talk about the MOV Attack since I never understood it as well as I wanted to after [Cyber Apocalypse CTF 2022](https://www.hackthebox.com/blog/movs-like-jagger-ca-ctf-2022-crypto-writeup). The challenge here reuses the same parameters for the elliptic curve, but I just rewrote it as an elliptic curve Diffie-Hellman thing.

## Solving the Challenge
**Prereqs:** SageMath, pwntools (Docker optional)

If you have Docker installed, you can use the [cryptohack](https://github.com/cryptohack/cryptohack-docker) Docker container to have all the tools already installed and ready to go. Just run the below command from inside the repository:

```shell
docker run -p 127.0.0.1:8888:8888 -it -v "$PWD:/data" hyperreality/cryptohack:latest
```

This will spawn a Jupyter instance at `127.0.0.1:8888`, where you can copy and paste the solve script. Otherwise, you can get an interactive shell on the Docker container, with the solve script stored on `/data`.

## References
- [cryptohack/ctf_archive](https://github.com/cryptohack/ctf_archive) for the Dockerfiles because I'm too lazy to make my own
- [wizardalfredo (HackTheBox)](https://www.hackthebox.com/blog/movs-like-jagger-ca-ctf-2022-crypto-writeup) for their writeup (again, too lazy to write it the solution myself from scratch)