import sideBar from "../../../locators/sideBarLocators";
import { localeContent as lc } from "../../../locators/loginLocators";
const { locators } = require("../../../locators/loginLocators.js");

describe("Login test cases", () => {
	it("Valid login", () => {
		cy.visit("/login");

		// Verify that login web elements exist
		cy.verifyElementsExist(locators.userField, locators.signInButton, locators.forgetPassLink);
		cy.getByLabelText(locators.passField).should("exist");

		// Type user and pass and click sign in button
		cy.login(Cypress.env("uiUser"), Cypress.env("uiPassword"));

		// Validate an element from UI to be sure user accessed dashboard
		cy.getByRole(sideBar.navigationMenuButtonReporting).should("be.visible");
	});

	it("Provide incorrect password and then login", () => {
		cy.visit("/login");

		// Verify that login web elements exist
		cy.verifyElementsExist(locators.userField, locators.signInButton, locators.forgetPassLink);
		cy.getByLabelText(locators.passField).should("exist");

		// Type user and pass and click sign in button
		cy.login(Cypress.env("uiUser"), "wrong password");
		cy.validatePopupMessage(lc.INVALID_USERNAME_PASSWORD);

		cy.login(Cypress.env("uiUser"), Cypress.env("uiPassword"));
		// Validate an element from UI to be sure user accessed dashboard
		cy.getByRole(sideBar.navigationMenuButtonReporting).should("be.visible");
	});

	it("Page title should be Siprocal", () => {
		cy.visit("/login");

		cy.title().should("eq", "Siprocal");
	});
});
