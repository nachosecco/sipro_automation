import { globalContent } from "../../../locators/globalLocators";
import { localeContent } from "../../../locators/mediaLocators";
import { createOrUpdateMedia } from "../../../support/demandCommands";
import { getDemandNames } from "../../../utils/resourceNameUtil";

const EXPRESSION_CHIP_TEST_ID = "expression-chip";

describe("Media - Custom Url Expression", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Supports setting a custom url expression", () => {
		const resourceNames = getDemandNames("Media - Custom Url Expression");
		createOrUpdateMedia(resourceNames).then((response) => {
			const media = response.body;
			// Visit edit media form
			cy.visit(`/dashboard/media/${media.id}`);

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

			// Validate pop up is visible and displaying correct text
			cy.validatePopupMessage(`${media.name} ${globalContent.SUCCESSFULLY_UPDATED_SUFFIX}`);

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

	it("Supports setting a custom url expression with multiple same key", () => {
		const resourceNames = getDemandNames("Media - Custom Url Expression multiple key");
		createOrUpdateMedia(resourceNames).then((response) => {
			const media = response.body;
			// Visit edit media form
			cy.visit(`/dashboard/media/${media.id}`);

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

			// Drag AND drop the operator into the dropzone
			cy.findByRole("button", { name: "OR" }).focus().type("{enter}{downArrow}{rightArrow}{enter}");

			// Open the add block modal
			cy.findByRole("button", {
				name: localeContent.FIELDS.CUSTOM_URL_PARAMETER.CUSTOM_LEAF_CREATION_BUTTON_LABEL,
			}).click();

			// Input a key name
			cy.findByLabelText("Key").type("content_genre");

			// Input a value
			cy.findByLabelText("Values").type("Action{enter}Spy{enter}");

			// Save the modal and wait for it to close completely
			cy.findByRole("button", { name: globalContent.SAVE }).click();
			cy.findByRole("dialog").should("not.exist");

			// Save the form
			cy.findByRole("button", { name: globalContent.SAVE }).click();

			// Validate pop up is visible and displaying correct text
			cy.validatePopupMessage(`${media.name} ${globalContent.SUCCESSFULLY_UPDATED_SUFFIX}`);

			// Open leaf block to prove items are still there
			cy.findAllByTestId(EXPRESSION_CHIP_TEST_ID, { name: "content_genre" })
				.eq(0)
				.within(() => {
					cy.findByRole("button", {
						name: localeContent.FIELDS.CUSTOM_URL_PARAMETER.EDIT_LEAF_BUTTON_LABEL,
					}).click();
				});

			cy.findAllByTestId("tags-chip").should("have.length", 2);
			cy.findAllByTestId("tags-chip").eq(0).should("have.text", "Comedy");
			cy.findAllByTestId("tags-chip").eq(1).should("have.text", "Drama");

			// Save the modal and wait for it to close completely
			cy.findByRole("button", { name: globalContent.SAVE }).click();
			cy.findByRole("dialog").should("not.exist");

			// Open second leaf block to prove items are still there
			cy.findAllByTestId(EXPRESSION_CHIP_TEST_ID, { name: "content_genre" })
				.eq(2)
				.within(() => {
					cy.findByRole("button", {
						name: localeContent.FIELDS.CUSTOM_URL_PARAMETER.EDIT_LEAF_BUTTON_LABEL,
					}).click();
				});

			cy.findAllByTestId("tags-chip").should("have.length", 2);
			cy.findAllByTestId("tags-chip").eq(0).should("have.text", "Action");
			cy.findAllByTestId("tags-chip").eq(1).should("have.text", "Spy");
		});
	});
});
