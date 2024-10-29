import getToken from "../../../utils/getToken";

const global = require("../../../locators/globalLocators.json");
const data = require("../../../fixtures/bidderCreationData.json");
import { globalGridLocators } from "../../../locators/globalGridLocators.js";

describe("Bidder delete test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Bidder delete validation", () => {
		// Check for base bidder
		cy.checkBaseBidderRequest(getToken());

		// Visit bidders index page
		cy.visit("/dashboard/bidders");

		// Search target bidder
		cy.search(data.baseName);

		// Wait for table to load and click action button and delete option
		cy.clickDataGridDeleteMenuItem();

		// Cancel and verify the record still exists
		cy.clickElement(global.confirmNo);
		cy.reload();
		cy.search(data.baseName);

		cy.getByRole(globalGridLocators.clearSearchButton).should("exist");
		cy.get(globalGridLocators.indexGrid).find('[data-field="name"]').eq(0).should("have.text", `${data.baseName}`);

		// Delete the record
		cy.getByRole(global.indexActionButton).eq(0).click();
		cy.contains("Delete").filter(":visible").click();
		cy.getByRole(global.confirmYes).click();

		// Validate that success pop up shows and displays correct text
		cy.validatePopupMessage(`${data.baseName} was successfully deleted`);
	});
});
