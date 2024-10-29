import { getDemandNames, getProgrammaticDemandNames, getSupplyNames } from "../../../utils/resourceNameUtil";
import { globalContent } from "../../../locators/globalLocators";
import {
	cleanupPlacement,
	createOrUpdatePlacement,
	createOrUpdatePlacementAlignments,
} from "../../../support/supplyCommands";
import {
	cleanupDemand,
	cleanupMedia,
	createOrUpdateMedia,
	createOrUpdateProgrammaticDemand,
} from "../../../support/demandCommands";
import placementLocators from "../../../locators/placementLocators";
import { DEFAULT_DEAL_PROGRAMMATIC_REQUEST_BODY } from "../../../fixtures/defaultDemandSideCreationData";

describe("Placement clone test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Placement clone with alignments", () => {
		const supplyNames = getSupplyNames("Placement clone with alignments");
		const mediaNames = getDemandNames("Media clone with alignments");
		const clonedPlacementName = supplyNames.placementName + "_cloned";
		cleanupPlacement(clonedPlacementName);
		cleanupMedia(mediaNames.mediaName);
		// create or update placement
		createOrUpdatePlacement(supplyNames).then((placementResponse) => {
			const placement = placementResponse.body;
			// create or update media
			createOrUpdateMedia(mediaNames).then((mediaResponse) => {
				const media = mediaResponse.body;
				media.auditEvent = null;
				// Align media with placement
				createOrUpdatePlacementAlignments({
					placementId: placement.id,
					medias: [media],
					programmaticDemands: [],
				}).then(() => {
					cy.visit(`/dashboard/placements/${placement.id}?clone=true`);
					cy.getByRole(placementLocators.placementNameField).type(clonedPlacementName);
					cy.findByRole("button", { name: globalContent.SAVE }).click();
					cy.validatePopupMessage(`${clonedPlacementName} ${globalContent.SUCCESSFULLY_CREATED_SUFFIX}`);
					cy.clickElement(placementLocators.alignmentTab);

					//validated newly created cloned placement has media aligned
					cy.findByTestId("alignment-table-aligned").within(() => {
						cy.findByText(mediaNames.mediaName).should("exist");
					});
				});
			});
		});
	});

	it("Placement clone without alignments", () => {
		const supplyNames = getSupplyNames("Placement clone without alignments");
		const mediaNames = getDemandNames("Media clone without alignments");
		const clonedPlacementName = supplyNames.placementName + "_cloned";
		cleanupPlacement(clonedPlacementName);
		cleanupMedia(mediaNames.mediaName);
		// create or update placement
		createOrUpdatePlacement(supplyNames).then((placementResponse) => {
			const placement = placementResponse.body;
			// create or update media
			createOrUpdateMedia(mediaNames).then((mediaResponse) => {
				const media = mediaResponse.body;
				media.auditEvent = null;
				// Align media with placement
				createOrUpdatePlacementAlignments({
					placementId: placement.id,
					medias: [media],
					programmaticDemands: [],
				}).then(() => {
					cy.visit(`/dashboard/placements/${placement.id}?clone=true`);
					cy.getByRole(placementLocators.placementNameField).type(clonedPlacementName);
					cy.clickElement(placementLocators.cloneAlignments);
					cy.findByRole("button", { name: globalContent.SAVE }).click();
					cy.validatePopupMessage(`${clonedPlacementName} ${globalContent.SUCCESSFULLY_CREATED_SUFFIX}`);
					cy.clickElement(placementLocators.alignmentTab);

					//validated newly created cloned placement should not aligned media
					cy.findByTestId("alignment-table-aligned").within(() => {
						cy.findByText(mediaNames.mediaName).should("not.exist");
					});
				});
			});
		});
	});

	it("Clone placement with Deal demands as alignments", () => {
		const supplyNames = getSupplyNames("Placement Clone with deal alignments");
		const demandNames = getProgrammaticDemandNames("Placement Clone with deal alignments");
		const clonedPlacementName = supplyNames.placementName + "_cloned";
		demandNames.programmaticBody = DEFAULT_DEAL_PROGRAMMATIC_REQUEST_BODY;

		cleanupPlacement(clonedPlacementName);
		cleanupDemand(demandNames.programmaticName);
		// create or update placement
		createOrUpdatePlacement(supplyNames).then((placementResponse) => {
			const placement = placementResponse.body;
			// create or update media
			createOrUpdateProgrammaticDemand(demandNames).then((demandResponse) => {
				const demand = demandResponse.body;
				demand.auditEvent = null;
				// Align media with placement
				createOrUpdatePlacementAlignments({
					id: placement.id,
					placementId: placement.id,
					medias: [],
					programmaticDemands: [demand],
				}).then(() => {
					cy.visit(`/dashboard/placements/${placement.id}?clone=true`);
					cy.getByRole(placementLocators.placementNameField).type(clonedPlacementName);
					cy.findByRole("button", { name: globalContent.SAVE }).click();
					cy.validatePopupMessage(`${clonedPlacementName} ${globalContent.SUCCESSFULLY_CREATED_SUFFIX}`);
					cy.clickElement(placementLocators.alignmentTab);

					//validated newly created cloned placement has media aligned
					cy.findByTestId("alignment-table-aligned").within(() => {
						cy.findByText(demandNames.programmaticName).should("exist");
					});
				});
			});
		});
	});

	it("Clone placement with Deal demands without alignments", () => {
		const supplyNames = getSupplyNames("Placement Clone without deal alignments");
		const demandNames = getProgrammaticDemandNames("Placement Clone without deal alignments");
		const clonedPlacementName = supplyNames.placementName + "_cloned";
		demandNames.programmaticBody = DEFAULT_DEAL_PROGRAMMATIC_REQUEST_BODY;

		cleanupPlacement(clonedPlacementName);
		cleanupDemand(demandNames.programmaticName);
		// create or update placement
		createOrUpdatePlacement(supplyNames).then((placementResponse) => {
			const placement = placementResponse.body;
			// create or update media
			createOrUpdateProgrammaticDemand(demandNames).then((demandResponse) => {
				const demand = demandResponse.body;
				demand.auditEvent = null;
				// Align media with placement
				createOrUpdatePlacementAlignments({
					id: placement.id,
					placementId: placement.id,
					medias: [],
					programmaticDemands: [demand],
				}).then(() => {
					cy.visit(`/dashboard/placements/${placement.id}?clone=true`);
					cy.getByRole(placementLocators.placementNameField).type(clonedPlacementName);
					cy.clickElement(placementLocators.cloneAlignments);
					cy.findByRole("button", { name: globalContent.SAVE }).click();
					cy.validatePopupMessage(`${clonedPlacementName} ${globalContent.SUCCESSFULLY_CREATED_SUFFIX}`);
					cy.clickElement(placementLocators.alignmentTab);

					//validated newly created cloned placement has not media aligned
					cy.findByTestId("alignment-table-aligned").within(() => {
						cy.findByText(demandNames.programmaticName).should("not.exist");
					});
				});
			});
		});
	});
});
