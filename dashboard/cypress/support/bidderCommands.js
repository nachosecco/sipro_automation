import DEFAULT_BIDDER_REQUEST_BODY from "../fixtures/defaultBidderRequestBody";
import getToken from "../utils/getToken";
import { DASHBOARD_API } from "../utils/serviceResources";
const data = require("../fixtures/bidderCreationData.json");

/* This command will fetch the api looking for a bidder, if that bidder is present,
 we delete it. It also creates a new base bidder */
Cypress.Commands.add("checkBaseBidderRequest", (token) => {
	cy.request({
		url: DASHBOARD_API.RTB_BIDDER.getIndex(),
		method: "GET",
		headers: {
			Authorization: token,
		},
	}).then((response) => {
		const body = response.body;
		const targetBidder = body.find((o) => o.name === data.baseName);

		if (targetBidder) {
			cy.request({
				url: DASHBOARD_API.RTB_BIDDER.getOne({ id: targetBidder.id }),
				method: "DELETE",
				headers: {
					Authorization: token,
				},
			});
		}

		cy.request({
			url: DASHBOARD_API.RTB_BIDDER.getIndex(),
			method: "POST",
			headers: {
				Authorization: token,
			},
			body: {
				name: data.baseName,
				status: data.status,
				rtbSpecVersion: data.rtbSpecVersion,
				testMode: false,
				companyAccessRestrictionConfig: {
					accessRestriction: data.accessRestriction,
					blacklist: data.blacklist,
					whitelist: data.whitelist,
				},
				cookieSyncUrl: data.cookieSyncUrl,
				cookieSyncPercentage: data.cookieSyncPercentage,
				matchedCookieEnforced: data.matchedCookieEnforced,
				rtbUrls: [
					{
						clientId: data.clientId,
						rtbRegionId: data.rtbRegionId,
						url: data.bidUrl,
					},
				],
				rtbBidderSeats: data.rtbBidderSeats,
				supportedRtbMediaTypes: data.supportedRtbMediaTypes,
				compressBidRequest: data.compressBidRequest,
				floor: data.floor,
				responseTimeout: data.responseTimeout,
				classOverride: data.classOverride,
				bidRequestConfig: {
					sendAllimps: data.sendAllimps,
					sendAllowedBidCurrencies: data.sendAllowedBidCurrencies,
					sendAuctionType: data.sendAuctionType,
					sendBidTimeout: data.sendBidTimeout,
					sendBlockedBuyerSeats: data.sendBlockedBuyerSeats,
					sendLanguages: data.sendLanguages,
					sendSource: data.sendSource,
				},
				bidSourceConfig: {
					sendSourceFd: data.sendSourceFd,
					sendSourcePChain: data.sendSourcePChain,
					sendSourceSChain: data.sendSourceSChain,
					sendSourceTid: data.sendSourceTid,
				},
				bidImpressionConfig: {
					sendBidFloorCurrency: data.sendBidFloorCurrency,
					sendBidFloor: data.sendBidFloor,
					sendMetrics: data.sendMetrics,
					sendTagId: data.sendTagId,
					sendInstl: data.sendInstl,
				},
				bidBannerConfig: {
					sendBannerFormat: data.sendBannerFormat,
					sendBannerWidth: data.sendBannerWidth,
					sendBannerHeight: data.sendBannerHeight,
					sendBannerMaxWidth: data.sendBannerMaxWidth,
					sendBannerMinWidth: data.sendBannerMinWidth,
					sendBannerMaxHeight: data.sendBannerMaxHeight,
					sendBannerMinHeight: data.sendBannerMinHeight,
					sendBannerPosition: data.sendBannerPosition,
					sendBlockedBannerAdTypes: data.sendBlockedBannerAdTypes,
					sendBlockedCreativeAttr: data.sendBlockedCreativeAttr,
					sendBannerMimeTypes: data.sendBannerMimeTypes,
					sendBannerTopFrame: data.sendBannerTopFrame,
					sendBannerExpDir: data.sendBannerExpDir,
					sendBannerApiFrameworks: data.sendBannerApiFrameworks,
				},
				bidVideoConfig: {
					sendDeliveryMethod: data.sendDeliveryMethod,
					sendMaxExtendedDuration: data.sendMaxExtendedDuration,
					sendMaxBitrate: data.sendMaxBitrate,
					sendMinBitrate: data.sendMinBitrate,
					sendPlacement: data.sendPlacement,
					sendPlayBackend: data.sendPlayBackend,
					sendVideoHeight: data.sendVideoHeight,
					sendVideoWidth: data.sendVideoWidth,
					sendVideoPosition: data.sendVideoPosition,
					sendSkip: data.sendSkip,
					sendApiFrameworks: data.sendApiFrameworks,
					sendSupportedProtocols: data.sendSupportedProtocols,
					sendVideoLinearity: data.sendVideoLinearity,
					sendStartDelay: data.sendStartDelay,
				},
				contentDeliveryMethodConfig: data.contentDeliveryMethodConfig,
				linearity: data.linearity,
				bidDealConfig: {
					sendDealFloorCurrency: data.sendDealFloorCurrency,
					sendPrivateDealFlag: data.sendPrivateDealFlag,
					sendDealFloor: data.sendDealFloor,
				},
				bidSiteConfig: {
					sendSiteId: data.sendSiteId,
					sendSiteDomain: data.sendSiteDomain,
					sendRef: data.sendRef,
					sendPageUrl: data.sendPageUrl,
				},
				bidPublisherConfig: {
					sendPublisherId: data.sendPublisherId,
					sendPublisherDomain: data.sendPublisherDomain,
					sendPublisherName: data.sendPublisherName,
				},
				bidDeviceConfig: {
					sendGeoObject: data.sendGeoObject,
					sendHeight: data.sendHeight,
					sendWidth: data.sendWidth,
					sendDeviceModel: data.sendDeviceModel,
					sendDeviceMake: data.sendDeviceMake,
					sendDeviceType: data.sendDeviceType,
					sendDoNotTrack: data.sendDoNotTrack,
					sendLimitAdTracking: data.sendLimitAdTracking,
					sendGeoFetch: data.sendGeoFetch,
					sendDeviceConnectionType: data.sendDeviceConnectionType,
					sendDeviceIpv4: data.sendDeviceIpv4,
					sendNativeAdvertiserId: data.sendNativeAdvertiserId,
					sendDeviceJsSupportFlag: data.sendDeviceJsSupportFlag,
					sendLanguage: data.sendLanguage,
					sendDeviceCarrierId: data.sendDeviceCarrierId,
					sendDeviceOs: data.sendDeviceOs,
					sendDeviceOsVersion: data.sendDeviceOsVersion,
					sendDeviceUserAgent: data.sendDeviceUserAgent,
				},
				bidGeoConfig: {
					sendCity: data.sendCity,
					sendCoordinates: data.sendCoordinates,
					sendCountry: data.sendCountry,
					sendIpService: data.sendIpService,
					sendMetro: data.sendMetro,
					sendRegion: data.sendRegion,
					sendZip: data.sendZip,
					sendUtcOffset: data.sendUtcOffset,
				},
				bidUserConfig: {
					sendBuyerUid: data.sendBuyerUid,
					sendGeoObject: data.uSendGeoObject,
				},
			},
		});
	});
});

export const createOrUpdateBidder = ({ token = getToken(), bidderName, bidderBody = DEFAULT_BIDDER_REQUEST_BODY }) => {
	return cy
		.request({
			url: DASHBOARD_API.RTB_BIDDER.getIndex(),
			method: "GET",
			headers: {
				Authorization: token,
			},
		})
		.then((response) => {
			const responseBody = response.body;
			const bidder = responseBody.find((item) => item.name === bidderName);
			const requestBody = { ...bidderBody, name: bidderName };
			if (bidder) {
				// Update
				return cy.request({
					url: DASHBOARD_API.RTB_BIDDER.getOne({ id: bidder.id }),
					method: "PUT",
					headers: {
						Authorization: token,
					},
					body: requestBody,
				});
			} else {
				// Create
				return cy.request({
					url: DASHBOARD_API.RTB_BIDDER.getIndex(),
					method: "POST",
					headers: {
						Authorization: token,
					},
					body: requestBody,
				});
			}
		});
};
