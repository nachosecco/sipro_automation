export const localeContent = { INDEX_HEADING: "Audiences" };

export const audienceLocators = {
	addAudienceButton: { locator: "Add Audience", role: "link" },
	audienceNameField: { locator: "Audience Name", role: "textbox" },
	descriptionField: { locator: "Description", role: "textbox" },
	searchField: "Search",
	andOperator: { locator: "AND", role: "button" },
	orOperator: { locator: "OR", role: "button" },
	notOperator: { locator: "NOT", role: "button" },
	parenthesisOperator: { locator: "( )", role: "button" },
	removeSegmentButton: "[data-testid='expression-chip'] > .MuiSvgIcon-root",
	targetSegmentButton: { locator: "Accessories", role: "button" },
};
