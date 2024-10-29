export const localeContent = {
	TITLE: "Programmatic Demand",
	FIELDS: {
		NAME: {
			LABEL: "Demand Name *",
		},
		FLOOR_PRICE: {
			LABEL: "Floor Price *",
		},
		DEAL: {
			LABEL: "Deal",
		},
		DEAL_ID: {
			LABEL: "Deal ID *",
		},
		PRIVATE_AUCTION: {
			LABEL: "Private Auction",
		},
		BIDDER_CONFIG: {
			ADD_BIDDER: "add",
			SEARCH: "Search",
		},
		DEAL_GOAL_TYPE: {
			IMPRESSION: {
				LABEL: "Impression",
			},
			SPEND: {
				LABEL: "Spend",
			},
			OPEN: {
				LABEL: "Open",
			},
		},
		DEAL_GOAL: {
			LABEL: "Deal Goal *",
		},
		END_DATE: {
			LABEL: "End Date",
		},
		SAVE_ALIGNMENTS: "Save Alignments",
		TOGGLE_ROW_SELECTED: "Toggle Row Selected",
		DAYPARTING: {
			LABEL: "Dayparting",
			DAY_LABEL: {
				MONDAY: "Monday",
			},
		},
		CUSTOM_URL_PARAMETER: {
			ENABLE_SWITCH_LABEL: "Custom URL Parameter",
			CUSTOM_LEAF_CREATION_BUTTON_LABEL: "add key/value group",
			EDIT_LEAF_BUTTON_LABEL: "Edit",
			RULE_VISUALIZER: {
				SHOW_RULE_LABEL: "Show Rule",
				HIDE_RULE_LABEL: "Hide Rule",
			},
		},
	},
	TEST_ID_FIELDS: {
		ALIGNMENTS_TABLE_AVAILABLE: "alignment-table-available",
		ALIGNMENTS_TABLE_ALIGN: "alignment-table-aligned",
	},
	TABS: {
		ALIGNMENTS: "Alignments",
		QUALITY: "Quality",
	},
	ERROR_MESSAGE: {
		POST_WITH_UNALLOWED_BIDDERS:
			"An active bidder is required to save this demand as active. - Please remove inactive bidders and seats",
		ACTIVATE_EXISTING_WITH_UNALLOWED_BIDDERS: "An active bidder is required to save this demand as active.",
	},
};

export default {
	addProgrammaticDemandButton: { locator: "Add Programmatic Demand", role: "link" },
	settingsTab: { locator: "Settings", role: "tab" },
	qualityTab: { locator: "Quality", role: "tab" },
	alignmentsTab: { locator: "Alignments", role: "tab" },
	demandNameField: { locator: "Demand Name", role: "textbox" },
	statusActiveRadio: { locator: "Active", role: "radio" },
	statusInactiveRadio: { locator: "Inactive", role: "radio" },
	dealToggle: { locator: "Deal", role: "checkbox" },
	availableDealersTable: { locator: "available bidders", role: "list" },
	selectedDealersTable: { locator: "Selected Bidders", role: "list" },
	searchBidderField: "Search",
	clearSelectedBiddersButton: { locator: "Clear", role: "button" },
	startDateField: "#startDate",
	endDateField: { locator: "Choose date", role: "textbox" },
	priorityDropdown: { locator: "Priority Backfill", role: "button" },
	weightDropdown: { locator: "Weight Backfill", role: "button" },
	addBidderButton: { locator: "add", role: "button" },
	auctionTypeDropdown: { locator: "Auction Type First Price", role: "button" },
	fixedPriceOption: { locator: "Fixed Price", role: "option" },
	dealIdField: { locator: "Deal ID", role: "textbox" },
	floorPriceField: { locator: "Floor Price", role: "spinbutton" },
	frequencyCappingSwitch: { locator: "Frequency Capping", role: "checkbox" },
	impressionsPerUserField: { locator: "Impressions Per User", role: "spinbutton" },
	timeframeDropdown: { locator: "Timeframe Per Day", role: "button" },
	perWeekOption: { locator: "Per Week", role: "option" },
	perWeekSelectedButton: { locator: "Timeframe Per Week", role: "button" },
	cloneAlignments: { locator: "Clone Alignments", role: "checkbox" },
};
