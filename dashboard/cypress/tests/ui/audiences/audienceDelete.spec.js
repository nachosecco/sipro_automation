import { globalContent } from "../../../locators/globalLocators";
import { createOrUpdateAudience } from "../../../support/audienceCommands";
import { getAudienceName } from "../../../utils/resourceNameUtil";

describe("Audience delete test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Audience delete validations", () => {
		const audienceNames = getAudienceName("delete");

		createOrUpdateAudience(audienceNames).then(() => {
			// Visit audience index page
			cy.visit("/dashboard/audiences");

			// Search target audience
			cy.search(audienceNames.audienceName);

			// Wait for table to load and click action button and delete option
			cy.clickDataGridDeleteMenuItem();
			// Cancel and verify the record still exists
			cy.findByRole("button", { name: globalContent.CANCEL }).click();
			cy.reload();
			cy.search(audienceNames.audienceName);
			// Record should exist
			cy.findByRole("cell", { name: audienceNames.audienceName }).should("exist");
			cy.get('[data-field="name"]').eq(1).should("have.text", audienceNames.audienceName);

			// Delete the record
			cy.clickDataGridDeleteMenuItem();
			cy.findByRole("button", { name: globalContent.CONFIRM_DELETE }).click();

			// Validate that success pop up shows and displays correct text
			cy.validatePopupMessage(`${audienceNames.audienceName} ${globalContent.SUCCESSFULLY_DELETED_SUFFIX}`);

			// Verify advertiser is deleted
			cy.reload();
			cy.search(audienceNames.audienceName);
			// Record should not exist
			cy.findByRole("cell", { name: audienceNames.audienceName }).should("not.exist");
		});
	});
});
