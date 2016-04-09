# Pure Python example: Benchmarking response durations

This directory contains a script that uses the psynteract package from pure
Python, without any graphical display or user interaction. The purpose of the
script is to measure technical latencies in a laboratory.

To this end, the script simulates a number of clients that start a trial at
(almost) exactly the same time. All but one client respond directly, but the
final 'participant' responds with a known latency. The script measures the
interval between the onset of the trial, and the time that the last client's
response has propagated to all other clients. Ideally, this should not be much
larger than the known response lag.

## Parameters

The file head contains the parameters that can be set:

* The total number of `bots` that will be connected to the server
* The number of seconds the 'slacker' will wait before committing a response
  (`slacker_sleep_s`)
* How many `cycles` to run in total
* An anticipated cycle duration, `cycle_length`, that is used to synchronize all
  connected clients. Specifically, at the end of a cycle, all clients wait until
  the epoch (the number of seconds since January 1st, 1970) is evenly divisible
  by this number. This assures that all clients start the cycle at (pretty much)
  the same time.

The connection settings, specifically the server url and database name, may also
have to be adjusted.
