DEFAULT_ADVERTISER_BODY = {
    "status": "active",
    "contactName": "test",
    "contactEmail": "test@test.com",
    "contactPhone": "1234567890",
    "contactAddress": "acme",
    "billingInfoApplicable": False,
    "billingContactName": "",
    "billingContactPhone": "",
    "billingContactEmail": "",
    "billingContactAddress": "",
    "pricingOptions": "ANY",
}

DEFAULT_INSERTION_ORDER_BODY = {
    "status": "active",
    "terms": 30,
    "useCustomSize": False,
}

DEFAULT_CAMPAIGN_BODY = {
    "cpm": 0,
    "goal": "open",
    "pacingStrategy": "even",
    "status": "running",
    "enableFrequencyCapping": False,
    "frequencyCappingPeriod": "86400",
    "frequencyCappingAmount": "",
    "impressionsTarget": "",
    "priority": "",
    "spendTarget": "",
    "weight": "",
    "singleAdMediaResponse": False,
    "useCustomSize": False,
    "houseAd": False,
    "endDate": None,
}

DEFAULT_MEDIA_BODY = {
    "cpm": 1,
    "adTag": "https://cdndev.siprocalads.com/c6internaltestpage/test_vast_mp4.xml",
    "status": "active",
    "enablePCPM": False,
    "pcpm": "",
    "thirdPartyId": "",
    "mediaTypeId": 2,
    "mediaSource": "tag",
    "creativeType": "mediaUrl",
    "size": "",
    "supportsVpaid": False,
    "mediaFiles": [],
    "mediaUrls": [],
    "position": "pre",
    "duration": 30,
    "clickThroughUrl": "",
    "priority": "",
    "weight": "",
    "trackers": [],
    "deviceTargeting": {"devices": []},
    "customSizeEnabled": False,
    "blacklistWhitelist": {"accessRestrictionType": "blacklist", "restrictions": []},
    "appNameBlacklistWhitelist": {
        "accessRestrictionType": "blacklist",
        "restrictions": [],
    },
    "appBundleIdBlacklistWhitelist": {
        "accessRestrictionType": "blacklist",
        "restrictions": [],
    },
    "locked": False,
}

DEFAULT_RTB_BIDDER = {"compressBidRequest": False, "customSizeEnabled": False}

DEFAULT_PROGRAMMATIC_DEMAND = {
    "useCustomSize": False,
    "enableFrequencyCapping": False,
    "privateDeal": False,
}
