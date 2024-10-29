import { appendPrefixDashboardApiManage } from "../utils/serviceResources";
// This command will delete target entity through an API request

const resourceEndPoint = (entity) => {
	if (entity === "advertiser") {
		return "advtsrs";
	} else if (entity === "audience") {
		return "audiences";
	} else if (entity === "bidder") {
		return "rtb-bidders";
	} else if (entity === "campaign") {
		return "campaigns";
	} else if (entity === "company") {
		return "companies";
	} else if (entity === "insertion") {
		return "insertion-orders";
	} else if (entity === "media") {
		return "media";
	} else if (entity === "placement") {
		return "placements";
	} else if (entity === "programmatic") {
		return "programmatic-demand";
	} else if (entity === "publisher") {
		return "publishers";
	} else if (entity === "role") {
		return "user-roles";
	} else if (entity === "site") {
		return "sites";
	} else if (entity === "user") {
		return "users";
	} else if (entity === "tracker") {
		return "trackers";
	} else {
		throw "Provided entity does not exist. Please verify the value.";
	}
};

// This command will delete target entity through an API request
Cypress.Commands.add("deleteTargetEntity", (token, entityName, endpoint, entityPropName = "name") => {
	console.log("This function is deprecated, use methods in demandCommands.js or suppluCommands.js");

	const endpointPath = resourceEndPoint(endpoint);
	const url = appendPrefixDashboardApiManage(endpointPath);
	console.log(endpoint);
	console.log(url);

	cy.request({
		url: url,
		method: "GET",
		headers: {
			Authorization: token,
		},
	}).then((response) => {
		const body = response.body;
		const targetEntity = body.find((o) => o[entityPropName] === entityName);
		if (!targetEntity) {
			cy.log("Test data for target entity was not found.");
		} else {
			cy.request({
				url: appendPrefixDashboardApiManage(`${resourceEndPoint(endpoint)}/${targetEntity.id}`),
				method: "DELETE",
				headers: {
					Authorization: token,
				},
			});
		}
	});
});
