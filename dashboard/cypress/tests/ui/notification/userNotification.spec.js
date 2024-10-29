import getToken from "../../../utils/getToken";
import getPrimaryCompanyId from "../../../utils/getPrimaryCompany";
import data, { localeContent as lc } from "../../../fixtures/notificationData";
import { cleanupNotification } from "../../../utils/cleanupCommands";

const timeStamp = new Date().getTime();
const badgeClass = ".MuiButtonBase-root";

describe("user notification test cases", () => {
	const userNotificationName = `${data.name} user`;
	beforeEach(() => {
		cy.loginGlobalUserProgrammatically();
	});

	let notificationName, notificationNameWithType;

	it("user notification read and delete", () => {
		cleanupNotification(userNotificationName);
		// Declare notification name
		notificationName = `${userNotificationName} ${timeStamp}`;
		notificationNameWithType = `${data.type}: ${userNotificationName} ${timeStamp}`;
		// Get the primary company Id.
		const companyId = getPrimaryCompanyId();
		// Create the base notification.
		cy.checkBaseNotificationRequest(getToken(), notificationName, companyId);
		// Visit user notification index page
		cy.visit("/dashboard/user-notifications");

		// Check if the newly created notification is unread
		cy.findByText(notificationNameWithType).should(($labels) => {
			expect($labels).to.have.css("font-weight", "700");
		});
		// Click on unread notification
		cy.findByText(notificationNameWithType).click();
		// After reading the notification, the newly created notification should be regular
		cy.findByText(notificationNameWithType).should(($labels) => {
			expect($labels).to.have.css("font-weight", "400");
		});

		// Delete the user Notification
		cy.findAllByTestId("DeleteIcon").first().click();

		cy.findByRole("dialog").within(() => {
			cy.findByRole("button", { name: lc.DELETE_BUTTON_TEXT }).click();
		});

		// Notification should be deleted so expect success message
		cy.validatePopupMessage(lc.DELETE_USER_NOTIFICATION_SUCCESS_MESSAGE);
	});

	it("check user notification badge", () => {
		cleanupNotification(userNotificationName);
		// Declare notification name
		notificationName = `${userNotificationName} ${timeStamp} Badge`;
		// Visit user notification index page
		cy.visit("/dashboard/user-notifications");

		// Wait for badge to lead
		cy.get(badgeClass).should("be.visible");

		// Get the unread notification count from badge before generation of notification
		cy.get(`[aria-label="notifications"]`)
			.children()
			.then(($muiBadge) => {
				const countBeforeNotificationGenerate = $muiBadge.text();
				cy.wrap(countBeforeNotificationGenerate).as("countBeforeNotificationGenerate");
			});

		// Get the primary company Id.
		const companyId = getPrimaryCompanyId();
		// Create the base notification.
		cy.checkBaseNotificationRequest(getToken(), notificationName, companyId);
		// Reload the application to get the latest count
		cy.reload();

		// Wait for badge to lead
		cy.get(badgeClass).should("be.visible");
		// Get the unread notification count after generation of notification
		cy.get(badgeClass).then(($muiBadge) => {
			const countAfterNotificationGenerate = $muiBadge.text();
			cy.wrap(countAfterNotificationGenerate).as("countAfterNotificationGenerate");
		});
		// After notification generate, the count on the badge should be equal to the badge count + 1 before notification generate.
		cy.get("@countBeforeNotificationGenerate").then((countBeforeNotificationGenerate) => {
			cy.get("@countAfterNotificationGenerate").then((countAfterNotificationGenerate) => {
				expect(countAfterNotificationGenerate).to.contain(Number(countBeforeNotificationGenerate) + 1);
			});
		});

		// Read the newly generated user Notification
		cy.get(".MuiTypography-body1").contains(notificationName).click();
		cy.reload();

		// Wait for badge to lead
		cy.get(badgeClass).should("be.visible");
		// Get the unread notification count after reading the notification
		cy.get(badgeClass).then(($muiBadge) => {
			const countAfterReadNotification = $muiBadge.text();
			cy.wrap(countAfterReadNotification).as("countAfterReadNotification");
		});
		// After Read notification, the count on the badge should be equal to the badge count before notification generate.
		cy.get("@countAfterReadNotification").then((countAfterReadNotification) => {
			cy.get("@countBeforeNotificationGenerate").then((countBeforeNotificationGenerate) => {
				expect(countAfterReadNotification).to.contain(Number(countBeforeNotificationGenerate));
			});
		});
		// Delete the latest notification
		cy.findAllByTestId("DeleteIcon").first().click();

		// confirm the delete notification
		cy.findByRole("dialog").within(() => {
			cy.findByRole("button", { name: lc.DELETE_BUTTON_TEXT }).click();
		});
		// Notification should be deleted so expect success message
		cy.validatePopupMessage(lc.DELETE_USER_NOTIFICATION_SUCCESS_MESSAGE);
	});

	it("check that generated notifications is not rendering the non html tags", () => {
		cleanupNotification(userNotificationName);
		const timeStamp = new Date().getTime();
		// Declare notification name
		notificationName = `${userNotificationName} ${timeStamp}`;
		notificationNameWithType = `${data.type}: ${notificationName}`;
		// Get the primary company Id.
		const companyId = getPrimaryCompanyId();
		// Create the base notification.
		cy.checkBaseNotificationRequest(
			getToken(),
			notificationName,
			companyId,
			`<p>${data.description} <script> this is alert("hey"); </script> ${timeStamp}</p>` // Append the Html and Non HTML tags
		);
		// Visit user notification index page
		cy.visit("/dashboard/user-notifications");

		// Check if the newly created notification is unread
		cy.findByText(notificationNameWithType).should(($labels) => {
			expect($labels).to.have.css("font-weight", "700");
		});
		// Click on unread notification
		cy.findByText(notificationNameWithType).click();
		// After reading the notification, the newly created notification should be regular
		cy.findByText(notificationNameWithType).should(($labels) => {
			expect($labels).to.have.css("font-weight", "400");
		});
		// Verify that it is not rendering the texts written within script tag.
		cy.findByText(`${data.description} ${timeStamp}`).should("exist");
		// Delete the user Notification
		cy.findAllByTestId("DeleteIcon").first().click();

		cy.findByRole("dialog").within(() => {
			cy.findByRole("button", { name: lc.DELETE_BUTTON_TEXT }).click();
		});

		// Notification should be deleted so expect success message
		cy.validatePopupMessage(lc.DELETE_USER_NOTIFICATION_SUCCESS_MESSAGE);
	});
});
