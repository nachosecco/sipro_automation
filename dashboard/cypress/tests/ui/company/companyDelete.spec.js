import getToken from "../../../utils/getToken";

const global = require("../../../locators/globalLocators.json");
const data = require("../../../fixtures/companyCreationData.json");

describe("Company delete test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Company deletion test", () => {
		// Look for a base company entity to delete
		cy.checkBaseCompanyRequest(getToken());

		// Visit company index page
		cy.visit("/dashboard/companies");
		// Search for target company
		cy.search(data.baseName);

		// Delete company and assert status code
		cy.clickDataGridDeleteMenuItem();
		cy.clickElement(global.confirmYes);

		// Validate pop up is visible and it's text
		cy.validatePopupMessage(`${data.baseName} was successfully deleted`);
	});
});
