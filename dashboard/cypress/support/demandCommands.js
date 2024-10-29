import {
	DEFAULT_MEDIA_BODY,
	DEFAULT_CAMPAIGN_BODY,
	DEFAULT_ADVERTISER_BODY,
	DEFAULT_INSERTION_ORDER_BODY,
	DEFAULT_PROGRAMMATIC_REQUEST_BODY,
	DEFAULT_DEMAND_ALIGNMENTS,
	DEFAULT_MEDIA_ALIGNMENTS,
} from "../fixtures/defaultDemandSideCreationData";
import getToken from "../utils/getToken";
import { DASHBOARD_API } from "../utils/serviceResources";
import { createOrUpdateBidder } from "./bidderCommands";

export const createOrUpdateAdvertiser = ({
	token = getToken(),
	advertiserName,
	advertiserBody = DEFAULT_ADVERTISER_BODY,
}) => {
	return cy
		.request({
			url: DASHBOARD_API.ADVERTISER.getIndex(),
			method: "GET",
			headers: {
				Authorization: token,
			},
		})
		.then((response) => {
			const responseBody = response.body;
			const advertiser = responseBody.find((item) => item.name === advertiserName);
			const requestBody = { ...advertiserBody, name: advertiserName };
			if (advertiser) {
				// Update
				return cy.request({
					url: DASHBOARD_API.ADVERTISER.getOne({ id: advertiser.id }),
					method: "PUT",
					headers: {
						Authorization: token,
					},
					body: requestBody,
				});
			} else {
				// Create
				return cy.request({
					url: DASHBOARD_API.ADVERTISER.getIndex(),
					method: "POST",
					headers: {
						Authorization: token,
					},
					body: requestBody,
				});
			}
		});
};

export const createOrUpdateInsertionOrder = ({
	token = getToken(),
	insertionOrderName,
	insertionOrderBody = DEFAULT_INSERTION_ORDER_BODY,
	advertiserName,
	advertiserBody,
}) => {
	return createOrUpdateAdvertiser({ advertiserName, advertiserBody }).then((response) => {
		const parentAdvertiserId = response.body.id;

		cy.request({
			url: DASHBOARD_API.INSERTION_ORDER.getIndex(),
			method: "GET",
			headers: {
				Authorization: token,
			},
		}).then((response) => {
			const responseBody = response.body;
			const insertionOrder = responseBody.find((item) => item.name === insertionOrderName);
			const requestBody = { ...insertionOrderBody, name: insertionOrderName, advId: parentAdvertiserId };
			if (insertionOrder) {
				// Update
				cy.request({
					url: DASHBOARD_API.INSERTION_ORDER.getOne({ id: insertionOrder.id }),
					method: "PUT",
					headers: {
						Authorization: token,
					},
					body: requestBody,
				});
			} else {
				// Create
				cy.request({
					url: DASHBOARD_API.INSERTION_ORDER.getIndex(),
					method: "POST",
					headers: {
						Authorization: token,
					},
					body: requestBody,
				});
			}
		});
	});
};

export const createOrUpdateCampaign = ({
	token = getToken(),
	campaignName,
	campaignBody = DEFAULT_CAMPAIGN_BODY,
	insertionOrderName,
	insertionOrderBody,
	advertiserName,
	advertiserBody,
}) => {
	return createOrUpdateInsertionOrder({
		advertiserName,
		advertiserBody,
		insertionOrderName,
		insertionOrderBody,
	}).then((response) => {
		const parentInsertionOrderId = response.body.id;

		cy.request({
			url: DASHBOARD_API.CAMPAIGN.getIndex(),
			method: "GET",
			headers: {
				Authorization: token,
			},
		}).then((response) => {
			const responseBody = response.body;
			const campaign = responseBody.find((item) => item.name === campaignName);
			const requestBody = { ...campaignBody, name: campaignName, insertionOrderId: parentInsertionOrderId };
			if (campaign) {
				// Update
				cy.request({
					url: DASHBOARD_API.CAMPAIGN.getOne({ id: campaign.id }),
					method: "PUT",
					headers: {
						Authorization: token,
					},
					body: requestBody,
				});
			} else {
				// Create
				cy.request({
					url: DASHBOARD_API.CAMPAIGN.getIndex(),
					method: "POST",
					headers: {
						Authorization: token,
					},
					body: requestBody,
				});
			}
		});
	});
};

export const createOrUpdateMedia = ({
	token = getToken(),
	mediaName,
	mediaBody = DEFAULT_MEDIA_BODY,
	campaignName,
	campaignBody,
	insertionOrderName,
	insertionOrderBody,
	advertiserName,
	advertiserBody,
}) => {
	return createOrUpdateCampaign({
		advertiserName,
		advertiserBody,
		insertionOrderName,
		insertionOrderBody,
		campaignName,
		campaignBody,
	}).then((response) => {
		const parentCampaignId = response.body.id;

		cy.request({
			url: DASHBOARD_API.MEDIA.getIndex(),
			method: "GET",
			headers: {
				Authorization: token,
			},
		}).then((response) => {
			const responseBody = response.body;
			const media = responseBody.find((item) => item.name === mediaName);
			const requestBody = { ...mediaBody, name: mediaName, campaignId: parentCampaignId };
			if (media) {
				// Update
				cy.request({
					url: DASHBOARD_API.MEDIA.getOne({ id: media.id }),
					method: "PUT",
					headers: {
						Authorization: token,
					},
					body: requestBody,
				});
			} else {
				// Create
				cy.request({
					url: DASHBOARD_API.MEDIA.getIndex(),
					method: "POST",
					headers: {
						Authorization: token,
					},
					body: requestBody,
				});
			}
		});
	});
};

// This func only support single bidder demand, we would need to refactor to support multi bidders when necessary
export const createOrUpdateProgrammaticDemand = ({
	token = getToken(),
	programmaticName,
	programmaticBody = DEFAULT_PROGRAMMATIC_REQUEST_BODY,
	bidderName,
	bidderBody,
	seats = [],
	headerExtensions,
}) => {
	return createOrUpdateBidder({
		token,
		bidderName,
		bidderBody,
	}).then((response) => {
		const bidder = response.body;
		const programmaticBidderConfigs = {
			rtbBidderId: bidder.id,
			rtbBidderSeats: seats,
		};
		const requestBody = {
			...programmaticBody,
			name: programmaticName,
			programmaticBidderConfigs: [programmaticBidderConfigs],
		};

		if (requestBody.dealId != null) {
			requestBody.dealId = requestBody.dealId + `${new Date().getTime()}`;
		}
		cy.request({
			url: DASHBOARD_API.PROGRAMMATIC_DEMAND.getIndex(),
			method: "GET",
			headers: {
				Authorization: token,
				...headerExtensions,
			},
		}).then((response) => {
			const body = response.body;
			const programmatic = body.find((o) => o.name === programmaticName);

			if (programmatic) {
				// Update
				return cy.request({
					url: DASHBOARD_API.PROGRAMMATIC_DEMAND.getOne({ id: programmatic.id }),
					method: "PUT",
					headers: {
						Authorization: token,
						...headerExtensions,
					},
					body: { ...requestBody, id: programmatic.id },
				});
			} else {
				// Create
				return cy.request({
					url: DASHBOARD_API.PROGRAMMATIC_DEMAND.getIndex(),
					method: "POST",
					headers: {
						Authorization: token,
						...headerExtensions,
					},
					body: requestBody,
				});
			}
		});
	});
};

export const createOrUpdateMediaAlignments = ({
	token = getToken(),
	defaultMediaAlignments = DEFAULT_MEDIA_ALIGNMENTS,
	placements,
	mediaId,
}) => {
	// create or Update
	return cy.request({
		url: DASHBOARD_API.MEDIA.getAlignments({ id: mediaId }),
		method: "PUT",
		headers: {
			Authorization: token,
		},
		body: {
			...defaultMediaAlignments,
			id: mediaId,
			placements: placements.map(({ id }) => ({ id })),
		},
	});
};

export const createOrUpdateDemandAlignments = ({
	token = getToken(),
	demandAlignmentsBody = DEFAULT_DEMAND_ALIGNMENTS,
	demandId,
	placements,
}) => {
	// create or Update
	return cy.request({
		url: DASHBOARD_API.PROGRAMMATIC_DEMAND.getAlignments({ id: demandId }),
		method: "PUT",
		headers: {
			Authorization: token,
		},
		body: {
			...demandAlignmentsBody,
			id: demandId,
			placements: placements.map(({ id }) => ({ id })),
		},
	});
};

export const cleanupDemand = (demandName) => {
	const pathDeleteResource = (resource) => {
		return DASHBOARD_API.PROGRAMMATIC_DEMAND.getOne({ id: resource.id });
	};
	const indexPathResources = DASHBOARD_API.PROGRAMMATIC_DEMAND.getIndex();

	const filterResourceToDelete = (resource) => resource.name === demandName;
	cy.cleanResources({ indexPathResources, pathDeleteResource, filterResourceToDelete });
};

export const cleanupMedia = (mediaName) => {
	const pathDeleteResource = (resource) => {
		return DASHBOARD_API.MEDIA.getOne({ id: resource.id });
	};
	const indexPathResources = DASHBOARD_API.MEDIA.getIndex();

	const filterResourceToDelete = (resource) => resource.name === mediaName;
	cy.cleanResources({ indexPathResources, pathDeleteResource, filterResourceToDelete });
};
