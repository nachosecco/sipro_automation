import { insertionOrderLocators, localeContent } from "../../../locators/insertionLocators";
import { getDemandNames } from "../../../utils/resourceNameUtil";
import { createOrUpdateAdvertiser } from "../../../support/demandCommands";

describe("Insertion ui validation test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Programmmatic demand is not listed as advertiser", () => {
		// Verify if base advertiser exists if not create it
		const demandNames = getDemandNames("Programmmatic demand is not listed as advertiser");
		createOrUpdateAdvertiser(demandNames);

		// Visit insertion index page
		cy.visit("/dashboard/insertion-orders");

		// Verify that page title is Insertion Orders
		cy.findByRole("heading", { name: localeContent.TITLE }).should("exist");

		// Validate list of advertisers
		cy.clickElement(insertionOrderLocators.addInsertionOrderButton);
		cy.getByRole(insertionOrderLocators.advertiserNameDropdown).type("Programmatic Demand");
		cy.getByRole(insertionOrderLocators.programmaticDemandOption).should("not.exist");
	});
});
