#!/bin/bash
docker rm -f crypto_schmoving
docker build --tag=crypto_schmoving challenge
docker run -p 1337:1337 --rm --name=crypto_schmoving crypto_schmoving