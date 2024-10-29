import locators, { localeContent } from "../../../locators/notificationLocators";
import data from "../../../fixtures/notificationData";
import { cleanupNotification } from "../../../utils/cleanupCommands";
import pressEscapeOnBody from "../../../utils/pressEscapeOnBody";

const global = require("../../../locators/globalLocators.json");

const timeStamp = new Date().getTime();
describe("notification creation test cases", () => {
	beforeEach(() => {
		cy.loginGlobalUserProgrammatically();
	});

	it("Notification creation", () => {
		const notificationName = `${data.name} create`;
		cleanupNotification(notificationName);
		// Wait for Notification API call to complete
		cy.intercept("GET", "**/notifications*").as("notifications");
		// Visit notification index page
		cy.visit("/dashboard/notifications");
		cy.wait("@notifications");

		// Access create notification form and validate fields
		cy.clickElement(locators.addNotificationButton);
		cy.verifyElementsExist(
			global.saveButton,
			locators.notificationNameField,
			locators.notificationTypeField,
			locators.sendImmediatelyCheck,
			locators.forceNotification
		);

		// Fill/Update the form.
		cy.getByRole(locators.notificationNameField).type(`${notificationName} ${timeStamp}`);
		cy.clickElement(locators.notificationTypeField);
		cy.clickElement(locators.OptimizationAlertOption);
		// Add the description to the quill editor
		cy.get(locators.notificationTextField).invoke("text", data.description);
		cy.clickElement(locators.forceNotification);
		cy.findByRole("checkbox", { name: localeContent.SET_EXPIRATION }).click();
		cy.findByRole("spinbutton", { name: localeContent.EXPIRES_IN }).type(data.expiresIn);
		cy.clickElement(locators.checkUserRole);
		cy.clickElement(locators.roleAudienceSelection);
		// NOTE: This will fail if there is no role with the name "Company Admin" in the environment.
		// In the future we should probably create/cleanup a role at the beginning of the test
		cy.clickElement(locators.selectCompanyAdminRole);
		pressEscapeOnBody();
		cy.clickElement(global.saveButton);

		// Notification should be saved so expect success message
		cy.validatePopupMessage(`${notificationName} ${timeStamp} was successfully created`);
	});

	it("Check Quill Editors have the required buttons.", () => {
		// Wait for Notification API call to complete
		cy.intercept("GET", "**/notifications*").as("notifications");
		// Visit notification index page
		cy.visit("/dashboard/notifications");
		cy.wait("@notifications");

		// Access create notification form and validate fields
		cy.clickElement(locators.addNotificationButton);
		cy.verifyElementsExist(
			global.saveButton,
			locators.notificationNameField,
			locators.notificationTypeField,
			locators.sendImmediatelyCheck,
			locators.forceNotification
		);

		// Verify that these control buttons should be visible.
		cy.get(locators.rteBold).should("be.visible");
		cy.get(locators.rteItalic).should("be.visible");
		cy.get(locators.rteUnderline).should("be.visible");
		cy.get(locators.rteLink).should("be.visible");
		cy.get(locators.rteList).should("be.visible");
		cy.get(locators.rteClean).should("be.visible");
		cy.get(locators.rtePicker).should("be.visible");
	});
});
