export const localeContent = {
	FIELDS: {
		defaultNetworkKpis: {
			LABEL: "Default Network KPIs",
		},
	},
};

export default {
	userFirstNameField: { locator: "First Name", role: "textbox" },
	userLastNameField: { locator: "Last Name", role: "textbox" },
	userPhoneNumberField: { locator: "Phone Number", role: "textbox" },
	userEmailAddressField: { locator: "Email Address", role: "textbox" },
	userTimezoneField: { locator: "Timezone", role: "combobox" },
	userHideInactiveItemsField: { locator: "Hide Inactive Items", role: "checkbox" },
	userDefaultCompanyViewField: { locator: "Default Company View", role: "combobox" },
	userCompanySelect: { locator: "user-settings-default-company-test-name", role: "option" },
	defaultDensityStandardField: { locator: "Default Density Standard", role: "button" },
	defaultDensityCompactField: { locator: "Default Density Compact", role: "button" },
	defaultDensitySelect: { locator: "Compact", role: "option" },

	userNetworkDimensionSelect: { locator: "Default Network Dimensions", role: "combobox" },
	userCampaignDimensionSelect: { locator: "Default Campaign Dimensions", role: "combobox" },
	userRTBDimensionSelect: { locator: "Default RTB Dimensions", role: "combobox" },
	userDimensionAppNameSelect: { name: "App Name" },
	userDimensionDealIdSelect: { name: "Deal Id" },

	userNetworkMetricsSelect: { locator: "Default Network Metrics", role: "combobox" },
	userCampaignMetricsSelect: { locator: "Default Campaign Metrics", role: "combobox" },
	userRTBMetricsSelect: { locator: "Default RTB Metrics", role: "combobox" },

	userNetworkKPIsSelect: { locator: "Default Network KPIs", role: "combobox" },
	userCampaignKPIsSelect: { locator: "Default Campaign KPIs", role: "combobox" },
	userRTBKPIsSelect: { locator: "Default RTB KPIs", role: "combobox" },

	userMetricsImpressionsOption: { name: "Impressions" },
	userMetricsQuartile100Option: { name: "Quartile 100" },
	userMetricsOpportunitiesOption: { name: "Opportunities" },
	userMetricsGrossRevenueOption: { name: "Gross Revenue" },
	userMetricsGrossCPMOption: { name: "Gross CPM" },
	dashboardSelectMetricsLabel: { locator: "select metrics", role: "button" },
};
