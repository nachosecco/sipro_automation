import { DASHBOARD_API } from "../utils/serviceResources";
import data from "../fixtures/notificationData";

// This command will fetch the API looking for a notification, if that notification does not exist it will create it.
Cypress.Commands.add(
	"checkBaseNotificationRequest",
	(token, notificationName = data.name, companyId = 1, notificationDescription = data.description) => {
		cy.request({
			url: `${DASHBOARD_API.NOTIFICATION.getIndex()}s`,
			method: "GET",
			headers: {
				Authorization: token,
			},
		}).then((notificationResponse) => {
			const body = notificationResponse.body;
			const targetNotification = body.find((o) => o.name === notificationName);
			if (!targetNotification) {
				cy.request({
					url: DASHBOARD_API.NOTIFICATION.getIndex(),
					method: "POST",
					headers: {
						Authorization: token,
					},
					body: {
						companyAudience: [companyId], // Notifying to the default company, TODD: will get this from the query string
						expires: false,
						forceNotify: true,
						name: notificationName,
						notificationText: notificationDescription,
						roleAudience: [],
						sendImmediately: true,
						type: "optimization",
						userAudience: [],
					},
				});
			}
		});
	}
);
