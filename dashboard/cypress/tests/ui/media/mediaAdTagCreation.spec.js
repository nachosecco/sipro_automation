import { globalContent } from "../../../locators/globalLocators";
import macroLocators from "../../../locators/macroLocators";
import { localeContent as lc, mediaLocators as media } from "../../../locators/mediaLocators";
import appendRequired from "../../../utils/appendRequired";
import { DASHBOARD_API } from "../../../utils/serviceResources";
import { DEFAULT_MEDIA_BODY } from "../../../fixtures/defaultDemandSideCreationData";
import { getDemandNames } from "../../../utils/resourceNameUtil";
import { createOrUpdateCampaign } from "../../../support/demandCommands";

const cleanup = (mediaNamePrefix) => {
	const pathDeleteResource = (resource) => {
		return DASHBOARD_API.MEDIA.getOne({ id: resource.id });
	};
	const indexPathResources = DASHBOARD_API.MEDIA.getIndex();

	const filterResourceToDelete = (resource) => resource.name.startsWith(mediaNamePrefix);
	cy.cleanResources({ indexPathResources, pathDeleteResource, filterResourceToDelete });
};

describe("Media creation test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Valid video media creation", () => {
		const resourceNames = getDemandNames("Valid video media creation");
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

			// Verify elements are visible for video
			cy.verifyElementsExist(
				media.settingsTab,
				media.qualityTab,
				media.mediaNameField,
				media.statusActiveRadio,
				media.statusInactiveRadio,
				media.cpmField,
				media.mediaTypeVideoRadio,
				media.mediaTypeDisplayRadio,
				media.mediaSourceAdTagRadio,
				media.mediaSourceAssetRadio,
				media.adTagField,
				media.vpaidSupportedTagYesRadio,
				media.vpaidSupportedTagNoRadio,
				media.positionDropdown,
				media.durationDropdown,
				media.mediaPriorityDropdown,
				media.mediaWeightDropdown,
				media.advertiserDomainField,
				media.customPassThroughParam
			);

			// Verify macro Search is visible
			cy.get(media.addMacroSearchInput).should("exist");

			// Verify that extra fields are visible or not for display
			cy.clickElement(media.mediaTypeDisplayRadio);
			cy.getByRole(media.sizeDropdown).should("exist");
			cy.verifyElementsNotExist(
				media.vpaidSupportedTagYesRadio,
				media.vpaidSupportedTagNoRadio,
				media.positionDropdown,
				media.durationDropdown
			);

			// Complete video mandatory fields
			cy.clickElement(media.mediaTypeVideoRadio);
			cy.getByRole(media.mediaNameField).type(`${resourceNames.mediaName}`);
			cy.getByRole(media.adTagField).type(DEFAULT_MEDIA_BODY.adTag);
			cy.getByRole(media.advertiserDomainField).type(DEFAULT_MEDIA_BODY.advertisersDomain);
			cy.getByRole(media.customPassThroughParam).click();
			cy.findByRole("textbox", { name: lc.FIELDS.CUSTOM_PARAMETER_PASSTHROUGH.KEY_INPUT_LABEL }).type("param1");
			cy.getByRole(media.customPassThroughParamAddKey).click();
			cy.findAllByRole("textbox", { name: lc.FIELDS.CUSTOM_PARAMETER_PASSTHROUGH.KEY_INPUT_LABEL })
				.eq(1)
				.type("param2");

			// View report button should not be visible until media is saved
			cy.findByRole("link", { name: globalContent.VIEW_REPORT }).should("not.exist");

			// Go to quality tab and assert fields are visible
			cy.clickElement(media.qualityTab);
			cy.verifyElementsExist(
				media.trackersMultiselect,
				media.deviceTargetingToggle,
				media.sizeTargetingToggle,
				media.domainTargetingToggle,
				media.appNameTargetingToggle,
				media.appBundleIDTargetingToggle
			);

			// Submit form
			cy.findByRole("button", { name: globalContent.SAVE }).click();

			// Validate pop up is visible and it's text
			cy.validatePopupMessage(`${resourceNames.mediaName} was successfully created`);

			// Validate values are saved
			cy.clickElement(media.settingsTab);
			cy.getByRole(media.advertiserDomainField).should("have.value", DEFAULT_MEDIA_BODY.advertisersDomain);

			// View report button should  be visible
			cy.findByRole("link", { name: globalContent.VIEW_REPORT }).should("exist");
			// Iterate through key inputs and expect values in order
			const expectedParams = ["param1", "param2"];
			cy.findAllByRole("textbox", {
				name: lc.FIELDS.CUSTOM_PARAMETER_PASSTHROUGH.KEY_INPUT_LABEL,
			}).each((el, index) => cy.wrap(el).should("have.value", expectedParams[index]));
		});
	});

	it("ad tag field should include all supported macros", () => {
		const resourceNames = getDemandNames("all supported macros");
		cleanup(resourceNames.mediaName);

		createOrUpdateCampaign(resourceNames).then((response) => {
			const campaign = response.body;

			// Visit create media page
			cy.visit("/dashboard/media/INIT");

			// Select a parent campaign
			cy.getByRole(media.campaignNameDropdown).type(campaign.name);

			cy.findAllByRole("option", { name: campaign.name }).first().click();

			// Add required field information
			cy.getByRole(media.mediaNameField).type(resourceNames.mediaName);

			// Type a valid uri to start the tag
			cy.findByLabelText(appendRequired(lc.FIELDS.AD_TAG.LABEL)).type("www.adtag.com?");

			// Select every macro in every category

			Object.entries(macroLocators.MACRO_OPTIONS).forEach(([, categoryConfig]) => {
				cy.get("*[name='macro-auto-complete-search']").find("input").clear();
				cy.get("*[name='macro-auto-complete-search']").find("input").type(categoryConfig.label);
				cy.get(".MuiAutocomplete-option").find(`*[macro='${categoryConfig.macro}']`).click();
			});

			// Join all the macros from each category together into a single string
			const allMacrosString = Object.entries(macroLocators.MACRO_OPTIONS)
				.reduce((agg, [, categoryConfig]) => {
					return [...agg, ...categoryConfig.macro];
				}, [])
				.join("");

			// Ad tag should have all expected macro strings in it
			cy.findByLabelText(appendRequired(lc.FIELDS.AD_TAG.LABEL)).should(
				"have.value",
				`www.adtag.com?${allMacrosString}`
			);

			// Submit form
			cy.findByRole("button", { name: globalContent.SAVE }).click();

			// All macros should be valid so expect success message
			cy.validatePopupMessage(`${resourceNames.mediaName} was successfully created`);
		});
	});

	it("submission of unsupported macros in the ad tag should show field validation message", () => {
		const resourceNames = getDemandNames("unsupported macros");
		cleanup(resourceNames.mediaName);

		createOrUpdateCampaign(resourceNames).then((response) => {
			const campaign = response.body;

			// Visit create media page
			cy.visit("/dashboard/media/INIT");

			// Select a parent campaign
			cy.getByRole(media.campaignNameDropdown).type(campaign.name);
			cy.findAllByRole("option", { name: campaign.name }).first().click();

			// Add required field information
			cy.getByRole(media.mediaNameField).type(resourceNames.mediaName);

			// Type multiple invalid macros
			cy.getByRole(media.adTagField).type(
				"www.adtag.com?myCustomMacro=[my_custom_macro]&anotherCustom=[another_custom_macro]"
			);

			// Submit form
			cy.findByRole("button", { name: globalContent.SAVE }).click();

			// Validation message should appear
			cy.findByText("Invalid Macros: [my_custom_macro], [another_custom_macro]");
		});
	});
});
