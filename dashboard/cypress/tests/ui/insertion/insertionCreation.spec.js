import { insertionOrderLocators, localeContent } from "../../../locators/insertionLocators";
import { globalContent } from "../../../locators/globalLocators";
import { getDemandNames } from "../../../utils/resourceNameUtil";
import { createOrUpdateAdvertiser } from "../../../support/demandCommands";
import { DASHBOARD_API } from "../../../utils/serviceResources";

const cleanup = (insertionOrder) => {
	const pathDeleteResource = (resource) => {
		return DASHBOARD_API.INSERTION_ORDER.getOne({ id: resource.id });
	};
	const indexPathResources = DASHBOARD_API.INSERTION_ORDER.getIndex();

	const filterResourceToDelete = (resource) => resource.name === insertionOrder;
	cy.cleanResources({ indexPathResources, pathDeleteResource, filterResourceToDelete });
};

describe("Insertion creation test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Valid insertion creation", () => {
		// Verify if base advertiser exists if not create it
		const resourceNames = getDemandNames("Insertion Order Creation");
		cleanup(resourceNames.insertionOrderName);

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

			// Verify elements are visible
			cy.verifyElementsExist(
				insertionOrderLocators.settingsTab,
				insertionOrderLocators.qualityTab,
				insertionOrderLocators.name,
				insertionOrderLocators.statusActiveRadio,
				insertionOrderLocators.statusInactiveRadio,
				insertionOrderLocators.paymentTerms
			);

			// validate that the view report button is not visible until the form is saved
			cy.findByRole("link", { name: globalContent.VIEW_REPORT }).should("not.exist");

			// Complete mandatory field
			cy.getByRole(insertionOrderLocators.name).type(resourceNames.insertionOrderName);

			// Validate that status and payment term have values
			cy.getByRole(insertionOrderLocators.statusActiveRadio).should("be.checked");
			cy.getByRole(insertionOrderLocators.paymentTerms).should("have.text", "30 Days");

			// Submit endpoint and submit
			cy.findByRole("button", { name: globalContent.SAVE }).click();

			// Validate pop up is visible and it's text
			cy.validatePopupMessage(`${resourceNames.insertionOrderName} ${globalContent.SUCCESSFULLY_CREATED_SUFFIX}`);

			// View report button should be visible
			cy.findByRole("link", { name: globalContent.VIEW_REPORT }).should("exist");
		});
	});
});
