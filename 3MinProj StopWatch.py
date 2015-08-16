# template for "Stopwatch: The Game"

# define global variables


# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(ticks):
    """
    Convert tenths of seconds to formatted time
    """   
    minutes = ticks // 600
    # minutes = ticks // 60
    tens_seconds =  (ticks // 100) % 6
    seconds = (ticks // 10) % 10
    tenths = ticks % 10
    return str(minutes) + ':' + str(tens_seconds) + \
           str(seconds) + '.' + str(tenths)
    
# define event handlers for buttons; "Start", "Stop", "Reset"


# define event handler for timer with 0.1 sec interval


# define draw handler

    
# create frame


# register event handlers


# start frame


# Please remember to review the grading rubric
