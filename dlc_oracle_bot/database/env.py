import os
import sys

file_path = os.path.realpath(__file__)
src_path = os.path.dirname(os.path.dirname(os.path.dirname(file_path)))
sys.path.append(src_path)
print(src_path)

from dlc_oracle_bot.database.migrations import run_migrations

run_migrations()
