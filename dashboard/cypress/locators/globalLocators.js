const addResource = (resourceName) => {
	return `Add ${resourceName}`;
};

const editResource = (resourceName) => {
	return `Edit ${resourceName}`;
};

export const globalContent = {
	SAVE: "Save",
	DELETE: "Delete",
	CANCEL: "Cancel",
	CONFIRM_DELETE: "Delete",
	SEARCH: "Search",
	OK: "OK",
	ADD_RESOURCE_HEADING: addResource,
	EDIT_RESOURCE_HEADING: editResource,
	SUCCESSFULLY_CREATED_SUFFIX: "was successfully created",
	SUCCESSFULLY_UPDATED_SUFFIX: "was successfully updated",
	SUCCESSFULLY_DELETED_SUFFIX: "was successfully deleted",
	STATUS_OPTION_LABEL: {
		ACTIVE: "Active",
		INACTIVE: "Inactive",
	},
	VIEW_REPORT: "View Report",
};
