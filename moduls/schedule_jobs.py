import schedule
import time
from dbConnections import sql_db_connection


def filter_rooms_by_check_in():
    """
    exec a sored procedure that filter the room table in db
    and change the status for all room that their check in date is over
    """
    sp_name = "dbo.FilterRoomsCheckIn"
    print("Filtering rooms by check_in")
    return sql_db_connection.exec_stored_procedures(sp_name, ())


schedule.every().day.at("00:00").do(filter_rooms_by_check_in)

while True:
    # Checks whether a scheduled task
    # is pending to run or not
    schedule.run_pending()
    time.sleep(1)
