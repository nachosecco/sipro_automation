import { globalContent } from "../../../locators/globalLocators";
import {
	cleanupDemand,
	createOrUpdateDemandAlignments,
	createOrUpdateProgrammaticDemand,
} from "../../../support/demandCommands";
import { getProgrammaticDemandNames, getSupplyNames } from "../../../utils/resourceNameUtil";
import { cleanupPlacement, createOrUpdatePlacement } from "../../../support/supplyCommands";

import programmaticLocators from "../../../locators/programmaticLocators";
import { DEFAULT_DEAL_PROGRAMMATIC_REQUEST_BODY } from "../../../fixtures/defaultDemandSideCreationData";

describe("Programmatic clone test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Programmatic clone with alignments", () => {
		const placementResourceNames = getSupplyNames("Programmatic clone with alignments");
		const resourceNames = getProgrammaticDemandNames("Programmatic clone with alignments");
		const clonedDemandName = resourceNames.programmaticName + "_cloned";
		cleanupDemand(clonedDemandName);
		cleanupPlacement(placementResourceNames.placementName);
		// Create or update programmatic demand
		createOrUpdateProgrammaticDemand(resourceNames).then((response) => {
			const programmaticDemand = response.body;

			// create of update placement
			createOrUpdatePlacement(placementResourceNames).then((placementResponse) => {
				const placement = placementResponse.body;

				// Align placement with the demand
				createOrUpdateDemandAlignments({ placements: [placement], demandId: programmaticDemand.id }).then(
					() => {
						cy.visit(`/dashboard/programmatic-demand/${programmaticDemand.id}?clone=true`);
						cy.getByRole(programmaticLocators.demandNameField).type(clonedDemandName);
						cy.findByRole("button", { name: globalContent.SAVE }).click();
						cy.validatePopupMessage(`${clonedDemandName} ${globalContent.SUCCESSFULLY_CREATED_SUFFIX}`);
						cy.clickElement(programmaticLocators.alignmentsTab);
						// Validate cloned demand should be aligned with the placement
						cy.findByTestId("alignment-table-aligned").within(() => {
							cy.findByText(placementResourceNames.placementName).should("exist");
						});
					}
				);
			});
		});
	});

	it("Programmatic clone without the alignments", () => {
		const placementResourceNames = getSupplyNames("Programmatic clone without alignments");
		const resourceNames = getProgrammaticDemandNames("Programmatic clone without alignments");
		const clonedDemandName = resourceNames.programmaticName + "_cloned";
		cleanupDemand(clonedDemandName);
		cleanupPlacement(placementResourceNames.placementName);
		// Create or update programmatic demand
		createOrUpdateProgrammaticDemand(resourceNames).then((response) => {
			const programmaticDemand = response.body;

			// create of update placement
			createOrUpdatePlacement(placementResourceNames).then((placementResponse) => {
				const placement = placementResponse.body;

				// Align placement with the demand
				createOrUpdateDemandAlignments({ placements: [placement], demandId: programmaticDemand.id }).then(
					() => {
						cy.visit(`/dashboard/programmatic-demand/${programmaticDemand.id}?clone=true`);
						cy.getByRole(programmaticLocators.demandNameField).type(clonedDemandName);
						cy.clickElement(programmaticLocators.cloneAlignments);
						cy.findByRole("button", { name: globalContent.SAVE }).click();
						cy.validatePopupMessage(`${clonedDemandName} ${globalContent.SUCCESSFULLY_CREATED_SUFFIX}`);
						cy.clickElement(programmaticLocators.alignmentsTab);
						// Validate cloned demand should not be aligned with the placement
						cy.findByTestId("alignment-table-aligned").within(() => {
							cy.findByText(placementResourceNames.placementName).should("not.exist");
						});
					}
				);
			});
		});
	});

	it("Deal Programmatic clone with alignments", () => {
		const placementResourceNames = getSupplyNames("Deal Programmatic clone with alignments");
		const resourceNames = getProgrammaticDemandNames("Deal Programmatic clone with alignments");
		resourceNames.programmaticBody = DEFAULT_DEAL_PROGRAMMATIC_REQUEST_BODY;
		const clonedDemandName = resourceNames.programmaticName + "_cloned";

		cleanupDemand(clonedDemandName);
		cleanupPlacement(placementResourceNames.placementName);

		// Create or update programmatic demand
		createOrUpdateProgrammaticDemand(resourceNames).then((response) => {
			const programmaticDemand = response.body;

			// create of update placement
			createOrUpdatePlacement(placementResourceNames).then((placementResponse) => {
				const placement = placementResponse.body;

				// Align placement with the demand
				createOrUpdateDemandAlignments({ placements: [placement], demandId: programmaticDemand.id }).then(
					() => {
						cy.visit(`/dashboard/programmatic-demand/${programmaticDemand.id}?clone=true`);
						cy.getByRole(programmaticLocators.demandNameField).type(clonedDemandName);
						cy.getByRole(programmaticLocators.dealIdField).type("clone");
						cy.findByRole("button", { name: globalContent.SAVE }).click();
						cy.clickElement(programmaticLocators.alignmentsTab);

						cy.validatePopupMessage(`${clonedDemandName} ${globalContent.SUCCESSFULLY_CREATED_SUFFIX}`);
						// Validate cloned demand should be aligned with the placement
						cy.findByTestId("alignment-table-aligned").within(() => {
							cy.findByText(placementResourceNames.placementName).should("exist");
						});
					}
				);
			});
		});
	});

	it("Deal Programmatic clone without the alignments", () => {
		const placementResourceNames = getSupplyNames("Deal Programmatic clone without alignments");
		const resourceNames = getProgrammaticDemandNames("Deal Programmatic clone without alignments");
		resourceNames.programmaticBody = DEFAULT_DEAL_PROGRAMMATIC_REQUEST_BODY;
		const clonedDemandName = resourceNames.programmaticName + "_cloned";

		cleanupDemand(clonedDemandName);
		cleanupPlacement(placementResourceNames.placementName);

		// Create or update programmatic demand
		createOrUpdateProgrammaticDemand(resourceNames).then((response) => {
			const programmaticDemand = response.body;

			// create of update placement
			createOrUpdatePlacement(placementResourceNames).then((placementResponse) => {
				const placement = placementResponse.body;

				// Align placement with the demand
				createOrUpdateDemandAlignments({ placements: [placement], demandId: programmaticDemand.id }).then(
					() => {
						cy.visit(`/dashboard/programmatic-demand/${programmaticDemand.id}?clone=true`);
						cy.getByRole(programmaticLocators.demandNameField).type(clonedDemandName);
						cy.getByRole(programmaticLocators.dealIdField).type("cloneCopy");
						cy.clickElement(programmaticLocators.cloneAlignments);
						cy.findByRole("button", { name: globalContent.SAVE }).click();
						cy.validatePopupMessage(`${clonedDemandName} ${globalContent.SUCCESSFULLY_CREATED_SUFFIX}`);
						// Validate cloned demand should not be aligned with the placement
						cy.clickElement(programmaticLocators.alignmentsTab);
						cy.findByTestId("alignment-table-aligned").within(() => {
							cy.findByText(placementResourceNames.placementName).should("not.exist");
						});
					}
				);
			});
		});
	});
});
