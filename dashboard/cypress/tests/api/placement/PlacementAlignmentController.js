import { getDemandNames, getSupplyNames } from "../../../utils/resourceNameUtil";
import { createOrUpdatePlacement, getAllAlignments } from "../../../support/supplyCommands";
import { createOrUpdateMedia, createOrUpdateMediaAlignments } from "../../../support/demandCommands";

describe("Placement api alignment test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Placement api alignment get all", () => {
		// Verify if base site exists if not create it
		const supplyNames = getSupplyNames("Placement api alignment get all");

		// Create the placement by api
		createOrUpdatePlacement(supplyNames).then((response) => {
			const placement = response.body;
			const demandNames = getDemandNames("Placement api alignment get all");

			createOrUpdateMedia(demandNames).then((response) => {
				const mediaId = response.body.id;

				createOrUpdateMediaAlignments({ placements: [placement], mediaId }).then(() => {
					//now that the placement & media is createad and align,
					// lets call the api and test if the value create is there
					getAllAlignments({}).then((response) => {
						const allAlignments = response.body;

						const alignments = allAlignments.filter((value) => value.idPlacement === placement.id);

						cy.wrap(Cypress._.size(alignments)).as("alignments").should("equal", 1);
					});
				});
			});
		});
	});
});
