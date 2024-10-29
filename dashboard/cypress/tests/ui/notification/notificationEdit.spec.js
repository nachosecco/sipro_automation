import getToken from "../../../utils/getToken";
import getPrimaryCompanyId from "../../../utils/getPrimaryCompany";

import { localeContent } from "../../../locators/notificationLocators";
const global = require("../../../locators/globalLocators.json");
import data from "../../../fixtures/notificationData";
import { cleanupNotification } from "../../../utils/cleanupCommands";

describe("notification edit test cases", () => {
	beforeEach(() => {
		cy.loginGlobalUserProgrammatically();
	});

	it("Notification edit", () => {
		const notificationName = `${data.name} edit`;
		// Cleanup both the original and edited names to account for failures before the rename
		cleanupNotification(notificationName);
		cleanupNotification(data.updatedName);

		// Get the primary company Id.
		const companyId = getPrimaryCompanyId();
		// Create the base notification.
		cy.checkBaseNotificationRequest(getToken(), notificationName, companyId);
		// Wait for Notification API call to complete
		cy.intercept("GET", "**/notifications*").as("notifications");
		// Visit notification index page
		cy.visit("/dashboard/notifications");
		cy.wait("@notifications");

		// Search for target notification
		cy.search(notificationName);

		// Edit the target notification
		cy.clickDataGridEditMenuItem();

		// Change the name notification
		cy.findByRole("textbox", { name: localeContent.NOTIFICATION_NAME }).as("notificationNameField");
		cy.get("@notificationNameField").clear();
		cy.get("@notificationNameField").type(data.updatedName);
		cy.clickElement(global.saveButton);

		// Notification should be saved so expect success message
		cy.validatePopupMessage(`${data.updatedName} was successfully updated`);
	});
});
