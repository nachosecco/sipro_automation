import "cypress-file-upload";
import { globalContent } from "../../../locators/globalLocators";
import { localeContent as localeContent, mediaLocators } from "../../../locators/mediaLocators";
import { getDemandNames } from "../../../utils/resourceNameUtil";
import { createOrUpdateCampaign } from "../../../support/demandCommands";
import { DASHBOARD_API } from "../../../utils/serviceResources";
import pressEscapeOnBody from "../../../utils/pressEscapeOnBody";

const cleanup = (mediaNamePrefix) => {
	const pathDeleteResource = (resource) => {
		return DASHBOARD_API.MEDIA.getOne({ id: resource.id });
	};
	const indexPathResources = DASHBOARD_API.MEDIA.getIndex();

	const filterResourceToDelete = (resource) => resource.name.startsWith(mediaNamePrefix);
	cy.cleanResources({ indexPathResources, pathDeleteResource, filterResourceToDelete });
};

describe("Video Media cloning", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("do not permit delete asset media in clone state", () => {
		const resourceNames = getDemandNames("clone do not allow del original creative");
		cleanup(resourceNames.mediaName);
		const clonedMediaName = resourceNames.mediaName + "_cloned";
		cleanup(clonedMediaName);
		createOrUpdateCampaign(resourceNames).then((response) => {
			const campaign = response.body;
			// Visit media index page
			cy.visit("/dashboard/media");

			// Add new media
			cy.clickElement(mediaLocators.addMediaButton);
			cy.getByRole(mediaLocators.campaignNameDropdown).type(campaign.name);

			cy.findAllByRole("option", { name: campaign.name }).first().click();

			cy.getByRole(mediaLocators.mediaNameField).type(`${resourceNames.mediaName}`);
			cy.getByRole(mediaLocators.cpmField).type(1);

			// Select display media options
			cy.clickElement(mediaLocators.mediaTypeVideoRadio);
			cy.clickElement(mediaLocators.mediaSourceAssetRadio);

			cy.findByRole("button", { name: localeContent.FIELDS.UPLOAD_VIDEO.UPLOAD_MEDIA_FILE_FORM_LABEL }).click();

			//upload the first video file
			const fileName = "480x270_video.mp4";
			cy.get(mediaLocators.uploadVideoMediaFile).attachFile({ filePath: `uploadFile/${fileName}` });

			cy.findByRole("spinbutton", { name: localeContent.FIELDS.UPLOAD_VIDEO.WIDTH_LABEL }).type(480);

			cy.findByRole("spinbutton", { name: localeContent.FIELDS.UPLOAD_VIDEO.HEIGHT_LABEL }).type(270);

			cy.findByRole("spinbutton", { name: localeContent.FIELDS.UPLOAD_VIDEO.BITRATE_LABEL }).type(200);

			cy.findByRole("button", { name: localeContent.FIELDS.UPLOAD_VIDEO.UPLOAD_LABEL }).click();

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

				//upload the second video file, in the cloned media
				cy.findByRole("button", {
					name: localeContent.FIELDS.UPLOAD_VIDEO.UPLOAD_MEDIA_FILE_FORM_LABEL,
				}).click();

				cy.get(mediaLocators.uploadVideoMediaFile).attachFile({ filePath: `uploadFile/${fileName}` });

				cy.findByRole("spinbutton", { name: localeContent.FIELDS.UPLOAD_VIDEO.WIDTH_LABEL }).type(480);

				cy.findByRole("spinbutton", { name: localeContent.FIELDS.UPLOAD_VIDEO.HEIGHT_LABEL }).type(270);

				cy.findByRole("spinbutton", { name: localeContent.FIELDS.UPLOAD_VIDEO.BITRATE_LABEL }).type(200);

				cy.findByRole("button", { name: localeContent.FIELDS.UPLOAD_VIDEO.UPLOAD_LABEL }).click();

				cy.findAllByRole("rowgroup")
					.eq(1)
					.within(() => {
						cy.findAllByRole("button").first().click();
					});

				cy.findByText(localeContent.FIELDS.DElETE_LABEL).should("not.exist");

				pressEscapeOnBody();

				// Submit form
				cy.findByRole("button", { name: globalContent.SAVE }).click();

				// Validate pop up is visible and it's text
				cy.validatePopupMessage(`${clonedMediaName} was successfully created`);

				cy.reload();

				cy.findAllByRole("rowgroup")
					.eq(1)
					.within(() => {
						cy.findAllByRole("button").first().click();
					});

				cy.findAllByText(localeContent.FIELDS.DElETE_LABEL).should("exist");
			});
		});
	});
});
