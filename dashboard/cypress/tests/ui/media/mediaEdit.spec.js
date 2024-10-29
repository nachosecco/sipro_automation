import { globalContent } from "../../../locators/globalLocators";
import { localeContent } from "../../../locators/mediaLocators";
import { createOrUpdateMedia } from "../../../support/demandCommands";
import { createOrUpdatePlacement } from "../../../support/supplyCommands";
import getPrimaryCompanyId from "../../../utils/getPrimaryCompany";
import { getDemandNames, getSupplyNames } from "../../../utils/resourceNameUtil";

describe("Media edit test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Media edit", () => {
		const resourceNames = getDemandNames("Media Edit");

		createOrUpdateMedia(resourceNames).then((response) => {
			const media = response.body;
			// Edit media form and submit

			cy.visit(`/dashboard/media/${media.id}`);

			cy.findByRole("radio", { name: localeContent.FIELDS.STATUS.INACTIVE }).click();
			cy.findByRole("button", { name: globalContent.SAVE }).click();

			// Validate pop up is visible and displaying correct text
			cy.validatePopupMessage(`${media.name} was successfully updated`);
		});
	});

	it("Media edit on custom dates validations", () => {
		const resourceNames = getDemandNames("Custom dates validation");

		createOrUpdateMedia(resourceNames).then((response) => {
			const media = response.body;
			// Visit media edit page
			cy.visit(`/dashboard/media/${media.id}`);

			//checks custom dates validations
			cy.findByRole("checkbox", { name: localeContent.FIELDS.CUSTOM_DATES_RANGE.LABEL })
				.check()
				.should("be.checked");

			// This is the happy path
			cy.findByRole("button", { name: globalContent.SAVE }).click();
			cy.validatePopupMessage(`${resourceNames.mediaName} ${globalContent.SUCCESSFULLY_UPDATED_SUFFIX}`);

			cy.setDateByLabelText(localeContent.FIELDS.CUSTOM_DATE_START.LABEL, "04/04/2012 06:00 pm");

			// This is not the happy path
			cy.findByRole("button", { name: globalContent.SAVE }).click();

			//It will check if the fail message is present
			cy.findByText(localeContent.FIELDS.CUSTOM_DATE_START.VALIDATION_MESSAGE);
		});
	});

	it("Media alignment smoke test", () => {
		const supplyNames = getSupplyNames("Media alignment smoke test");
		const demandNames = getDemandNames("Media alignment smoke test");
		const companyId = getPrimaryCompanyId();

		createOrUpdateMedia(demandNames).then(({ body: { id: mediaId } }) => {
			createOrUpdatePlacement(supplyNames).then(({ body: { id: placementId } }) => {
				cy.visit(`/dashboard/media/${mediaId}`);
				cy.findByRole("tab", { name: localeContent.TABS.ALIGNMENTS }).click();

				const expectedPlacementURL = `/dashboard/placements/${placementId}?companyId=${companyId}`;

				cy.findByTestId(localeContent.TEST_ID_FIELDS.ALIGNMENTS_TABLE_AVALIABLE).within(() => {
					cy.findByPlaceholderText(globalContent.SEARCH).type(supplyNames.placementName);

					// Asserting that the link is the placement created
					cy.findByRole("link", { name: supplyNames.placementName }).should(
						"have.attr",
						"href",
						expectedPlacementURL
					);

					// Asserting that the link it will open in a new tab
					cy.findByRole("link", { name: supplyNames.placementName }).should("have.attr", "target", `_blank`);

					// Saving aligments
					cy.findByLabelText(localeContent.FIELDS.TOGGLE_ROW_SELECTED).click();

					cy.findByRole("button", { name: localeContent.FIELDS.SAVE_ALIGNMENTS }).click();
				});

				cy.findByTestId(localeContent.TEST_ID_FIELDS.ALIGNMENTS_TABLE_ALIGN).within(() => {
					cy.findByPlaceholderText(globalContent.SEARCH).type(supplyNames.placementName);

					// checking the link is aligned
					cy.findByRole("link", { name: supplyNames.placementName }).should(
						"have.attr",
						"href",
						expectedPlacementURL
					);

					// we are going to unaligned to leave ready for the next execution of the test
					cy.findByLabelText(localeContent.FIELDS.TOGGLE_ROW_SELECTED).click();

					cy.findByRole("button", { name: localeContent.FIELDS.SAVE_ALIGNMENTS }).click();
				});

				// checking is un-align
				cy.findByTestId(localeContent.TEST_ID_FIELDS.ALIGNMENTS_TABLE_AVALIABLE).within(() => {
					cy.findByPlaceholderText(globalContent.SEARCH).type(supplyNames.placementName);

					// Asserting that the link is the programmatic demand created
					cy.findByRole("link", { name: supplyNames.placementName }).should(
						"have.attr",
						"href",
						expectedPlacementURL
					);
				});
			});
		});
	});
});
