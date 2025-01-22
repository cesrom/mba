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
This module provides functionality to calculate the estimated finish time for a run
based on the production rate, remaining parts, and other parameters defined in the MES system.

Functions:
    - calcFinishTime: Calculates the estimated finish time for a production run.
"""

#default database name
db = 'mes_core'

from datetime import datetime, timedelta

def calcFinishTime(parentPath, db=db):
    """
    Calculates the estimated finish time for a production run based on the provided 
    parent path and database.

    Parameters:
        parentPath (str): The path to the parent tag in the MES system.
        db (str): The database name to use for the query. Defaults to 'mes_core'.

    Returns:
        str: The estimated finish time in ISO format, or 'No Order' if no active run is found.
    """
    import system

    # SQL query to retrieve run and schedule information
    query = """
        SELECT r.ID AS 'ID', wo.WorkOrder AS 'WorkOrder', r.RunStartDateTime AS 'StartTime',
               sch.ScheduleFinishDateTime AS 'FinishTime', sch.Quantity AS 'Quantity'
        FROM run r
        LEFT JOIN schedule sch ON r.ScheduleID = sch.ID
        LEFT JOIN workorder wo ON sch.WorkOrderID = wo.ID
        WHERE r.ID = ? AND wo.Closed = 0
    """

    # Retrieve run ID from the tag path
    runID = system.tag.readBlocking(["{}/OEE/RunID".format(parentPath)])[0].value

    if runID != -1:
        # Query the database for run data
        runData = system.db.runPrepQuery(query, [runID], db)

        for row in runData:
            quantity = row['Quantity']

            # Retrieve tag values for good parts and production rate
            goodParts = system.tag.readBlocking(["{}/OEE/Good Count".format(parentPath)])[0].value
            remainingParts = quantity - goodParts
            productionRate = system.tag.readBlocking(["{}/OEE/Production Rate".format(parentPath)])[0].value

            # Calculate remaining hours to complete the production
            if productionRate > 0:
                hoursRemaining = remainingParts / productionRate
            else:
                productionRate = 1
                hoursRemaining = remainingParts / productionRate

            # Calculate the estimated finish time
            currentTime = datetime.now().replace(microsecond=0)
            finishTime = currentTime + timedelta(hours=hoursRemaining)
            return finishTime.isoformat()
    else:
        return 'No Order'

def updateRun(runID, db=db):
    '''
    Updates run information based on the given runID. It calculates and updates various run metrics
    such as infeed, outfeed, waste, OEE, availability, performance, and quality.

    Parameters:
        runID (int): The unique identifier of the run.
        db (str): The database name to use for the query. Defaults to 'mes_core'.

    Returns:
        int: Returns 1 if the update was successful, or 0 if there was an error.
    '''
    from datetime import datetime, timedelta
    from java.lang import Exception
    from shared.mes_core.logging import log

    try:
        # log(f"Starting updateRun process for RunID: {runID}", "info")  # Use for debugging

        # Build a query to retrieve LineID and LinePath
        lineQuery = """
            SELECT l.ID as 'Line ID', 
                   CONCAT('[mes_core]', e.NAME, '/', s.NAME, '/', a.NAME, '/', l.NAME, '/Line') as 'Line Path'
            FROM run r
            LEFT JOIN schedule sch ON r.ScheduleID = sch.ID
            LEFT JOIN workorder wo ON sch.WorkOrderID = wo.ID
            LEFT JOIN line l ON sch.LineID = l.ID
            LEFT JOIN area a ON l.ParentID = a.ID
            LEFT JOIN site s ON a.ParentID = s.ID
            LEFT JOIN enterprise e ON s.ParentID = e.ID
            WHERE r.ID = ?
        """
        data = system.db.runPrepQuery(lineQuery, [runID], db)

        if not data:
            log("No data found for RunID: {}".format(runID), "warn")
            return 0

        for row in data:
            lineID = row['Line ID']
            linePath = row['Line Path']

        # log("LineID: {}, LinePath: {}".format(lineID, linePath), "info")  # Use for debugging

        # Calculate Finish Time
        finishTime = calcFinishTime(linePath)
        # log("Calculated FinishTime: {}".format(finishTime), "info")  # Use for debugging

        # Get current Timestamp and format
        timeStamp = datetime.now()
        timeStamp = timeStamp.replace(microsecond=0)

        # List of tag paths
        tagPaths = [
            linePath + '/Dispatch/OEE Infeed/Count',
            linePath + '/Dispatch/OEE Outfeed/Count',
            linePath + '/Dispatch/OEE Waste/Count',
            linePath + '/OEE/Total Count',
            linePath + '/OEE/Bad Count',
            linePath + '/OEE/Good Count',
            linePath + '/OEE/Quality',
            linePath + '/OEE/Performance',
            linePath + '/OEE/Availability',
            linePath + '/OEE/Run Time',
            linePath + '/OEE/Unplanned Downtime',
            linePath + '/OEE/Planned Downtime',
            linePath + '/OEE/Total Time'
        ]

        # Single call to system.tag.readBlocking
        tagValues = system.tag.readBlocking(tagPaths)

        # Assigning values from the tag read results
        infeed = tagValues[0].value
        outfeed = tagValues[1].value
        waste = tagValues[2].value
        totalCount = tagValues[3].value
        badCount = tagValues[4].value
        goodCount = tagValues[5].value
        quality = tagValues[6].value
        performance = tagValues[7].value
        availability = tagValues[8].value
        runTime = tagValues[9].value
        unplannedDowntime = tagValues[10].value
        plannedDowntime = tagValues[11].value
        totalTime = tagValues[12].value

        # log("All tag values read successfully.", "info")  # Use for debugging

        # Update Run
        query = """
        UPDATE run SET 
            CurrentInfeed = ?, 
            CurrentOutfeed = ?, 
            CurrentWaste = ?, 
            TotalCount = ?, 
            BadCount = ?, 
            GoodCount = ?, 
            Availability = ?, 
            Performance = ?, 
            Quality = ?, 
            OEE = ?, 
            RunTime = ?, 
            UnplannedDowntime = ?, 
            PlannedDowntime = ?, 
            TotalTime = ?, 
            TimeStamp = ?, 
            Closed = ?, 
            EstimatedFinishTime = ?
        WHERE ID = ?
        """
        args = [infeed, outfeed, waste, totalCount, badCount, goodCount, availability,
                performance, quality, (availability * performance * quality), runTime,
                unplannedDowntime, plannedDowntime, totalTime, str(timeStamp), 0, str(finishTime), runID]

        system.db.runPrepUpdate(query, args, db)
        # log("Run {} updated successfully.".format(runID), "info")  # Use for debugging
        return 1

    except Exception as e:
        log("Error updating Run {}: {}".format(runID, str(e)), "error")
        return 0
