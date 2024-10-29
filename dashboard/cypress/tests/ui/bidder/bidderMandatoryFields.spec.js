import { bidderLocators } from "../../../locators/bidderLocators";
import { globalContent } from "../../../locators/globalLocators";

describe("Bidder test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Mandatory fields validation", () => {
		// Visit add bidder form
		cy.visit("/dashboard/bidders/INIT");

		// Click save button without filling mandatory fields
		cy.findByRole("button", { name: globalContent.SAVE }).click();

		// Verify that the user remains on INIT
		cy.url().should("include", "/INIT");

		// Verify that settings badge counts 2
		cy.get(bidderLocators.setttingsBadge).should("have.text", 2);

		// Verify mandatory fields and related text areas
		cy.verifyMandatoryFields(
			bidderLocators.nameLabel,
			bidderLocators.bidUrlRegionLabel,
			bidderLocators.bidUrlLabel
		);
		cy.get(bidderLocators.nameHelper).should("exist");
		cy.get(bidderLocators.bidUrlRegionLabelHelper).should("exist");
		cy.get(bidderLocators.bidUrlLabelHelper).should("exist");
	});
});
