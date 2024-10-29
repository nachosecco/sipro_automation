import { createOrUpdateCampaign } from "../../../support/demandCommands";
import { globalContent } from "../../../locators/globalLocators";
import { getDemandNames } from "../../../utils/resourceNameUtil";

describe("Campaign delete test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Campaign delete validations", () => {
		const resourceNames = getDemandNames("Campaign Delete");

		createOrUpdateCampaign(resourceNames).then((response) => {
			const campaign = response.body;

			// Visit campaigns index page
			cy.visit("/dashboard/campaigns");

			// Search target campaign
			cy.search(campaign.name);

			// Wait for table to load and click action button and delete option
			cy.clickDataGridDeleteMenuItem();

			// Cancel and verify the record still exists
			cy.findByRole("button", { name: globalContent.CANCEL }).click();
			cy.reload();
			cy.search(campaign.name);
			// Record should exist
			cy.findByRole("cell", { name: campaign.name }).should("exist");
			cy.get('[data-field="name"]').eq(1).should("have.text", campaign.name);

			// Wait for table to load and click action button and delete option
			cy.clickDataGridDeleteMenuItem();
			cy.findByRole("button", { name: globalContent.CONFIRM_DELETE }).click();

			// Validate that success pop up shows and displays correct text
			cy.validatePopupMessage(`${campaign.name} ${globalContent.SUCCESSFULLY_DELETED_SUFFIX}`);

			// Verify campaign is deleted
			cy.reload();
			cy.search(campaign.name);
			// Record should not exist
			cy.findByRole("cell", { name: campaign.name }).should("not.exist");
		});
	});
});
