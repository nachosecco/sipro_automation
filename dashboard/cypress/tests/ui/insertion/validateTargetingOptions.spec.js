import { insertionOrderLocators, localeContent } from "../../../locators/insertionLocators";
import { getDemandNames } from "../../../utils/resourceNameUtil";
import { createOrUpdateAdvertiser } from "../../../support/demandCommands";

describe("Validate Targeting options test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Valid insertion creation", () => {
		// Verify if base advertiser exists if not create it
		const resourceNames = getDemandNames("Insertion Order - Targeting Option Verification");

		createOrUpdateAdvertiser(resourceNames).then((response) => {
			const advertiser = response.body;

			// Visit insertion index page
			cy.visit("/dashboard/insertion-orders");

			// Verify that page title is Insertion Orders
			cy.findByRole("heading", { name: localeContent.TITLE }).should("exist");

			// Add new insertion
			cy.clickElement(insertionOrderLocators.addInsertionOrderButton);
			cy.getByRole(insertionOrderLocators.advertiserNameDropdown).type(advertiser.name);

			cy.findAllByRole("option", { name: advertiser.name }).first().click();

			// Complete mandatory field
			cy.getByRole(insertionOrderLocators.name).type(resourceNames.insertionOrderName);

			// Validate that status and payment term have values
			cy.getByRole(insertionOrderLocators.statusActiveRadio).should("be.checked");
			cy.getByRole(insertionOrderLocators.paymentTerms).should("have.text", "30 Days");

			// Go to quality tab and assert fields are visible
			cy.clickElement(insertionOrderLocators.qualityTab);

			// select the Domain Targeting
			cy.verifyElementsExist(insertionOrderLocators.domainTargetingToggle);
			cy.clickElement(insertionOrderLocators.domainTargetingToggle);

			// Verify default option Allow should be preselected
			cy.getByRole(insertionOrderLocators.statusAllowRadio).should("be.checked");
			cy.getByRole(insertionOrderLocators.statusBlockRadio).should("not.be.checked");
			// Close the domain targeting toggle
			cy.clickElement(insertionOrderLocators.domainTargetingToggle);

			// select the App Name Targeting
			cy.verifyElementsExist(insertionOrderLocators.appNameTargetingToggle);
			cy.clickElement(insertionOrderLocators.appNameTargetingToggle);

			// Verify default option Allow should be preselected
			cy.getByRole(insertionOrderLocators.statusAllowRadio).should("be.checked");
			cy.getByRole(insertionOrderLocators.statusBlockRadio).should("not.be.checked");
			// Close the App Name targeting toggle
			cy.clickElement(insertionOrderLocators.appNameTargetingToggle);

			// select the App Bundle ID Targeting
			cy.verifyElementsExist(insertionOrderLocators.appBundleIdTargetingToggle);
			cy.clickElement(insertionOrderLocators.appBundleIdTargetingToggle);

			// Verify default option Allow should be preselected
			cy.getByRole(insertionOrderLocators.statusAllowRadio).should("be.checked");
			cy.getByRole(insertionOrderLocators.statusBlockRadio).should("not.be.checked");
			// Close the App Bundle ID targeting toggle
			cy.clickElement(insertionOrderLocators.appBundleIdTargetingToggle);
		});
	});
});
