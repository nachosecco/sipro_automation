import { globalContent } from "../../../locators/globalLocators";
import { getSupplyNames } from "../../../utils/resourceNameUtil";
import siteLocators from "../../../locators/siteLocators";
import { createOrUpdateSite } from "../../../support/supplyCommands";

describe("Site edit test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Site edit smoke test", () => {
		const supplyNames = getSupplyNames("Site edit smoke test");
		createOrUpdateSite(supplyNames);

		// Visit sites index page
		cy.visit("/dashboard/sites");
		// Search for target site
		cy.search(supplyNames.siteName);
		// cy.searchIndexPage(supplyNames.siteName);

		// Wait for table to load, click action button and edit
		cy.clickDataGridEditMenuItem();

		// Edit site form and submit
		const editedName = "Edited Name";
		cy.getByRole(siteLocators.siteNameField).clear().type(editedName);
		cy.getByRole(siteLocators.defaultFloorField).clear().type(1);
		cy.getByRole(siteLocators.RevenueShareField).clear().type(5);
		cy.getByRole(siteLocators.UrlField).clear().type("test.com");

		// Save Form
		cy.intercept("PUT", "**/sites/**").as("update");
		cy.findByRole("button", { name: globalContent.SAVE }).click();

		// Validate site PUT request method endpoint status code
		cy.wait("@update").its("response.statusCode").should("eq", 200);

		// Validate pop up is visible and displaying correct text
		cy.validatePopupMessage(`${editedName} ${globalContent.SUCCESSFULLY_UPDATED_SUFFIX}`);

		// Set name back to original and save form so that subsequent test runs can find it
		cy.getByRole(siteLocators.siteNameField).clear().type(supplyNames.siteName);
		cy.findByRole("button", { name: globalContent.SAVE }).click();
		cy.validatePopupMessage(`${supplyNames.siteName} ${globalContent.SUCCESSFULLY_UPDATED_SUFFIX}`);
	});
});
