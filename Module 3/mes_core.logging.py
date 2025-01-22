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
This script is designed to take two arguments, [message, level], 
for the Ignition Logging engine. The `message` parameter is the 
payload published to the MES logger, and `level` represents the 
severity of the log. Supported log levels are:

- fatal
- error
- warn
- info
- debug
- trace
'''

def log(message, level):
    import system
    
    # Initialize the logger for the MES system
    logger = system.util.getLogger('MES')
    
    # Map the level argument to the corresponding log level
    if level.lower() == 'info':
        logger.info(message)
    elif level.lower() == 'fatal':
        logger.fatal(message)
    elif level.lower() == 'error':
        logger.error(message)
    elif level.lower() == 'warn':
        logger.warn(message)
    elif level.lower() == 'debug':
        logger.debug(message)
    elif level.lower() == 'trace':
        logger.trace(message)
    else:
        # Handle unsupported log levels
        # logger.warn(f"Unsupported log level: {level}. Defaulting to 'info'.") # deleted f-string

        # using .format() instead of f-string
        logger.warn("Unsupported log level: {}. Defaulting to 'info'.".format(level))

        logger.info(message)
