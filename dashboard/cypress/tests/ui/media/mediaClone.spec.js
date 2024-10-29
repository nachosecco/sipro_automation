import { globalContent } from "../../../locators/globalLocators";
import { createOrUpdateMedia, createOrUpdateMediaAlignments, cleanupMedia } from "../../../support/demandCommands";
import { getDemandNames, getSupplyNames } from "../../../utils/resourceNameUtil";
import { createOrUpdatePlacement } from "../../../support/supplyCommands";
import { mediaLocators } from "../../../locators/mediaLocators";

describe("Media clone test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Media clone with alignments", () => {
		const resourceNames = getDemandNames("clone with alignments");
		const placementResourceNames = getSupplyNames("clone with alignments");
		const clonedMediaName = resourceNames.mediaName + "_cloned";
		cleanupMedia(clonedMediaName);
		// create or update media
		createOrUpdateMedia(resourceNames).then((response) => {
			const media = response.body;
			// create or update placement
			createOrUpdatePlacement(placementResourceNames).then((placementResponse) => {
				const placement = placementResponse.body;
				// Align placement with the media
				createOrUpdateMediaAlignments({ placements: [placement], mediaId: media.id }).then(() => {
					cy.visit(`/dashboard/media/${media.id}?clone=true`);
					cy.getByRole(mediaLocators.mediaNameField).type(clonedMediaName);
					cy.findByRole("button", { name: globalContent.SAVE }).click();
					cy.validatePopupMessage(`${clonedMediaName} ${globalContent.SUCCESSFULLY_CREATED_SUFFIX}`);
					cy.clickElement(mediaLocators.alignmentsTab);

					// validate cloned media has the placement aligned
					cy.findByTestId("alignment-table-aligned").within(() => {
						cy.findByText(placementResourceNames.placementName).should("exist");
					});
				});
			});
		});
	});

	it("Media clone without alignments", () => {
		const resourceNames = getDemandNames("clone without alignments");
		const placementResourceNames = getSupplyNames("clone without alignments");
		const clonedMediaName = resourceNames.mediaName + "_cloned";
		cleanupMedia(clonedMediaName);
		// create or update media
		createOrUpdateMedia(resourceNames).then((response) => {
			const media = response.body;
			// create or update placement
			createOrUpdatePlacement(placementResourceNames).then((placementResponse) => {
				const placement = placementResponse.body;
				// Do not Align placement with the media
				createOrUpdateMediaAlignments({ placements: [placement], mediaId: media.id }).then(() => {
					cy.visit(`/dashboard/media/${media.id}?clone=true`);
					cy.getByRole(mediaLocators.mediaNameField).type(clonedMediaName);
					cy.clickElement(mediaLocators.cloneAlignments);
					cy.findByRole("button", { name: globalContent.SAVE }).click();
					cy.validatePopupMessage(`${clonedMediaName} ${globalContent.SUCCESSFULLY_CREATED_SUFFIX}`);
					cy.clickElement(mediaLocators.alignmentsTab);

					// validate cloned media has not the placement aligned
					cy.findByTestId("alignment-table-aligned").within(() => {
						cy.findByText(placementResourceNames.placementName).should("not.exist");
					});
				});
			});
		});
	});
});
