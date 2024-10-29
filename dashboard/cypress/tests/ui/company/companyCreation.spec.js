import getToken from "../../../utils/getToken";
import { companyLocators as company, localeContent } from "../../../locators/companyLocators.js";
import { getTestResourceName } from "../../../utils/resourceNameUtil";
import { createOrUpdateCompany } from "../../../support/companyCommands";
import { globalContent } from "../../../locators/globalLocators";

const global = require("../../../locators/globalLocators.json");
const data = require("../../../fixtures/companyCreationData.json");

const timeStamp = new Date().getTime();

describe("Company creation test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	afterEach(() => {
		cy.deleteTargetEntity(getToken(), `${data.name} ${timeStamp}`, "company");
	});

	it("Valid company creation", () => {
		// Visit company index page
		cy.visit("/dashboard/companies");

		// Validate page title
		cy.get(global.pageTitle).should("have.text", "Companies");

		// Go to company creation form and assert that all elements are present
		cy.clickElement(company.addCompanyButton);
		cy.verifyElementsExist(
			company.settingsTab,
			company.defaultsTab,
			company.companyNameField,
			company.statusActiveRadio,
			company.statusInactiveRadio,
			company.companyDomainField,
			company.isConfidentialYesRadio,
			company.isConfidentialNoRadio,
			company.showHelpLinkToggle,
			company.privacyPolicyUrlField,
			company.termsAndConditionUrlField,
			company.rootDomainField,
			company.adServerField,
			company.mobileAdServerField,
			company.eventField,
			company.rtbField,
			company.cookiesField,
			company.publisherField,
			company.manageField,
			company.mediaField,
			company.cdnField,
			company.primaryColor,
			company.supportEmailField,
			company.reportingEmailField
		);

		cy.clickElement(company.defaultsTab);
		cy.verifyElementsExist(
			company.rtbLimitDimensionsField,
			company.rtbLimitDimensionsMaxRage,
			company.networkLimitDimensionsField,
			company.networkLimitDimensionsMaxRangeField,
			company.campaignLimitDimensionsField,
			company.campaignLimitDimensionsMaxRange,
			company.publisherLimitDimensionsField,
			company.publisherLimitDimensionsMaxRangeField,
			company.defaultPublisherRevenueShareField,
			company.defaultMarginField,
			company.defaultMinBitrateField,
			company.defaultMaxBitrateField,
			company.bidRequestMultiplier,
			company.opportunityCostMultiplier
		);

		// Verify that the bid request multiplier has the default value.
		cy.getByRole(company.bidRequestMultiplier).should("have.value", 0.000002);

		// Verify that the opportunity cost multiplier has the default value.
		cy.getByRole(company.opportunityCostMultiplier).should("have.value", 0.000002);

		cy.clickElement(company.campaignLimitDimensionsField);
		cy.findByRole("option", { name: localeContent.OPTION_DEAL }).should("not.exist");

		// Selecting Media Type CPM Priority
		cy.findByRole("radio", { name: localeContent.FIELDS.MEDIA_TYPE_PRIORIZATION.OPTIONS.CPM.LABEL }).click();

		// Selecting Media Type Priority that is the default.

		cy.findByRole("radio", { name: localeContent.FIELDS.MEDIA_TYPE_PRIORIZATION.OPTIONS.PRIORITY.LABEL }).click();

		// Go to settings tab and complete mandatory fields
		cy.clickElement(company.settingsTab);
		cy.getByRole(company.companyNameField).type(`${data.name} ${timeStamp}`);
		cy.getByRole(company.companyDomainField).type(`${data.domain}`);
		cy.clickElement(company.primaryColor);
		cy.clickElement(company.brownPrimaryColor);

		// Submit the form
		cy.clickElement(global.saveButton);

		// Validate pop up is visible and it's text
		cy.validatePopupMessage(`${data.name} ${timeStamp} was successfully created`);

		// Validate page loads with newly created company
		cy.location("pathname").then((path) => {
			//Extract new company id from the url from company edit page
			const newCompanyId = path.split("/")[3];
			cy.visit(`/dashboard/?companyId=${newCompanyId}`);
			cy.findByText("Reporting").should("exist");
		});
	});

	it("User can click on enable server side request button and it should be persist after save it", () => {
		// Search for base company, if not found create it
		const companyName = getTestResourceName("Enable Server Side Request");
		createOrUpdateCompany({ companyName }).then((response) => {
			const companyId = response.body.id;

			cy.visit(`/dashboard/companies/${companyId}`);

			cy.clickElement(company.defaultsTab);

			cy.getByRole(company.serverSideRequestsSwitch).should("not.be.checked");

			cy.clickElement(company.serverSideRequestsSwitch);

			cy.clickElement(global.saveButton);

			cy.validatePopupMessage(`${companyName} ${globalContent.SUCCESSFULLY_UPDATED_SUFFIX}`);

			cy.visit(`/dashboard/companies/${companyId}`);

			cy.clickElement(company.defaultsTab);

			cy.getByRole(company.serverSideRequestsSwitch).should("be.checked");
		});
	});
});
