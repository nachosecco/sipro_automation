import { createOrUpdatePublisher } from "../../../support/supplyCommands";
import { getSupplyNames } from "../../../utils/resourceNameUtil";
import publisherLocators from "../../../locators/publisherLocators";
import { DASHBOARD_API } from "../../../utils/serviceResources";

describe("Publisher download ad txt test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Publisher download ad txt smoke test", () => {
		const supplyNames = getSupplyNames("Publisher download ad txt smoke test");
		createOrUpdatePublisher(supplyNames);

		// Visit publisher index page
		cy.visit("/dashboard/publishers");

		cy.request({
			url: DASHBOARD_API.PUBLISHER.getIndex(),
			method: "GET",
			headers: {
				Authorization: window.localStorage.getItem("token"),
			},
		}).then((response) => {
			const responseBody = response.body;
			const publisher = responseBody.find((item) => item.name === supplyNames.publisherName);
			if (publisher) {
				// Search target publisher
				cy.search(supplyNames.publisherName);

				cy.findByRole("link", { name: supplyNames.publisherName }).click();
				// Go to verification tab and validate fields
				cy.clickElement(publisherLocators.verificationTab);

				cy.get("a:contains(DOWNLOAD ADS.TXT)").each(($a) => {
					cy.downloadFile($a.attr("href"), "cypress/downloads", "ads.txt");
					cy.readFile("cypress/downloads/ads.txt").then((adServers) => {
						expect(adServers).not.contain(
							`altitude-arena.com, ${
								publisher.adsTxtAccountId
							}, ${publisher.accountRelationship.toUpperCase()}`
						);

						expect(adServers).to.contain(
							`siprocalads.com, ${
								publisher.adsTxtAccountId
							}, ${publisher.accountRelationship.toUpperCase()}`
						);
					});
				});
			}
		});
	});
});
