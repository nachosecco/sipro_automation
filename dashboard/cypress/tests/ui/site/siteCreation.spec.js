import getToken from "../../../utils/getToken";
import siteLocators, { localeContent } from "../../../locators/siteLocators";
import { getSupplyNames } from "../../../utils/resourceNameUtil";
import { createOrUpdatePublisher } from "../../../support/supplyCommands";
import { globalContent } from "../../../locators/globalLocators";

describe("Site creation test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	afterEach(() => {});

	it("Site creation smoke test", () => {
		// Verify if base pub exists if not create it
		const supplyNames = getSupplyNames("Site creation smoke test");
		// Delete the site created by the most recent test run
		cy.deleteTargetEntity(getToken(), `${supplyNames.siteName}`, "site");
		// Create the parent pub
		createOrUpdatePublisher(supplyNames);

		// Visit sites index page
		cy.visit("/dashboard/sites");

		// Verify that page title is sites
		cy.findByRole("heading", { name: localeContent.INDEX_HEADING });

		// Add new site
		cy.clickElement(siteLocators.addSiteButton);
		cy.getByRole(siteLocators.publisherNameDropdown).type(supplyNames.publisherName);
		cy.findByRole("option", { name: supplyNames.publisherName }).click();

		// Verify elements are visible
		cy.verifyElementsExist(
			siteLocators.settingsTab,
			siteLocators.placementsTab,
			siteLocators.siteNameField,
			siteLocators.statusRadioActive,
			siteLocators.statusRadioInactive,
			siteLocators.defaultFloorField,
			siteLocators.RevenueShareField,
			siteLocators.UrlField
		);

		// Complete mandatory field
		cy.getByRole(siteLocators.siteNameField).type(supplyNames.siteName);

		// validate that the view report button is not visible until the form is saved
		cy.findByRole("link", { name: globalContent.VIEW_REPORT }).should("not.exist");

		// Submit form
		cy.findByRole("button", { name: globalContent.SAVE }).click();

		// Validate success message is displayed
		cy.validatePopupMessage(`${supplyNames.siteName} ${globalContent.SUCCESSFULLY_CREATED_SUFFIX}`);

		// View report button should be visible
		cy.findByRole("link", { name: globalContent.VIEW_REPORT }).should("exist");
	});
});
