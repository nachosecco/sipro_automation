import { companyLocators, localeContent } from "../../../locators/companyLocators.js";
import { createOrUpdateCompany } from "../../../support/companyCommands";
import { getTestResourceName } from "../../../utils/resourceNameUtil";
import { globalContent } from "../../../locators/globalLocators";

describe("Company edit test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Company edit test", () => {
		const companyName = getTestResourceName("Company smoke edit");
		createOrUpdateCompany({ companyName }).then(() => {
			// Visit company index page
			cy.visit("/dashboard/companies");

			// Search for target company
			cy.search(companyName);

			// Edit the target company
			cy.clickDataGridEditMenuItem();

			// Edit the target company
			const editedName = `${companyName} edited`;

			cy.getByRole(companyLocators.companyNameField).clear().type(editedName);

			cy.findByRole("button", { name: globalContent.SAVE }).click();

			// Validate pop up is visible and displaying correct text
			cy.validatePopupMessage(`${editedName} ${globalContent.SUCCESSFULLY_UPDATED_SUFFIX}`);

			// Set name back to original and save form so that subsequent test runs can find it
			cy.getByRole(companyLocators.companyNameField).clear().type(companyName);
			cy.findByRole("button", { name: globalContent.SAVE }).click();
			cy.validatePopupMessage(`${companyName} ${globalContent.SUCCESSFULLY_UPDATED_SUFFIX}`);
		});
	});

	/**
	 * NOTE: This test is meant to be a place to test our field mappings between client, server, and db.
	 * If we're adding fields that simply pass data, this is a good place to test them
	 */
	it("Company test edit fields", () => {
		const companyName = getTestResourceName("Company test edit fields");
		createOrUpdateCompany({ companyName }).then(({ body: { id: companyId } }) => {
			cy.visit(`/dashboard/companies/${companyId}`);

			// Navigate to defaults tab
			cy.clickElement(companyLocators.defaultsTab);

			// Change Fields from defaults
			// Turn on the bidder service
			cy.findByRole("checkbox", { name: localeContent.FIELDS.BIDDER_SERVICE_ENABLED.LABEL }).should(
				"not.be.checked"
			);
			cy.findByRole("checkbox", { name: localeContent.FIELDS.BIDDER_SERVICE_ENABLED.LABEL }).click();

			// Change Fields from defaults
			// Turn on the traffic shaping
			cy.findByRole("checkbox", { name: localeContent.FIELDS.TRAFFIC_SHAPING_ENABLED.LABEL }).should(
				"not.be.checked"
			);
			cy.findByRole("checkbox", { name: localeContent.FIELDS.TRAFFIC_SHAPING_ENABLED.LABEL }).click();

			// Save the company
			cy.findByRole("button", { name: globalContent.SAVE }).click();

			// Validate pop up is visible and displaying correct text
			cy.validatePopupMessage(`${companyName} ${globalContent.SUCCESSFULLY_UPDATED_SUFFIX}`);

			// Refresh the page
			cy.visit(`/dashboard/companies/${companyId}`);

			// Navigate to defaults tab
			cy.clickElement(companyLocators.defaultsTab);

			// Verify fields have changed from defaults
			cy.findByRole("checkbox", { name: localeContent.FIELDS.BIDDER_SERVICE_ENABLED.LABEL }).should("be.checked");
			cy.findByRole("checkbox", { name: localeContent.FIELDS.TRAFFIC_SHAPING_ENABLED.LABEL }).should(
				"be.checked"
			);
		});
	});

	it("Company edit a default company and change priority to cpm", () => {
		const companyName = getTestResourceName("Company priority edit");
		createOrUpdateCompany({ companyName }).then(({ body: { id: companyPriority } }) => {
			cy.visit(`/dashboard/companies/${companyPriority}`);

			cy.clickElement(companyLocators.defaultsTab);

			// Selecting Media Type CPM Priority
			cy.findByRole("radio", { name: localeContent.FIELDS.MEDIA_TYPE_PRIORIZATION.OPTIONS.CPM.LABEL }).click();

			//saving the company
			cy.findByRole("button", { name: globalContent.SAVE }).click();

			// Validate pop up is visible and displaying correct text
			cy.validatePopupMessage(`${companyName} ${globalContent.SUCCESSFULLY_UPDATED_SUFFIX}`);
		});
	});

	it("Company edit a default company and Max Ad Response Size", () => {
		const companyName = getTestResourceName("Company max ad response size edit");
		createOrUpdateCompany({ companyName }).then(({ body: { id: companyId } }) => {
			cy.visit(`/dashboard/companies/${companyId}`);

			cy.clickElement(companyLocators.defaultsTab);

			// Edit Max Ad Response Size

			cy.findByRole("spinbutton", { name: localeContent.FIELDS.MAX_AD_RESPONSE_AD_SIZE.LABEL }).type("5");

			//saving the company
			cy.findByRole("button", { name: globalContent.SAVE }).click();

			// Validate pop up is visible and displaying correct text
			cy.validatePopupMessage(`${companyName} ${globalContent.SUCCESSFULLY_UPDATED_SUFFIX}`);

			cy.visit(`/dashboard/companies/${companyId}`);

			cy.clickElement(companyLocators.defaultsTab);

			// Verify fields have changed from defaults

			cy.findByRole("spinbutton", { name: localeContent.FIELDS.MAX_AD_RESPONSE_AD_SIZE.LABEL }).should(
				"have.value",
				"5"
			);
		});
	});
});
