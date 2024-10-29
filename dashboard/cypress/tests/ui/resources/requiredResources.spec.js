const { DASHBOARD_API } = require("../../../utils/serviceResources");

describe("Check expected resources are present in the dashboard-api", () => {
	it("check favicon & logos", () => {
		const resources = ["favicon.ico", "/images/core-assets/logo.svg", "/images/core-assets/email-logo.svg"];
		resources.forEach((resource) => {
			const url = `${DASHBOARD_API}${resource}`;
			cy.request({
				url,
				method: "GET",
			}).then((resp) => {
				expect(resp.status).to.eq(200);
			});
		});
	});
});
