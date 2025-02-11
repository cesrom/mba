

from datetime import datetime
# Retrieve parent container for easier reference
parent = event.source.parent  

# Get product code from the selected row in the table
productCode = event.source.parent.selectedProductCode
productCodeID = event.source.parent.selectedProductCodeID

# Replace spaces with underscores in the product code
productCodeFormatted = productCode.replace(" ", "_")

# Get quantity from the QuantityField component
quantity = parent.getComponent('QuantityField').intValue

# Database connection name
db = 'mes_core'

# Format current timestamp as YYYYMMDD for the work order
timestamp = datetime.now().strftime("%Y%m%d")

# Generate a sequence number (001 as a placeholder for now)
sequence = "001"  # Start at 001 if no previous sequence
#query = "SELECT MAX(SUBSTRING_INDEX(WorkOrder, '-', -1)) FROM workorder WHERE ProductCode = ?"
#result = system.db.runPrepQuery(query, [productCode], 'mes_core')
#
#if result[0][0] is None:
#    sequence = "001"  # Start at 001 if no previous sequence
#else:
#    sequence = str(int(result[0][0]) + 1).zfill(3)  # Increment and pad with zeros

# Construct the work order name using product code, timestamp, and sequence
workOrder = "WO-{productCodeFormatted}-{timestamp}-{sequence}".format(productCodeFormatted=productCodeFormatted, timestamp=timestamp, sequence=sequence)

# SQL query to insert a new work order into the database
query = """
    INSERT INTO WorkOrder (WorkOrder, Quantity, Closed, Hide, TimeStamp, ProductCode, ProductCodeID) 
    VALUES (?, ?, ?, ?, ?, ?, ?)
"""

# Prepare the arguments for the query
args = [workOrder, quantity, 0, 0, datetime.now(), productCode, productCodeID]  # Replace 1 with the actual ProductCodeID if available

# Execute the SQL query using Ignition's system.db.runSFPrepUpdate
system.db.runSFPrepUpdate(query, args, [db])

# Log the work order creation for debugging (optional)
system.util.getLogger("WorkOrderScript").info("Work Order created: {}".format(workOrder))