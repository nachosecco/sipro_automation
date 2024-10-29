const global = require("../../../locators/globalLocators.json");
import { createOrUpdateMedia } from "../../../support/demandCommands";
import { getDemandNames } from "../../../utils/resourceNameUtil";
import { globalGridLocators } from "../../../locators/globalGridLocators.js";

describe("Media delete test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Media delete", () => {
		const resourceNames = getDemandNames("Media Delete");

		createOrUpdateMedia(resourceNames).then((response) => {
			const media = response.body;

			// Visit media index page
			cy.visit("/dashboard/media");

			// Search target media
			cy.search(media.name);

			// Click action button and delete option
			cy.clickDataGridDeleteMenuItem();

			// Cancel and verify the record still exists
			cy.clickElement(global.confirmNo);
			cy.reload();
			cy.search(media.name);
			cy.getByRole(globalGridLocators.clearSearchButton).should("exist");
			cy.get(globalGridLocators.indexGrid).find('[data-field="name"]').eq(0).should("have.text", `${media.name}`);

			// Delete the record
			cy.clickDataGridDeleteMenuItem();
			cy.clickElement(global.confirmYes);

			// Validate that success pop up shows and displays correct text
			cy.validatePopupMessage(`${media.name} was successfully deleted`);
		});
	});
});
