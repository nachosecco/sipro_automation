import "cypress-file-upload";
import { globalContent } from "../../../locators/globalLocators";
import { localeContent as lc, mediaLocators as media } from "../../../locators/mediaLocators";
import { getDemandNames } from "../../../utils/resourceNameUtil";
import { createOrUpdateCampaign } from "../../../support/demandCommands";
import { DASHBOARD_API } from "../../../utils/serviceResources";

const cleanup = (mediaNamePrefix) => {
	const pathDeleteResource = (resource) => {
		return DASHBOARD_API.MEDIA.getOne({ id: resource.id });
	};
	const indexPathResources = DASHBOARD_API.MEDIA.getIndex();

	const filterResourceToDelete = (resource) => resource.name.startsWith(mediaNamePrefix);
	cy.cleanResources({ indexPathResources, pathDeleteResource, filterResourceToDelete });
};

describe("Display Media creation", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Valid display media - asset upload", () => {
		const resourceNames = getDemandNames("Valid display media");
		cleanup(resourceNames.mediaName);

		createOrUpdateCampaign(resourceNames).then((response) => {
			const campaign = response.body;
			// Visit media index page
			cy.visit("/dashboard/media");

			cy.findByRole("heading", { name: lc.TITLE }).should("exist");

			// Add new media
			cy.clickElement(media.addMediaButton);
			cy.getByRole(media.campaignNameDropdown).type(campaign.name);

			cy.findAllByRole("option", { name: campaign.name }).first().click();

			cy.getByRole(media.mediaNameField).type(`${resourceNames.mediaName}`);
			cy.getByRole(media.cpmField).type(1);

			// Select display media options
			cy.clickElement(media.mediaTypeDisplayRadio);
			cy.clickElement(media.mediaSourceAssetRadio);
			cy.clickElement(media.sizeDropdown);
			cy.clickElement(media.sizeDropdownOption970x250);

			//upload the image file
			const fileName = "970x250_Display.png";
			cy.get(media.uploadMediaFile).attachFile({ filePath: `uploadFile/${fileName}` });

			cy.validatePopupMessage(`${lc.UPLOAD_MESSAGE} ${fileName}`);

			// Submit form
			cy.findByRole("button", { name: globalContent.SAVE }).click();

			// Validate pop up is visible and it's text
			cy.validatePopupMessage(`${resourceNames.mediaName} was successfully created`);
		});
	});
});
