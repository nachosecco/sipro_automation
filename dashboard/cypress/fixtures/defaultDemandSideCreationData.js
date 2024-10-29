import { currentTimestamp } from "../support/globalCommands";

export const DEFAULT_ADVERTISER_BODY = {
	status: "active",
	contactName: "test",
	contactEmail: "test@test.com",
	contactPhone: "1234567890",
	contactAddress: "acme",
	billingInfoApplicable: false,
	billingContactName: "",
	billingContactPhone: "",
	billingContactEmail: "",
	billingContactAddress: "",
	pricingOptions: "ANY",
	demandFeePercentage: "10",
};

export const DEFAULT_INSERTION_ORDER_BODY = {
	status: "active",
	terms: 30,
	useCustomSize: false,
};

export const DEFAULT_CAMPAIGN_BODY = {
	cpm: 0,
	goal: "open",
	pacingStrategy: "even",
	status: "running",
	enableFrequencyCapping: false,
	frequencyCappingPeriod: "86400",
	endDate: null,
	frequencyCappingAmount: "",
	impressionsTarget: "",
	priority: "",
	spendTarget: "",
	weight: "",
	singleAdMediaResponse: false,
	useCustomSize: false,
	dayParting: null,
	houseAd: false,
	startDate: currentTimestamp(new Date()),
};

export const DEFAULT_MEDIA_BODY = {
	cpm: 1,
	adTag: "https://cdndev.siprocalads.com/c6internaltestpage/test_vast_mp4.xml",
	status: "active",
	enablePCPM: false,
	pcpm: "",
	thirdPartyId: "",
	mediaTypeId: 2,
	mediaSource: "tag",
	creativeType: "mediaFile",
	size: "",
	supportsVpaid: false,
	mediaFiles: [],
	mediaUrls: [],
	position: "pre",
	duration: 30,
	clickThroughUrl: "",
	priority: "",
	weight: "",
	trackers: [],
	deviceTargeting: {
		devices: [],
	},
	customSizeEnabled: false,
	blacklistWhitelist: {
		accessRestrictionType: "blacklist",
		restrictions: [],
	},
	appNameBlacklistWhitelist: {
		accessRestrictionType: "blacklist",
		restrictions: [],
	},
	appBundleIdBlacklistWhitelist: {
		accessRestrictionType: "blacklist",
		restrictions: [],
	},
	locked: false,
	advertisersDomain: "ford.com",
	customUrlParamsExpression: "",
};

export const DEFAULT_DISPLAY_MEDIA_BODY = {
	...DEFAULT_MEDIA_BODY,
	adTag: "https://cdndev.siprocalads.com/c6internaltestpage/970x250-starbucks-nitro.jpg",
	size: "970x250",
	mediaTypeId: 6,
};

export const DEFAULT_PROGRAMMATIC_REQUEST_BODY = {
	status: "active",
	enableDeal: false,
	privateDeal: false,
	auctionType: "SECOND_PRICE",
	dealId: "",
	rtbBidderSeats: [],
	startDate: currentTimestamp(new Date()),
	endDate: null,
	floor: 5,
	priority: "",
	weight: "",
	trackers: [],
	seatType: "wseat",
	useCustomSize: false,
	blacklistWhitelist: {},
	enableFrequencyCapping: false,
	frequencyCappingAmount: 0,
	frequencyCappingPeriod: 86400,
	customUrlParamsExpression: "",
	// Leaving reference here
	// programmaticBidderConfigs: [
	// 	{
	// 		rtbBidderId: 123,
	// 		rtbBidderSeats: []
	// 	},
	// ],
};

export const DEFAULT_DEAL_PROGRAMMATIC_REQUEST_BODY = {
	name: "Deal Programmatic Demand",
	status: "active",
	enableDeal: true,
	privateDeal: false,
	auctionType: "FIRST_PRICE",
	dealId: "defaultDealProgrammatic",
	seatType: "wseat",
	dealGoal: "open",
	impressionsTarget: "",
	spendTarget: "",
	startDate: "07/28/2023 02:44 PM",
	endDate: null,
	floor: 1,
	id: null,
	customSizeEnabled: false,
	frequencyCappingAmount: 0,
	enableFrequencyCapping: false,
	frequencyCappingPeriod: 86400,
	customUrlParamsExpression: "",
};

export const DEFAULT_MEDIA_ALIGNMENTS = { id: "", ronMargin: 0, alignmentType: "STATIC", placements: [{ id: "" }] };

export const DEFAULT_DEMAND_ALIGNMENTS = { id: "", placements: [{ id: "" }] };
