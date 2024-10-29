import { getDemandNames, getProgrammaticDemandNames, getSupplyNames } from "../../../utils/resourceNameUtil";

import placementLocators, { localeContent } from "../../../locators/placementLocators";
import { globalContent } from "../../../locators/globalLocators";
import { createOrUpdatePlacement } from "../../../support/supplyCommands";
import { createOrUpdateMedia, createOrUpdateProgrammaticDemand } from "../../../support/demandCommands";
import getPrimaryCompanyId from "../../../utils/getPrimaryCompany";
import {
	DEFAULT_DISPLAY_PLACEMENT_BODY,
	DEFAULT_PLACEMENT_BODY,
} from "../../../fixtures/defaultSupplySideCreationData";
import { DEFAULT_DISPLAY_MEDIA_BODY, DEFAULT_MEDIA_BODY } from "../../../fixtures/defaultDemandSideCreationData";
import getToken from "../../../utils/getToken";

describe("Check the Status filter in Alignment", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Filter the active and inactive aligned items", () => {
		// Search for base placement, if not found create it
		const supplyNames = getSupplyNames("Alignments status filter");
		createOrUpdatePlacement(supplyNames).then(({ body: { id } }) => {
			// Navigate to edit placement route
			cy.visit(`/dashboard/placements/${id}`);
		});
		// Filter dimension options come from druid data and are non-deterministic so we mock them
		cy.intercept("GET", "**/search-dimension*", { fixture: "alignments/alignmentFilterOptions.json" }).as(
			"search-dimensions:status"
		);
		// Intercept the alignments request
		cy.intercept("GET", "**/placements/*/alignments", { fixture: "alignments/alignmentStatusFilter.json" }).as(
			"alignmentStatusFilter"
		);

		cy.clickElement(placementLocators.alignmentTab);

		// Check the Active Items
		// Open Filter
		cy.clickElement(placementLocators.addFilterDropdown);
		// Open Dimension list
		cy.clickElement(placementLocators.addDimensionDropdown);
		// Select status as dimension
		cy.clickElement(placementLocators.statusOptionSelect);
		// Select a status option
		cy.findByLabelText(placementLocators.filterValue).click();
		cy.findByRole("option", { name: placementLocators.filterStatusOptionActive }).click();
		// Click on save button
		cy.findByRole("button", { name: globalContent.SAVE }).click();
		cy.findByTestId("alignment-table-aligned")
			.contains("td", placementLocators.activeAlignedItemTitle)
			.should("be.visible");
		// Delete the Active filter
		cy.findByTestId("CancelIcon").click();

		// Check the Inactive Items
		// Open Filter
		cy.clickElement(placementLocators.addFilterDropdown);
		// Open Dimension list
		cy.clickElement(placementLocators.addDimensionDropdown);
		// Select status as dimension
		cy.clickElement(placementLocators.statusOptionSelect);
		// Select a status option
		cy.findByLabelText(placementLocators.filterValue).click();
		cy.findByRole("option", { name: placementLocators.filterStatusOptionInactive }).click();
		// Click on save button
		cy.findByRole("button", { name: globalContent.SAVE }).click();
		cy.findByTestId("alignment-table-aligned")
			.contains("td", placementLocators.inactiveAlignedItemTitle)
			.should("be.visible");
	});

	it("Placement alignment smoke test for media", () => {
		const supplyNames = getSupplyNames("Placement alignment smoke test for media");
		supplyNames.placmentBody = JSON.parse(JSON.stringify(DEFAULT_PLACEMENT_BODY));
		supplyNames.placmentBody.floor = 2;
		const demandNames = getDemandNames("Placement alignment smoke test for media");
		demandNames.mediaBody = JSON.parse(JSON.stringify(DEFAULT_MEDIA_BODY));
		demandNames.mediaBody.mediaCPM = 1;

		const companyId = getPrimaryCompanyId();
		createOrUpdateMedia(demandNames).then(({ body: { id: mediaId } }) => {
			createOrUpdatePlacement(supplyNames).then(({ body: { id: placementId } }) => {
				cy.visit(`/dashboard/placements/${placementId}`);
				cy.findByRole("tab", { name: localeContent.TABS.ALIGNMENTS }).click();

				const expectedMediaURL = `/dashboard/media/${mediaId}?companyId=${companyId}`;

				cy.findByTestId(localeContent.TEST_ID_FIELDS.ALIGNMENTS_TABLE_AVALIABLE).within(() => {
					cy.findByPlaceholderText("Search").clear().type(demandNames.mediaName);

					// Asserting that the link is the programmatic demand created
					cy.findByRole("link", { name: demandNames.mediaName }).should(
						"have.attr",
						"href",
						expectedMediaURL
					);

					cy.findByRole("link", { name: demandNames.mediaName }).should("have.attr", "target", "_blank");

					// Asserting that the link it will open in a new tab
					cy.findByRole("link", { name: demandNames.mediaName }).should("have.attr", "target", "_blank");

					// Saving aligments
					cy.findByLabelText(localeContent.FIELD_NAMES.TOGGLE_ROW_SELECTED).click();

					cy.findByRole("button", { name: localeContent.FIELD_NAMES.SAVE_ALIGNMENTS }).click();
				});

				cy.reload();
				cy.findByRole("tab", { name: localeContent.TABS.ALIGNMENTS }).click();

				cy.findByTestId(localeContent.TEST_ID_FIELDS.ALIGNMENTS_TABLE_ALIGN).within(() => {
					cy.findByPlaceholderText("Search").clear().type(demandNames.mediaName);

					// checking the link is aligned
					cy.findByRole("link", { name: demandNames.mediaName }).should(
						"have.attr",
						"href",
						expectedMediaURL
					);

					// we are going to unaligned to leave ready for the next execution of the test
					cy.findByLabelText(localeContent.FIELD_NAMES.TOGGLE_ROW_SELECTED).click();

					cy.findByRole("button", { name: localeContent.FIELD_NAMES.SAVE_ALIGNMENTS }).click();
				});

				cy.reload();
				cy.findByRole("tab", { name: localeContent.TABS.ALIGNMENTS }).click();

				// checking is un-align
				cy.findByTestId(localeContent.TEST_ID_FIELDS.ALIGNMENTS_TABLE_AVALIABLE).within(() => {
					cy.findByPlaceholderText("Search").clear().type(demandNames.mediaName);

					// Asserting that the link is the media created
					cy.findByRole("link", { name: demandNames.mediaName }).should(
						"have.attr",
						"href",
						expectedMediaURL
					);
				});
			});
		});
	});

	it("Placement alignment smoke test for display media", () => {
		const supplyNames = getSupplyNames("Placement display alignment smoke test for media");
		supplyNames.placementBody = DEFAULT_DISPLAY_PLACEMENT_BODY;
		const demandNames = getDemandNames("Placement display alignment smoke test for media");
		demandNames.mediaBody = JSON.parse(JSON.stringify(DEFAULT_DISPLAY_MEDIA_BODY));
		cy.deleteTargetEntity(getToken(), supplyNames.placementName, "placement");

		const companyId = getPrimaryCompanyId();
		createOrUpdateMedia(demandNames).then(({ body: { id: mediaId } }) => {
			createOrUpdatePlacement(supplyNames).then(({ body: { id: placementId } }) => {
				cy.visit(`/dashboard/placements/${placementId}`);
				cy.findByRole("tab", { name: localeContent.TABS.ALIGNMENTS }).click();

				const expectedMediaURL = `/dashboard/media/${mediaId}?companyId=${companyId}`;

				cy.findByTestId(localeContent.TEST_ID_FIELDS.ALIGNMENTS_TABLE_AVALIABLE).within(() => {
					cy.findByPlaceholderText("Search").clear().type(demandNames.mediaName);

					// Asserting that the link is the programmatic demand created
					cy.findByRole("link", { name: demandNames.mediaName }).should(
						"have.attr",
						"href",
						expectedMediaURL
					);

					// Saving alignments
					cy.findByLabelText(localeContent.FIELD_NAMES.TOGGLE_ROW_SELECTED).click();

					cy.findByRole("button", { name: localeContent.FIELD_NAMES.SAVE_ALIGNMENTS }).click();
				});

				cy.reload();
				cy.findByRole("tab", { name: localeContent.TABS.ALIGNMENTS }).click();
				cy.findByText("Aligned Demand");
				// checking is aligned
				cy.findByTestId(localeContent.TEST_ID_FIELDS.ALIGNMENTS_TABLE_ALIGN).within(() => {
					cy.findByPlaceholderText("Search").clear().type(demandNames.mediaName);

					// Asserting media is aligned
					cy.findByText(demandNames.mediaName).should("exist");
				});
			});
		});
	});

	it("Placement alignment smoke test for programmatic demand", () => {
		const supplyNames = getSupplyNames("Placement alignment smoke test for programmatic demand");
		const demandNames = getProgrammaticDemandNames("Placement alignment smoke test for programmatic demand");
		const companyId = getPrimaryCompanyId();

		createOrUpdateProgrammaticDemand(demandNames).then(({ body: { id: programmaticId } }) => {
			createOrUpdatePlacement(supplyNames).then(({ body: { id: placementId } }) => {
				cy.visit(`/dashboard/placements/${placementId}`);
				cy.findByRole("tab", { name: localeContent.TABS.ALIGNMENTS }).click();

				const expectedProgrammaticURL = `/dashboard/programmatic-demand/${programmaticId}?companyId=${companyId}`;

				cy.findByTestId(localeContent.TEST_ID_FIELDS.ALIGNMENTS_TABLE_AVALIABLE).within(() => {
					cy.findByPlaceholderText("Search").type(demandNames.programmaticName);

					// Asserting that the link is the programmatic demand created
					cy.findByRole("link", { name: demandNames.programmaticName }).should(
						"have.attr",
						"href",
						expectedProgrammaticURL
					);

					// Asserting that the link it will open in a new tab
					cy.findByRole("link", { name: demandNames.programmaticName }).should(
						"have.attr",
						"target",
						`_blank`
					);

					// Saving aligments
					cy.findByLabelText(localeContent.FIELD_NAMES.TOGGLE_ROW_SELECTED).click();

					cy.findByRole("button", { name: localeContent.FIELD_NAMES.SAVE_ALIGNMENTS }).click();
				});

				cy.findByTestId(localeContent.TEST_ID_FIELDS.ALIGNMENTS_TABLE_ALIGN).within(() => {
					cy.findByPlaceholderText("Search").type(demandNames.programmaticName);

					// checking the link is aligned
					cy.findByRole("link", { name: demandNames.programmaticName }).should(
						"have.attr",
						"href",
						expectedProgrammaticURL
					);

					// we are going to unaligned to leave ready for the next execution of the test
					cy.findByLabelText(localeContent.FIELD_NAMES.TOGGLE_ROW_SELECTED).click();

					cy.findByRole("button", { name: localeContent.FIELD_NAMES.SAVE_ALIGNMENTS }).click();
				});

				// checking is un-align
				cy.findByTestId("alignment-table-available").within(() => {
					cy.findByPlaceholderText("Search").type(demandNames.programmaticName);

					// Asserting that the link is the programmatic demand created
					cy.findByRole("link", { name: demandNames.programmaticName }).should(
						"have.attr",
						"href",
						expectedProgrammaticURL
					);
				});
			});
		});
	});

	it("Deleted Placement not visible in aligned tab in media", () => {
		// Search for base placement, if not found create it
		const supplyNames = getSupplyNames("Deleted Placement Not Visible in Aligned Tab");
		createOrUpdatePlacement(supplyNames);
		// search for media, if not found create it
		const demandNames = getDemandNames("Deleted Placement Not Visible in Aligned Tab");
		createOrUpdateMedia(demandNames).then(({ body: { id: mediaId } }) => {
			// visit media
			cy.visit(`/dashboard/media/${mediaId}`);
			// click on alignment tab
			cy.findByRole("tab", { name: localeContent.TABS.ALIGNMENTS }).click();
			cy.findByTestId(localeContent.TEST_ID_FIELDS.ALIGNMENTS_TABLE_AVALIABLE).within(() => {
				// select placement via searching
				cy.findByPlaceholderText(globalContent.SEARCH).type(supplyNames.placementName);
				// Saving alignments
				cy.findByLabelText(localeContent.TOGGLE_ROW_SELECTED).click();
				cy.findByRole("button", { name: localeContent.SAVE_ALIGNMENTS }).click();
			});
			// Visit placements index page
			cy.visit("/dashboard/placements");
			// Search target placement
			cy.search(supplyNames.placementName);
			// Wait for table to load and Click action button and delete option
			cy.clickDataGridDeleteMenuItem();
			cy.findByRole("button", { name: globalContent.CONFIRM_DELETE }).click();
			// Validate that success pop up shows and displays correct text
			cy.validatePopupMessage(`${supplyNames.placementName} ${globalContent.SUCCESSFULLY_DELETED_SUFFIX}`);
			// visit media again
			cy.visit(`/dashboard/media/${mediaId}`);
			// click on alignment tab
			cy.findByRole("tab", { name: localeContent.TABS.ALIGNMENTS }).click();
			// visit aligned tab
			cy.findByTestId(localeContent.TEST_ID_FIELDS.ALIGNMENTS_TABLE_ALIGN).within(() => {
				// select aligned placement via searching
				cy.findByPlaceholderText(globalContent.SEARCH).type(supplyNames.placementName);
				// checking the link is aligned
				cy.findByRole("link", { name: supplyNames.placementName }).should("not.exist");
			});
		});
	});
});
