import { globalContent } from "../../../locators/globalLocators";
import { createOrUpdatePublisher } from "../../../support/supplyCommands";
import { getSupplyNames } from "../../../utils/resourceNameUtil";

describe("Publisher delete test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Publisher delete smoke test", () => {
		const supplyNames = getSupplyNames("Publisher delete smoke test");
		createOrUpdatePublisher(supplyNames);

		// Visit publisher index page
		cy.visit("/dashboard/publishers");

		// Search target publisher
		cy.search(supplyNames.publisherName);

		// Wait for table to load and click action button and delete option
		cy.clickDataGridDeleteMenuItem();

		// Cancel and verify the record still exists
		cy.findByRole("button", { name: globalContent.CANCEL }).click();
		cy.reload();
		cy.search(supplyNames.publisherName);

		cy.findByRole("cell", { name: supplyNames.publisherName }).should("exist");
		cy.get('[data-field="name"]').eq(1).should("have.text", `${supplyNames.publisherName}`);

		// Delete the record
		cy.clickDataGridDeleteMenuItem();
		cy.findByRole("button", { name: globalContent.CONFIRM_DELETE }).click();

		// Validate that success pop up shows and displays correct text
		cy.validatePopupMessage(`${supplyNames.publisherName} ${globalContent.SUCCESSFULLY_DELETED_SUFFIX}`);

		// Verify site is deleted
		cy.reload();
		cy.search(supplyNames.publisherName);
		// Record should not exist
		cy.findByRole("cell", { name: supplyNames.publisherName }).should("not.exist");
	});
});
