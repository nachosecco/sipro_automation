export const DEFAULT_PUBLISHER_BODY = {
	status: "active",
	defaultFloor: "",
	defaultRevenueShare: 0,
	contactName: "test",
	contactEmail: "test@test.com",
	contactPhone: "1234567890",
	contactAddress: "123 Four St.",
	billingInfoApplicable: false,
	billingContactName: null,
	billingContactEmail: null,
	billingContactPhone: null,
	billingContactAddress: null,
	adSystemDomain: "siprocalads.com, ad.local",
	adsTxtAccountId: "",
	accountRelationship: "direct",
	certAuthorityID: "",
	webSiteDomain: "test.com",
	sellerType: "publisher",
	confidential: false,
};

export const DEFAULT_SITE_BODY = {
	status: "active",
	defaultFloor: 0,
	defaultRevenueShare: 0,
	url: "test.com",
};

// We default to a ctv/mobile placement as it's our main business focus
export const DEFAULT_PLACEMENT_BODY = {
	status: "active",
	locked: "false",
	type: "mobile",
	enableVPAID: "false",
	enableC6AdManager: false,
	vastVersion: "4.0",
	revenueType: "rev_share",
	revenueShare: "60.5",
	floor: "1",
	auctionFloorIncrement: "",
	auctionType: "SECOND_PRICE",
	trackers: [],
	enableIVTFiltering: "true",
	moatCustomerId: "",
	allowRon: "false",
	maxDuration: "60",
	instreamSkipTime: "",
	enableAdResponseMediaLimit: false,
	adResponseMediaLimit: "",
	minBitrate: "300",
	maxBitrate: "25000",
	blacklistWhitelist: {
		accessRestrictionType: "blacklist",
		restrictions: [],
	},
	advertiserDomainBlacklistWhitelist: {
		accessRestrictionType: "blacklist",
		restrictions: [],
	},
	passback: "",
};

export const DEFAULT_DISPLAY_PLACEMENT_BODY = {
	...DEFAULT_PLACEMENT_BODY,
	type: "display",
	size: "970x250",
	typeName: "Display",
};

export const DEFAULT_INSTREAM_PLACEMENT_BODY = {
	...DEFAULT_PLACEMENT_BODY,
	type: "vast",
	size: "970x250",
	typeName: "Instream",
};
export const DEFAULT_PLACEMENT_ALIGNMENTS = { id: "", media: [], programmaticDemands: [], allowRon: false };
