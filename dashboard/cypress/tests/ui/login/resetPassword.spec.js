const { localeContent, locators } = require("../../../locators/resetPasswordLocators.js");

describe("ResetPassword test cases", () => {
	it("Invalid Token", () => {
		cy.visit("/reset?token=token");

		// Veryfy that reset password is loaded
		cy.verifyElementsExist(locators.submitButton);
		const password = "abcd1235#A";

		cy.getByLabelText(locators.confirmPasswordField).type(password);
		cy.getByLabelText(locators.newPasswordField).type(password);
		cy.getByRole(locators.submitButton).click();

		cy.validatePopupMessage(localeContent.invalidToken);

		cy.contains(localeContent.forgotPasswordLabel).should("exist");
	});

	it("Password requirements failed", () => {
		cy.visit("/reset?token=token");

		cy.verifyElementsExist(locators.submitButton);
		const password = "abcd1235";
		cy.getByLabelText(locators.confirmPasswordField).type(password);
		cy.getByLabelText(locators.newPasswordField).type(password);
		cy.getByRole(locators.submitButton).click();

		cy.contains(localeContent.minLength);
		cy.contains(localeContent.specialCharMissing);
		cy.contains(localeContent.upperCaseMissing);
	});

	it("One Password requirement failed", () => {
		cy.visit("/reset?token=token");

		cy.verifyElementsExist(locators.submitButton);
		const password = "Abcdefghi#";
		cy.getByLabelText(locators.confirmPasswordField).type(password);
		cy.getByLabelText(locators.newPasswordField).type(password);
		cy.getByRole(locators.submitButton).click();

		cy.contains(localeContent.numberMissing);
	});
});
