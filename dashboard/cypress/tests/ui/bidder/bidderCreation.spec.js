import { bidderLocators } from "../../../locators/bidderLocators";
import getToken from "../../../utils/getToken";
import { globalContent } from "../../../locators/globalLocators";

const global = require("../../../locators/globalLocators.json");
const data = require("../../../fixtures/bidderCreationData.json");

const timeStamp = new Date().getTime();

describe("Bidder creation test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	afterEach(() => {
		cy.deleteTargetEntity(getToken(), `${data.name} ${timeStamp}`, "bidder");
	});

	it("Valid bidder creation", () => {
		// Visit bidders index page
		cy.visit("/dashboard/bidders");

		// Go to bidder form
		cy.clickElement(bidderLocators.addBidderButton);

		// Verify visible fields
		cy.verifyElementsExist(
			bidderLocators.settingsTab,
			bidderLocators.bidParametersTab,
			bidderLocators.qualityTab,
			global.saveButton,
			bidderLocators.bidderNameField,
			bidderLocators.statusActiveRadio,
			bidderLocators.statusInactiveRadio,
			bidderLocators.openRtbVersionDropdown,
			bidderLocators.testModeToggle,
			bidderLocators.multipleImpObjects,
			bidderLocators.companyAccessDropdown,
			bidderLocators.cookieSyncUrlField,
			bidderLocators.cookieSyncPercentageField,
			bidderLocators.matchedCookieBiddingToggle,
			bidderLocators.bidUrlRegionDropdown,
			bidderLocators.bidUrlField,
			bidderLocators.addRegionButton,
			bidderLocators.addSeatButton,
			bidderLocators.rtbMediaTypeDropdown,
			bidderLocators.compressBidRequestsToggle,
			bidderLocators.rtbFloorField,
			bidderLocators.timeoutDurationField,
			bidderLocators.classOverrideField,
			bidderLocators.demandFeePercentage
		);

		// Complete mandatory fields
		cy.getByRole(bidderLocators.bidderNameField).type(`${data.name} ${timeStamp}`);
		cy.clickElement(bidderLocators.bidUrlRegionDropdown);
		cy.clickElement(bidderLocators.uswestOption);
		cy.getByRole(bidderLocators.bidUrlField).type(data.bidUrl);
		cy.getByRole(bidderLocators.demandFeePercentage).type(20);
		cy.getByRole(bidderLocators.rtbFloorField).type(data.rtbFloor);

		// view report button should not be visible until form is saved
		cy.findByRole("link", { name: globalContent.VIEW_REPORT }).should("not.exist");

		// Go to parameters and validate fields
		cy.clickElement(bidderLocators.bidParametersTab);
		cy.verifyElementsExist(
			bidderLocators.omittedBidRequestParametersDropdown,
			bidderLocators.omittedSourceParametersDropdown,
			bidderLocators.omittedImpressionsParameters,
			bidderLocators.omittedImpressionsParametersExp,
			bidderLocators.omittedBannerParametersDropdown,
			bidderLocators.omittedVideoParametersDropdown,
			bidderLocators.contentDeliveryTypeMultiselect,
			bidderLocators.videoLinearityTypeLinearRadio,
			bidderLocators.videLinearityTypeNonLinearRadio,
			bidderLocators.omittedDealParametersDropdown,
			bidderLocators.omittedSiteParametersDropdown,
			bidderLocators.omittedPublisherParametersDropdown,
			bidderLocators.omittedDeviceParametersDropdown,
			bidderLocators.omittedGeoParametersDropdown,
			bidderLocators.omittedUserParametersDropdown
		);

		cy.clickElement(bidderLocators.omittedUserParametersDropdown);
		cy.findByRole("option", { name: "eids" }).should("exist");

		// Submit the form

		cy.findByRole("button", { name: globalContent.SAVE }).click();

		// Validate pop up is visible and it's text
		cy.validatePopupMessage(`${data.name} ${timeStamp} was successfully created`);

		// Go to settings and validate view report button should be visible
		cy.clickElement(bidderLocators.settingsTab);

		cy.findByRole("link", { name: globalContent.VIEW_REPORT }).should("exist");
	});

	it("Valid bidder creation with checked impression bid object", () => {
		// Visit bidders index page
		cy.visit("/dashboard/bidders");

		// Go to bidder form
		cy.clickElement(bidderLocators.addBidderButton);

		// Verify visible fields
		cy.verifyElementsExist(
			bidderLocators.settingsTab,
			bidderLocators.bidParametersTab,
			bidderLocators.qualityTab,
			global.saveButton,
			bidderLocators.bidderNameField,
			bidderLocators.statusActiveRadio,
			bidderLocators.statusInactiveRadio,
			bidderLocators.openRtbVersionDropdown,
			bidderLocators.testModeToggle,
			bidderLocators.multipleImpObjects,
			bidderLocators.companyAccessDropdown,
			bidderLocators.cookieSyncUrlField,
			bidderLocators.cookieSyncPercentageField,
			bidderLocators.matchedCookieBiddingToggle,
			bidderLocators.bidUrlRegionDropdown,
			bidderLocators.bidUrlField,
			bidderLocators.addRegionButton,
			bidderLocators.addSeatButton,
			bidderLocators.rtbMediaTypeDropdown,
			bidderLocators.compressBidRequestsToggle,
			bidderLocators.rtbFloorField,
			bidderLocators.timeoutDurationField,
			bidderLocators.classOverrideField
		);

		// Complete mandatory fields
		cy.getByRole(bidderLocators.bidderNameField).type(`${data.name} ${timeStamp}`);
		cy.clickElement(bidderLocators.bidUrlRegionDropdown);
		cy.clickElement(bidderLocators.uswestOption);
		cy.getByRole(bidderLocators.bidUrlField).type(data.bidUrl);
		cy.getByRole(bidderLocators.rtbFloorField).type(data.rtbFloor);
		//
		// click on the multiple impression object
		cy.getByRole(bidderLocators.multipleImpObjects).click();

		// Go to parameters and validate fields
		cy.clickElement(bidderLocators.bidParametersTab);
		cy.verifyElementsExist(
			bidderLocators.omittedBidRequestParametersDropdown,
			bidderLocators.omittedSourceParametersDropdown,
			bidderLocators.omittedImpressionsParameters,
			bidderLocators.omittedImpressionsParametersExp,
			bidderLocators.omittedBannerParametersDropdown,
			bidderLocators.omittedVideoParametersDropdown,
			bidderLocators.contentDeliveryTypeMultiselect,
			bidderLocators.videoLinearityTypeLinearRadio,
			bidderLocators.videLinearityTypeNonLinearRadio,
			bidderLocators.omittedDealParametersDropdown,
			bidderLocators.omittedSiteParametersDropdown,
			bidderLocators.omittedPublisherParametersDropdown,
			bidderLocators.omittedDeviceParametersDropdown,
			bidderLocators.omittedGeoParametersDropdown,
			bidderLocators.omittedUserParametersDropdown
		);

		// Submit the form
		//cy.clickElement(global.saveButton);
		cy.findByRole("button", { name: globalContent.SAVE }).click();

		// Validate pop up is visible and it's text
		cy.validatePopupMessage(`${data.name} ${timeStamp} was successfully created`);
	});

	it("should default Demand Fee Percentage to 0 if left empty", () => {
		// Visit bidders index page
		cy.visit("/dashboard/bidders");

		// Go to bidder form
		cy.clickElement(bidderLocators.addBidderButton);

		// Complete mandatory fields
		cy.getByRole(bidderLocators.bidderNameField).type(`${data.name} ${timeStamp}`);
		cy.clickElement(bidderLocators.bidUrlRegionDropdown);
		cy.clickElement(bidderLocators.uswestOption);
		cy.getByRole(bidderLocators.bidUrlField).type(data.bidUrl);
		cy.getByRole(bidderLocators.rtbFloorField).type(data.rtbFloor);

		// Submit the form

		cy.findByRole("button", { name: globalContent.SAVE }).click();

		//Validate that the default for demand fee percentage is 0
		cy.getByRole(bidderLocators.demandFeePercentage).should("have.value", "0");
	});
});
