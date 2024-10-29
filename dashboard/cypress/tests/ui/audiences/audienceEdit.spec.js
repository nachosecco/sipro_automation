import { audienceLocators } from "../../../locators/audienceLocators";
import { globalContent } from "../../../locators/globalLocators";
import { createOrUpdateAudience } from "../../../support/audienceCommands";
import { getAudienceName } from "../../../utils/resourceNameUtil";

describe("Audience edit test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Valid audience edit", () => {
		const audienceNames = getAudienceName("edit");

		createOrUpdateAudience(audienceNames).then(() => {
			// Visit audience index page
			cy.visit("/dashboard/audiences");

			// Search for base entity and edit it
			cy.search(audienceNames.audienceName);
			cy.clickDataGridEditMenuItem();
			// Edit desired fields and submit
			const editedName = `${audienceNames.audienceName} updated`;
			cy.getByRole(audienceLocators.audienceNameField).clear().type(editedName);

			cy.findByRole("button", { name: globalContent.SAVE }).click();

			// Validate pop up is visible and displaying correct text
			cy.validatePopupMessage(`${editedName} ${globalContent.SUCCESSFULLY_UPDATED_SUFFIX}`);

			// Set name back to original and save form so that subsequent test runs can find it
			cy.getByRole(audienceLocators.audienceNameField).clear().type(audienceNames.audienceName);
			cy.findByRole("button", { name: globalContent.SAVE }).click();
			cy.validatePopupMessage(`${audienceNames.audienceName} ${globalContent.SUCCESSFULLY_UPDATED_SUFFIX}`);
		});
	});
});
