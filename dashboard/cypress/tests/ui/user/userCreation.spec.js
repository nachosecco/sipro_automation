import { userLocators } from "../../../locators/userLocators";
import { globalContent } from "../../../locators/globalLocators";
import { getUserNames } from "../../../utils/resourceNameUtil";
import { DASHBOARD_API } from "../../../utils/serviceResources";

const cleanup = (userName) => {
	const pathDeleteResource = (resource) => {
		return DASHBOARD_API.USER.getOne({ id: resource.id });
	};
	const indexPathResources = DASHBOARD_API.USER.getIndex();
	const filterResourceToDelete = (resource) => resource.firstName == userName;
	cy.cleanResources({ indexPathResources, pathDeleteResource, filterResourceToDelete });
};

describe("User creation test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Valid user creation", () => {
		const userNames = getUserNames("User creation", "automation@test.com");
		cleanup(userNames.firstName);

		// Visit user index page
		cy.visit("/dashboard/users");

		// Access user form and validate fields
		cy.clickElement(userLocators.addUserButton);
		cy.findByRole("button", { name: globalContent.SAVE }).should("exist");
		cy.verifyElementsExist(
			userLocators.firstNameField,
			userLocators.lastNameField,
			userLocators.phoneNumberField,
			userLocators.emailAddressField,
			userLocators.timeZoneDropdown,
			userLocators.statusActiveRadio,
			userLocators.statusInactiveRadio,
			userLocators.rolesDropdown,
			userLocators.publisherAccessDropdownAllowAll,
			userLocators.advertiserAccessDropdownAllowAll
		);

		// Verify extra fields are shown depending on access selection
		cy.clickElement(userLocators.publisherAccessDropdownAllowAll);
		cy.verifyElementsExist(
			userLocators.allowAllOption,
			userLocators.blockAllOption,
			userLocators.blockListOption,
			userLocators.allowListOption
		);
		cy.clickElement(userLocators.blockListOption);

		cy.clickElement(userLocators.advertiserAccessDropdownAllowAll);
		cy.verifyElementsExist(
			userLocators.allowAllOption,
			userLocators.blockAllOption,
			userLocators.blockListOption,
			userLocators.allowListOption
		);
		cy.clickElement(userLocators.blockListOption);

		cy.verifyElementsExist(userLocators.publisherBlockListDropdown, userLocators.advertiserBlockListDropdown);

		cy.clickElement(userLocators.publisherAccessDropdownBlockList);
		cy.clickElement(userLocators.allowListOption);
		cy.clickElement(userLocators.advertiserAccessDropdownBlockList);
		cy.clickElement(userLocators.allowListOption);

		cy.verifyElementsExist(userLocators.publisherAllowListDropdown, userLocators.advertiserAllowListDropdown);

		// Fill the form
		cy.clickElement(userLocators.publisherAccessDropdownAllowList);
		cy.clickElement(userLocators.allowAllOption);
		cy.clickElement(userLocators.advertiserAccessDropdownAllowList);
		cy.clickElement(userLocators.allowAllOption);

		cy.getByRole(userLocators.firstNameField).type(userNames.firstName);
		cy.getByRole(userLocators.lastNameField).type(userNames.lastName);
		cy.getByRole(userLocators.phoneNumberField).type("1234567890");
		cy.getByRole(userLocators.emailAddressField).type(userNames.email);
		cy.clickElement(userLocators.rolesDropdown);
		cy.get(userLocators.roleOptionZero).click();

		// Verify default values are selected
		cy.getByRole(userLocators.timeZoneDropdown).should("have.value", "Coordinated Universal Time (UTC)");
		cy.getByRole(userLocators.statusActiveRadio).should("be.checked");

		// Submit form
		cy.findByRole("button", { name: globalContent.SAVE }).click();

		// Validate pop up is visible and it's text
		cy.validatePopupMessage(
			`${userNames.firstName} ${userNames.lastName} ${globalContent.SUCCESSFULLY_CREATED_SUFFIX}`
		);
	});
});
