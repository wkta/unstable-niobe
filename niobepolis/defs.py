import katagames_engine as kengi


DEBUG = False
MAXFPS = 45

# always try to keep your event number low: model->view or model->ctrl comms only
MyEvTypes = kengi.event.enum_ev_types(
    'MapChanges',  # contains new_map, gate_name

    'ConvStarts',  # contains convo_obj, portrait

    'ConvChoice',  # contains value
    'ConvEnds',

    # in Niobe Polis a portal can teleport you(tp) to another world
    'PortalActivates',  # contains portal_id

    'TerminalStarts',
    'SlotMachineStarts',
    
    # -----------------------
    #  related to poker
    # -----------------------
    'CashChanges',  # contains int "value"
    'StageChanges',
    'EndRoundRequested',
    'Victory',  # contains: amount
    'Tie',
    'Defeat'  # contains: loss
)
