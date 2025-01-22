# 4.0 Solutions LLC CONFIDENTIAL
#
# ___________________________
#
# [2015] – [2025] 4.0 Solutions LLC
# ALL Rights Reserved.
#
# NOTICE: All information contained herein is, and remains
# the property of 4.0 Solutions LLC and its suppliers,
# if any. The intellectual and technical concepts contained
# herein are proprietary to 4.0 Solutions LLC
# and its suppliers and may be covered by U.S. and Foreign Patents,
# patents in process, and are protected by trade secret or copyright law.
# 
# THIS MATERIAL IS AVAILABLE TO ALL STUDENTS WHO PURCHASED A LICENSE
# TO THE MES BOOTCAMP TRAINING PROGRAM ON IIoT UNIVERSITY BY 4.0 SOLUTIONS.
# LICENSED USERS ARE GRANTED PERMISSION TO USE, MODIFY, AND DISTRIBUTE THIS 
# CODE WITHIN THEIR ORGANIZATION OR FOR THEIR CUSTOMERS AS PART OF MES 
# SOLUTIONS. USERS MAY MODIFY THE CODE WITHOUT PRIOR APPROVAL, BUT ALL USE 
# IS SUBJECT TO THE TERMS OF THE LICENSE AGREEMENT. THIS INCLUDES USAGE FOR 
# INTERNAL PROJECTS OR CUSTOMER-DELIVERABLES PROVIDED THROUGH THE LICENSED USER.

"""
Description:
This module provides functionality for managing state history within the MES Core database.
It includes functions to handle updates and insertions into the `statehistory` table based
on changes in state reasons and associated line identifiers.

Functions:
    - storeStateHistory: Updates the end time for the previous state history entry and 
      inserts a new entry for the current state based on the provided reasonCode and lineID.

"""

#default database name
db = 'mes_core'

def storeStateHistory(reasonCode, lineID, db=db):
    '''
    This function takes two arguments from the tag event -- the reasonCode and the lineID. 
    When called from the tag event, this function will fill in the end time of the previous 
    state history entry and create a new entry for the current state.

    Parameters:
        reasonCode (int): The code for the reason of the state change.
        lineID (int): The ID of the line associated with the state change.
        db (str): The database name to use for the query. Defaults to 'mes_core'.

    Returns:
        None
    '''
    import system
    from datetime import datetime
    import time

    try:
    
        # Current timestamp
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Retrieve reasonID and reasonName based on reasonCode and lineID
        data = system.db.runPrepQuery(
            'SELECT ID, ReasonName FROM statereason WHERE ReasonCode = ? AND ParentID = ?',
            [reasonCode, lineID],
            db
        )

        if len(data) > 0:
            reasonID, reasonName = data[0][0], data[0][1]
        else:
            system.util.getLogger("storeStateHistory").warn("No matching reason found for reasonCode: {}, lineID: {}".format(reasonCode, lineID))
            return

        # Update the end time of the previous state history entry
        endQuery = 'UPDATE statehistory SET EndDateTime = ? WHERE LineID = ? AND EndDateTime IS NULL'
        system.db.runSFPrepUpdate(endQuery, [stamp, lineID], [db])

        # Wait briefly before inserting the new state (simulate realistic processing delay)
        time.sleep(2)

        # Insert a new state history entry
        query = ('INSERT INTO statehistory (StateReasonID, ReasonName, LineID, ReasonCode, StartDateTime) '
                'VALUES (?, ?, ?, ?, ?)')
        system.db.runSFPrepUpdate(query, [reasonID, reasonName, lineID, reasonCode, stamp], [db])

        # info logging for debugging
        system.util.getLogger("storeStateHistory").info("New state stored successfully for reasonCode: {}, lineID: {}".format(reasonCode, lineID))

    except Exception as e:
        system.util.getLogger("storeStateHistory").error("Error storing state history: {}".format(str(e)))
