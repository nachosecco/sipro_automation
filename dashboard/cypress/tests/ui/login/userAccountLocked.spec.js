import getToken from "../../../utils/getToken";
import { localeContent as lc } from "../../../locators/loginLocators.js";
import sideBarLocators from "../../../locators/sideBarLocators.js";

const timeStamp = new Date().getTime();
const username = `automationentity${timeStamp}@test.com`;

describe("User account locks after certain wrong attempts", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	afterEach(() => {
		cy.deleteTargetEntity(getToken(), username, "user", "email");
	});

	it("user account gets locked", () => {
		cy.createUserWithPermissions({
			userRoleName: `Automation_Test_Role_UserAccountLock`,
			username: username,
			permissionsToEnable: ["AUTHENTICATE_MANAGER"],
		});
		const allowedFailedAttempts = 5;
		cy.visit("/");
		cy.getByRole(sideBarLocators.logoutButton).click();
		// try log in  5 times with wrong password
		for (let i = 1; i <= allowedFailedAttempts; i++) {
			cy.login(username, "wrongpassword");
			if (i !== allowedFailedAttempts) {
				cy.validatePopupMessage(lc.INVALID_USERNAME_PASSWORD);
			}
		}
		// account gets locked by now
		// Check if it's redirecting to the forgot password screen
		cy.contains("h1", lc.FORGOT_PASSWORD_LABEL);
		cy.validatePopupMessage(lc.ACCOUNT_LOCKED_MESSAGE);
		// login again so that the new user entity can be deleted
		cy.loginProgrammatically();
	});
});
