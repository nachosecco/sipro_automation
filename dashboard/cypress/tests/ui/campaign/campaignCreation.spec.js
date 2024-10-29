import { campaignLocators, localeContent } from "../../../locators/campaignLocators";
import { getDemandNames } from "../../../utils/resourceNameUtil";
import { createOrUpdateInsertionOrder } from "../../../support/demandCommands";

import { globalContent } from "../../../locators/globalLocators";
import { DASHBOARD_API } from "../../../utils/serviceResources";

const cleanup = (campaignName) => {
	const pathDeleteResource = (resource) => {
		return DASHBOARD_API.CAMPAIGN.getOne({ id: resource.id });
	};
	const indexPathResources = DASHBOARD_API.CAMPAIGN.getIndex();

	const filterResourceToDelete = (resource) => resource.name === campaignName;
	cy.cleanResources({ indexPathResources, pathDeleteResource, filterResourceToDelete });
};

describe("Campaign creation test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Valid campaign creation", () => {
		const resourceNames = getDemandNames("Valid video media creation");
		cleanup(resourceNames.campaignName);

		createOrUpdateInsertionOrder(resourceNames).then((response) => {
			const insertionOrder = response.body;

			// Visit campaigns index page
			cy.visit("/dashboard/campaigns");

			// Verify that page title is campaigns
			cy.findByRole("heading", { name: localeContent.TITLE }).should("exist");

			// Add new campaign
			cy.clickElement(campaignLocators.addCampaignButton);
			cy.getByRole(campaignLocators.insertionOrderDropdown).type(insertionOrder.name);

			cy.findByRole("option", { name: insertionOrder.name }).click();

			// Verify elements are visible for default form
			cy.verifyElementsExist(
				campaignLocators.settingsTab,
				campaignLocators.qualityTab,
				campaignLocators.campaignNameField,
				campaignLocators.statusActiveRadio,
				campaignLocators.statusInactiveRadio,
				campaignLocators.cpmField,
				campaignLocators.endDateField,
				campaignLocators.goalTypeImpressionRadio,
				campaignLocators.goalTypeSpendRadio,
				campaignLocators.goalTypeOpenRadio,
				campaignLocators.impressionGoalField,
				campaignLocators.pacingTypeEvenRadio,
				campaignLocators.pacingTypeAsapRadio,
				campaignLocators.frequencyCappingSwitch,
				campaignLocators.campaignPriorityDropdown,
				campaignLocators.campaignWeightDropdown
			);
			cy.get(campaignLocators.startDateField).should("be.visible");

			// Verify that extra fields are visible for goal type spend
			cy.clickElement(campaignLocators.goalTypeSpendRadio);
			cy.getByRole(campaignLocators.spendGoalField).should("be.visible");

			// Verify that extra fields are not present for goal type open
			cy.clickElement(campaignLocators.goalTypeOpenRadio);
			cy.verifyElementsNotExist(
				campaignLocators.impressionGoalField,
				campaignLocators.pacingTypeEvenRadio,
				campaignLocators.pacingTypeAsapRadio,
				campaignLocators.spendGoalField
			);

			// Verify that extra elements are visible for freq cap
			cy.clickElement(campaignLocators.frequencyCappingSwitch);
			cy.verifyElementsExist(campaignLocators.impressionsPerUserField, campaignLocators.timeframeDropdown);
			cy.clickElement(campaignLocators.frequencyCappingSwitch);

			// Complete mandatory fields
			cy.getByRole(campaignLocators.campaignNameField).type(`${resourceNames.campaignName}`);
			cy.getByRole(campaignLocators.cpmField).type(5);

			// view report button should not be visible until form is saved
			cy.findByRole("link", { name: globalContent.VIEW_REPORT }).should("not.exist");

			// Go to quality tab and assert fields are visible
			cy.clickElement(campaignLocators.qualityTab);
			cy.getByRole(campaignLocators.returnOneMediaInAdResponseCheckbox).should("exist");

			// Submit form
			cy.findByRole("button", { name: globalContent.SAVE }).click();

			// Validate pop up is visible and it's text
			cy.validatePopupMessage(`${resourceNames.campaignName} ${globalContent.SUCCESSFULLY_CREATED_SUFFIX}`);

			// Go to settings tab and assert fields are visible
			cy.clickElement(campaignLocators.settingsTab);

			// View report button should be visible
			cy.findByRole("link", { name: globalContent.VIEW_REPORT }).should("exist");
		});
	});
});
