# Import the necessary libraries
from psychopy import visual, core, event, data
import psynteract

# Create a new window
win = visual.Window()

# Render a message onscreen
msg = visual.TextStim(win,
    text=u"Just a moment, please",
    wrapWidth=5 # don't wrap text
    )
instruction = visual.TextStim(win,
    text="We're waiting for the experimenter to start the session",
    alignHoriz="center",
    pos=(0, -0.25),
    height=0.05,
    wrapWidth=5
    )
msg.draw()
instruction.draw()
win.flip()

# Connect to the server
c = psynteract.Connection(
    server_uri='http://localhost:5984',
    db_name='psynteract',
    design='stranger', # Type of design
    group_size=2, # Number of clients in a group
    groupings_needed=1, # Number of unique groupings (see below)
    initial_data={
        'choices': [] # Create a list of choices by default
    },
    offline=False # Offline mode: play against yourself without a server
                  # (change to True to test locally without a server)
)

# Wait until the session is started
c.wait(lambda doc: doc['status'] == 'running', check='session')

# Generate five rounds/trials
trials = data.TrialHandler(
    trialList=range(2), # Number the trials consecutively
    nReps=1, # Repeat each trial once
    method='sequential' # Run trials in sequence
)

# Create a list to tally wins and losses
outcomes = []

# Translate response shorthand into text
response_key_meanings = {
    'r': 'rock',
    'p': 'paper',
    's': 'scissors'
}

# Run the trials
for trial in trials:
    print('Running trial', trial)
    # Elicit a response
    msg = visual.TextStim(win,
        text="Rock, paper, scissors, which one is it?",
        alignHoriz="center",
        wrapWidth=5 # don't wrap
        )
    msg.draw()
    instruction = visual.TextStim(win,
        text="Please press R, P or S",
        alignHoriz="center",
        pos=(0, -0.25),
        height=0.05
        )
    instruction.draw()
    win.flip()

    # Wait for a keypress
    response = event.waitKeys(keyList=['r', 'p', 's'])[0]
    print('Local participant responded with {}'.format(response))

    # Show a waiting screen
    msg = visual.TextStim(win,
        text="Waiting for the other player(s)",
        alignHoriz="center",
        wrapWidth=5 # don't wrap
        )
    msg.draw()
    win.flip()

    # Add the participant's response to the
    # shared data, and push it to the server
    c.data['choices'].append(response)
    c.push()

    # Wait until all other clients have
    # provided the same number of responses
    c.wait(lambda doc: len(doc['data']['choices']) > trial, check='clients')

    # Retrieve the partner's response
    # from the data
    partner = c.current_partners[0]

    # Retrieve the last response given by the partner
    partner_response = c.get(partner)['data']['choices'][-1]
    print('Partner responded with {}'.format(partner_response))

    # Compute the outcome
    if response == partner_response:
        outcomes.append(0)
        outcome_text = 'tied'
    elif (response == 'r' and partner_response == 'p') or (response == 's' and partner_response == 'r') or (response == 'p' and partner_response == 's'):
        outcomes.append(-1)
        outcome_text = 'lost'
    else:
        outcomes.append(1)
        outcome_text = 'won'

    # Provide feedback
    msg = visual.TextStim(win,
        text="You chose " + response_key_meanings[response] + " " +
        "and your partner " + response_key_meanings[partner_response]  + ".",
        alignHoriz="center",
        wrapWidth=5, # don't wrap
        pos=(0, 0.06)
        )
    msg1 = visual.TextStim(win,
        text="You " + outcome_text + "!",
        alignHoriz="center",
        wrapWidth=5, # don't wrap
        pos=(0, -0.06)
        )
    instruction = visual.TextStim(win,
        text="Please press any key to continue",
        alignHoriz="center",
        pos=(0, -0.25),
        height=0.05
        )
    msg.draw()
    msg1.draw()
    instruction.draw()
    win.flip()
    event.waitKeys()

    # Finalize the trial by saving the data locally
    trials.data.add('response', response)
    trials.data.add('partner_response', partner_response)

# Calculate overall score
# (by weighting individiual outcomes)
outcome_weighting = {
    -1: 0,
    0: 0,
    1: 1
}

# Compute the final outcome
# as the sum of all the weighted individual outcomes
print('Overall outcomes: {}'.format(outcomes))
outcome_total = sum(map(lambda o: outcome_weighting[o], outcomes))
print('Total outcome: {}'.format(outcome_total))

# Goodbyes
msg = visual.TextStim(win,
    text="That's it; Thank you for playing!",
    alignHoriz="center",
    wrapWidth=5, # don't wrap
    pos=(0, 0.06)
    )
msg1 = visual.TextStim(win,
    text="You won {} point(s)".format(outcome_total),
    alignHoriz="center",
    wrapWidth=5, # don't wrap
    pos=(0, -0.06)
    )
instruction = visual.TextStim(win,
    text="Please press any key to quit the experiment",
    alignHoriz="center",
    pos=(0, -0.25),
    height=0.05
    )

msg.draw()
msg1.draw()
instruction.draw()
win.flip()

# Wait for final response
event.waitKeys()

# Save data locally
trials.saveAsText('output.csv')

# End the experiment by closing the window
win.close()
