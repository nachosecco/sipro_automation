import getToken from "../../../utils/getToken";
import publisherLocators, { localeContent } from "../../../locators/publisherLocators";
import { getSupplyNames } from "../../../utils/resourceNameUtil";
import { globalContent } from "../../../locators/globalLocators";

describe("Publisher creation test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Publisher creation smoke test", () => {
		const supplyNames = getSupplyNames("Publisher creation smoke test");
		// Delete the publisher created by the most recent test run
		cy.deleteTargetEntity(getToken(), supplyNames.publisherName, "publisher");
		// Visit publisher index page
		cy.visit("/dashboard/publishers");

		// Verify that page title is publishers
		cy.findByRole("heading", { name: localeContent.INDEX_HEADING });

		// Assert presence of add pub button and click it
		cy.clickElement(publisherLocators.addPublisherButton);

		// Validate these elements are visible
		cy.verifyElementsExist(
			publisherLocators.settingsTab,
			publisherLocators.verificationTab,
			publisherLocators.sitesTab,
			publisherLocators.publisherNameField,
			publisherLocators.statusActiveRadio,
			publisherLocators.statusInactiveRadio,
			publisherLocators.defaultFloorField,
			publisherLocators.revenueShareField,
			publisherLocators.contactNameField,
			publisherLocators.contactEmailField,
			publisherLocators.phoneNumberField,
			publisherLocators.companyAddressField,
			publisherLocators.billingDiffCheckbox
		);

		// Validate that default is active
		cy.getByRole(publisherLocators.statusActiveRadio).should("be.checked");

		// Fill the form
		cy.getByRole(publisherLocators.publisherNameField).type(supplyNames.publisherName);
		cy.getByRole(publisherLocators.contactNameField).type("Automated contact");
		cy.getByRole(publisherLocators.contactEmailField).type("automated@test.com");
		cy.getByRole(publisherLocators.phoneNumberField).type("12024956");
		cy.getByRole(publisherLocators.companyAddressField).type("Automated Street 123");

		// Go to verification tab and validate fields
		cy.clickElement(publisherLocators.verificationTab);
		cy.verifyElementsExist(
			publisherLocators.adSystemDomainField,
			publisherLocators.accountIdField,
			publisherLocators.accountRelationshipRadioDirect,
			publisherLocators.accountRelationshipRadioReseller,
			publisherLocators.certificationAuthorityIdField,
			publisherLocators.publisherDomainField,
			publisherLocators.sellerTypeRadioPublisher,
			publisherLocators.sellerTypeRadioIntermediary,
			publisherLocators.sellerTypeRadioBoth,
			publisherLocators.isConfidentialRadioYes,
			publisherLocators.isConfidentialRadioNo
		);

		// Verify that domain, account relationship, seller type and is confidential fields have values
		cy.getByRole(publisherLocators.adSystemDomainField).should("have.value", "siprocalads.com");
		cy.getByRole(publisherLocators.accountRelationshipRadioDirect).should("be.checked");
		cy.getByRole(publisherLocators.sellerTypeRadioPublisher).should("be.checked");
		cy.getByRole(publisherLocators.isConfidentialRadioNo).should("be.checked");

		// Complete mandatory fields and submit
		cy.getByRole(publisherLocators.publisherDomainField).type("automated.test.com");
		cy.findByRole("button", { name: globalContent.SAVE }).click();

		// validate that the view report button is not visible until the form is saved
		cy.findByRole("link", { name: globalContent.VIEW_REPORT }).should("not.exist");

		// Validate pop message
		cy.validatePopupMessage(`${supplyNames.publisherName} ${globalContent.SUCCESSFULLY_CREATED_SUFFIX}`);

		//Validate that Account ID was generated
		cy.getByRole(publisherLocators.accountIdField).invoke("val").should("not.be.empty");
		cy.clickElement(publisherLocators.settingsTab);

		// View report button should be visible
		cy.findByRole("link", { name: globalContent.VIEW_REPORT }).should("exist");
	});
	it("Publisher creation without filling the contact information", () => {
		const supplyNames = getSupplyNames("Publisher creation without contact info smoke test");
		// Delete the publisher created by the most recent test run
		cy.deleteTargetEntity(getToken(), supplyNames.publisherName, "publisher");
		// Visit publisher index page
		cy.visit("/dashboard/publishers");

		// Verify that page title is publishers
		cy.findByRole("heading", { name: localeContent.INDEX_HEADING });

		// Assert presence of add pub button and click it
		cy.clickElement(publisherLocators.addPublisherButton);

		// Fill the form
		cy.getByRole(publisherLocators.publisherNameField).type(supplyNames.publisherName);

		// Go to verification tab and validate fields
		cy.clickElement(publisherLocators.verificationTab);

		// Complete mandatory fields and submit
		cy.getByRole(publisherLocators.publisherDomainField).type("automated.test.com");
		cy.findByRole("button", { name: globalContent.SAVE }).click();

		// Validate pop message
		cy.validatePopupMessage(`${supplyNames.publisherName} ${globalContent.SUCCESSFULLY_CREATED_SUFFIX}`);

		//Validate that Account ID was generated
		cy.getByRole(publisherLocators.accountIdField).invoke("val").should("not.be.empty");
	});
});
