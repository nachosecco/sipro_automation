import { getDemandNames } from "../../../utils/resourceNameUtil";
import { campaignLocators, localeContent } from "../../../locators/campaignLocators";
import { globalContent } from "../../../locators/globalLocators";
import { createOrUpdateCampaign } from "../../../support/demandCommands";

describe("Campaign edit test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Campaign edit smoke test", () => {
		const resourceNames = getDemandNames("Campaign edit smoke test");

		createOrUpdateCampaign(resourceNames).then((response) => {
			const campaign = response.body;

			// Visit campaigns index page
			cy.visit("/dashboard/campaigns");
			// Search and edit
			cy.search(campaign.name);
			cy.clickDataGridEditMenuItem();

			// Edit campaign form and submit
			const editedName = `${campaign.name} updated`;
			cy.getByRole(campaignLocators.campaignNameField).clear().type(editedName);
			cy.getByRole(campaignLocators.statusInactiveRadio).click();
			cy.findByRole("button", { name: globalContent.SAVE }).click();

			// Validate pop up is visible and displaying correct text
			cy.validatePopupMessage(`${editedName} ${globalContent.SUCCESSFULLY_UPDATED_SUFFIX}`);

			// Set name back to original and save form so that subsequent test runs can find it
			cy.findByRole("textbox", { name: localeContent.FIELD_NAMES.NAME }).clear().type(resourceNames.campaignName);
			cy.findByRole("button", { name: globalContent.SAVE }).click();
			cy.validatePopupMessage(`${resourceNames.campaignName} ${globalContent.SUCCESSFULLY_UPDATED_SUFFIX}`);
		});
	});

	it("user should be able to edit dayparting", () => {
		const demandNames = getDemandNames("can edit dayparting");
		// Check for base campaign
		createOrUpdateCampaign(demandNames).then(({ body: { id } }) => {
			cy.visit(`/dashboard/campaigns/${id}`);
		});

		cy.clickElement(campaignLocators.qualityTab);
		cy.findByRole("checkbox", { name: localeContent.FIELD_NAMES.DAYPARTING }).click();

		// Click Monday to select all hours
		cy.findByRole("button", { name: localeContent.DAYPARTING.DAY_LABEL.MONDAY }).click();
		cy.findByRole("button", { name: globalContent.SAVE }).click();

		// Validate successful save
		cy.validatePopupMessage(`${demandNames.campaignName} ${globalContent.SUCCESSFULLY_UPDATED_SUFFIX}`);

		// Reload the page
		cy.reload();

		// Dayparting should be enabled with all monday hours selected
		cy.clickElement(campaignLocators.qualityTab);
		cy.findByRole("checkbox", { name: localeContent.FIELD_NAMES.DAYPARTING }).should("be.checked");

		cy.findByRole("table").within(() => {
			cy.findAllByRole("checkbox").each((checkbox) => {
				const ariaLabel = checkbox.attr("aria-label");
				if (ariaLabel.includes(localeContent.DAYPARTING.DAY_LABEL.MONDAY)) {
					cy.wrap(checkbox).should("be.checked");
				} else {
					cy.wrap(checkbox).should("not.be.checked");
				}
			});
		});
	});

	it("User can set Opportunity Exposure and it should be there after saved", () => {
		const resourceNames = getDemandNames("Campaign edit Opportunity Exposure smoke test");

		createOrUpdateCampaign(resourceNames).then((response) => {
			const campaign = response.body;
			// Visit campaigns index page
			cy.visit("/dashboard/campaigns");

			// Search and edit
			cy.search(campaign.name);
			cy.clickDataGridEditMenuItem();

			cy.getByRole(campaignLocators.opportunityExposureSpin).clear().type(30);

			cy.findByRole("button", { name: globalContent.SAVE }).click();
			cy.validatePopupMessage(`${campaign.name} ${globalContent.SUCCESSFULLY_UPDATED_SUFFIX}`);

			// Refresh
			cy.visit(`/dashboard/campaigns/${campaign.id}`);

			// Verify
			cy.getByRole(campaignLocators.opportunityExposureSpin).should("have.value", "30");
		});
	});
});
