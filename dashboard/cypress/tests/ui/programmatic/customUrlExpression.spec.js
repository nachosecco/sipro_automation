import { localeContent } from "../../../locators/programmaticLocators";
import { getProgrammaticDemandNames } from "../../../utils/resourceNameUtil";
import { globalContent } from "../../../locators/globalLocators";
import { createOrUpdateProgrammaticDemand } from "../../../support/demandCommands";

const EXPRESSION_CHIP_TEST_ID = "expression-chip";

describe("Programmatic Demand - Custom Url Expression", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Supports setting a custom url expression", () => {
		const resourceNames = getProgrammaticDemandNames("Programmatic - Custom Url Expression");
		createOrUpdateProgrammaticDemand(resourceNames).then((response) => {
			const programmatic = response.body;
			// Visit edit form for the created programmatic demand
			cy.visit(`/dashboard/programmatic-demand/${programmatic.id}`);

			// Navigate to the Quality Tab
			cy.findByRole("tab", { name: localeContent.TABS.QUALITY }).click();

			// Enable the expression field
			cy.findByLabelText(localeContent.FIELDS.CUSTOM_URL_PARAMETER.ENABLE_SWITCH_LABEL).click();

			// Open the add block modal
			cy.findByRole("button", {
				name: localeContent.FIELDS.CUSTOM_URL_PARAMETER.CUSTOM_LEAF_CREATION_BUTTON_LABEL,
			}).click();

			// Input a key name
			cy.findByLabelText("Key").type("content_genre");

			// Input a value
			cy.findByLabelText("Values").type("Comedy{enter}Drama{enter}");

			// Save the modal and wait for it to close completely
			cy.findByRole("button", { name: globalContent.SAVE }).click();
			cy.findByRole("dialog").should("not.exist");

			// Save the form
			cy.findByRole("button", { name: globalContent.SAVE }).click();

			// Success message should display
			cy.validatePopupMessage(`${resourceNames.programmaticName} ${globalContent.SUCCESSFULLY_UPDATED_SUFFIX}`);

			// Open leaf block to prove items are still there
			cy.findByTestId(EXPRESSION_CHIP_TEST_ID, { name: "content_genre" }).within(() => {
				cy.findByRole("button", {
					name: localeContent.FIELDS.CUSTOM_URL_PARAMETER.EDIT_LEAF_BUTTON_LABEL,
				}).click();
			});

			cy.findAllByTestId("tags-chip").should("have.length", 2);
			cy.findAllByTestId("tags-chip").eq(0).should("have.text", "Comedy");
			cy.findAllByTestId("tags-chip").eq(1).should("have.text", "Drama");
		});
	});
});
