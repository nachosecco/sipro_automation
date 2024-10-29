import { globalContent } from "../../../locators/globalLocators";
import { createOrUpdateProgrammaticDemand } from "../../../support/demandCommands";
import { getProgrammaticDemandNames } from "../../../utils/resourceNameUtil";

describe("Programmatic delete test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Programmatic delete validations", () => {
		const resourceNames = getProgrammaticDemandNames("Programmatic Delete");
		createOrUpdateProgrammaticDemand(resourceNames).then((response) => {
			const programmatic = response.body;

			// Visit programmatic index page
			cy.visit("/dashboard/programmatic-demand");

			// Search target programmatic demand
			cy.search(programmatic.name);

			// Wait for table to load and click action button and delete option
			cy.clickDataGridDeleteMenuItem();

			// Cancel and verify the record still exists
			cy.findByRole("button", { name: globalContent.CANCEL }).click();
			cy.reload();
			cy.search(programmatic.name);

			cy.get('[data-field="name"]').eq(1).should("have.text", programmatic.name);

			// Delete the record
			cy.clickDataGridDeleteMenuItem();
			cy.findByRole("button", { name: globalContent.DELETE }).click();

			// Success message should display
			cy.validatePopupMessage(`${programmatic.name} ${globalContent.SUCCESSFULLY_DELETED_SUFFIX}`);
		});
	});
});
