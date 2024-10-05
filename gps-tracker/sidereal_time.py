# based on https://github.com/jhaupt/Sidereal-Time-Calculator

from datetime import datetime, timezone

def sidereal_time(Long):
    
    t = datetime.now(timezone.utc)

    MM = t.month
    DD = t.day
    YY = t.year
    UT = t.hour + t.minute/60

    JD = (367*YY) - int((7*(YY+int((MM+9)/12)))/4) + int((275*MM)/9) + DD + 1721013.5 + (UT/24)

    GMST = 18.697374558 + 24.06570982441908*(JD - 2451545)
    GMST %= 24

    Long = Long/15
    LST = GMST+Long
    if LST < 0:
        LST = LST +24

    return LST