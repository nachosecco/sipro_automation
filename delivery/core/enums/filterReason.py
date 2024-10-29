from enum import Enum


# class syntax
class FilterReason(Enum):
    APP_NAME_SUPPLY_SIDE = "Placement: {} did not pass appName filters for value: {}", [
        "uid",
        "app_name",
    ]
    APP_NAME_DEMAND_SIDE = "Placement {} removed for reason TARGETING_APP_NAME", ["uid"]
    APP_NAME_GLOBAL_BLOCKLIST = (
        "Placement {} removed for reason APP_NAME_BLACKLISTED",
        ["uid"],
    )
    APP_BUNDLE_SUPPLY_SIDE = (
        "Placement: {} did not pass appBundle filters for value: {}",
        ["uid", "app_id"],
    )
    APP_BUNDLE_DEMAND_SIDE = "Placement {} removed for reason TARGETING_APP_BUNDLE", [
        "uid"
    ]
    APP_BUNDLE_GLOBAL_BLOCKLIST = (
        "Placement {} removed for reason APP_BUNDLE_ID_BLACKLISTED",
        ["uid"],
    )
    APP_DOMAIN_GLOBAL_BLOCKLIST = (
        "Placement {} removed for reason BLACKLISTED",
        ["uid"],
    )
    SIZES_RULE = "Did not pass targeting rule:SizesRule because of:TARGETING_SIZE", []
    PUBLISHER_FILTER = "Placement {} removed for reason PUBLISHER_FILTER", ["uid"]
    TARGETING_DOMAIN = "Placement {} removed for reason TARGETING_DOMAIN", ["uid"]

    TARGETING_IVT_DEVICE_ID_INVALID = (
        "Placement {} removed for reason TARGETING_IVT_DEVICE_ID_INVALID",
        ["uid"],
    )

    TARGETING_AUDIENCE = (
        "Placement {} removed for reason TARGETING_AUDIENCE",
        ["uid"],
    )

    TARGETING_PARAMS = ("Placement {} removed for reason TARGETING_PARAMS", ["uid"])
    APP_MEDIA_BUNDLE_SUPPLY_SIDE = (
        "did not pass appBundle rule for value {}",
        ["app_id"],
    )

    BLOCKED_CPM_BELOW_MIN_PRICE = (
        "Placement {} removed for reason BLOCKED_CPM_BELOW_MIN_PRICE",
        ["uid"],
    )

    BLOCKED_EXPOSURE_THROTTLE = (
        "Placement {} removed for reason BLOCKED_EXPOSURE_THROTTLE",
        ["uid"],
    )

    AD_RESPONSE_SIZE_EXCEEDED = (
        "was blocked by MediaSourceLimitEnforcer as exceeded the limit of",
        [],
    )

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, message, props):
        self.message = message
        self.props = props

    def get_formatted_string(self, obj):
        pre_res = [
            getattr(obj, prop, "No %s property found" % prop) for prop in self.props
        ]
        return self.message.format(*pre_res)
