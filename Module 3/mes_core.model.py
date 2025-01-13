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
shared.mes_core.model

This library provides advanced filtering capabilities for the Unified Namespace (UNS). 
It is designed to allow navigation through the UNS, retrieve specific IDs for a given 
location, and interact with the backend systems efficiently. 

The MESFilterResults class serves as the core of this library, transforming query results 
into a manageable object format with named tuples for quick access to column values. 
This is particularly useful for MES systems where navigating and querying large datasets 
within the UNS is required.

Typical use cases:
- Navigate the UNS to locate specific nodes or data points.
- Retrieve IDs or metadata for backend processing.
- Simplify and organize database query results into a structured object format.

Dependencies:
- This library requires `queryResults` from database queries and the `re` module for 
  regular expression support (if needed).
"""

import re

from shared.mes_core.logging import log

#default database name
db = 'mes_core'

class MESFilterResults(object):
    """
    A class to transform query results into a more manageable object format with named tuples
    for fast access to columns and their values. It allows efficient navigation and retrieval
    of specific data within the Unified Namespace (UNS).
    """

    def __init__(self, queryResults):
        """
        Initializes the MESFilterResults object by extracting headers and transforming the query
        results into ResultEntry objects.

        Args:
            queryResults: The results of a database query.
        """
        # Create a named tuple for fast object creation
        self._headers = [str(c) for c in queryResults.getUnderlyingDataset().getColumnNames()]

        # Nested class for result entry
        class ResultEntry(object):
            __slots__ = self._headers

            def __init__(self, *args):
                self._values = args
                self.__dict__.update(zip(self.__slots__, self._values))

                # Dynamically set getters for each property
                for propertyName in self.__slots__:
                    getterName = "get" + propertyName.capitalize()
                    getter = lambda self=self, propertyName=propertyName: self.getPropertyValue(propertyName)
                    setattr(self, getterName, getter)

            def __iter__(self):
                return (value for value in self._values)

            def __repr__(self):
                return str(dict(zip(self.__slots__, self._values)))

            def __getitem__(self, key):
                try:
                    return self._values[key]
                except:
                    if key in self.__slots__:
                        return self.__dict__.get(key)

            def getPropertyValue(self, propertyName):
                return self.__dict__.get(propertyName)

        # Convert the result set into a list of ResultEntry objects
        self.results = []
        for row in queryResults:
            self.results.append(ResultEntry(*row))

    def __iter__(self):
        return (result for result in self.results)
    
class MESFilter(object):
    """
    MESFilter is a utility class designed to provide filtering capabilities for MES objects 
    within the Unified Namespace (UNS). It supports object types such as 'Enterprise', 'Site', 
    'Area', 'Line', and 'Cell', and enforces schema validation during the filtering process.

    This class allows developers to:
    - Set and validate MES object types for filtering.
    - Enable or restrict searching based on object states.
    """

    # Supported MES object types
    mesObjectTypes = ['Enterprise', 'Site', 'Area', 'Line', 'Cell']

    def __init__(self):
        """
        Initializes the MESFilter object with default values.
        - enabled: Boolean flag to determine whether filtering is restricted to enabled objects.
        - mesObjectType: The type of MES object being filtered (default is None).
        """
        self.enabled = True
        self.mesObjectType = None

    def setMESObjectTypeName(self, mesObjectType):
        """
        Sets the MES object type for filtering and validates its existence in the schema.

        Args:
            mesObjectType (str): The MES object type to filter (e.g., 'Enterprise', 'Line').

        Raises:
            ValueError: If the provided object type is not in the supported schema.
        """
        if mesObjectType not in self.mesObjectTypes:
            raise ValueError("Object type not in model schema")
        self.mesObjectType = mesObjectType

    def setEnableStateName(self, stateName='ENABLED'):
        """
        Sets the state name to filter enabled or disabled objects. Currently, only enabled 
        states are supported.

        Args:
            stateName (str): The state name to filter by (default is 'ENABLED').

        Raises:
            NotImplementedError: If filtering for disabled objects is attempted.
        """
        if stateName != 'ENABLED' and stateName is not True:
            raise NotImplementedError("Searching disabled lines is not yet implemented")

def loadMESObjects(mesFilter, db=db):
    """
    Loads MES objects based on the specified filter.

    Args:
        mesFilter (MESFilter): The filter object.
        db (str): The database name.

    Returns:
        MESFilterResults: Filtered results.
    """
    try:
        results = system.db.runPrepQuery(
            loadMESObjectsQueries[mesFilter.mesObjectType],
            [],
            db
        )
        return MESFilterResults(results)
    except Exception as e:
        log(f"Error loading MES objects: {e}", level='error')
        raise

def getEnterpriseID(modelPath, db=db):
    """
    Retrieves the Enterprise ID for a given model path.

    Args:
        modelPath (str): Path to the Enterprise in the UNS.
        db (str): Database name.

    Returns:
        int: The Enterprise ID.
    """
    modelParts = re.findall(r"([^/]+)", modelPath)
    try:
        return system.db.runPrepQuery(
            "SELECT e.ID FROM enterprise AS e WHERE e.Name = ?",
            [modelParts[0]],
            db
        )[0][0]
    except IndexError:
        log(f"Enterprise '{modelParts[0]}' not found.", level='error')
        raise ValueError(f"Enterprise '{modelParts[0]}' not found.")
    except Exception as e:
        log(f"Error in getEnterpriseID: {e}", level='error')
        raise

def getSiteID(modelPath, db=db):
    """
    Retrieves the Site ID for a given model path.

    Args:
        modelPath (str): Path to the Site in the UNS.
        db (str): Database name.

    Returns:
        int: The Site ID.
    """
    modelParts = re.findall(r"([^/]+)", modelPath)
    try:
        return system.db.runPrepQuery(
            """
            SELECT s.ID 
            FROM enterprise AS e 
            INNER JOIN site AS s ON s.ParentID = e.ID 
            WHERE e.Name = ? AND s.Name = ?
            """,
            modelParts[:2],
            db
        )[0][0]
    except IndexError:
        log(f"Site '{modelParts[1]}' not found under Enterprise '{modelParts[0]}'.", level='error')
        raise ValueError(f"Site '{modelParts[1]}' not found under Enterprise '{modelParts[0]}'.")
    except Exception as e:
        log(f"Error in getSiteID: {e}", level='error')
        raise

def getID(modelPath, db=db):
    """
    Retrieves the ID for the specified model path by determining its type.

    Args:
        modelPath (str): The model path.
        db (str): Database name.

    Returns:
        int: The ID for the specified model path.
    """
    modelParts = re.findall(r"([^/]+)", modelPath)
    modelLookup = {
        1: getEnterpriseID,
        2: getSiteID,
    }
    try:
        return modelLookup[len(modelParts)](modelPath, db=db)
    except KeyError:
        log(f"Unsupported model path structure: {modelPath}", level='error')
        raise NotImplementedError("Only Enterprise and Site are supported.")
    except Exception as e:
        log(f"Error in getID: {e}", level='error')
        raise