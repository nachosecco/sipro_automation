import DEFAULT_COMPANY_REQUEST_BODY from "../../../fixtures/defaultCompanyRequestBody";
import { createOrUpdateCompany } from "../../../support/companyCommands";
import { cleanupPlacement, createOrUpdateSite } from "../../../support/supplyCommands";
import { getSupplyNames, getTestResourceName } from "../../../utils/resourceNameUtil";
import { globalContent } from "../../../locators/globalLocators";
import appendRequired from "../../../utils/appendRequired";
import { localeContent as placementLc } from "../../../locators/placementLocators";
import { localeContent as companyLc } from "../../../locators/companyLocators";

describe("Bidder Service Placements", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Bidder Placements are enabled based on company setting", () => {
		// Configure entity names
		const companyName = getTestResourceName("Bidder Placements");
		const supplyNames = getSupplyNames("Bidder Placements");
		const invalidPlacementName = getTestResourceName("Bidder Placements - Invalid");
		// Programmatically create the Bidder Service company, disabling the bidder service
		createOrUpdateCompany({
			companyName,
			companyBody: { ...DEFAULT_COMPANY_REQUEST_BODY, bidderServiceEnabled: false },
		}).then(({ body: { id: newCompanyId } }) => {
			// Search for last test run placements and delete if found
			cleanupPlacement(supplyNames.placementName, newCompanyId);
			cleanupPlacement(invalidPlacementName, newCompanyId);

			// Programmatically create a site under the new company
			createOrUpdateSite({ ...supplyNames, companyOverride: newCompanyId }).then(
				({ body: { id: newSiteId } }) => {
					// Navigate to the create placement page for the new company with the new site's parent id prefilled
					cy.visit(`/dashboard/placements/INIT?parentId=${newSiteId}&companyId=${newCompanyId}`);
					// Expect the Request Type field not to be rendered
					cy.findByLabelText(appendRequired(placementLc.FIELD_NAMES.placementName)).should("exist");
					cy.findByLabelText(placementLc.FIELD_NAMES.REQUEST_TYPE.LABEL).should("not.exist");

					// Navigate to the new company's settings page
					cy.visit(`/dashboard/companies/${newCompanyId}`);
					// Click on defaults tab
					cy.findByRole("tab", { name: placementLc.TABS.DEFAULTS }).click();
					// Turn on the bidder service
					cy.findByLabelText(companyLc.FIELDS.BIDDER_SERVICE_ENABLED.LABEL).click();
					// Save the form
					cy.findByRole("button", { name: globalContent.SAVE }).click();
					// Verify success message
					cy.validatePopupMessage(`${companyName} ${globalContent.SUCCESSFULLY_UPDATED_SUFFIX}`);

					// Navigate to the create placement page with the new site's parent id prefilled
					cy.visit(`/dashboard/placements/INIT?parentId=${newSiteId}&companyId=${newCompanyId}`);
					// Create a placement using the bidder service to prove it works
					cy.findByLabelText(appendRequired(placementLc.FIELD_NAMES.placementName)).type(
						supplyNames.placementName
					);
					cy.findByLabelText(placementLc.FIELD_NAMES.REQUEST_TYPE.LABEL).should("exist");
					// Turn on the service
					cy.findByRole("radio", { name: placementLc.FIELD_NAMES.REQUEST_TYPE.OPTIONS.RTB }).click();
					// Save the form
					cy.findByRole("button", { name: globalContent.SAVE }).click();
					// Verify success message
					cy.validatePopupMessage(
						`${supplyNames.placementName} ${globalContent.SUCCESSFULLY_CREATED_SUFFIX}`
					);

					// Navigate once more to the create placement page with new site's parent id prefilled
					cy.visit(`/dashboard/placements/INIT?parentId=${newSiteId}&companyId=${newCompanyId}`);
					// Wait for form to load
					cy.findByLabelText(appendRequired(placementLc.FIELD_NAMES.placementName)).should("exist");
					// Programmatically disable the bidder service for the company in the background
					createOrUpdateCompany({
						companyName,
						companyBody: { ...DEFAULT_COMPANY_REQUEST_BODY, bidderServiceEnabled: false },
					});
					// Attempt to create a Bidder Placement that will not be allowed because service is off now
					cy.findByLabelText(appendRequired(placementLc.FIELD_NAMES.placementName)).type(
						invalidPlacementName
					);
					cy.findByRole("radio", { name: placementLc.FIELD_NAMES.REQUEST_TYPE.OPTIONS.RTB }).click();
					// Attempt to save the form
					cy.findByRole("button", { name: globalContent.SAVE }).click();
					// Expect server side error message to render and no success message
					cy.findByText(placementLc.VALIDATION_MESSAGES.BIDDER_SERVICE_NOT_ENABLED_FOR_COMPANY).should(
						"exist"
					);
					cy.findByText(`${invalidPlacementName} ${globalContent.SUCCESSFULLY_CREATED_SUFFIX}`).should(
						"not.exist"
					);
				}
			);
		});
	});

	it("Saves placement as a tag type after enabling bidder service and switching placement type to a non-allowed variant", () => {
		// Configure entity names
		const companyName = getTestResourceName("Bidder Placements - Placement Type");
		const supplyNames = getSupplyNames("Bidder Placements - Placement Type");
		const instreamPlacementName = getTestResourceName("Bidder Placements - Instream");
		const outstreamPlacementName = getTestResourceName("Bidder Placements - Outstream");
		const displayPlacementName = getTestResourceName("Bidder Placements - Display");
		// Programmatically create the Bidder Service company, enabling the bidder service
		createOrUpdateCompany({
			companyName,
			companyBody: { ...DEFAULT_COMPANY_REQUEST_BODY, bidderServiceEnabled: true },
		}).then(({ body: { id: newCompanyId } }) => {
			// Search for last test run placements and delete if found
			cleanupPlacement(instreamPlacementName, newCompanyId);
			cleanupPlacement(outstreamPlacementName, newCompanyId);
			cleanupPlacement(displayPlacementName, newCompanyId);

			// Programmatically create a site under the new company
			createOrUpdateSite({ ...supplyNames, companyOverride: newCompanyId }).then(
				({ body: { id: newSiteId } }) => {
					// Create a function to enable bidder, then change type to one that can't use the bidder service and save form.
					const testPlacementType = (placementTypeLabel, placementName, fillOutAdditionalRequiredFields) => {
						// Navigate to the create placement page for the new company with the new site's parent id prefilled
						cy.visit(`/dashboard/placements/INIT?parentId=${newSiteId}&companyId=${newCompanyId}`);
						// Select the Bidder Service radio
						cy.findByRole("radio", { name: placementLc.FIELD_NAMES.REQUEST_TYPE.OPTIONS.RTB }).click();
						// Change the placement type
						cy.findByLabelText(placementLc.FIELD_NAMES.TYPE.LABEL).click();
						cy.findByRole("option", { name: placementTypeLabel }).click();
						// Give the placement a name and save the form
						cy.findByLabelText(appendRequired(placementLc.FIELD_NAMES.placementName)).type(placementName);
						// Some types have additional required fields
						if (fillOutAdditionalRequiredFields) {
							fillOutAdditionalRequiredFields();
						}
						cy.findByRole("button", { name: globalContent.SAVE }).click();
						// Verify success message
						cy.validatePopupMessage(`${placementName} ${globalContent.SUCCESSFULLY_CREATED_SUFFIX}`);
					};

					testPlacementType(placementLc.FIELD_NAMES.TYPE.OPTIONS.VAST, instreamPlacementName);
					testPlacementType(placementLc.FIELD_NAMES.TYPE.OPTIONS.OUTSTREAM, outstreamPlacementName);
					// Display has an additional required field
					testPlacementType(
						placementLc.FIELD_NAMES.TYPE.OPTIONS.DISPLAY,
						displayPlacementName,
						function fillOutRequiredDisplayFields() {
							cy.findByLabelText(appendRequired(placementLc.FIELD_NAMES.SIZE)).click();
							cy.findAllByRole("option").eq(0).click();
						}
					);
				}
			);
		});
	});
});
