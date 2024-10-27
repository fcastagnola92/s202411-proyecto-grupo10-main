from logic import functions
def card_process_task(event, context):
    functions.sync_verification_state(event, context)