import { locators as login } from "../locators/loginLocators.js";

// Login through UI command
Cypress.Commands.add("login", (user, password) => {
	cy.visit("/login");
	cy.getByRole(login.userField).type(user);
	cy.getByLabelText(login.passField).type(password, { log: false });
	cy.getByRole(login.signInButton).click();
});
