from hazelcast.serialization.data import *
from hazelcast.serialization.bits import *
from hazelcast.protocol.client_message import ClientMessage
from hazelcast.protocol.custom_codec import *
from hazelcast.protocol.codec.client_message_type import *

REQUEST_TYPE = CLIENT_GETPARTITIONS
RESPONSE_TYPE = 108
RETRYABLE = False


def calculate_size():
    """ Calculates the request payload size"""
    data_size = 0
    return data_size


def encode_request():
    """ Encode request into client_message"""
    client_message = ClientMessage(payload_size=calculate_size())
    client_message.set_message_type(REQUEST_TYPE)
    client_message.set_retryable(RETRYABLE)
    client_message.update_frame_length()
    return client_message


def decode_response(client_message):
    """ Decode response from client message"""
    parameters = dict(partitions=None)
    partitions_size = client_message.getInt()
    partitions = {}
    for partitions_index in xrange(0,partitions_size):
        partitions_key = AddressCodec.decode(client_message)
        partitions_val_size = client_message.read_int()
        partitions_val = []
        for partitions_val_index in xrange(0, partitions_val_size):
            partitions_val_item = client_message.read_int()
            partitions_val.append(partitions_val_item)
        parameters['partitions_val'] = partitions_val
        partitions['partitions_key'] = partitions_val
    parameters['partitions'] = partitions
    return parameters



