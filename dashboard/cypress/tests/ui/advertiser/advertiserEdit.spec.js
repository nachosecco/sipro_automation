import { localeContent } from "../../../locators/advertiserLocators";
import { globalContent } from "../../../locators/globalLocators";
import { createOrUpdateAdvertiser } from "../../../support/demandCommands";
import { getDemandNames } from "../../../utils/resourceNameUtil";

describe("Advertiser edit test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Advertiser edit", () => {
		const demandNames = getDemandNames("Advertiser edit");
		createOrUpdateAdvertiser(demandNames).then(() => {
			// Visit advertiser index page
			cy.visit("/dashboard/advertisers");
			// Look for base advertiser
			cy.search(demandNames.advertiserName);

			// Wait for table to load and click action button and edit option
			cy.clickDataGridEditMenuItem();

			// Edit advertiser form and submit
			const editedName = `${demandNames.advertiserName} updated`;
			cy.findByRole("textbox", { name: localeContent.FIELD_NAMES.NAME }).clear().type(editedName);
			cy.findByRole("spinbutton", { name: localeContent.FIELD_NAMES.DEMAND_FEE_PERCENTAGE }).clear().type("20");
			cy.findByRole("button", { name: globalContent.SAVE }).click();

			// Validate pop up is visible and displaying correct text
			cy.validatePopupMessage(`${editedName} ${globalContent.SUCCESSFULLY_UPDATED_SUFFIX}`);

			// Set name back to original and save form so that subsequent test runs can find it
			cy.findByRole("textbox", { name: localeContent.FIELD_NAMES.NAME }).clear().type(demandNames.advertiserName);
			cy.findByRole("spinbutton", { name: localeContent.FIELD_NAMES.DEMAND_FEE_PERCENTAGE }).clear().type("10");
			cy.findByRole("button", { name: globalContent.SAVE }).click();
			cy.validatePopupMessage(`${demandNames.advertiserName} ${globalContent.SUCCESSFULLY_UPDATED_SUFFIX}`);
		});
	});
});
