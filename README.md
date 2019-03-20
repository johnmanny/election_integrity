# Election Integrity

This project is a webserver (setup for heroku deployment) which demonstrates
a small-scale election encryption scheme which allows for voters to transmit
their encrypted votes to different vote counters as well as verify the voting results.

## Authors:
Taylor Santos, John Nemeth

## How it works
The operation of the project can be described as showcasing a voting encryption scheme 
which uses homomorphic secret sharing and features vote verification using Lagrange polynomial interpolation.
Each vote is encoded as a constant term in a polynomial with the coefficients of the remaining terms
acting as user-defined keys. Those user-defined coefficients help facilitate the creation of separate
encrypted values which are transmitted to the respective vote counters.

### Voting
A polynomial with a degree equal to the number of vote counters minus one is then used with 
the voter-defined coefficients to calculate each specific vote counters value. An
election-wide prime modulus is then used with this value before sending it off to its 
respective vote counter. 

### Voting results
To tally up votes, each vote counter's sum of encrypted values are used as points for
an Interpolating Lagrange Polynomial in order to find the constant term. Once it's found,
and after the prime modulus is used with this constant term, 
the number of maximum voters allowed (defined at the beginning of the election) is used to
find the vote tally for each election option when expressing the resulting value as a linear 
combination of the maximum voter count.

## Creating a vote
Defining elections and their options must be done through the administration page. 
The password is temporarily defined in the main flask server file.

## Sources/References
It uses pip3, python3, Flask, PostgreSQL (also setup/hosted on heroku) and associated 
dependencies as well as math and cryptography libraries.
