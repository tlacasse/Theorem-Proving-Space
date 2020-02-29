
# steps need to be used at least this many times
# to be considered as a dimension in the conjecture position
HOLSTEP_STEPUSAGE_LOWER_BOUND = 20

# not set value, this multiplied by HOLSTEP_METRIC_MAX, with overflow in uint16,
# will wrap around to a value greater than HOLSTEP_METRIC_MAX.
HOLSTEP_METRIC_BUILD_NOT_SET = -0.001

# maximum distance between conjectures
HOLSTEP_METRIC_MAX = 65000
