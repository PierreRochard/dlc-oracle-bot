from marshmallow import Schema, fields


class Event(Schema):
    label = fields.Str(data_key='eventName')
    nonces = fields.List(fields.Str)
    signing_version = fields.Str(data_key='signingVersion')
    maturation_time = fields.DateTime(data_key='maturationTime')
    maturation_time_epoch = fields.Int(data_key='maturationTimeEpoch')
    announcement_signature = fields.Str(data_key='announcementSignature')
    event_descriptor_tlv = fields.Str(data_key='eventDescriptorTLV')
    event_tlv = fields.Str(data_key='eventTLV')
    announcement_tlv = fields.Str(data_key='announcementTLV')
    attestations = fields.List(fields.Str(), allow_none=True)
    outcomes = fields.List(fields.List(fields.Int))
    signed_outcome = fields.Int(data_key='signedOutcome', allow_none=True)


event_schema = Event()
