import { globalContent } from "../../../locators/globalLocators";
import { createOrUpdateAdvertiser } from "../../../support/demandCommands";
import { getDemandNames } from "../../../utils/resourceNameUtil";

describe("Advertiser delete test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Advertiser delete", () => {
		const resourceNames = getDemandNames("Advertiser delete");
		const advertiserName = resourceNames.advertiserName;

		createOrUpdateAdvertiser(resourceNames).then((response) => {
			const advertiser = response.body;
			// Visit advertiser index page
			cy.visit("/dashboard/advertisers");

			// Search target advertiser
			cy.search(advertiser.name);

			// Wait for table to load and click action button and delete option
			cy.clickDataGridDeleteMenuItem();

			// Cancel and verify the record still exists
			cy.findByRole("button", { name: globalContent.CANCEL }).click();
			cy.reload();
			cy.search(advertiserName);
			// Record should exist
			cy.findByRole("cell", { name: advertiserName }).should("exist");
			cy.get('[data-field="name"]').eq(1).should("have.text", advertiserName);

			// Delete the record
			cy.clickDataGridDeleteMenuItem();
			cy.findByRole("button", { name: globalContent.CONFIRM_DELETE }).click();

			// Validate that success pop up shows and displays correct text
			cy.validatePopupMessage(`${resourceNames.advertiserName} ${globalContent.SUCCESSFULLY_DELETED_SUFFIX}`);

			// Verify advertiser is deleted
			cy.reload();
			cy.search(advertiserName);
			// Record should not exist
			cy.findByRole("cell", { name: advertiserName }).should("not.exist");
		});
	});
});
