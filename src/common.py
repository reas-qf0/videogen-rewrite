def seconds_to_string(secs,duration=0):
    secs = int(secs)
    if secs >= 3600 or duration >= 3600:
        return '%02d' % (secs // 3600) + \
               ':' + \
               '%02d' % ((secs % 3600) // 60) + \
               ':' + \
               '%02d' % (secs % 60)
    else:
        return '%02d' % (secs // 60) + \
               ':' + \
               '%02d' % (secs % 60)
