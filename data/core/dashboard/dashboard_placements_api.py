from core.dashboard.authorization_context import AuthorizationContext
from core.dashboard.resource_util import ResourceUtil


def fetch_placement(auth_ctx: AuthorizationContext, gui: str):
    json_placements = ResourceUtil(auth_ctx).get_resource_index(
        "/v2/manage/placements", "Placements"
    )

    for p in json_placements:
        if p.get("guid") == gui:
            return p

    raise Exception("No placement")


def fetch_aligned_medias(auth_ctx: AuthorizationContext, placement_guid):
    placement_id = fetch_placement(auth_ctx, placement_guid).get("id")
    url = f"/v2/manage/placements/{placement_id}/alignments"
    alignments = ResourceUtil(auth_ctx).get_resource_index(url, "Alignments")
    medias = alignments.get("media")
    if len(medias) == 0:
        raise Exception(f"Could not find media for placement {placement_guid}.")

    return medias
