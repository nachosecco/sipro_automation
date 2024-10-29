PUBLISHER_DATA_DEFAULT = {
    "status": "active",
    "defaultFloor": "",
    "defaultRevenueShare": 0,
    "contactName": "test",
    "contactEmail": "test@test.com",
    "contactPhone": "1234567890",
    "contactAddress": "123 Four St.",
    "billingInfoApplicable": False,
    "adSystemDomain": "siprocalads.com, ad.local",
    "adsTxtAccountId": "",
    "accountRelationship": "direct",
    "certAuthorityID": "",
    "webSiteDomain": "test.com",
    "sellerType": "publisher",
    "confidential": False,
}

SITE_DATA_DEFAULT = {
    "status": "active",
    "defaultFloor": 0,
    "defaultRevenueShare": 0,
    "url": "test.com",
}

# We default to a ctv/mobile placement as it's our main business focus
DEFAULT_PLACEMENT_BODY = {
    "status": "active",
    "locked": "false",
    "type": "mobile",
    "enableVPAID": "false",
    "enableC6AdManager": False,
    "vastVersion": "4.0",
    "revenueType": "rev_share",
    "revenueShare": "60.5",
    "floor": "1",
    "auctionFloorIncrement": "",
    "auctionType": "SECOND_PRICE",
    "trackers": [],
    "enableIVTFiltering": "true",
    "moatCustomerId": "",
    "allowRon": "false",
    "maxDuration": "60",
    "instreamSkipTime": "",
    "enableAdResponseMediaLimit": False,
    "adResponseMediaLimit": "",
    "minBitrate": "300",
    "maxBitrate": "25000",
    "blacklistWhitelist": {"accessRestrictionType": "blacklist", "restrictions": []},
    "advertiserDomainBlacklistWhitelist": {
        "accessRestrictionType": "blacklist",
        "restrictions": [],
    },
    "passback": "",
}

DEFAULT_PLACEMENT_ALIGN = {}
