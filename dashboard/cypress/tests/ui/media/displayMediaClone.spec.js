import "cypress-file-upload";
import { globalContent } from "../../../locators/globalLocators";
import { localeContent as lc, mediaLocators } from "../../../locators/mediaLocators";
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
		const clonedMediaName = resourceNames.mediaName + "_cloned";
		cleanup(clonedMediaName);
		createOrUpdateCampaign(resourceNames).then((response) => {
			const campaign = response.body;
			// Visit media index page
			cy.visit("/dashboard/media");

			cy.findByRole("heading", { name: lc.TITLE }).should("exist");

			// Add new media
			cy.clickElement(mediaLocators.addMediaButton);
			cy.getByRole(mediaLocators.campaignNameDropdown).type(campaign.name);

			cy.findAllByRole("option", { name: campaign.name }).first().click();

			cy.getByRole(mediaLocators.mediaNameField).type(`${resourceNames.mediaName}`);
			cy.getByRole(mediaLocators.cpmField).type(1);

			// Select display media options
			cy.clickElement(mediaLocators.mediaTypeDisplayRadio);
			cy.clickElement(mediaLocators.mediaSourceAssetRadio);
			cy.clickElement(mediaLocators.sizeDropdown);
			cy.clickElement(mediaLocators.sizeDropdownOption970x250);

			//upload the image file
			const fileName = "970x250_Display.png";
			cy.get(mediaLocators.uploadMediaFile).attachFile({ filePath: `uploadFile/${fileName}` });

			cy.validatePopupMessage(`${lc.UPLOAD_MESSAGE} ${fileName}`);

			// Submit form
			cy.findByRole("button", { name: globalContent.SAVE }).click();

			// Validate pop up is visible and it's text
			cy.validatePopupMessage(`${resourceNames.mediaName} was successfully created`);

			cy.location("pathname").then((path) => {
				// extract newly created media id from the url
				const mediaId = path.split("/")[3];
				//Clone the new display media
				cy.visit(`/dashboard/media/${mediaId}?clone=true`);
				cy.getByRole(mediaLocators.mediaNameField).type(clonedMediaName);
				// Submit form
				cy.findByRole("button", { name: globalContent.SAVE }).click();

				// Validate pop up is visible and it's text
				cy.validatePopupMessage(`${clonedMediaName} was successfully created`);

				cy.visit(`/dashboard/media/${mediaId}`);
				cy.findByText(mediaLocators.displayPreviewText).should("be.visible");
			});
		});
	});
});
