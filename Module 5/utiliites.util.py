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

import re
htmlPatternBR = re.compile(r'<br>', re.I)
htmlPatternGeneric = re.compile('<.*?>', re.I)

def stripHTML(string, handleBreaks=False):
    """This removes the HTML markup tags from a string.
    Not to be confused with parsing, of which this does *NONE*.
    https://stackoverflow.com/a/1732454
    """
    if handleBreaks:
        # Line breaks are line feeds
        string = htmlPatternBR.sub('\n', string)

    # Everything else can be stripped
    string = htmlPatternGeneric.sub('', string)

    return string

def clipboard(imagePath):
    from java.awt.datatransfer import StringSelection
    from java.awt.datatransfer import Clipboard
    from java.awt import Toolkit
    from java.awt.datatransfer import DataFlavor
    
    toolkit = Toolkit.getDefaultToolkit()
    clipboard = toolkit.getSystemClipboard()
    clipboard.setContents(StringSelection(imagePath), None)
    contents = clipboard.getContents(None)
    
    logger = system.util.getLogger("IntellicInfo")
    content = contents.getTransferData(DataFlavor.stringFlavor)
    logger.infof('Image %s copied to clipboard. Content: %s', imagePath, content)

def retarget(project):
    system.util.retarget(project)