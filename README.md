# Tournament Schedule Maker

This is a tool to help make a tournament schedule maker for any type of competition. It will create matchups that use a round-robin type of scheduling, which is considered the standard for such tournaments. We make the following assumptions:
* there are an even number of teams
* the number of games per team < the number of total teams
* the number of courts <= # of teams/2

Under these conditions, you can expect an evenly distributed set of games that fit on the number of courts you provide, ensuring every team only plays another once and never twice in the same round. The output can be stored in a CSV file, it can generate a master sheet of all games and a sheet for each team. It can also be stored in a database, such as a MySQL table.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Python 3.X

## Running the tests

We care a great deal about accuracy, so we wrote unit tests.

```
python run_test.py
```
