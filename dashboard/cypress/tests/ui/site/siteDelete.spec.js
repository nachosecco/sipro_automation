import { globalContent } from "../../../locators/globalLocators";
import { createOrUpdateSite } from "../../../support/supplyCommands";
import { getSupplyNames } from "../../../utils/resourceNameUtil";

describe("Site delete test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Site delete smoke test", () => {
		const supplyNames = getSupplyNames("Site delete smoke test");
		createOrUpdateSite(supplyNames);

		// Visit sites index page
		cy.visit("/dashboard/sites");

		// Search target site
		cy.search(supplyNames.siteName);

		// Wait for table to load and click action button and delete option
		cy.clickDataGridDeleteMenuItem();

		// Cancel and verify the record still exists
		cy.findByRole("button", { name: globalContent.CANCEL }).click();
		cy.reload();
		cy.search(supplyNames.siteName);

		cy.findByRole("cell", { name: supplyNames.siteName }).should("exist");
		cy.get('[data-field="name"]').eq(1).should("have.text", `${supplyNames.siteName}`);

		// Delete the record
		cy.clickDataGridDeleteMenuItem();
		cy.findByRole("button", { name: globalContent.CONFIRM_DELETE }).click();

		// Validate that success pop up shows and displays correct text
		cy.validatePopupMessage(`${supplyNames.siteName} was successfully deleted`);

		// Verify site is deleted
		cy.reload();
		cy.search(supplyNames.siteName);
		// Record should not exist
		cy.findByRole("cell", { name: supplyNames.siteName }).should("not.exist");
	});
});
