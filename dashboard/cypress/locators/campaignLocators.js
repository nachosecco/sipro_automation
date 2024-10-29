export const localeContent = {
	TITLE: "Campaigns",
	FIELD_NAMES: {
		DAYPARTING: "Dayparting",
		NAME: "Campaign Name",
	},
	DAYPARTING: {
		DAY_LABEL: {
			MONDAY: "Monday",
		},
	},
};

export const campaignLocators = {
	addCampaignButton: { locator: "Add Campaign", role: "link" },
	insertionOrderDropdown: { locator: "Insertion Name", role: "combobox" },
	settingsTab: { locator: "Settings", role: "tab" },
	qualityTab: { locator: "Quality", role: "tab" },
	mediaTab: { locator: "MEDIA", role: "tab" },
	campaignNameField: { locator: "Campaign Name", role: "textbox" },
	statusActiveRadio: { locator: "Active", role: "radio" },
	statusInactiveRadio: { locator: "Inactive", role: "radio" },
	cpmField: { locator: "CPM", role: "spinbutton" },
	opportunityExposureSpin: { locator: "Opportunity Exposure %", role: "spinbutton" },
	startDateField: "#startDate",
	endDateField: { locator: "Choose date", role: "textbox" },
	goalTypeImpressionRadio: { locator: "Impression", role: "radio" },
	goalTypeSpendRadio: { locator: "Spend", role: "radio" },
	goalTypeOpenRadio: { locator: "Open", role: "radio" },
	impressionGoalField: { locator: "Impression Goal", role: "spinbutton" },
	pacingTypeEvenRadio: { locator: "Even", role: "radio" },
	pacingTypeAsapRadio: { locator: "ASAP", role: "radio" },
	frequencyCappingSwitch: { locator: "Frequency Capping", role: "checkbox" },
	frequencyCappingDisableRadio: { locator: "Disable", role: "radio" },
	spendGoalField: { locator: "Spend Goal", role: "spinbutton" },
	campaignPriorityDropdown: { locator: "Campaign Priority Backfill", role: "button" },
	campaignWeightDropdown: { locator: "Campaign Weight Backfill", role: "button" },
	returnOneMediaInAdResponseCheckbox: { locator: "Return One Media in Ad Response", role: "checkbox" },
	insertionOrderOptionZero: { locator: "Automation Entity", role: "option" },
	impressionsPerUserField: { locator: "Impressions Per User", role: "spinbutton" },
	timeframeDropdown: { locator: "Timeframe Per Day", role: "button" },
};
