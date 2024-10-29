import { DEFAULT_AUDIENCE_BODY } from "../fixtures/defaultAudienceRequestBody";
import getToken from "../utils/getToken";
import { DASHBOARD_API } from "../utils/serviceResources";

export const expresionSegmentForOne = (segmentId) => JSON.stringify({ nodeType: "SEGMENT", segmentId: segmentId });

export const createOrUpdateAudience = ({ token = getToken(), audienceName, audienceBody = DEFAULT_AUDIENCE_BODY }) => {
	return cy
		.request({
			url: DASHBOARD_API.AUDIENCE.getIndex(),
			method: "GET",
			headers: {
				Authorization: token,
			},
		})
		.then((response) => {
			const responseBody = response.body;

			const audience = responseBody.find((item) => item.name === audienceName);
			const requestBody = { ...audienceBody, name: audienceName };
			if (audience) {
				// Update
				return cy.request({
					url: DASHBOARD_API.AUDIENCE.getOne({ id: audience.id }),
					method: "PUT",
					headers: {
						Authorization: token,
					},
					body: requestBody,
				});
			} else {
				// Create
				return cy.request({
					url: DASHBOARD_API.AUDIENCE.getIndex(),
					method: "POST",
					headers: {
						Authorization: token,
					},
					body: requestBody,
				});
			}
		});
};

/*
This command will look for a target segment, type it into the search field and drag it to the drop zone
in audience form.
*/
Cypress.Commands.add("dragAndDropTargetSegment", (targetSegment) => {
	cy.getByRole(targetSegment)
		.eq(0)
		.click()
		.type("{enter}{downarrow}{downarrow}{downarrow}{downarrow}{downarrow}{downarrow}{enter}");
});
