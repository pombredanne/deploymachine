
from kokki import Resource, ResourceArgument

class ElasticIP(Resource):
    actions = ["associate", "disassociate"]

    aws_access_key = ResourceArgument()
    aws_secret_access_key = ResourceArgument()
    ip = ResourceArgument()
    timeout = ResourceArgument(default=3*60) # None or 0 for no timeout

class EBSVolume(Resource):
    provider = "*aws.EBSVolumeProvider"

    actions = ["create", "attach", "detach", "snapshot"]

    volume_id = ResourceArgument()
    aws_access_key = ResourceArgument()
    aws_secret_access_key = ResourceArgument()
    size = ResourceArgument()
    snapshot_id = ResourceArgument()
    snapshot_required = ResourceArgument(default=False)
    availability_zone = ResourceArgument()
    device = ResourceArgument()
    timeout = ResourceArgument(default=3*60) # None or 0 for no timeout
