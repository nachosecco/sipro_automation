import { dataDistributionLocators } from "../../../locators/dataDistributionLocators";
import { globalContent } from "../../../locators/globalLocators";
import { createOrUpdateDataDistribution } from "../../../support/dataDistributionCommands";

describe("Data Distribution edit test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Data Distribution edit", () => {
		const name = `Automation Entity Edit`;

		createOrUpdateDataDistribution({ displayName: name }).then(({ body: { id: distributionId } }) => {
			// Visit data distribution edit page
			cy.visit(`/dashboard/data-distributions/${distributionId}`);

			// Edit advertiser form and submit
			const editedName = `${name} updated`;
			cy.getByRole(dataDistributionLocators.displayNameField).clear();
			cy.getByRole(dataDistributionLocators.displayNameField).type(editedName);
			cy.getByRole(dataDistributionLocators.defaultNameField).should("be.disabled");

			cy.findByRole("button", { name: globalContent.SAVE }).click();
			// Validate pop up is visible and displaying correct text
			cy.validatePopupMessage(`${editedName} ${globalContent.SUCCESSFULLY_UPDATED_SUFFIX}`);

			// Set name back to original and save form so that subsequent test runs can find it
			cy.getByRole(dataDistributionLocators.displayNameField).clear();
			cy.getByRole(dataDistributionLocators.displayNameField).type(name);
			cy.findByRole("button", { name: globalContent.SAVE }).click();
			cy.validatePopupMessage(`${name} ${globalContent.SUCCESSFULLY_UPDATED_SUFFIX}`);
		});
	});
});
