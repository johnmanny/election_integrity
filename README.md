# Election Integrity Webpage
Collaborative Project on Election Integrity Topics

## Authors:
Taylor Santos, John Nemeth

## Details
This project is a webserver (setup for heroku deployment) which demonstrates
a small-scale election and allows for voters to securely transmit their vote 
to different vote counters as well as verify the voting results.

It uses pip3, python3, Flask, PostgreSQL (also setup/hosted on heroku) and associated 
dependencies as well as math and cryptography libraries.

## How it works
The operation of the project can be described as showcasing a voting encryption scheme 
which uses homomorphic secret sharing and features vote verification using Lagrange polynomials.
Each vote is encoded as a constant term in a polynomial with the coefficients of the remaining terms
acting as user-defined keys. Those user-defined coefficients allow the voter to send separate encrypted
values to the respective vote counters.

Here's the math explanation:

Each encrypted value represents their polynomial equation 
using terms equal to the number of vote counters where each term is (vote counter number
*chosen coefficients^votecounterindex). After each calculated term is summed (also adding a constant value
representing their vote), a voter-wide prime modulus chosen at the beginning of the vote 
is used to obtain the encrypted value to be sent to the vote counters. 

## Creating a vote
Defining elections and their options must be done through the administration page. 
The password is temporarily defined in the main flask server file.
