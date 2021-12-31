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

## Running this for your tournament
The unit tests serve as the main driver that creates artifacts needed for a schedule. Add a test like this for your custom input:

```
def test_final_schedule_2022(self):
    mock_schedule = Schedule(range(7,15), range(1,7), 72, 40, 5, datetime.strptime("1/8/2022 10:00", '%m/%d/%Y %H:%M'), timedelta(minutes=25), datetime.strptime("1/8/2022 14:10", '%m/%d/%Y %H:%M'), datetime.strptime("1/8/2022 15:30", '%m/%d/%Y %H:%M'))
    result = mock_schedule.generate()
    self.assert_no_dup_teams_in_round(result)
    mock_schedule.writeToCsv()
    mock_schedule.writeToDBSchema()
```

The results can be found in the ```/output``` directory.
