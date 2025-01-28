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
This script handles operations related to product codes
in the MES core database. It includes functionality for
adding product codes and ensuring they are updated if
duplicates exist.
'''
#default database name
db = 'mes_core'

from mes_core.model import getLineID
from mes_core.logging import log

# Function to add or update a product code
def addProductCode(productCode, description, disable=0, db=db):
    '''
    This function inserts a new product code into the database or updates
    an existing entry if the product code already exists.
    
    Parameters:
    - productCode: The unique code for the product.
    - description: A text description of the product.
    - disable: A flag to indicate if the product is disabled (default is 0).
    - db: The name of the database (default is 'mes_core').

    Returns:
    - The primary key of the inserted or updated product code.
    '''
    try:
        query = """
            INSERT INTO productcode (ProductCode, Description, Disable, TimeStamp)
            VALUES (?, ?, ?, NOW())
            ON DUPLICATE KEY UPDATE
                ProductCode = VALUES(ProductCode),
                Description = VALUES(Description),
                Disable = VALUES(Disable),
                TimeStamp = NOW()
        """
        key = system.db.runPrepUpdate(query, [productCode, description, disable], db, getKey=1)
        return key
    except Exception as e:
        log("Error in addProductCode: {}".format(str(e)), 'error')
        return None

# Function to update the product code line status
def updateProductCodeLineStatus(productCode, modelPath, enable=True, db=db):
    '''
    This function updates or inserts a record in the product code line table based on the
    provided product code and model path.

    Parameters:
    - productCode: The product code to update or insert.
    - modelPath: The path used to determine the line ID.
    - enable: A boolean indicating whether to enable or disable the product code line (default: True).
    - db: The database name (default: 'MES_Core').

    Returns:
    - 1 if the operation succeeds.
    - 0 if an error occurs.
    '''
    try:
        # Retrieve product code ID
        productCodeID = system.db.runScalarPrepQuery("""
            SELECT ID FROM productcode
            WHERE ProductCode = ?
        """, [productCode], db)

        # Retrieve line ID
        lineID = getLineID(modelPath)

        # Check if the product code line already exists
        pcID = system.db.runScalarPrepQuery("""
            SELECT ID FROM productcodeline
            WHERE ProductCodeID = ? AND LineID = ?
        """, [productCodeID, lineID], db)

        # Update or insert the product code line
        if pcID:
            system.db.runPrepUpdate("""
                UPDATE productcodeline
                SET Enable = ?, TimeStamp = NOW()
                WHERE ProductCodeID = ? AND LineID = ?
            """, [enable, productCodeID, lineID], db)
        else:
            system.db.runPrepUpdate("""
                INSERT INTO productcodeline (ProductCodeID, LineID, Enable, TimeStamp)
                VALUES (?, ?, ?, NOW())
            """, [productCodeID, lineID, enable], db)

        return 1
    except Exception as e:
        log("Error in updateProductCodeLineStatus: {}".format(str(e)), 'error')
        return 0


# Function to add a work order entry
def addWorkOrderEntry(workOrder, productCode, quantity, db=db):
    '''
    This function adds a work order entry to the database. If the work order already exists,
    it updates the quantity, product code ID, product code, and timestamp.

    Parameters:
    - workOrder: The work order identifier.
    - productCode: The associated product code.
    - quantity: The quantity for the work order.
    - db: The database name (default: 'mes_Core').

    Returns:
    - None.
    '''
    try:
        # Retrieve the product code ID
        pcID = system.db.runScalarPrepQuery("""
            SELECT ID
            FROM productcode
            WHERE ProductCode = ?
        """, [productCode], db)

        # Insert or update the work order entry
        query = """
            INSERT INTO workorder (WorkOrder, Quantity, Closed, Hide, TimeStamp, ProductCodeID, ProductCode)
            VALUES (?, ?, 0, 0, NOW(), ?, ?)
            ON DUPLICATE KEY UPDATE
                Quantity = VALUES(Quantity),
                ProductCodeID = VALUES(ProductCodeID),
                ProductCode = VALUES(ProductCode),
                TimeStamp = NOW()
        """
        system.db.runPrepUpdate(query, [workOrder, quantity, pcID, productCode], db)
    except Exception as e:
        log("Error in addWorkOrderEntry: {}".format(str(e)), 'error')
        return 0