import "cypress-file-upload";
import { getSupplyNames } from "../../../utils/resourceNameUtil";
import { globalContent } from "../../../locators/globalLocators";
import placementLocators, { localeContent } from "../../../locators/placementLocators";
import { createOrUpdatePlacement } from "../../../support/supplyCommands";
import { DASHBOARD_API } from "../../../utils/serviceResources";
import getPrimaryCompanyId from "../../../utils/getPrimaryCompany";
import { companyLocators as company } from "../../../locators/companyLocators";
import { DEFAULT_INSTREAM_PLACEMENT_BODY } from "../../../fixtures/defaultSupplySideCreationData";

describe("Placement edit test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	const cleanup = (placementNamePrefix) => {
		const pathDeleteResource = (resource) => {
			return DASHBOARD_API.PLACEMENT.getOne({ id: resource.id });
		};
		const indexPathResources = DASHBOARD_API.PLACEMENT.getIndex();

		const filterResourceToDelete = (resource) => resource.name.startsWith(placementNamePrefix);
		cy.cleanResources({ indexPathResources, pathDeleteResource, filterResourceToDelete });
	};

	it("User can navigate to edit placement form from index and save changes", () => {
		// Search for base placement, if not found create it
		const supplyNames = getSupplyNames("Placement edit smoke test");
		cleanup(supplyNames.placementName);
		createOrUpdatePlacement(supplyNames);

		// Visit placements index page
		cy.visit("/dashboard/placements");
		// Search for base placement
		cy.search(supplyNames.placementName);

		// Load the page and Click action button and edit
		cy.clickDataGridEditMenuItem();

		// Edit placement form and submit
		const editedName = "Edited Name";
		cy.findByRole("textbox", { name: localeContent.FIELD_NAMES.placementName }).clear().type(editedName);
		cy.findByRole("button", { name: globalContent.SAVE }).click();

		// Validate pop up is visible and displaying correct text
		cy.validatePopupMessage(`${editedName} was successfully updated`);
		// Validate name field has correct value
		cy.findByRole("textbox", { name: localeContent.FIELD_NAMES.placementName }).should("have.value", editedName);

		// Set name back to original and save form so that subsequent test runs can find it
		cy.findByRole("textbox", { name: localeContent.FIELD_NAMES.placementName })
			.clear()
			.type(supplyNames.placementName);

		cy.findByRole("button", { name: globalContent.SAVE }).click();
		cy.validatePopupMessage(`${supplyNames.placementName} was successfully updated`);
	});

	it("User can upload file and add manually for targeting", () => {
		// Search for base placement, if not found create it
		const supplyNames = getSupplyNames("Placement upload targeting");
		cleanup(supplyNames.placementName);
		createOrUpdatePlacement(supplyNames);

		// Visit placements index page
		cy.visit("/dashboard/placements");
		// Search for base placement
		cy.search(supplyNames.placementName);

		// Load the page and Click action button and edit
		cy.clickDataGridEditMenuItem();

		cy.clickElement(placementLocators.qualityTab);
		// Add app targeting
		cy.findByRole("checkbox", { name: localeContent.FIELD_NAMES.APP_ID_TARGETING }).click();
		//upload the image file
		const fileName = "appIds.csv";
		cy.get(placementLocators.uploadButton).attachFile({ filePath: `uploadFile/${fileName}` });
		// Validate appIds are uploaded
		cy.findByText("rokuappid").should("exist");
		// Validate app ids can be by typing in
		cy.findByPlaceholderText(localeContent.FIELD_NAMES.APP_BUNDLE_ID).type("appidtyped{enter}");
		cy.findByText("appidtyped").should("exist");
		cy.findByPlaceholderText(localeContent.FIELD_NAMES.APP_BUNDLE_ID).should("be.empty");

		cy.findByRole("button", { name: globalContent.SAVE }).click();
		cy.validatePopupMessage(`${supplyNames.placementName} was successfully updated`);
	});

	it("User can click allow cpm per second and it should be there after saved", () => {
		const companyId = getPrimaryCompanyId();

		cy.visit(`/dashboard/companies/${companyId}`);

		cy.clickElement(company.defaultsTab);

		cy.getByRole(company.serverSideRequestsSwitch)
			.invoke("is", ":checked")
			.then((checked) => {
				if (!checked) {
					cy.clickElement(company.serverSideRequestsSwitch);
				}
			});

		cy.findByRole("button", { name: globalContent.SAVE }).click();

		// Search for base placement, if not found create it
		const supplyNames = getSupplyNames("CPM per Second");
		createOrUpdatePlacement(supplyNames).then((response) => {
			const placement = response.body;
			cy.visit(`/dashboard/placements/${placement.id}`);

			cy.findByRole("checkbox", { name: localeContent.FIELD_NAMES.SERVER_SIDE_REQUEST }).click();

			cy.findByRole("radio", { name: localeContent.FIELD_NAMES.AUCTION_TYPE_FIRST_PRICE }).click();

			cy.findByRole("checkbox", { name: localeContent.FIELD_NAMES.CPM_PER_SECOND }).click();

			cy.findByRole("button", { name: globalContent.SAVE }).click();

			cy.validatePopupMessage(`${supplyNames.placementName} ${globalContent.SUCCESSFULLY_UPDATED_SUFFIX}`);

			cy.visit(`/dashboard/placements/${placement.id}`);

			cy.findByRole("checkbox", { name: localeContent.FIELD_NAMES.CPM_PER_SECOND }).should("be.checked");
		});
	});

	it("Validate tags should existing in Mobile/CTV type placements", () => {
		const supplyNames = getSupplyNames("Tag validations for Mobile/CTV Type Placements");
		createOrUpdatePlacement(supplyNames).then(({ body: { id: placementId } }) => {
			cy.visit(`/dashboard/placements/${placementId}`);
			cy.getByRole(placementLocators.placementTagField).should("not.be.empty");
			cy.getByRole(placementLocators.placementTagField).should("contain.text", "ssai=[REPLACE]");
			cy.getByRole(placementLocators.placementTagField).should("contain.text", "eid=[REPLACE]");
		});
	});

	it("User select placement type as instream while creating placement, then while editing it do not track flag should visible", () => {
		const supplyNames = getSupplyNames("Placement Instream type tag validation");
		supplyNames.placementBody = DEFAULT_INSTREAM_PLACEMENT_BODY;
		createOrUpdatePlacement(supplyNames).then(({ body: { id: placementId } }) => {
			cy.visit(`/dashboard/placements/${placementId}`);
			cy.getByRole(placementLocators.placementTagField).should("not.be.empty");
			cy.getByRole(placementLocators.placementTagField).should("contain.text", "dnt=[REPLACE]");
		});
	});

	it("User select placement type as ctv while creating placement, then while editing it allowInventoryPartnerDomain click", () => {
		const supplyNames = getSupplyNames("Placement ctv allowInventoryPartnerDomain true");
		supplyNames.placementBody = DEFAULT_INSTREAM_PLACEMENT_BODY;
		createOrUpdatePlacement(supplyNames).then(({ body: { id: placementId } }) => {
			cy.visit(`/dashboard/placements/${placementId}`);

			cy.findByRole("checkbox", { name: localeContent.FIELD_NAMES.ALLOW_INVENTORY_PARTNER_DOMAIN }).check();

			cy.findByRole("button", { name: globalContent.SAVE }).click();
			cy.validatePopupMessage(`${supplyNames.placementName} ${globalContent.SUCCESSFULLY_UPDATED_SUFFIX}`);

			cy.visit(`/dashboard/placements/${placementId}`);

			cy.findByRole("checkbox", { name: localeContent.FIELD_NAMES.ALLOW_INVENTORY_PARTNER_DOMAIN }).should(
				"be.checked"
			);
		});
	});

	it("Checks that only multiple impression or multiple impression can be selected in Mobile/CTV type placements", () => {
		const supplyNames = getSupplyNames("only multiple impression or multiple impression can be selected");
		createOrUpdatePlacement(supplyNames).then(({ body: { id: placementId } }) => {
			cy.visit(`/dashboard/placements/${placementId}`);
			cy.findByRole("radiogroup", { name: localeContent.FIELD_NAMES.MULTIPLE_WINNERS.LABEL }).within(() => {
				cy.findByRole("radio", { name: localeContent.FIELD_NAMES.MULTIPLE_WINNERS.OPTIONS.YES }).click();
			});

			//this should not be visible if multiple impression is on
			cy.findByRole("checkbox", { name: localeContent.FIELD_NAMES.MULTIPLE_IMP_OBJECTS }).check();

			cy.findByRole("button", { name: globalContent.SAVE }).click();

			cy.validatePopupMessage(`${supplyNames.placementName} ${globalContent.SUCCESSFULLY_UPDATED_SUFFIX}`);

			//this should not be visible if multiple impression is on (after saved)
			cy.getByRole("radiogroup", { name: localeContent.FIELD_NAMES.MULTIPLE_WINNERS.LABEL }).should("not.exist");

			//removing selecction of multiple impression
			cy.findByRole("checkbox", { name: localeContent.FIELD_NAMES.MULTIPLE_IMP_OBJECTS }).click();

			//then this should be avaliable and with the value of NO
			cy.findByRole("radiogroup", { name: localeContent.FIELD_NAMES.MULTIPLE_WINNERS.LABEL }).should("exist");

			cy.findByRole("radiogroup", { name: localeContent.FIELD_NAMES.MULTIPLE_WINNERS.LABEL }).within(() => {
				cy.findByRole("radio", { name: localeContent.FIELD_NAMES.MULTIPLE_WINNERS.OPTIONS.NO }).should(
					"be.checked"
				);
			});
		});
	});
});
