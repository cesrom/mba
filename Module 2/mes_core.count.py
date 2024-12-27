'''
This script is for handling count events from ignition tags. Events are summed and stored in the mes_core database.
'''

def storeCountHistory(currentCount, lastCount, tagID, countTypeID, db='mes_core'):
    '''
    This function takes four arguments from the tag event--the currentCount, lastCount, tagID, and countTypeID.
    When called from the tag event, this function will calculate the count delta and then insert a new count
    history record with the delta, count type, tagID, and timestamp. We return the currentValue to the tag event
    so the value can be written to the last count tag to be used by the next count delta calculation.
    
    Parameters:
        currentCount (int): The current count value.
        lastCount (int): The last count value.
        tagID (int): The ID of the tag associated with the count.
        countTypeID (int): The ID representing the type of count.
        db (str): The database name to use for the query. Defaults to 'mes_core'.

    Returns:
        int: The currentCount if the delta is >= 1; otherwise, -1.
    '''
    import system
    from datetime import datetime
    import time

    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    countDelta = currentCount - lastCount

    if abs(countDelta) >= 1:
        query = 'INSERT INTO counthistory (TagID, CountTypeID, Count, TimeStamp) VALUES (?, ?, ?, ?)'
        system.db.runSFPrepUpdate(query, [tagID, countTypeID, countDelta, stamp], [db])
        return currentCount
    else:
        return -1
