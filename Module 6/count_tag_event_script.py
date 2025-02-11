def valueChanged(tag, tagPath, previousValue, currentValue, initialChange, missedEvents):
    """
    Tag Event Script for valueChanged on the Count tag.
    This script will call the storeCountHistory function from the mes_core.count module.
    """
    from mes_core.count import storeCountHistory

    if initialChange:
        return  # Ignore the initial tag change event

    # Correct tag paths using relative reference in the same folder
    tagPaths = [
        "[.]Enable",
        "[.]LastCount",
        "[.]TagID",
        "[.]CountTypeID"
    ]

    # Read tag values in one call
    tagValues = system.tag.readBlocking(tagPaths)

    enable = tagValues[0].value
    lastCount = tagValues[1].value
    tagID = tagValues[2].value
    countTypeID = tagValues[3].value

    # Check if the counter is enabled
    if enable == 1:
        # Call storeCountHistory and check the result
        result = storeCountHistory(currentValue.value, lastCount, tagID, countTypeID)
        
        # Update LastCount tag if the count delta was successfully recorded
        if result != -1:
            system.tag.writeBlocking(["[.]LastCount"], [result])
