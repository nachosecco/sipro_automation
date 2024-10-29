import { advertiserLocators, localeContent } from "../../../locators/advertiserLocators";

import { globalContent } from "../../../locators/globalLocators";
import { getDemandNames } from "../../../utils/resourceNameUtil";
import { DASHBOARD_API } from "../../../utils/serviceResources";

const cleanup = (advertiserName) => {
	const pathDeleteResource = (resource) => {
		return DASHBOARD_API.ADVERTISER.getOne({ id: resource.id });
	};
	const indexPathResources = DASHBOARD_API.ADVERTISER.getIndex();
	const filterResourceToDelete = (resource) => resource.name == advertiserName;
	cy.cleanResources({ indexPathResources, pathDeleteResource, filterResourceToDelete });
};

describe("Advertiser creation test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Advertiser creation", () => {
		const demandNames = getDemandNames("Advertiser creation");
		cleanup(demandNames.advertiserName);

		// Visit advertiser index page
		cy.visit("/dashboard/advertisers");

		// Verify that page title is advertisers
		cy.findByRole("heading", { name: localeContent.INDEX_HEADING });

		// Assert presence of add advertiser button and click it
		cy.clickElement(advertiserLocators.addAdvertiserButton);

		// Validate these elements are visible
		cy.verifyElementsExist(
			advertiserLocators.advertiserNameField,
			advertiserLocators.statusActiveRadio,
			advertiserLocators.statusInactiveRadio,
			advertiserLocators.cpmRadio,
			advertiserLocators.predictedCpmRadio,
			advertiserLocators.cpmAndPcpmRadio,
			advertiserLocators.contactNameField,
			advertiserLocators.contactEmailField,
			advertiserLocators.phoneNumberField,
			advertiserLocators.companyAddressField,
			advertiserLocators.billingDifferentFromContactInfoCheckbox,
			advertiserLocators.tabSettings,
			advertiserLocators.demandFeePercentage
		);

		// Validate that default is active and cpm
		cy.getByRole(advertiserLocators.statusActiveRadio).should("be.checked");
		cy.getByRole(advertiserLocators.cpmRadio).should("be.checked");

		// Fill the form and submit
		cy.getByRole(advertiserLocators.advertiserNameField).type(demandNames.advertiserName);
		cy.getByRole(advertiserLocators.contactNameField).type("Automated contact");
		cy.getByRole(advertiserLocators.contactEmailField).type("automated@test.com");
		cy.getByRole(advertiserLocators.phoneNumberField).type("12024956");
		cy.getByRole(advertiserLocators.demandFeePercentage).type("12");
		cy.getByRole(advertiserLocators.companyAddressField).type("Automated Street 123");

		cy.findByRole("button", { name: globalContent.SAVE }).click();

		// Validate pop message
		cy.validatePopupMessage(`${demandNames.advertiserName} ${globalContent.SUCCESSFULLY_CREATED_SUFFIX}`);
	});

	it("should default Demand Fee Percentage to 0 if left empty", () => {
		const demandNames = getDemandNames("Advertiser creation");
		cleanup(demandNames.advertiserName);
		// Visit advertiser index page
		cy.visit("/dashboard/advertisers");

		// Verify that page title is advertisers
		cy.findByRole("heading", { name: localeContent.INDEX_HEADING });

		// Assert presence of add advertiser button and click it
		cy.clickElement(advertiserLocators.addAdvertiserButton);

		// Fill the form and submit
		cy.getByRole(advertiserLocators.advertiserNameField).type(demandNames.advertiserName);
		cy.getByRole(advertiserLocators.contactNameField).type("Automated contact");
		cy.getByRole(advertiserLocators.contactEmailField).type("automated@test.com");
		cy.getByRole(advertiserLocators.phoneNumberField).type("12024956");
		cy.getByRole(advertiserLocators.companyAddressField).type("Automated Street 123");

		// validate that the view report button is not visible until the form is saved
		cy.findByRole("link", { name: globalContent.VIEW_REPORT }).should("not.exist");

		cy.findByRole("button", { name: globalContent.SAVE }).click();

		//Validate that the default for demand fee percentage is 0
		cy.getByRole(advertiserLocators.demandFeePercentage).should("have.value", "0");

		// View report button should be visible
		cy.findByRole("link", { name: globalContent.VIEW_REPORT }).should("exist");
	});
});
