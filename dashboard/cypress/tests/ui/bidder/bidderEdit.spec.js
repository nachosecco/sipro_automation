import { bidderLocators } from "../../../locators/bidderLocators";
import getToken from "../../../utils/getToken";

const global = require("../../../locators/globalLocators.json");
const data = require("../../../fixtures/bidderCreationData.json");

describe("Bidder edit test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	afterEach(() => {
		cy.deleteTargetEntity(getToken(), data.updatedName, "bidder");
	});

	it("Bidder edit validation", () => {
		// Check for base bidder
		cy.checkBaseBidderRequest(getToken());

		// Visit bidders index page
		cy.visit("/dashboard/bidders");
		// Search for target bidder
		cy.search(data.baseName);

		// Wait for table to load and click action button and edit option
		cy.clickDataGridEditMenuItem();

		// Edit the form
		cy.getByRole(bidderLocators.bidderNameField).clear().type(data.updatedName);
		cy.getByRole(bidderLocators.rtbFloorField).clear().type(data.updatedRtbFloor);
		cy.getByRole(bidderLocators.demandFeePercentage).clear().type(data.updateDemandFeePercentage);

		// Go to parameters, and verify impression exp parameter is omitted and is clickable
		cy.clickElement(bidderLocators.bidParametersTab);
		cy.verifyElementsExist(bidderLocators.omittedImpressionsParametersExp);
		cy.clickElement(bidderLocators.omittedImpressionsParametersExp);

		// Save the bidder
		cy.getByRole(global.saveButton).click();

		// Validate pop up is visible and displaying correct text
		cy.validatePopupMessage(`${data.updatedName} was successfully updated`);
	});
});
