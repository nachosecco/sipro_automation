import getToken from "../../../utils/getToken";
import userSettings from "../../../locators/userSettingsLocators";
import sidebarLocators from "../../../locators/sideBarLocators";
import { getDemandNames } from "../../../utils/resourceNameUtil";
import { createOrUpdateAdvertiser } from "../../../support/demandCommands";
import { globalGridLocators } from "../../../locators/globalGridLocators";
import pressEscapeOnBody from "../../../utils/pressEscapeOnBody";
import rl from "../../../locators/reportingLocators";

const global = require("../../../locators/globalLocators.json");
const userSettingsData = require("../../../fixtures/userSettingsUpdateData.js");

const timeStamp = new Date().getTime();
const username = `${timeStamp}automation-user@test.com`;

const demandNames = getDemandNames("advertiser for new user");

function selectDropdownValue(dropDownlocator, option) {
	cy.getByRole(dropDownlocator).type(option.name); // Select App Name Dimension for Network
	cy.findByRole("option", option).click();
	pressEscapeOnBody();
}

describe("User settings update test cases", () => {
	beforeEach(() => {
		cy.loginGlobalUserProgrammatically();
		cy.createUserWithPermissions({
			userRoleName: userSettingsData.userRoleName,
			username,
			permissionsToEnable: userSettingsData.createUserPermissions,
		});
	});

	afterEach(() => {
		// Login with the Main test user to perform the new user delete operation.
		cy.loginProgrammatically().then(() => {
			// Adding it inside the callback because its an async call.
			// Delete User
			cy.deleteTargetEntity(getToken(), username, "user", "email");

			// Delete Company
			cy.deleteTargetEntity(getToken(), userSettingsData.companyName, "company");
			cy.deleteTargetEntity(getToken(), demandNames.advertiserName, "advertiser");
		});
	});

	it("Login with newly created test user and align company with default user dimensions, metrics and column density", () => {
		// Login With New user
		cy.loginProgrammatically({
			username,
		});

		// Create company
		cy.checkBaseCompanyRequest(getToken(), userSettingsData.companyName);
		// create advertiser for testing whether changing default changes the data

		createOrUpdateAdvertiser(demandNames);

		// Visit User Settings index page
		cy.visit("/dashboard/user-settings");

		// Edit User Settings form and submit
		cy.getByRole(userSettings.userFirstNameField).clear().type(userSettingsData.updatedUserFirstName);
		cy.getByRole(userSettings.userLastNameField).clear().type(userSettingsData.updatedUserLastName);
		cy.getByRole(userSettings.userPhoneNumberField).clear().type(userSettingsData.updatedUserPhone);
		cy.getByRole(userSettings.userEmailAddressField); // Not updating the email because its associated with the user's credentials
		cy.getByRole(userSettings.userTimezoneField); // Keeping the default time zone
		cy.getByRole(userSettings.userHideInactiveItemsField); // Keeping the default status
		cy.clickElement(userSettings.userDefaultCompanyViewField);
		// Search and Select newly created test company
		cy.getByRole(userSettings.userDefaultCompanyViewField).clear().type(userSettingsData.companyName);
		cy.clickElement(userSettings.userCompanySelect);
		// Change column density from standard to compact
		cy.clickElement(userSettings.defaultDensityStandardField);
		cy.clickElement(userSettings.defaultDensitySelect);
		// Select App Name Dimension for Network
		selectDropdownValue(userSettings.userNetworkDimensionSelect, userSettings.userDimensionAppNameSelect);
		// Select App Name Dimension for Campaign
		selectDropdownValue(userSettings.userCampaignDimensionSelect, userSettings.userDimensionAppNameSelect);
		// Select Deal Id Dimension for RTB
		selectDropdownValue(userSettings.userRTBDimensionSelect, userSettings.userDimensionDealIdSelect);

		// Un Select Network KPIs - Impression
		selectDropdownValue(userSettings.userNetworkKPIsSelect, userSettings.userMetricsImpressionsOption);

		// Select Network KPIs - Quartile 100%
		selectDropdownValue(userSettings.userNetworkKPIsSelect, userSettings.userMetricsQuartile100Option);

		// Un Select Campaign KPIs - Impression
		selectDropdownValue(userSettings.userCampaignMetricsSelect, userSettings.userMetricsImpressionsOption);

		// Un Select RTB KPIs - Impression
		selectDropdownValue(userSettings.userRTBKPIsSelect, userSettings.userMetricsImpressionsOption);

		// Select RTB KPIs - Quartile 100%
		selectDropdownValue(userSettings.userRTBKPIsSelect, userSettings.userMetricsQuartile100Option);

		// Click on the save button.
		cy.clickElement(global.saveButton);

		// Logout the current user
		cy.clickElement(sidebarLocators.logoutButton);

		// Login back with new user to verify the details
		cy.visit("/login");
		cy.login(username, Cypress.env("uiPassword"));

		// Visit User Settings index page
		cy.clickElement(sidebarLocators.userSettingsButton);

		// verify the fields
		cy.verifyElementsExist(
			userSettings.userFirstNameField,
			userSettings.userLastNameField,
			userSettings.userPhoneNumberField,
			userSettings.userEmailAddressField,
			userSettings.userTimezoneField,
			userSettings.userHideInactiveItemsField,
			userSettings.userDefaultCompanyViewField
		);

		// Verify the updated values
		cy.getByRole(userSettings.userFirstNameField).should("have.value", userSettingsData.updatedUserFirstName);
		cy.getByRole(userSettings.userLastNameField).should("have.value", userSettingsData.updatedUserLastName);
		cy.getByRole(userSettings.userPhoneNumberField).should("have.value", userSettingsData.updatedUserPhone);
		cy.getByRole(userSettings.userEmailAddressField).should("have.value", username);
		cy.getByRole(userSettings.userTimezoneField).should("have.value", userSettingsData.userTimezoneText);
		cy.getByRole(userSettings.userHideInactiveItemsField).should("not.be.checked");
		cy.getByRole(userSettings.userDefaultCompanyViewField).should("have.value", userSettingsData.companyName);
		cy.getByRole(userSettings.defaultDensityCompactField).should("exist");

		// Navigate to the side bar
		cy.clickElement(sidebarLocators.navigationMenuButtonCompanyMenu);
		// Verify if the default company is already selected
		cy.getByRole(sidebarLocators.activeCompanyDropdown).should("have.value", userSettingsData.companyName);
		// Close the side bar
		cy.clickElement(sidebarLocators.collapseLinkClick);

		cy.clickElement(sidebarLocators.navigationMenuButtonDemand);
		cy.clickElement(sidebarLocators.advertisersButton);
		// Look for base advertiser
		cy.search(demandNames.advertiserName);
		// record created for primary company in advertiser is not found
		cy.getByRole(globalGridLocators.clearSearchButton).should("exist");
		cy.getByRole(global.indexActionButton).should("not.exist");
		cy.get(globalGridLocators.indexGrid).get('[data-field="name"]').eq(1).should("not.exist");

		// Logout from the New user
		cy.clickElement(sidebarLocators.logoutButton);

		// Login back with new user to verify the details
		cy.visit("/login");
		cy.login(username, Cypress.env("uiPassword"));

		// Validate the selected Dimension should be available on the Dashboard
		const expectedLabels = [userSettings.userDimensionAppNameSelect.name];
		cy.findAllByTestId("dimensions-toolbar-chip")
			.should("have.length", expectedLabels.length)
			.each((chip, index) => {
				cy.wrap(chip).should("have.text", expectedLabels[index]);
			});
		// Validate the selected METRICS should be checked on the Dashboard
		cy.clickElement(userSettings.dashboardSelectMetricsLabel);
		[userSettings.userMetricsImpressionsOption.name].forEach((metricLabel) => {
			cy.findByRole("checkbox", { name: metricLabel }).should("be.checked");
		});
		pressEscapeOnBody();
		// Validate preferred column density "compact" is selected
		cy.clickElement(globalGridLocators.densityMenu);
		cy.getByRole({ locator: "Compact", role: "menuitem" }).should("have.class", "Mui-selected");

		// Validate selected KPIs exist
		cy.findAllByText(userSettings.userMetricsQuartile100Option.name).should("be.visible");
		// removed kpi shouldn't exist
		cy.findAllByTestId("data-testid=impressions").should("not.exist");

		// Switch to campaign tab
		cy.clickElement(rl.campaignTab);
		// removed kpi shouldn't exist
		cy.findAllByTestId("data-testid=impressions").should("not.exist");
		// Validate selected KPIs exist
		cy.findAllByText(userSettings.userMetricsQuartile100Option.name).should("be.visible");

		// Switch to rtb tab
		cy.clickElement(rl.rtbTab);
		// removed kpi shouldn't exist
		cy.findAllByTestId("data-testid=impressions").should("not.exist");
		// Validate selected KPIs exist
		cy.findAllByText(userSettings.userMetricsQuartile100Option.name).should("be.visible");
		// Validate user's default dimension exist
		cy.findAllByText(userSettings.userDimensionDealIdSelect.name).should("be.visible");
	});
});
