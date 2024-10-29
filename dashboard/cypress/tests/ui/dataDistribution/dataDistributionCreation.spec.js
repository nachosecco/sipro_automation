import { dataDistributionLocators, localeContent } from "../../../locators/dataDistributionLocators";

import { globalContent } from "../../../locators/globalLocators";
import { DASHBOARD_API } from "../../../utils/serviceResources";
import { defaultResourceCleanup } from "../../../utils/cleanupCommands";

describe("Data Distribution creation test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Data Distribution creation", () => {
		// Visit advertiser index page
		const name = `Automation Entity create data distribution`;
		defaultResourceCleanup(DASHBOARD_API.DATA_DISTRIBUTION, "displayName", name);
		cy.visit("/dashboard/data-distributions");

		// Verify that page title is advertisers
		cy.findByRole("heading", { name: localeContent.INDEX_HEADING });

		// Assert presence of add advertiser button and click it
		cy.clickElement(dataDistributionLocators.addDistributionDropdown);

		// Validate these elements are visible
		cy.verifyElementsExist(
			dataDistributionLocators.displayNameField,
			dataDistributionLocators.defaultNameField,
			dataDistributionLocators.allowAccessField
		);

		// Fill the form and submit
		cy.getByRole(dataDistributionLocators.displayNameField).type(name);
		cy.getByRole(dataDistributionLocators.defaultNameField).type(name);
		// Select column6 company
		cy.getByRole(dataDistributionLocators.allowAccessField).type("Column6");
		["Column6"].forEach((label) => cy.findByRole("option", { name: label }).click());

		cy.findByRole("button", { name: globalContent.SAVE }).click();

		// Validate pop message
		cy.validatePopupMessage(`${name} ${globalContent.SUCCESSFULLY_CREATED_SUFFIX}`);
	});
});
