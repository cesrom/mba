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

'''
This script handles OEE (Overall Equipment Effectiveness) calculations for the MES core system.
'''

#default database name
db = 'mes_core'

# Import the logging module
from shared.mes_core.logging import log

# Log for debugging purposes (commented for production)
# log('MES Core: Calculating OEE', 'info')

def calcQuality(totalCountPath, goodCountPath, oeeQualityPath):
    '''
    Calculates the quality component of OEE.

    Parameters:
    - totalCountPath: The tag path for the total count.
    - goodCountPath: The tag path for the good count.
    - oeeQualityPath: The tag path to store the calculated quality.

    Returns:
    - quality (float): The calculated quality percentage.
    '''
    # Use a single readBlocking call
    tagValues = system.tag.readBlocking([totalCountPath, goodCountPath])
    totalCount = tagValues[0].value
    goodCount = tagValues[1].value

    try:
        quality = float(goodCount) / float(totalCount)
    except:
        quality = 1

    system.tag.writeBlocking([oeeQualityPath], [quality])
    return quality

def calcAvailability(runTimePath, totalTimePath, oeeAvailabilityPath):
    '''
    Calculates the availability component of OEE.

    Parameters:
    - runTimePath: The tag path for the runtime.
    - totalTimePath: The tag path for the total time.
    - oeeAvailabilityPath: The tag path to store the calculated availability.

    Returns:
    - availability (float): The calculated availability percentage.
    '''
    # Use a single readBlocking call
    tagValues = system.tag.readBlocking([runTimePath, totalTimePath])
    runTime = tagValues[0].value
    totalTime = tagValues[1].value

    try:
        availability = float(runTime) / float(totalTime)
    except:
        availability = 1

    system.tag.writeBlocking([oeeAvailabilityPath], [availability])
    return availability

def calcPerformance(totalCountPath, targetCountPath, oeePerformancePath):
    '''
    Calculates the performance component of OEE.

    Parameters:
    - totalCountPath: The tag path for the total count.
    - targetCountPath: The tag path for the target count.
    - oeePerformancePath: The tag path to store the calculated performance.

    Returns:
    - performance (float): The calculated performance percentage.
    '''
    # Use a single readBlocking call
    tagValues = system.tag.readBlocking([totalCountPath, targetCountPath])
    totalCount = tagValues[0].value
    targetCount = tagValues[1].value

    try:
        performance = float(totalCount) / float(targetCount)
    except:
        performance = 1

    system.tag.writeBlocking([oeePerformancePath], [performance])
    return performance

def getTagIDs(lineID, db=db):
    '''
    Retrieves a list of Tag IDs associated with the specified Line ID.

    Parameters:
    - lineID (str): The tag path for the Line ID.
    - db (str): The database name. Defaults to 'mes_core'.

    Returns:
    - listOfTags (list): A list of Tag IDs associated with the given Line ID.
    '''
    # Initialize an empty list to hold the tag IDs
    listOfTags = []

    # Read the value of the Line ID tag
    id = system.tag.readBlocking([lineID])[0].value

    # Query to retrieve Tag IDs where ParentID matches the Line ID
    query = 'SELECT ID FROM counttag WHERE parentID = ?'
    data = system.db.runPrepQuery(query, [id], db)

    # Append each Tag ID to the list
    for row in data:
        tagID = row[0]
        listOfTags.append(tagID)

    return listOfTags

def getGoodCount(lineID, goodCountPath, startTimePath, endTimePath, tagID, countTypeID, db=db):
    '''
    Calculates the total good count for a given lineID, tagID, and countTypeID within a specific time range.
    Writes the result to the specified goodCountPath.

    Parameters:
    - lineID (str): The tag path for the Line ID.
    - goodCountPath (str): The tag path where the good count will be written.
    - startTimePath (str): The tag path for the start time of the count range.
    - endTimePath (str): The tag path for the end time of the count range.
    - tagID (int): The ID of the tag being queried.
    - countTypeID (int): The type ID of the count being queried.
    - db (str): The database name. Defaults to 'mes_core'.

    Returns:
    - goodCount (int): The calculated good count.
    '''
    try:
        # Read all relevant tag values in one call for optimization
        tags = [lineID, startTimePath, endTimePath]
        tagValues = system.tag.readBlocking(tags)

        # Extract values from the result
        id = tagValues[0].value
        startTime = tagValues[1].value
        endTime = tagValues[2].value

        # Query to calculate the sum of counts from the database
        query = """
            SELECT SUM(Count) FROM counthistory
            WHERE TagID = ? AND CountTypeID = ? AND TimeStamp BETWEEN ? AND ?
        """
        data = system.db.runPrepQuery(query, [tagID, countTypeID, startTime, endTime], db)

        # Default goodCount to 'None'
        goodCount = None

        # Process the result
        for row in data:
            goodCount = row[0]

        # Handle None case
        if goodCount is None:
            goodCount = 0

        # Write the good count value to the specified path
        system.tag.writeBlocking([goodCountPath], [goodCount])

        return goodCount
    except Exception as e:
        # Log the exception for debugging
        from shared.mes_core.logging import log
        log(f"Error in getGoodCount: {str(e)}", 'error')
        return 0

def getBadCount(badCountPath, startTimePath, endTimePath, tagID, countTypeID, db=db):
    """
    Calculates the total bad count for a given tagID and countTypeID within a specific time range.

    Parameters:
        badCountPath (str): The tag path where the bad count will be written.
        startTimePath (str): The tag path to retrieve the start time.
        endTimePath (str): The tag path to retrieve the end time.
        tagID (int): The tag identifier to query the count history.
        countTypeID (int): The count type identifier to query the count history.
        db (str): The database name to use for the query. Defaults to 'mes_core'.

    Returns:
        int: The total bad count or -1 if an error occurs.
    """
    try:
        # Read all required tag values in a single call
        tagPaths = [startTimePath, endTimePath]
        tagValues = system.tag.readBlocking(tagPaths)

        startTime = tagValues[0].value
        endTime = tagValues[1].value

        # Query to calculate bad count
        query = """
            SELECT SUM(Count) FROM counthistory
            WHERE TagID = ? AND CountTypeID = ? AND TimeStamp BETWEEN ? AND ?
        """
        data = system.db.runPrepQuery(query, [tagID, countTypeID, startTime, endTime], db)

        badCount = None
        for row in data:
            badCount = row[0]

        # Handle cases where no data is returned
        if badCount is None:
            badCount = 0

        # Write the bad count to the specified tag path
        system.tag.writeBlocking([badCountPath], [badCount])

        return badCount
    except Exception as e:
        # Log any errors
        from shared.mes_core.logging import log
        log(f"Error in getBadCount: {str(e)}", 'error')
        return -1

def getTotalCount(db=db, lineID=None, totalCountPath=None, startTimePath=None, endTimePath=None):
    """
    Retrieves the total count of items within a specified time range.

    Args:
        db (str): The database name (default: db).
        lineID (str): The tag path for the line ID.
        totalCountPath (str): The tag path to write the total count.
        startTimePath (str): The tag path for the start time.
        endTimePath (str): The tag path for the end time.

    Returns:
        int: Total count.
    """
    # Read all necessary tags in a single call
    tagValues = system.tag.readBlocking([lineID, startTimePath, endTimePath])
    lineIDValue = tagValues[0].value
    startTime = tagValues[1].value
    endTime = tagValues[2].value

    tagIDs = getTagIDs(lineIDValue)
    tagIDs = str(tagIDs).replace('[', '(').replace(']', ')').replace(' ', '')
    query = '''
        SELECT SUM(Count) FROM counthistory
        WHERE countTypeID NOT IN (1, 4) 
        AND TimeStamp BETWEEN ? AND ?
        AND TagID IN %s
    ''' % tagIDs

    data = system.db.runPrepQuery(query, [startTime, endTime], db)
    totalCount = 0 if not data or data[0][0] is None else data[0][0]
    system.tag.writeBlocking([totalCountPath], [totalCount])
    return totalCount


def getUnplannedDowntimeSeconds(db=db, startTimePath=None, unplannedDowntimePath=None, lineID=None):
    """
    Retrieves the total unplanned downtime in seconds.

    Args:
        db (str): The database name (default: db).
        startTimePath (str): The tag path for the start time.
        unplannedDowntimePath (str): The tag path to write the downtime.
        lineID (str): The tag path for the line ID.

    Returns:
        int: Unplanned downtime in seconds.
    """
    # Read all necessary tags in a single call
    tagValues = system.tag.readBlocking([startTimePath, lineID])
    startTime = tagValues[0].value
    lineIDValue = tagValues[1].value

    query = '''
        SELECT SUM(TIME_TO_SEC(TIMEDIFF(s.EndDateTime, s.StartDateTime))) AS 'Total in Seconds'
        FROM statehistory s
        LEFT JOIN statereason st ON s.StateReasonID = st.ID
        WHERE st.RecordDowntime = 1 
        AND s.LineID = ? 
        AND StartDateTime > ? 
        AND (EndDateTime <= CURRENT_TIMESTAMP() OR Active = 1)
    '''
    data = system.db.runPrepQuery(query, [lineIDValue, startTime], db)
    unplannedDowntime = 0 if not data or data[0][0] is None else data[0][0]
    system.tag.writeBlocking([unplannedDowntimePath], [unplannedDowntime])
    return unplannedDowntime


def getPlannedDowntimeSeconds(db=db, startTimePath=None, plannedDowntimePath=None, lineID=None):
    """
    Retrieves the total planned downtime in seconds.

    Args:
        db (str): The database name (default: db).
        startTimePath (str): The tag path for the start time.
        plannedDowntimePath (str): The tag path to write the downtime.
        lineID (str): The tag path for the line ID.

    Returns:
        int: Planned downtime in seconds.
    """
    # Read all necessary tags in a single call
    tagValues = system.tag.readBlocking([startTimePath, lineID])
    startTime = tagValues[0].value
    lineIDValue = tagValues[1].value

    query = '''
        SELECT SUM(TIME_TO_SEC(TIMEDIFF(s.EndDateTime, s.StartDateTime))) AS 'Total in Seconds'
        FROM statehistory s
        LEFT JOIN statereason st ON s.StateReasonID = st.ID
        WHERE st.PlannedDowntime = 1 
        AND s.LineID = ? 
        AND StartDateTime > ? 
        AND (EndDateTime <= CURRENT_TIMESTAMP() OR Active = 1)
    '''
    data = system.db.runPrepQuery(query, [lineIDValue, startTime], db)
    plannedDowntime = 0 if not data or data[0][0] is None else data[0][0]
    system.tag.writeBlocking([plannedDowntimePath], [plannedDowntime])
    return plannedDowntime


def getOee(parentPath):
    """
    Retrieves and calculates OEE metrics.

    Args:
        parentPath (str): The parent path to the OEE tags.

    Returns:
        None
    """
    # Declare all tag paths
    lineID = f"{parentPath}/OEE/ID"
    unplannedDowntimePath = f"{parentPath}/OEE/Unplanned Downtime"
    totalTimePath = f"{parentPath}/OEE/Total Time"
    totalCountPath = f"{parentPath}/OEE/Total Count"
    targetCountPath = f"{parentPath}/OEE/Target Count"
    startTimePath = f"{parentPath}/OEE/Start Time"
    runTimePath = f"{parentPath}/OEE/Runtime"
    plannedDowntimePath = f"{parentPath}/OEE/Planned Downtime"
    oeeQualityPath = f"{parentPath}/OEE/OEE Quality"
    oeePerformancePath = f"{parentPath}/OEE/OEE Performance"
    oeeAvailabilityPath = f"{parentPath}/OEE/OEE Availability"
    goodCountPath = f"{parentPath}/OEE/Good Count"
    badCountPath = f"{parentPath}/OEE/Bad Count"

    # Perform calculations and write tag updates
    getUnplannedDowntimeSeconds(db, startTimePath, unplannedDowntimePath, lineID)
    getPlannedDowntimeSeconds(db, startTimePath, plannedDowntimePath, lineID)
    calcQuality(totalCountPath, goodCountPath, oeeQualityPath)
    calcAvailability(runTimePath, totalTimePath, oeeAvailabilityPath)
    calcPerformance(totalCountPath, targetCountPath, oeePerformancePath)
