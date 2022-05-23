# coffeeculator
Okay, okay yes I know what you're thinking; alembic
and sqlalchemy is overkill for a toy like this, but
I wanted to be fancy

## current setup
If you wanna run this

1. create a venv
1. pip install the crap
1. `make local` which creates your db
1. `make run-alembic` will create the crap in the db

then a good ole `make brew` will kick off the coffeeculator!

## other miscellany
I added a way to back up the dockerized postgres backend so
that you don't lose your brew deets if the container dies.

`make db-dump` throws a dump of the db into
`/dump/{year-month-day}/{hour-minute}/` and then you can
restore from that dump by running
`make db-restore /dump/{year-month-day}/{hour-minute}/`
