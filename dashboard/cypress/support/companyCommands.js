import DEFAULT_COMPANY_REQUEST_BODY from "../fixtures/defaultCompanyRequestBody";
import getToken from "../utils/getToken";
import { DASHBOARD_API } from "../utils/serviceResources";
const data = require("../fixtures/companyCreationData.json");

// This command will fetch the API looking for a company, if that company does not exist it will create it
Cypress.Commands.add("checkBaseCompanyRequest", (token, companyName = data.baseName) => {
	cy.request({
		url: DASHBOARD_API.COMPANY.getIndex(),
		method: "GET",
		headers: {
			Authorization: token,
		},
	}).then((companyResponse) => {
		const body = companyResponse.body;
		const targetCompany = body.find((o) => o.name === companyName);
		if (!targetCompany) {
			cy.request({
				url: DASHBOARD_API.COMPANY.getIndex(),
				method: "POST",
				headers: {
					Authorization: token,
				},
				body: {
					name: companyName,
					status: data.status,
					companyDomain: data.companyDomain,
					confidential: data.confidential,
					showHelpText: data.showHelpText,
					privacyPolicyUrl: data.privacyPolicyUrl,
					tcUrl: data.tcUrl,
					rootDomain: data.rootDomain,
					arenaDomain: data.arenaDomain,
					mobileDomain: data.mobileDomain,
					eventDomain: data.eventDomain,
					rtbDomain: data.rtbDomain,
					cookieDomain: data.cookieDomain,
					publisherDomain: data.publisherDomain,
					manageDomain: data.manageDomain,
					mediaDomain: data.mediaDomain,
					cdnDomain: data.cdnDomain,
					branding: data.branding,
					supportEmail: data.supportEmail,
					reportingEmail: data.reportingEmail,
					cloneRoles: data.cloneRoles,
					reportingLimitRtbDimensions: data.reportingLimitRtbDimensions,
					reportingLimitRtbDimensionsRange: data.reportingLimitRtbDimensionsRange,
					reportingLimitNetworkDimensions: data.reportingLimitNetworkDimensions,
					reportingLimitNetworkDimensionsRange: data.reportingLimitNetworkDimensionsRange,
					reportingLimitCampaignDimensions: data.reportingLimitCampaignDimensions,
					reportingLimitCampaignDimensionsRange: data.reportingLimitCampaignDimensionsRange,
					reportingLimitPublisherDimensions: data.reportingLimitPublisherDimensions,
					reportingLimitPublisherDimensionsRange: data.reportingLimitPublisherDimensionsRange,
					defaultRevShare: data.defaultRevShare,
					defaultMargin: data.defaultMargin,
					minBitrate: data.minBitrate,
					maxBitrate: data.maxBitrate,
					allowIVTFiltering: data.allowIVTFiltering,
					enforceIVTFiltering: data.enforceIVTFiltering,
					ivtProbabilityThreshold: data.ivtProbabilityThreshold,
					defaultRtbMargin: data.defaultRtbMargin,
					bidRequestMultiplier: data.bidRequestMultiplier,
					opportunityCostMultiplier: data.opportunityCostMultiplier,
				},
			});
		}
	});
});

export const createOrUpdateCompany = ({
	token = getToken(),
	companyName,
	companyBody = DEFAULT_COMPANY_REQUEST_BODY,
}) => {
	return cy
		.request({
			url: DASHBOARD_API.COMPANY.getIndex(),
			method: "GET",
			headers: {
				Authorization: token,
			},
		})
		.then((response) => {
			const responseBody = response.body;
			const company = responseBody.find((item) => item.name === companyName);
			const requestBody = { ...companyBody, name: companyName };
			if (company) {
				// Update
				return cy.request({
					url: DASHBOARD_API.COMPANY.getOne({ id: company.id }),
					method: "PUT",
					headers: {
						Authorization: token,
					},
					// Branding companyId starts null but afterward needs to be tied to the company using the company's id. Seems like that should be immutable from the client's perspective...maybe a refactor in the future
					body: { ...requestBody, branding: { ...requestBody.branding, companyId: company.id } },
				});
			} else {
				// Create
				return cy.request({
					url: DASHBOARD_API.COMPANY.getIndex(),
					method: "POST",
					headers: {
						Authorization: token,
					},
					body: requestBody,
				});
			}
		});
};
