import { roleLocators } from "../../../locators/roleLocators";
import { globalContent } from "../../../locators/globalLocators";
import { getRoleName } from "../../../utils/resourceNameUtil";
import { createOrUpdateUserRoles } from "../../../support/userCommands";

describe("Role edit tests", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Role edit test", () => {
		const roleName = getRoleName("edit");
		createOrUpdateUserRoles({ roleName }).then(() => {
			// Visit roles index page
			cy.visit("/dashboard/roles");

			// Access role form
			cy.search(roleName);
			cy.clickDataGridEditMenuItem();

			const updatedName = `${roleName} updated`;

			// Update the entity and submit
			cy.getByRole(roleLocators.nameField).clear().type(updatedName);
			// Submit form
			cy.findByRole("button", { name: globalContent.SAVE }).click();

			// Validate pop up is visible and it's text
			cy.validatePopupMessage(`${updatedName} ${globalContent.SUCCESSFULLY_UPDATED_SUFFIX}`);

			// Set name back to original and save form so that subsequent test runs can find it
			cy.getByRole(roleLocators.nameField).clear().type(roleName);

			cy.findByRole("button", { name: globalContent.SAVE }).click();

			// Success message should display
			cy.validatePopupMessage(`${roleName} ${globalContent.SUCCESSFULLY_UPDATED_SUFFIX}`);
		});
	});
});
