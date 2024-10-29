import { createOrUpdateInsertionOrder } from "../../../support/demandCommands";
import { getDemandNames } from "../../../utils/resourceNameUtil";
import { globalContent } from "../../../locators/globalLocators";

describe("Insertion delete test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Insertion delete validations", () => {
		const resourceNames = getDemandNames("Insertion Order Delete");
		createOrUpdateInsertionOrder(resourceNames).then((response) => {
			const insertionOrder = response.body;

			// Visit insertion index page
			cy.visit("/dashboard/insertion-orders");

			// Search target insertion
			cy.search(insertionOrder.name);

			// Wait for table to load and click action button and delete option
			cy.clickDataGridDeleteMenuItem();

			// Cancel and verify the record still exists
			cy.findByRole("button", { name: globalContent.CANCEL }).click();
			cy.reload();
			cy.search(insertionOrder.name);

			cy.get('[data-field="name"]').eq(1).should("have.text", `${insertionOrder.name}`);

			// Delete the record
			cy.clickDataGridDeleteMenuItem();

			cy.findByRole("button", { name: globalContent.DELETE }).click();

			// Validate that success pop up shows and displays correct text
			cy.validatePopupMessage(`${insertionOrder.name} ${globalContent.SUCCESSFULLY_DELETED_SUFFIX}`);
		});
	});
});
