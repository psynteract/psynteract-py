import time
from datetime import datetime
from psynteract import Connection

# Setup parameters
bots = 4 # Number of clients
# One client is the 'slacker';
# it takes longer to complete the cycle
slacker_sleep_s = 5
# Total number of cycles to run through
cycles = 10
# Assumed cycle length in seconds.
# This should be larger than the slacker's sleep
# period plus the time needed by the clients to
# synchronize.
cycle_length = 10

# Open connection
c = Connection(
    'http://localhost:5984',
    'psynteract',
    initial_data={
        'round': -1
    },
    roles=(bots - 1) * ['normal'] + 1 * ['slacker'],
    group_size=bots
)

# A simple function to synchronize clients:
# wait until the epoch is evenly divisible by a given number
def sync(cycle_length):
    epoch = (datetime.now() - datetime(1970, 1, 1)).total_seconds()
    time.sleep(cycle_length - epoch % cycle_length)

# Wait for the session to start
c.wait(lambda session: session['status'] == 'running', check='session')

# Output debug info
print('This is client', c._id, 'my role is', c.current_role)

# Use the function above to sync up the clients
sync(cycle_length)

# Run through the cycles
for i in range(cycles):
    # Output current time
    print('Starting new cycle at ', datetime.utcnow())

    # Start timer
    t1 = datetime.now()

    # If the client is the 'slacker', wait for some additional time
    if c.current_role == 'slacker':
        print('waiting')
        time.sleep(slacker_sleep_s)

    # Update document and push contents to server
    c.doc['data'] = { 'round': i }
    c.push()

    # Wait for the other clients to complete this
    c.wait(lambda doc: doc['data']['round'] == i)

    # Retrieve document
    partner_doc = c.get(c.current_partners[0])

    # End timer
    t2 = datetime.now()

    # Output round and timestamp
    print('Lag: {:4} {}'.format(
        i, round((t2 - t1).total_seconds() - slacker_sleep_s, 3)
    ))

    # The cycle is now over, sync up the time before starting the next
    sync(cycle_length)
