### Creating a migration
alembic --config dlc_oracle_bot/database/alembic.ini revision --autogenerate -m "Initial tables"


### Migrating
alembic --config dlc_oracle_bot/database/alembic.ini upgrade head