# Tournament Schedule Maker

This is a tool to help make a tournament schedule for any type of competition. It will create matchups that use a round-robin type of scheduling, which is considered the standard for such tournaments. We make the following assumptions:
* there are an even number of teams
* the number of games per team < the number of total teams
* the number of courts <= # of teams/2

Under these conditions, you can expect an evenly distributed set of games that fit on the number of courts you provide, ensuring every team only plays another once and never twice in the same round. The output can be stored in a CSV file, it can generate a master sheet of all games and a sheet for each team. It can also be stored in a database, such as a MySQL table.

## Getting Started

### Prerequisites

python 3.x

## Running the tests

We care a great deal about accuracy, so we wrote unit tests.

```
python run_test.py
```
