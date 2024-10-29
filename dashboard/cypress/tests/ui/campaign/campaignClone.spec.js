import "cypress-file-upload";

import { getDemandNames, getSupplyNames } from "../../../utils/resourceNameUtil";
import { campaignLocators } from "../../../locators/campaignLocators";
import { globalContent } from "../../../locators/globalLocators";
import {
	createOrUpdateCampaign,
	createOrUpdateMedia,
	createOrUpdateMediaAlignments,
} from "../../../support/demandCommands";
import { createOrUpdatePlacement } from "../../../support/supplyCommands";
import { localeContent as lc, mediaLocators as media, mediaLocators } from "../../../locators/mediaLocators";
import { DASHBOARD_API } from "../../../utils/serviceResources";

const cleanup = (campaignNamePrefix) => {
	const pathDeleteResource = (resource) => {
		return DASHBOARD_API.CAMPAIGN.getOne({ id: resource.id });
	};
	const indexPathResources = DASHBOARD_API.CAMPAIGN.getIndex();

	const filterResourceToDelete = (resource) => resource.name.startsWith(campaignNamePrefix);
	cy.cleanResources({ indexPathResources, pathDeleteResource, filterResourceToDelete });
};

describe("Campaign clone test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("clone with ad tag media and alignments", () => {
		const resourceNames = getDemandNames("Campaign clone");
		const placementResourceNames = getSupplyNames("clone with alignments");
		cleanup(resourceNames.campaignName);
		const clonedCampaignName = resourceNames.campaignName + "_cloned";
		cleanup(clonedCampaignName);

		createOrUpdateMedia(resourceNames).then((response) => {
			const media = response.body;
			const campaignId = media.campaignId;

			// create or update placement
			createOrUpdatePlacement(placementResourceNames).then((placementResponse) => {
				const placement = placementResponse.body;
				// Align placement with the media
				createOrUpdateMediaAlignments({ placements: [placement], mediaId: media.id }).then(() => {
					// Clone a campaign
					cy.visit(`/dashboard/campaigns/${campaignId}?clone=true`);
					cy.getByRole(campaignLocators.campaignNameField).type(clonedCampaignName);
					cy.findByRole("button", { name: globalContent.SAVE }).click();
					cy.validatePopupMessage(`${clonedCampaignName} ${globalContent.SUCCESSFULLY_CREATED_SUFFIX}`);
					// Validate media got cloned
					cy.clickElement(campaignLocators.mediaTab);
					cy.findByText(clonedCampaignName + " - " + resourceNames.mediaName + " - Clone").click();
					cy.clickElement(mediaLocators.alignmentsTab);

					// validate cloned media has the placement aligned
					cy.findByTestId("alignment-table-aligned").within(() => {
						cy.findByText(placementResourceNames.placementName).should("exist");
					});
				});
			});
		});
	});

	it("clone with display media asset", () => {
		const resourceNames = getDemandNames("Campaign clone display");
		cleanup(resourceNames.campaignName);
		const clonedCampaignName = resourceNames.campaignName + "_cloned";
		cleanup(clonedCampaignName);

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

			cy.visit(`/dashboard/campaigns/${campaign.id}?clone=true`);
			cy.getByRole(campaignLocators.campaignNameField).type(clonedCampaignName);
			cy.findByRole("button", { name: globalContent.SAVE }).click();

			cy.validatePopupMessage(`${clonedCampaignName} ${globalContent.SUCCESSFULLY_CREATED_SUFFIX}`);
			// Validate media got cloned
			cy.clickElement(campaignLocators.mediaTab);
			cy.findByText(clonedCampaignName + " - " + resourceNames.mediaName + " - Clone").click();
			cy.findByText(mediaLocators.displayPreviewText).should("be.visible");
		});
	});

	it("Clone with video media asset", () => {
		const resourceNames = getDemandNames("Campaign clone video");
		cleanup(resourceNames.campaignName);
		const clonedCampaignName = resourceNames.campaignName + "_cloned";
		cleanup(clonedCampaignName);

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

			// Select video media options
			cy.clickElement(mediaLocators.mediaTypeVideoRadio);
			cy.clickElement(mediaLocators.mediaSourceAssetRadio);
			cy.clickElement(mediaLocators.uploadFileType);
			cy.clickElement(mediaLocators.uploadVideoMediaFileButton);
			//upload the video file
			const fileName = "480x270_video";
			cy.get(mediaLocators.uploadVideoMediaFile).attachFile({ filePath: `uploadFile/${fileName}.mp4` });

			cy.getByRole(mediaLocators.bitRateTextBox).type(`256`);
			cy.getByRole(mediaLocators.widthTextBox).type(`480`);
			cy.getByRole(mediaLocators.heightTextBox).type(`270`);
			cy.getByRole(mediaLocators.uploadButton).click();
			cy.validatePopupMessage(`${lc.UPLOAD_MESSAGE} ${fileName}`);

			// Submit form
			cy.findByRole("button", { name: globalContent.SAVE }).click();

			// Validate pop up is visible and it's text
			cy.validatePopupMessage(`${resourceNames.mediaName} was successfully created`);

			cy.visit(`/dashboard/campaigns/${campaign.id}?clone=true`);
			cy.getByRole(campaignLocators.campaignNameField).type(clonedCampaignName);
			cy.findByRole("button", { name: globalContent.SAVE }).click();
			cy.validatePopupMessage(`${clonedCampaignName} ${globalContent.SUCCESSFULLY_CREATED_SUFFIX}`, {
				timeout: 10000,
			});
			// Validate media got cloned
			cy.clickElement(campaignLocators.mediaTab);
			cy.findByText(clonedCampaignName + " - " + resourceNames.mediaName + " - Clone").click();
			cy.findAllByRole("cell", { name: /480x270_video/i }).should("be.visible");
		});
	});
});
