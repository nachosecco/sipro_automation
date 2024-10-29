import { DASHBOARD_API } from "../utils/serviceResources";
import getToken from "../utils/getToken";
import { DEFAULT_USER_REQUEST_BODY, DEFAULT_ROLE_REQUEST_BODY } from "../fixtures/defaultUserRequestBody";

export const createOrUpdateUser = ({
	token = getToken(),
	firstName,
	lastName,
	userBody = DEFAULT_USER_REQUEST_BODY,
	roleName,
	roleBody,
	email,
}) => {
	return createOrUpdateUserRoles({
		roleName,
		roleBody,
	}).then((response) => {
		const roleId = response.body.id;
		cy.request({
			url: DASHBOARD_API.USER.getIndex(),
			method: "GET",
			headers: {
				Authorization: token,
			},
		}).then((response) => {
			const responseBody = response.body;
			const user = responseBody.find((item) => item.name === firstName + " " + lastName);
			const requestBody = {
				...userBody,
				firstName: firstName,
				lastName: lastName,
				roles: [roleId],
				email: email,
			};
			if (user) {
				// Update
				cy.request({
					url: DASHBOARD_API.USER.getOne({ id: user.id }),
					method: "PUT",
					headers: {
						Authorization: token,
					},
					body: requestBody,
				});
			} else {
				// Create
				cy.request({
					url: DASHBOARD_API.USER.getIndex(),
					method: "POST",
					headers: {
						Authorization: token,
					},
					body: requestBody,
				});
			}
		});
	});
};

export const createOrUpdateUserRoles = ({ token = getToken(), roleName, roleBody = DEFAULT_ROLE_REQUEST_BODY }) => {
	return cy
		.request({
			url: DASHBOARD_API.USER_ROLES.getIndex(),
			method: "GET",
			headers: {
				Authorization: token,
			},
		})
		.then((response) => {
			const responseBody = response.body;
			const role = responseBody.find((item) => item.name === roleName);
			const requestBody = {
				...roleBody,
				name: roleName,
			};
			// If it exists, edit it to a deterministic starting value
			if (role) {
				return cy.request({
					url: DASHBOARD_API.USER_ROLES.getOne({ id: role.id }),
					method: "PUT",
					headers: {
						Authorization: token,
					},
					body: requestBody,
				});
			} else {
				// Else create it with the known value
				return cy.request({
					url: DASHBOARD_API.USER_ROLES.getIndex(),
					method: "POST",
					headers: {
						Authorization: token,
					},
					body: requestBody,
				});
			}
		});
};
