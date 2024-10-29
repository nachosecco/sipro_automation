import { DASHBOARD_API } from "./serviceResources";

export const cleanupNotification = (notificationName) => {
	const pathDeleteResource = (resource) => {
		return DASHBOARD_API.NOTIFICATION.getOne({ id: resource.id });
	};
	const indexPathResources = `${DASHBOARD_API.NOTIFICATION.getIndex()}s`;

	const filterResourceToDelete = (resource) => resource.name.startsWith(notificationName);
	cy.cleanResources({ indexPathResources, pathDeleteResource, filterResourceToDelete });
};

export const defaultResourceCleanup = (APIConfig, resourceIdentifierKey, resourceIdentifierValue) => {
	const pathDeleteResource = (resource) => {
		return APIConfig.getOne({ id: resource.id });
	};
	const indexPathResources = APIConfig.getIndex();

	const filterResourceToDelete = (resource) => resource[resourceIdentifierKey] === resourceIdentifierValue;
	cy.cleanResources({ indexPathResources, pathDeleteResource, filterResourceToDelete });
};
