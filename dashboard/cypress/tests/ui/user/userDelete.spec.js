import { createOrUpdateUser } from "../../../support/userCommands";
import { getUserNames } from "../../../utils/resourceNameUtil";
import { globalContent } from "../../../locators/globalLocators";

describe("User delete test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("User delete validations", () => {
		const userNames = getUserNames("User edit", "automation@test.com");
		createOrUpdateUser(userNames).then(() => {
			// Visit user index page
			cy.visit("/dashboard/users");

			// Search target user
			cy.search(userNames.firstName);

			// Wait for table to load and click action button and delete option
			cy.clickDataGridDeleteMenuItem();

			// Cancel and verify the record still exists
			cy.findByRole("button", { name: globalContent.CANCEL }).click();
			cy.reload();
			cy.search(userNames.firstName);
			const name = `${userNames.firstName} ${userNames.lastName}`;
			// Record should exist
			cy.findByRole("cell", { name: name }).should("exist");
			cy.get('[data-field="name"]').eq(1).should("have.text", name);

			// Delete the record
			cy.clickDataGridDeleteMenuItem();
			cy.findByRole("button", { name: globalContent.CONFIRM_DELETE }).click();

			// Validate that success pop up shows and displays correct text
			cy.validatePopupMessage(`${name} ${globalContent.SUCCESSFULLY_DELETED_SUFFIX}`);
		});
	});
});
