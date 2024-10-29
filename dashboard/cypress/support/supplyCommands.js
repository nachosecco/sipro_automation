import {
	DEFAULT_PLACEMENT_ALIGNMENTS,
	DEFAULT_PLACEMENT_BODY,
	DEFAULT_PUBLISHER_BODY,
	DEFAULT_SITE_BODY,
} from "../fixtures/defaultSupplySideCreationData";
import getToken from "../utils/getToken";
import { DASHBOARD_API } from "../utils/serviceResources";

const getHeaders = (token, companyOverride) => ({
	Authorization: token,
	"X-COMPANY-OVERRIDE": companyOverride,
});

export const createOrUpdatePublisher = ({
	token = getToken(),
	publisherName,
	publisherBody = DEFAULT_PUBLISHER_BODY,
	companyOverride,
}) => {
	const headers = getHeaders(token, companyOverride);
	return cy
		.request({
			url: DASHBOARD_API.PUBLISHER.getIndex(),
			method: "GET",
			headers,
		})
		.then((response) => {
			const responseBody = response.body;
			const publisher = responseBody.find((item) => item.name === publisherName);
			const requestBody = { ...publisherBody, name: publisherName };
			if (publisher) {
				// Update
				cy.request({
					url: DASHBOARD_API.PUBLISHER.getOne({ id: publisher.id }),
					method: "PUT",
					headers,
					body: requestBody,
				});
			} else {
				// Create
				cy.request({
					url: DASHBOARD_API.PUBLISHER.getIndex(),
					method: "POST",
					headers,
					body: requestBody,
				});
			}
		});
};

export const createOrUpdateSite = ({
	token = getToken(),
	siteName,
	siteBody = DEFAULT_SITE_BODY,
	publisherName,
	publisherBody,
	companyOverride,
}) => {
	const headers = getHeaders(token, companyOverride);
	return createOrUpdatePublisher({ publisherName, publisherBody, companyOverride }).then((response) => {
		const parentPublisherId = response.body.id;
		cy.request({
			url: DASHBOARD_API.SITE.getIndex(),
			method: "GET",
			headers,
		}).then((response) => {
			const responseBody = response.body;
			const site = responseBody.find((item) => item.name === siteName);
			const requestBody = { ...siteBody, name: siteName, publisherId: parentPublisherId };
			if (site) {
				// Update
				cy.request({
					url: DASHBOARD_API.SITE.getOne({ id: site.id }),
					method: "PUT",
					headers,
					body: requestBody,
				});
			} else {
				// Create
				cy.request({
					url: DASHBOARD_API.SITE.getIndex(),
					method: "POST",
					headers,
					body: requestBody,
				});
			}
		});
	});
};

export const createOrUpdatePlacement = ({
	token = getToken(),
	placementName,
	placementBody = DEFAULT_PLACEMENT_BODY,
	siteName,
	siteBody,
	publisherName,
	publisherBody,
	companyOverride,
}) => {
	const headers = getHeaders(token, companyOverride);
	return createOrUpdateSite({ publisherName, publisherBody, siteName, siteBody, companyOverride }).then(
		(response) => {
			const parentSiteId = response.body.id;
			cy.request({
				url: DASHBOARD_API.PLACEMENT.getIndex(),
				method: "GET",
				headers,
			}).then((response) => {
				const responseBody = response.body;
				const placement = responseBody.find((item) => item.name === placementName);
				const requestBody = {
					...placementBody,
					name: placementName,
					siteId: parentSiteId,
					cloneAlignments: false,
				};
				if (placement) {
					// Update
					cy.request({
						url: DASHBOARD_API.PLACEMENT.getOne({ id: placement.id }),
						method: "PUT",
						headers,
						body: requestBody,
					});
				} else {
					// Create
					cy.request({
						url: DASHBOARD_API.PLACEMENT.getIndex(),
						method: "POST",
						headers,
						body: requestBody,
					});
				}
			});
		}
	);
};

export const createOrUpdatePlacementAlignments = ({
	token = getToken(),
	placementAlignmentBody = DEFAULT_PLACEMENT_ALIGNMENTS,
	placementId,
	medias,
	programmaticDemands,
}) => {
	// create or Update
	return cy.request({
		url: DASHBOARD_API.PLACEMENT.getAlignments({ id: placementId }),
		method: "PUT",
		headers: {
			Authorization: token,
		},
		body: { ...placementAlignmentBody, id: placementId, media: medias, programmaticDemands: programmaticDemands },
	});
};

export const getAllAlignments = ({ token = getToken() }) => {
	return cy.request({
		url: DASHBOARD_API.PLACEMENT.getAllAlignments(),
		method: "GET",
		headers: {
			Authorization: token,
		},
	});
};

export const cleanupPlacement = (placementName, companyOverride) => {
	const pathDeleteResource = (resource) => {
		return DASHBOARD_API.PLACEMENT.getOne({ id: resource.id });
	};
	const indexPathResources = DASHBOARD_API.PLACEMENT.getIndex();

	const filterResourceToDelete = (resource) => resource.name === placementName;
	cy.cleanResources({ indexPathResources, pathDeleteResource, filterResourceToDelete, companyOverride });
};
