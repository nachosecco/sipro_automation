import locators from "../../../locators/notificationLocators";

describe("Show the list of the notifications", () => {
	beforeEach(() => {
		cy.loginGlobalUserProgrammatically();
	});

	it("see if all the screen is properly rendered with all the required headers", () => {
		// Wait for Notification API call to complete
		cy.intercept("GET", "**/notifications*").as("notifications");
		// Visit Notification index page
		cy.visit("/dashboard/notifications");
		cy.wait("@notifications");
		// Verify the Notifications list items header
		cy.verifyElementsExist(
			locators.column.name,
			locators.column.status,
			locators.column.type,
			locators.column.createdBy,
			locators.column.createDate,
			locators.column.notificationDates,
			locators.column.inactiveDate,
			locators.column.audienceSize
		);
	});
});
