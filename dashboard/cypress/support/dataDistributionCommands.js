import getToken from "../utils/getToken";

import { DASHBOARD_API } from "../utils/serviceResources";

const DEFAULT_DATA_DISTRIBUTION_BODY = {
	allowedCompanyIds: [1],
	defaultName: "Automation default Name",
	displayName: "Automation Displayed Name",
};

export const createOrUpdateDataDistribution = ({
	displayName,
	token = getToken(),
	dataDistributionBody = DEFAULT_DATA_DISTRIBUTION_BODY,
}) => {
	return cy
		.request({
			url: DASHBOARD_API.DATA_DISTRIBUTION.getIndex(),
			method: "GET",
			headers: {
				Authorization: token,
			},
		})
		.then((response) => {
			const responseBody = response.body;
			const dataDistribution = responseBody.find((item) => item.displayName === displayName);

			const requestBody = { ...dataDistributionBody, displayName: displayName };
			if (dataDistribution) {
				// Update
				return cy.request({
					url: DASHBOARD_API.DATA_DISTRIBUTION.getOne({ id: dataDistribution.id }),
					method: "PUT",
					headers: {
						Authorization: token,
					},
					body: requestBody,
				});
			} else {
				// Create
				return cy.request({
					url: DASHBOARD_API.DATA_DISTRIBUTION.getIndex(),
					method: "POST",
					headers: {
						Authorization: token,
					},
					body: { ...dataDistributionBody, displayName: displayName },
				});
			}
		});
};
