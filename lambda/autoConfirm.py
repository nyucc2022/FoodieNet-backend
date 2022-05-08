import json

def lambda_handler(event, context):

    print(event)

    event['response']['autoConfirmUser'] = True

    print(event)

    # TODO implement
    return event
