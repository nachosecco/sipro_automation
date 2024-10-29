import getToken from "../../../utils/getToken";

import placementLocators, { localeContent } from "../../../locators/placementLocators";
import { getSupplyNames } from "../../../utils/resourceNameUtil";
import { globalContent } from "../../../locators/globalLocators";
import { createOrUpdateSite } from "../../../support/supplyCommands";
import { companyLocators as company } from "../../../locators/companyLocators";
import getPrimaryCompanyId from "../../../utils/getPrimaryCompany";

describe("Placement creation test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Placement creation", () => {
		// Verify if base site exists if not create it
		const supplyNames = getSupplyNames("Placement creation");
		// Delete the placement created by the most recent test run
		cy.deleteTargetEntity(getToken(), supplyNames.placementName, "placement");
		// Create the parent site and pub
		createOrUpdateSite(supplyNames);

		// Visit placements index page
		cy.visit("/dashboard/placements");

		// Verify that page title is placements
		cy.findByRole("heading", { name: localeContent.INDEX_HEADING });

		// Add new placement
		cy.clickElement(placementLocators.addPlacementButton);
		cy.getByRole(placementLocators.siteNameDropdown).type(supplyNames.siteName);
		cy.findByRole("option", { name: supplyNames.siteName }).click();

		// Verify elements exist for mobile
		cy.verifyElementsExist(
			placementLocators.settingsTab,
			placementLocators.qualityTab,
			placementLocators.placementNameField,
			placementLocators.statusRadioActive,
			placementLocators.statusRadioInactive,
			placementLocators.revenueShareRadio,
			placementLocators.flatRateRadio,
			placementLocators.floorField,
			placementLocators.auctionFloorIncrementField,
			placementLocators.auctionTypeFirstPriceRadio,
			placementLocators.auctionTypeSecondPriceRadio,
			placementLocators.auctionMultipleWinnersField,
			placementLocators.typeMobileDropDown,
			placementLocators.vastVersionDropDown
		);

		// Verify default values are set
		cy.getByRole(placementLocators.auctionTypeFirstPriceRadio).should("be.checked");
		cy.getByRole(placementLocators.auctionMultipleWinnersField)
			.findByLabelText(localeContent.FIELD_NAMES.MULTIPLE_WINNERS.OPTIONS.YES)
			.should("be.checked");

		// Verify that extra elements are visible for instream
		cy.clickElement(placementLocators.typeMobileDropDown);
		cy.clickElement(placementLocators.instreamOption);
		cy.verifyRadioByGroupExist(placementLocators.supportVpaidRadioGroup, placementLocators.supportVpaidYesRadio);
		cy.verifyRadioByGroupExist(placementLocators.supportVpaidRadioGroup, placementLocators.supportVpaidNoRadio);
		cy.verifyRadioByGroupExist(
			placementLocators.enableC6ManagerRadioGroup,
			placementLocators.enableC6AdManagerYesRadio
		);
		cy.verifyRadioByGroupExist(
			placementLocators.enableC6ManagerRadioGroup,
			placementLocators.enableC6AdManagerNoRadio
		);

		// Verify that extra fields are visible for outstream
		cy.clickElement(placementLocators.typeInstreamDropDown);
		cy.clickElement(placementLocators.outstreamOption);
		cy.verifyElementsExist(
			placementLocators.defaultFormatDropDown,
			placementLocators.mobileFormatDropDown,
			placementLocators.audioToggle,
			placementLocators.setFrequencyCapToggle,
			placementLocators.browserBlacklistMultiSelect,
			placementLocators.pageElemetsBlacklistField,
			placementLocators.framebusterField,
			placementLocators.viewUrlField,
			placementLocators.clickUrlField,
			placementLocators.passbackField
		);

		// Verify that extra elements are visible for display
		cy.clickElement(placementLocators.typeOutstreamDropDown);
		cy.clickElement(placementLocators.displayOption);
		cy.verifyElementsExist(placementLocators.sizeDropDown);

		// Complete instream mandatory fields
		cy.clickElement(placementLocators.typeDisplayDropDown);
		cy.clickElement(placementLocators.instreamOption);
		cy.findByRole("textbox", { name: localeContent.FIELD_NAMES.placementName }).type(supplyNames.placementName);
		cy.getByRole(placementLocators.floorField).type(5);

		// validate that the view report button is not visible until the form is saved
		cy.findByRole("link", { name: globalContent.VIEW_REPORT }).should("not.exist");

		// Go to quality tab and assert fields are visible
		cy.clickElement(placementLocators.qualityTab);
		cy.verifyElementsExist(
			placementLocators.trackersMultiSelect,
			placementLocators.maxDurationField,
			placementLocators.placementSkipField,
			placementLocators.limitAdResponseSizeToggle
		);

		// Submit form
		cy.findByRole("button", { name: globalContent.SAVE }).click();

		// Validate pop up is visible and it's text
		cy.validatePopupMessage(`${supplyNames.placementName} ${globalContent.SUCCESSFULLY_CREATED_SUFFIX}`);

		// Validate that the placement tag was generated
		cy.clickElement(placementLocators.settingsTab);
		cy.getByRole(placementLocators.placementTagField).should("not.be.empty");

		// View report button should be visible
		cy.findByRole("link", { name: globalContent.VIEW_REPORT }).should("exist");
	});

	it("Placement creation validate multiple impression object field", () => {
		// Verify if base site exists if not create it
		const supplyNames = getSupplyNames("Placement creation validate multiple impression object field");
		// Delete the placement created by the most recent test run
		cy.deleteTargetEntity(getToken(), supplyNames.placementName, "placement");
		// Create the parent site and pub
		createOrUpdateSite(supplyNames);

		// Visit placements index page
		cy.visit("/dashboard/placements");

		// Add new placement
		cy.clickElement(placementLocators.addPlacementButton);
		cy.getByRole(placementLocators.siteNameDropdown).type(supplyNames.siteName);
		cy.findByRole("option", { name: supplyNames.siteName }).click();

		// Verify elements exist for mobile
		cy.verifyElementsExist(placementLocators.multipleImpObjectsField);

		cy.findByRole("textbox", { name: localeContent.FIELD_NAMES.placementName }).type(supplyNames.placementName);
		//checks custom dates validations
		cy.findByRole("checkbox", { name: localeContent.FIELD_NAMES.MULTIPLE_IMP_OBJECTS }).check();
		cy.findByRole("checkbox", { name: localeContent.FIELD_NAMES.MULTIPLE_IMP_OBJECTS }).should("be.checked");

		cy.getByRole(placementLocators.floorField).clear();
		cy.getByRole(placementLocators.floorField).type(5);

		// Submit form
		cy.findByRole("button", { name: globalContent.SAVE }).click();

		// Validate pop up is visible and it's text
		cy.validatePopupMessage(`${supplyNames.placementName} ${globalContent.SUCCESSFULLY_CREATED_SUFFIX}`);

		// Validate that the placement tag was generated
		// Visit placements index page
		cy.visit("/dashboard/placements");
		// Search for base placement
		cy.search(supplyNames.placementName);

		// Load the page and Click action button and edit
		cy.clickDataGridEditMenuItem();
		cy.getByRole(placementLocators.placementTagField).should("not.be.empty");
		cy.getByRole(placementLocators.multipleImpObjectsField).should("be.checked");
	});

	it("Validate that CPM per Sec is visible for placement creation if server side requests flag is enabled in company", () => {
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

		// Verify if base site exists if not create it
		const supplyNames = getSupplyNames("Placement creation validate CPM per Sec should be visible");

		// Create the parent site and pub
		createOrUpdateSite(supplyNames);

		// Visit placements index page
		cy.visit(`/dashboard/placements?companyId=${companyId}`);

		// Add new placement
		cy.clickElement(placementLocators.addPlacementButton);

		cy.getByRole(placementLocators.siteNameDropdown).type(supplyNames.siteName);

		cy.findByRole("option", { name: supplyNames.siteName }).click();

		cy.findByRole("checkbox", { name: localeContent.FIELD_NAMES.SERVER_SIDE_REQUEST }).click();

		cy.findByRole("radio", { name: localeContent.FIELD_NAMES.AUCTION_TYPE_FIRST_PRICE }).click();

		cy.findByLabelText(localeContent.FIELD_NAMES.CPM_PER_SECOND).should("exist");
	});

	it("Validate that CPM per Sec is not visible for placement creation if server side requests flag is disabled in company", () => {
		const companyId = getPrimaryCompanyId();

		cy.visit(`/dashboard/companies/${companyId}`);

		cy.clickElement(company.defaultsTab);

		cy.getByRole(company.serverSideRequestsSwitch)
			.invoke("is", ":checked")
			.then((checked) => {
				if (checked) {
					cy.clickElement(company.serverSideRequestsSwitch);
				}
			});

		cy.findByRole("button", { name: globalContent.SAVE }).click();

		// Verify if base site exists if not create it
		const supplyNames = getSupplyNames("Placement creation validate CPM per Sec should not be visible");

		// Create the parent site and pub
		createOrUpdateSite(supplyNames);

		// Visit placements index page
		cy.visit(`/dashboard/placements?companyId=${companyId}`);

		// Add new placement
		cy.clickElement(placementLocators.addPlacementButton);

		cy.getByRole(placementLocators.siteNameDropdown).type(supplyNames.siteName);

		cy.findByRole("option", { name: supplyNames.siteName }).click();

		cy.findByRole("radio", { name: localeContent.FIELD_NAMES.AUCTION_TYPE_FIRST_PRICE }).click();

		cy.findByLabelText(localeContent.FIELD_NAMES.CPM_PER_SECOND).should("not.exist");
	});
});
