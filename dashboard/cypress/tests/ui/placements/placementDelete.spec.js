import { globalContent } from "../../../locators/globalLocators";
import { createOrUpdatePlacement } from "../../../support/supplyCommands";
import { getSupplyNames } from "../../../utils/resourceNameUtil";

describe("Placement delete test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Placement delete", () => {
		// Check for base entity
		const supplyNames = getSupplyNames("Placement delete smoke test");
		createOrUpdatePlacement(supplyNames);

		// Visit placements index page
		cy.visit("/dashboard/placements");

		// Search target placement
		cy.search(supplyNames.publisherName);

		// Wait for table to load and Click action button and delete option
		cy.clickDataGridDeleteMenuItem();

		// Cancel and verify the record still exists
		cy.findByRole("button", { name: globalContent.CANCEL }).click();
		cy.reload();
		cy.search(supplyNames.publisherName);
		// Record should exist
		cy.findByRole("cell", { name: supplyNames.placementName }).should("exist");
		cy.get('[data-field="name"]').eq(1).should("have.text", `${supplyNames.placementName}`);

		// Delete the record
		cy.clickDataGridDeleteMenuItem();
		cy.findByRole("button", { name: globalContent.CONFIRM_DELETE }).click();

		// Validate that success pop up shows and displays correct text
		cy.validatePopupMessage(`${supplyNames.placementName} was successfully deleted`);

		// Verify placement is deleted
		cy.reload();
		cy.search(supplyNames.publisherName);
		// Record should not exist
		cy.findByRole("cell", { name: supplyNames.placementName }).should("not.exist");
	});
});
