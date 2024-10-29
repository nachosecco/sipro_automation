import { DASHBOARD_API } from "../utils/serviceResources";

const buildUserModel = (username, testUserRole, userModelExtension = {}) => ({
	firstName: "Automation Test",
	lastName: "User",
	phoneNumber: "1112223333",
	email: username,
	timeZone: "Z",
	status: "active",
	roles: [testUserRole.id],
	publisherAccessRestrictionConfig: { accessRestriction: "all", blacklist: [], whitelist: [] },
	advertiserAccessRestrictionConfig: { accessRestriction: "all", blacklist: [], whitelist: [] },
	...userModelExtension,
});

/**
 * We can reuse users and roles on a per-test basis, but we need to use unique role and username per test to avoid test interference
 */
Cypress.Commands.add("createUserWithPermissions", (config = {}) => {
	const { userRoleName, username, permissionsToEnable, userModelExtension } = config;

	const commonHeaders = {
		Authorization: window.localStorage.getItem("token"),
	};

	let permissionsOptions;
	let testUserRole;

	// Get the list of permissions from the API
	cy.request({
		url: DASHBOARD_API.USER_ROLES.getInit(),
		method: "GET",
		headers: commonHeaders,
	}).then((rolesInitResponse) => {
		permissionsOptions = rolesInitResponse.body.permissions;
	});

	// Configure role
	cy.request({
		url: DASHBOARD_API.USER_ROLES.getIndex(),
		method: "GET",
		headers: commonHeaders,
	})
		.then((userRolesResponse) => {
			const enabledPermissions = permissionsOptions.map((permission) => ({
				...permission,
				enabled: permissionsToEnable.includes(permission.name),
			}));
			const userRoleParams = {
				name: userRoleName,
				description: "created by an automated test that relies on permissions",
				permissions: enabledPermissions,
			};
			const userRole = userRolesResponse.body.find((userRole) => userRole.name === userRoleName);
			// If it exists, edit it to a deterministic starting value
			if (userRole) {
				return cy.request({
					url: DASHBOARD_API.USER_ROLES.getOne({ id: userRole.id }),
					method: "PUT",
					headers: commonHeaders,
					body: { ...userRole, ...userRoleParams },
				});
			} else {
				// Else create it with the known value
				return cy.request({
					url: DASHBOARD_API.USER_ROLES.getIndex(),
					method: "POST",
					headers: commonHeaders,
					body: userRoleParams,
				});
			}
		})
		.then((userRoleResponse) => {
			// Regardless of whether we get the userRole from a PUT or a POST, save the result
			testUserRole = userRoleResponse.body;
		});

	// Setup the user with the role
	cy.request({
		url: DASHBOARD_API.USER.getIndex(),
		method: "GET",
		headers: commonHeaders,
	})
		.then((usersResponse) => {
			// If user exists, get the full user information
			const existingUser = usersResponse.body.find((user) => user.email === username);
			if (existingUser) {
				return cy.request({
					url: DASHBOARD_API.USER.getOne({ id: existingUser.id }),
					method: "GET",
					headers: commonHeaders,
				});
			} else {
				// Create the user
				return cy.request({
					url: DASHBOARD_API.USER.getIndex(),
					method: "POST",
					headers: commonHeaders,
					body: buildUserModel(username, testUserRole, userModelExtension),
				});
			}
		})
		.then((userResponse) => {
			const user = userResponse.body;
			// Reset the user's password and make sure we set the user data to the known value in case it was existing and someone edited it manually in the UI
			cy.request({
				url: DASHBOARD_API.USER.getOne({ id: user.id }),
				method: "PUT",
				headers: commonHeaders,
				body: {
					id: user.id,
					...buildUserModel(username, testUserRole, userModelExtension),
					resetPassword: ["resetPassword"],
					password: Cypress.env("uiPassword"),
					passwordConfirm: Cypress.env("uiPassword"),
				},
			});
		});
});
