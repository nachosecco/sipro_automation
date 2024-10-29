import { insertionOrderLocators, localeContent } from "../../../locators/insertionLocators";
import { createOrUpdateInsertionOrder } from "../../../support/demandCommands";
import { getDemandNames } from "../../../utils/resourceNameUtil";
import { globalContent } from "../../../locators/globalLocators";
import { DEFAULT_ADVERTISER_BODY } from "../../../fixtures/defaultDemandSideCreationData";

describe("Insertion edit test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Insertion edit validations", () => {
		const resourceNames = getDemandNames("Insertion Order Edit");
		createOrUpdateInsertionOrder(resourceNames).then((response) => {
			const insertionOrder = response.body;

			// Visit insertion index page
			cy.visit("/dashboard/insertion-orders");
			// Search for target insertion
			cy.search(insertionOrder.name);

			// Wait for table to load and click action button and delete option
			cy.clickDataGridEditMenuItem();

			// Edit insertion form and submit
			const updatedName = `${resourceNames.insertionOrderName} updated`;
			cy.getByRole(insertionOrderLocators.name).clear().type(updatedName);
			cy.findByRole("button", { name: globalContent.SAVE }).click();

			// Validate pop up is visible and displaying correct text
			cy.validatePopupMessage(`${updatedName} ${globalContent.SUCCESSFULLY_UPDATED_SUFFIX}`);

			// Set name back to original and save form so that subsequent test runs can find it
			cy.getByRole(insertionOrderLocators.name).clear().type(resourceNames.insertionOrderName);
			cy.findByRole("button", { name: globalContent.SAVE }).click();

			cy.validatePopupMessage(`${resourceNames.insertionOrderName} ${globalContent.SUCCESSFULLY_UPDATED_SUFFIX}`);
		});
	});

	it("Edit insertion having inactive parent should show warning on tab switch and not shown on page switch as location is updated.", () => {
		const resourceNames = getDemandNames("Insertion Order Edit Having inactive parent");
		createOrUpdateInsertionOrder({
			insertionOrderName: resourceNames.insertionOrderName,
			advertiserName: resourceNames.advertiserName,
			advertiserBody: {
				...DEFAULT_ADVERTISER_BODY,
				status: "inactive",
			},
		}).then((response) => {
			const insertionId = response.body.id;

			// Visit insertion edit page
			cy.visit(`/dashboard/insertion-orders/${insertionId}`);

			// Warning should exist on screen.
			cy.findByText(localeContent.ADVERTISER_WARNING_MSG).should("exist");
			//switch the tab
			cy.clickElement(insertionOrderLocators.qualityTab);
			// Warning should still exist on tab switch
			cy.findByText(localeContent.ADVERTISER_WARNING_MSG).should("exist");

			// Visit insertion index page (location is arbitrary, we just need to navigate away from the form)
			cy.visit("/dashboard/insertion-orders");
			// Warning should be dismissed now that location has changed.
			cy.findByText(localeContent.ADVERTISER_WARNING_MSG).should("not.exist");
		});
	});
});
