from hazelcast.serialization.data import *
from hazelcast.serialization.bits import *
from hazelcast.protocol.client_message import ClientMessage
from hazelcast.protocol.custom_codec import *
from hazelcast.protocol.codec.replicated_map_message_type import *
from hazelcast.protocol.event_response_const import *

REQUEST_TYPE = REPLICATEDMAP_ADDENTRYLISTENERTOKEYWITHPREDICATE
RESPONSE_TYPE = 104
RETRYABLE = False


def calculate_size(name, key, predicate, local_only):
    """ Calculates the request payload size"""
    data_size = 0
    data_size += calculate_size_str(name)
    data_size += calculate_size_data(key)
    data_size += calculate_size_data(predicate)
    data_size += BOOLEAN_SIZE_IN_BYTES
    return data_size


def encode_request(name, key, predicate, local_only):
    """ Encode request into client_message"""
    client_message = ClientMessage(payload_size=calculate_size(name, key, predicate, local_only))
    client_message.set_message_type(REQUEST_TYPE)
    client_message.set_retryable(RETRYABLE)
    client_message.append_str(name)
    client_message.append_data(key)
    client_message.append_data(predicate)
    client_message.append_bool(local_only)
    client_message.update_frame_length()
    return client_message


def decode_response(client_message):
    """ Decode response from client message"""
    parameters = dict(response=None)
    parameters['response'] = client_message.read_str()
    return parameters


def handle(client_message, handle_event_entry = None):
    """ Event handler """
    messageType = client_message.get_message_type()
    if messageType == EVENT_ENTRY and handle_event_entry is not None:
        if not client_message.read_bool():
            key = client_message.read_data()
        if not client_message.read_bool():
            value = client_message.read_data()
        if not client_message.read_bool():
            old_value = client_message.read_data()
        if not client_message.read_bool():
            merging_value = client_message.read_data()
        event_type = client_message.read_int()
        uuid = client_message.read_str()
        number_of_affected_entries = client_message.read_int()
        handle_event_entry(client_message, key, value, old_value, merging_value, event_type, uuid, number_of_affected_entries)

