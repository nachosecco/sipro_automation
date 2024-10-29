import { createOrUpdateUser } from "../../../support/userCommands";
import { getUserNames } from "../../../utils/resourceNameUtil";
import { localeContent } from "../../../locators/userLocators";
import { globalContent } from "../../../locators/globalLocators";

describe("User edit test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Edit user validations", () => {
		const userNames = getUserNames("User edit", "automation@test.com");
		createOrUpdateUser(userNames).then(() => {
			// Visit user index page
			cy.visit("/dashboard/users");
			// Search for target user
			cy.search(userNames.firstName);

			cy.clickDataGridEditMenuItem();

			const editedFirstName = `${userNames.firstName} edit`;

			// Edit the form
			cy.findByRole("textbox", { name: localeContent.FIELDS.FIRST_NAME }).clear().type(editedFirstName);
			cy.findByRole("textbox", { name: localeContent.FIELDS.LAST_NAME }).clear().type(userNames.lastName);
			// Submit the form
			cy.findByRole("button", { name: globalContent.SAVE }).click();

			const editedName = `${editedFirstName} ${userNames.lastName}`;

			// Validate pop up is visible and displaying correct text
			cy.validatePopupMessage(`${editedName} ${globalContent.SUCCESSFULLY_UPDATED_SUFFIX}`);

			// Set name back to original and save form so that subsequent test runs can find it
			cy.findByRole("textbox", { name: localeContent.FIELDS.FIRST_NAME }).clear().type(userNames.firstName);
			cy.findByRole("button", { name: globalContent.SAVE }).click();

			const name = `${userNames.firstName} ${userNames.lastName}`;

			cy.validatePopupMessage(`${name} ${globalContent.SUCCESSFULLY_UPDATED_SUFFIX}`);
		});
	});
});
