import "cypress-file-upload";
import { globalContent } from "../../../locators/globalLocators";
import { DEFAULT_MEDIA_BODY } from "../../../fixtures/defaultDemandSideCreationData";
import { DASHBOARD_API } from "../../../utils/serviceResources";
import { getDemandNames } from "../../../utils/resourceNameUtil";
import { localeContent } from "../../../locators/mediaLocators";
import { mediaLocators as media } from "../../../locators/mediaLocators";
import { createOrUpdateCampaign } from "../../../support/demandCommands";

const global = require("../../../locators/globalLocators.json");

describe("Media creation - GeoTargeting", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Validate postal code", () => {
		const resourceNames = getDemandNames("Validate postal code");

		const mediaAdTag = DEFAULT_MEDIA_BODY.adTag;

		const pathDeleteResource = (resource) => {
			return DASHBOARD_API.MEDIA.getOne({ id: resource.id });
		};
		const indexPathResources = DASHBOARD_API.MEDIA.getIndex();

		//Clean prior test runs, using the prefix
		const filterResourceToDelete = (resource) => resource.name.startsWith(resourceNames.mediaName);
		cy.cleanResources({ indexPathResources, pathDeleteResource, filterResourceToDelete });

		// Verify if base campaign exists if not create it
		createOrUpdateCampaign(resourceNames).then((response) => {
			const campaign = response.body;

			// Visit media index page
			cy.visit("/dashboard/media");

			// Verify that page title is media
			cy.get(global.pageTitle).should("have.text", localeContent.TITLE);

			// Add new media
			cy.clickElement(media.addMediaButton);
			cy.getByRole(media.campaignNameDropdown).type(campaign.name);

			cy.findAllByRole("option", { name: campaign.name }).first().click();

			// Verify that extra fields are visible or not for display
			cy.clickElement(media.mediaTypeDisplayRadio);
			cy.getByRole(media.sizeDropdown).should("exist");

			// Complete video mandatory fields
			cy.clickElement(media.mediaTypeVideoRadio);
			cy.getByRole(media.mediaNameField).type(resourceNames.mediaName);

			cy.getByRole(media.adTagField).type(mediaAdTag);

			// Go to quality tab and assert fields are visible
			cy.clickElement(media.qualityTab);

			cy.getByRole(media.geoTargetingToggle).check();
			cy.getByPlaceholderText(media.newPostalCodeInput).type("12345{enter}");

			cy.get(media.postalCodeUploadButton).attachFile({ filePath: "uploadFile/postalCodes.csv" });

			cy.intercept("**/media*").as("media");

			// Submit form
			cy.findByRole("button", { name: globalContent.SAVE }).click();

			cy.wait("@media").then(({ response }) => {
				cy.wrap(response.statusCode).should("be.oneOf", [200, 201]);
			});

			// Validate pop up is visible and it's text
			cy.validatePopupMessage(`${resourceNames.mediaName} was successfully created`);

			cy.contains("42345"); //postal code added via upload
			cy.contains("12345");
		});
	});
});
