def set_state(user_id, state):
    with open("{}".format(user_id), 'w') as f:
        f.write(str(state))

def get_state(user_id):
    state = 0
    try:
        with open("{}".format(user_id), 'r') as f:
            state = int(f.readline())
    
    except FileNotFoundError:
        set_state(user_id, 0)
        
    return state