import { globalContent } from "../../../locators/globalLocators";
import { createOrUpdatePublisher } from "../../../support/supplyCommands";
import { getSupplyNames } from "../../../utils/resourceNameUtil";
import publisherLocators from "../../../locators/publisherLocators";

describe("Publisher edit test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Publisher edit validations", () => {
		const supplyNames = getSupplyNames("Publisher delete smoke test");
		createOrUpdatePublisher(supplyNames);

		// Visit publisher index page
		cy.visit("/dashboard/publishers");

		// Search target publisher
		cy.search(supplyNames.publisherName);

		// Wait for table to load and click action button and edit option
		cy.clickDataGridEditMenuItem();

		// Edit publisher form and submit
		const editedName = `${supplyNames.publisherName} edited`;
		cy.getByRole(publisherLocators.publisherNameField).clear().type(editedName);
		cy.getByRole(publisherLocators.defaultFloorField).clear().type("1");
		cy.getByRole(publisherLocators.revenueShareField).clear().type("5");
		cy.getByRole(publisherLocators.contactNameField).clear().type("Automated contact");
		cy.getByRole(publisherLocators.contactEmailField).clear().type("automated@test.com");
		cy.getByRole(publisherLocators.phoneNumberField).clear().type("12024956");
		cy.getByRole(publisherLocators.companyAddressField).clear().type("Automated Street 123");
		cy.getByRole(publisherLocators.tmaxField).clear().type(123);

		// Save form
		cy.intercept("PUT", "**/manage/publishers/*").as("update");
		cy.findByRole("button", { name: globalContent.SAVE }).click();

		// Validate PUT is successful
		cy.wait("@update").its("response.statusCode").should("eq", 200);

		// Validate pop up is visible and displaying correct text
		cy.validatePopupMessage(`${editedName} ${globalContent.SUCCESSFULLY_UPDATED_SUFFIX}`);

		// Set name back to original and save form so that subsequent test runs can find it
		cy.getByRole(publisherLocators.publisherNameField).clear().type(supplyNames.publisherName);
		cy.findByRole("button", { name: globalContent.SAVE }).click();
		cy.validatePopupMessage(`${supplyNames.publisherName} ${globalContent.SUCCESSFULLY_UPDATED_SUFFIX}`);
	});
});
