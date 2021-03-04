"""
CLI for FlashCards
"""

def timed_input(buffer = "", timeout = 10):

    result = buffer
    time_spent = 0
    s_steps = 0.05
    s = 0
    count_down = int(timeout/s_steps)
    show_countdown = False
    crlf_pressed = False

    for remaining in range(count_down, 0, -1):
        if show_countdown:
            sys.stdout.write("\r%2d seconds remaining, answer: %s"%(int(remaining*s_steps), result)) 
        else:
            sys.stdout.write("\r%s    "%(result)) 
        sys.stdout.flush()
        
        time.sleep(s_steps)
        s += s_steps
        time_spent +=s_steps
        if s >=1/s_steps:
            s -=1/s_steps
            sys.stdout.write("\r")
            sys.stdout.write("\r%s    "%(result)) 
            
            sys.stdout.flush()
        
        if isData():
            c = sys.stdin.read(1)
            if c == '\x1b':         # x1b is ESC
                raise Exception(EXCEPTION_ESCAPED)
            elif ord(c) == 10 or ord(c)==13:
                crlf_pressed = True
                break
            elif ord(c) == 127:
                #backspace
                result = result[:-1]
            else:
                result +=c
    return(result, crlf_pressed, time_spent)