import { getProgrammaticDemandNames, getSupplyNames } from "../../../utils/resourceNameUtil";

import { globalContent } from "../../../locators/globalLocators";
import { createOrUpdatePlacement } from "../../../support/supplyCommands";
import { createOrUpdateBidder } from "../../../support/bidderCommands";
import programmaticLocators, { localeContent } from "../../../locators/programmaticLocators";
import { DASHBOARD_API } from "../../../utils/serviceResources";
import getPrimaryCompanyId from "../../../utils/getPrimaryCompany";
import { createOrUpdateProgrammaticDemand } from "../../../support/demandCommands";

const cleanup = (programmaticDemand) => {
	const pathDeleteResource = (resource) => {
		return DASHBOARD_API.PROGRAMMATIC_DEMAND.getOne({ id: resource.id });
	};
	const indexPathResources = DASHBOARD_API.PROGRAMMATIC_DEMAND.getIndex();
	const filterResourceToDelete = (resource) => resource.name === programmaticDemand;
	cy.cleanResources({ indexPathResources, pathDeleteResource, filterResourceToDelete });
};

describe("Alignments in programmatic demand", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});
	it("Deleted Placement not visible in aligned tab in programmatic demand", () => {
		// Search for base placement, if not found create it
		const supplyNames = getSupplyNames("Deleted Placement not visible in aligned tab in programmatic demand");
		createOrUpdatePlacement(supplyNames);

		const resourceNames = getProgrammaticDemandNames(
			"Deleted Placement not visible in aligned tab in programmatic demand"
		);
		cleanup(resourceNames.programmaticName);

		createOrUpdateBidder(resourceNames);

		// Visit programmatic index page
		cy.visit("/dashboard/programmatic-demand");

		// Assert and click add programmatic button
		cy.clickElement(programmaticLocators.addProgrammaticDemandButton);
		// Complete mandatory fields
		cy.findByLabelText(localeContent.FIELDS.NAME.LABEL).type(resourceNames.programmaticName);
		cy.findByPlaceholderText(localeContent.FIELDS.BIDDER_CONFIG.SEARCH).type(resourceNames.bidderName);

		cy.findAllByRole("listitem", { name: resourceNames.bidderName })
			.first()
			// Submit form
			.within(() => {
				cy.findByRole("button", { name: localeContent.FIELDS.BIDDER_CONFIG.ADD_BIDDER }).click();
			});

		cy.findByText(resourceNames.bidderName).click();
		cy.findByRole("button", { name: "add Seat1" }).click();

		cy.findByRole("button", { name: globalContent.SAVE }).click();

		// click on alignment tab
		cy.findByRole("tab", { name: localeContent.TABS.ALIGNMENTS }).click();
		cy.findByTestId(localeContent.TEST_ID_FIELDS.ALIGNMENTS_TABLE_AVAILABLE).within(() => {
			// select placement via searching
			cy.findByPlaceholderText(globalContent.SEARCH).type(supplyNames.placementName);
			// Saving alignments
			cy.findByLabelText(localeContent.FIELDS.TOGGLE_ROW_SELECTED).click();
			cy.findByRole("button", { name: localeContent.FIELDS.SAVE_ALIGNMENTS }).click();
		});

		// Visit placements index page
		cy.visit("/dashboard/placements");
		// Search target placement
		cy.search(supplyNames.publisherName);
		// Wait for table to load and Click action button and delete option
		cy.clickDataGridDeleteMenuItem();
		cy.findByRole("button", { name: globalContent.CONFIRM_DELETE }).click();
		// Validate that success pop up shows and displays correct text
		cy.validatePopupMessage(`${supplyNames.placementName} ${globalContent.SUCCESSFULLY_DELETED_SUFFIX}`);

		// Visit programmatic index page
		cy.visit("/dashboard/programmatic-demand");
		// Search for target programmatic demand entity
		cy.search(resourceNames.programmaticName);
		cy.findByRole("link", { name: resourceNames.programmaticName }).click();

		cy.findByRole("tab", { name: localeContent.TABS.ALIGNMENTS }).click();
		// visit aligned tab
		cy.findByTestId(localeContent.TEST_ID_FIELDS.ALIGNMENTS_TABLE_ALIGN).within(() => {
			// select aligned placement via searching
			cy.findByPlaceholderText(globalContent.SEARCH).type(supplyNames.placementName);
			// checking the link is aligned
			cy.findByRole("link", { name: supplyNames.placementName }).should("not.exist");
		});
	});

	it("Programmatic smoke alignment tests", () => {
		const supplyNames = getSupplyNames("Programmatic smoke alignment tests");
		const demandNames = getProgrammaticDemandNames("Programmatic smoke alignment tests");
		const companyId = getPrimaryCompanyId();

		createOrUpdateProgrammaticDemand(demandNames).then(({ body: { id: programmaticId } }) => {
			createOrUpdatePlacement(supplyNames).then(({ body: { id: placementId } }) => {
				cy.visit(`/dashboard/programmatic-demand/${programmaticId}`);
				cy.findByRole("tab", { name: localeContent.TABS.ALIGNMENTS }).click();

				const expectedPlacementURL = `/dashboard/placements/${placementId}?companyId=${companyId}`;

				cy.findByTestId(localeContent.TEST_ID_FIELDS.ALIGNMENTS_TABLE_AVAILABLE).within(() => {
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
				cy.findByTestId(localeContent.TEST_ID_FIELDS.ALIGNMENTS_TABLE_AVAILABLE).within(() => {
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
