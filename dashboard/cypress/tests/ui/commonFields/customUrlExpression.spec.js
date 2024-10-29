import { globalContent } from "../../../locators/globalLocators";
import { localeContent as mediaLc } from "../../../locators/mediaLocators";
import { localeContent as programmaticLc } from "../../../locators/programmaticLocators";
import { createOrUpdateMedia } from "../../../support/demandCommands";
import { getDemandNames } from "../../../utils/resourceNameUtil";
import { createOrUpdateProgrammaticDemand } from "../../../support/demandCommands";
import { getProgrammaticDemandNames } from "../../../utils/resourceNameUtil";

const EXPRESSION_CHIP_TEST_ID = "expression-chip";
const RULE_VISUALIZER_TEST_ID = "rule-visualizer";
const REMOVE_BLOCK_ICON_TEST_ID = "CancelIcon"; // This is controlled by MUI

describe("Custom Url Expression", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	describe("no custom url expression", () => {
		it("Users can load media without custom url params", () => {
			const resourceNames = getDemandNames("Media - No Custom Url Expression");
			createOrUpdateMedia(resourceNames).then((response) => {
				const media = response.body;
				// Visit edit for the created media
				cy.visit(`/dashboard/media/${media.id}`);

				cy.findByLabelText(mediaLc.FIELDS.NAME.LABEL).should("have.value", media.name);
			});
		});

		it("Users can load programmatic demand without custom url params", () => {
			const resourceNames = getProgrammaticDemandNames("Programmatic - No Custom Url Expression");
			createOrUpdateProgrammaticDemand(resourceNames).then((response) => {
				const programmatic = response.body;
				// Visit edit form for the created programmatic demand
				cy.visit(`/dashboard/programmatic-demand/${programmatic.id}`);

				cy.findByLabelText(programmaticLc.FIELDS.NAME.LABEL).should("have.value", programmatic.name);
			});
		});
	});

	// We're using cypress to run these tests so that we can use the drag and drop to build an expression. We're using media as the example here, but the same tests could be run for programmatic demand.
	it("Visualizer updates as rule is updated", () => {
		const resourceNames = getDemandNames("Custom Url Visualizer");
		createOrUpdateMedia(resourceNames).then((response) => {
			const media = response.body;
			// Visit edit media form
			cy.visit(`/dashboard/media/${media.id}`);

			// Navigate to the Quality Tab
			cy.findByRole("tab", { name: mediaLc.TABS.QUALITY }).click();

			// Enable the expression field
			cy.findByLabelText(mediaLc.FIELDS.CUSTOM_URL_PARAMETER.ENABLE_SWITCH_LABEL).click();

			// Open the add block modal to add a first block
			cy.findByRole("button", {
				name: mediaLc.FIELDS.CUSTOM_URL_PARAMETER.CUSTOM_LEAF_CREATION_BUTTON_LABEL,
			}).click();

			// Input a key name
			cy.findByLabelText("Key").type("content_genre");

			// Input a value
			cy.findByLabelText("Values").type("Comedy{enter}Drama{enter}");

			// Save the modal and wait for it to close completely
			cy.findByRole("button", { name: globalContent.SAVE }).click();
			cy.findByRole("dialog").should("not.exist");

			// Show the visualizer
			cy.findByRole("button", {
				name: mediaLc.FIELDS.CUSTOM_URL_PARAMETER.RULE_VISUALIZER.SHOW_RULE_LABEL,
			}).click();

			// Visualizer should have full rule
			cy.findByTestId(RULE_VISUALIZER_TEST_ID).should("have.text", "( Comedy OR Drama )");

			// Drag AND operator into the dropzone
			cy.findByRole("button", { name: "AND" }).focus().type("{enter}{downArrow}{rightArrow}{enter}");

			// Visualizer should have full rule
			cy.findByTestId(RULE_VISUALIZER_TEST_ID).should("have.text", "( Comedy OR Drama ) AND ");

			// Open the add block modal to add a second block
			cy.findByRole("button", {
				name: mediaLc.FIELDS.CUSTOM_URL_PARAMETER.CUSTOM_LEAF_CREATION_BUTTON_LABEL,
			}).click();

			// Input a key name
			cy.findByLabelText("Key").type("content_title");

			// Input a value
			cy.findByLabelText("Values").type("Jumanji{enter}Ace Ventura{enter}");

			// Save the modal and wait for it to close completely
			cy.findByRole("button", { name: globalContent.SAVE }).click();
			cy.findByRole("dialog").should("not.exist");

			// Visualizer should have full rule
			cy.findByTestId(RULE_VISUALIZER_TEST_ID).should(
				"have.text",
				"( Comedy OR Drama ) AND ( Jumanji OR Ace Ventura )"
			);

			// Remove last block
			cy.findAllByTestId(EXPRESSION_CHIP_TEST_ID)
				.eq(2)
				.within(() => {
					cy.findByTestId(REMOVE_BLOCK_ICON_TEST_ID).click();
				});

			// Visualizer should have full rule
			cy.findByTestId(RULE_VISUALIZER_TEST_ID).should("have.text", "( Comedy OR Drama ) AND ");

			// Remove AND operator
			cy.findAllByTestId(EXPRESSION_CHIP_TEST_ID)
				.eq(1)
				.within(() => {
					cy.findByTestId(REMOVE_BLOCK_ICON_TEST_ID).click();
				});

			// Visualizer should have full rule
			cy.findByTestId(RULE_VISUALIZER_TEST_ID).should("have.text", "( Comedy OR Drama )");
		});
	});
});
