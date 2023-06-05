from datetime import datetime


def get_duration_minutes(duration):

    dt = 0

    if 'H' in duration:
        dt = datetime.strptime(duration, "PT%HH%MM%SS") 
    elif 'M' in duration:
        dt=datetime.strptime(duration, "PT%MM%SS") 
    else: 
        dt=datetime.strptime(duration, "PT%SS") 

    return (dt - datetime.strptime("0", "%S")).total_seconds()/60