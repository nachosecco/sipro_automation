import getToken from "../utils/getToken";

/**
 * This will search all resources with the filter and delete it
 */
Cypress.Commands.add(
	"cleanResources",
	({ token = getToken(), indexPathResources, pathDeleteResource, filterResourceToDelete, companyOverride }) => {
		const headers = {
			Authorization: token,
			"X-COMPANY-OVERRIDE": companyOverride,
		};
		cy.request({
			url: indexPathResources,
			method: "GET",
			headers,
		}).then((response) => {
			const body = response.body;

			body.filter((resource) => filterResourceToDelete(resource)).forEach((resource) => {
				const pathToDelete = pathDeleteResource(resource);

				cy.request({
					url: pathToDelete,
					method: "DELETE",
					headers,
				});
			});
		});
	}
);
