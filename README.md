# Election Integrity
Collaborative Project on Election Integrity

## Authors:
Taylor Santos, John Nemeth

## Details
This project is a webserver (setup for heroku deployment) which demonstrates
a small-scale election encryption scheme which allows for voters to transmit
their encrypted votes to different vote counters as well as verify the voting results.

## How it works
The operation of the project can be described as showcasing a voting encryption scheme 
which uses homomorphic secret sharing and features vote verification using Lagrange polynomials.
Each vote is encoded as a constant term in a polynomial with the coefficients of the remaining terms
acting as user-defined keys. Those user-defined coefficients help facilitate the creation of separate
encrypted values which are transmitted to the respective vote counters.

### Voting
Each encrypted value represents their polynomial equation 
using terms equal to the number of vote counters where each term is (vote counter number
*chosen coefficients^votecounterindex). After each calculated term is summed (also adding a constant value
representing their vote), a voter-wide prime modulus chosen at the beginning of the vote 
is used to obtain the encrypted value to be sent to the vote counters. 

### Voting results
tbd

## Creating a vote
Defining elections and their options must be done through the administration page. 
The password is temporarily defined in the main flask server file.

## Sources/References
It uses pip3, python3, Flask, PostgreSQL (also setup/hosted on heroku) and associated 
dependencies as well as math and cryptography libraries.
