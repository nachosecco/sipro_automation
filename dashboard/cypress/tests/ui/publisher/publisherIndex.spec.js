import publisherLocators from "../../../locators/publisherLocators";
import { globalGridLocators } from "../../../locators/globalGridLocators.js";

describe("Publisher test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Index elements and pagination validations", () => {
		// Visit publisher index page
		cy.visit("/dashboard/publishers");

		// Validate that index elements are visible
		cy.verifyElementsExist(
			publisherLocators.nameColumn,
			publisherLocators.statusColumn,
			publisherLocators.opportunitiesColumn,
			publisherLocators.impressionsColumn,
			publisherLocators.revenueColumn
		);
		cy.getByRole(globalGridLocators.searchBox);

		// Verify that other pagination buttons are visible when not on first page
		cy.clickElement(globalGridLocators.nextPageButton);
		cy.verifyElementsExist(globalGridLocators.nextPageButton, globalGridLocators.previousPageButton);
	});

	it("Sorting validations", () => {
		cy.intercept("**/manage/publishers", { fixture: "publisherIndexMock.json" });

		// Visit publisher index page
		cy.visit("/dashboard/publishers");

		// Name sorting validations
		cy.clickElement(publisherLocators.nameColumn);

		cy.get(globalGridLocators.indexGrid).find('[data-field="name"]').eq(0).should("have.text", "ZBA Test");

		cy.clickElement(publisherLocators.nameColumn);

		cy.get(globalGridLocators.indexGrid).find('[data-field="name"]').eq(0).should("have.text", "ABC Test");

		// Status sorting validations
		cy.clickElement(publisherLocators.statusColumn);

		cy.get(globalGridLocators.indexGrid).find('[data-field="status"]').eq(0).should("have.text", "Inactive");

		cy.clickElement(publisherLocators.statusColumn);

		cy.get(globalGridLocators.indexGrid).find('[data-field="status"]').eq(0).should("have.text", "Active");

		// Opportunities sorting validations
		cy.clickElement(publisherLocators.opportunitiesColumn);

		cy.get(globalGridLocators.indexGrid).find('[data-field="opportunities"]').eq(0).should("have.text", "17,356");

		cy.clickElement(publisherLocators.opportunitiesColumn);

		cy.get(globalGridLocators.indexGrid).find('[data-field="opportunities"]').eq(0).should("have.text", "250");

		// Impressions sorting validations
		cy.clickElement(publisherLocators.impressionsColumn);

		cy.get(globalGridLocators.indexGrid).find('[data-field="impressions"]').eq(0).should("have.text", "201");

		cy.clickElement(publisherLocators.impressionsColumn);

		cy.get(globalGridLocators.indexGrid).find('[data-field="impressions"]').eq(0).should("have.text", "2");

		// Revenue sorting validations
		cy.clickElement(publisherLocators.revenueColumn);

		cy.get(globalGridLocators.indexGrid).find('[data-field="revenue"]').eq(0).should("have.text", "6.50");

		cy.clickElement(publisherLocators.revenueColumn);

		cy.get(globalGridLocators.indexGrid).find('[data-field="revenue"]').eq(0).should("have.text", "0.01");
	});

	it("Hide and show column validations", () => {
		// Visit publisher index page
		cy.visit("/dashboard/publishers");

		// Verify all columns are marked to be shown as default
		cy.clickElement(publisherLocators.selectColumns);
		cy.verifyCheckedElements(
			publisherLocators.hideShowStatus,
			publisherLocators.hideShowOpportunities,
			publisherLocators.hideShowImpressions,
			publisherLocators.hideShowRevenue
		);

		// Uncheck every column
		cy.uncheckElements(
			publisherLocators.hideShowStatus,
			publisherLocators.hideShowOpportunities,
			publisherLocators.hideShowImpressions,
			publisherLocators.hideShowRevenue
		);

		// Verify columns are not present
		cy.verifyElementsNotExist(
			publisherLocators.statusColumn,
			publisherLocators.opportunitiesColumn,
			publisherLocators.impressionsColumn,
			publisherLocators.revenueColumn
		);
	});
});
