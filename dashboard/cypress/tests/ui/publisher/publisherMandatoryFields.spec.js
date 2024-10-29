import { globalContent } from "../../../locators/globalLocators";
import publisherLocators from "../../../locators/publisherLocators";

describe("Publisher test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Mandatory fields validation", () => {
		// Visit create publisher
		cy.visit("/dashboard/publishers/INIT");

		// Click save button without filling mandatory fields
		cy.findByRole("button", { name: globalContent.SAVE }).click();

		// Verify that the user remains on INIT
		cy.url().should("include", "/INIT");

		// Verify that settings badge counts 5
		cy.get(publisherLocators.setttingsBadge).should("have.text", 1);

		// Verify mandatory fields and related text areas
		cy.verifyMandatoryFields(publisherLocators.nameLabel);
		cy.get(publisherLocators.nameHelper).should("exist");
		// Go to Verification tab and verify mandatory fields and text areas
		cy.clickElement(publisherLocators.verificationTabMandatory);
		cy.get(publisherLocators.verificationBadge).should("have.text", 1);
		cy.verifyMandatoryFields(publisherLocators.domainLabel);
		cy.get(publisherLocators.domainHelperText).should("exist");
	});
});
