import locators, { localeContent as lc } from "../../../locators/reportingLocators.js";
import { getHomepagePermissions } from "../../../utils/getBasePermissions";
import userSettings, { localeContent } from "../../../locators/userSettingsLocators";
import pressEscapeOnBody from "../../../utils/pressEscapeOnBody";
import sidebarLocators from "../../../locators/sideBarLocators";

const global = require("../../../locators/globalLocators.json");

describe("Display key metrics", () => {
	let count = 0;

	beforeEach(() => {
		cy.loginProgrammatically();
		count = 0;
	});

	const interceptPerformanceRequest = (reportType) => {
		cy.intercept("GET", `**/performance?reportType=${reportType}*`, (req) => {
			count++;
			//There are now 3 requests in rtb so handling it in separate condition
			if (reportType != "rtb") {
				if (count % 2 === 1) {
					req.reply({
						statusCode: 200,
						fixture: `reporting/kpiMetrics/${reportType}.json`,
					});
				} else {
					if (count % 2 === 0) {
						req.reply({
							statusCode: 200,
							fixture: `reporting/kpiMetrics/${reportType}PrevDateRange.json`,
						});
					}
				}
			} else {
				if (count % 3 === 2) {
					req.reply({
						statusCode: 200,
						fixture: `reporting/kpiMetrics/${reportType}.json`,
					});
				} else {
					if (count % 3 === 1) {
						req.reply({
							statusCode: 200,
							fixture: `reporting/kpiMetrics/${reportType}PrevDateRange.json`,
						});
					}
				}
			}
		});
	};

	const validateKPIMetric = (kpi, value, change) => {
		cy.findAllByTestId(`${kpi}Value`).should("be.visible").should("have.text", value);
		cy.findAllByTestId(`${kpi}Change`).should("be.visible").should("have.text", change);
	};

	it("display key metrics items should be there", () => {
		// Visit reporting page
		cy.visit("/dashboard/reporting");
		// Mock the Network metrics data
		interceptPerformanceRequest("network");

		// Check all labels of Network Types are there.
		Object.entries({
			opportunities: lc.METRIC_LABEL.OPPORTUNITIES,
			impressions: lc.METRIC_LABEL.IMPRESSIONS,
			fillrate: lc.METRIC_LABEL.FILL_RATE,
			opportunityCostPercent: lc.METRIC_LABEL.OPPORTUNITY_COST_PERCENT,
			pubcpm: lc.METRIC_LABEL.PUBLISHER_CPM,
			pubrevenue: lc.METRIC_LABEL.PUBLISHER_REVENUE,
			grosscpm: lc.METRIC_LABEL.GROSS_CPM,
			grossrevenue: lc.METRIC_LABEL.GROSS_REVENUE,
		}).forEach(([key, metric]) => {
			cy.findAllByTestId(key).should("be.visible").should("have.text", metric);
		});
		// Check the calculated metrics values of network.
		validateKPIMetric("opportunities", "5,600", "+24%");

		//Validate the color of the KPI Change percentage is green for positive
		cy.findAllByTestId("opportunitiesChange").within(() => {
			cy.findByText("+24%").should("have.css", "color", "rgb(0, 128, 0)");
		});

		validateKPIMetric("impressions", "20", "-20%");

		//Validate the color of the KPI Change percentage is red for negative
		cy.findAllByTestId("impressionsChange").within(() => {
			cy.findByText("-20%").should("have.css", "color", "rgb(255, 0, 0)");
		});
		validateKPIMetric("pubrevenue", "$1,080.50", "-4%");
		validateKPIMetric("grosscpm", "$5,250.00", "+25%");
		validateKPIMetric("fillrate", "0.36%", "-36%");
		validateKPIMetric("opportunityCostPercent", "0.01%", "+24%");

		validateKPIMetric("pubcpm", "$54,025.00", "+20%");
		validateKPIMetric("grossrevenue", "$105.00", "0%");

		// Mock the Campaign metrics data

		interceptPerformanceRequest("campaign");

		// Change Report Type to Campaign
		cy.findByRole("tab", { name: "Campaign" }).click();

		// Check all labels of Campaign Types are there.
		Object.entries({
			impressions: lc.METRIC_LABEL.IMPRESSIONS,
			pubcpm: lc.METRIC_LABEL.PUBLISHER_CPM,
			pubrevenue: lc.METRIC_LABEL.PUBLISHER_REVENUE,
			grosscpm: lc.METRIC_LABEL.GROSS_CPM,
			grossrevenue: lc.METRIC_LABEL.GROSS_REVENUE,
		}).forEach(([key, metric]) => {
			cy.findAllByTestId(key).should("be.visible").should("have.text", metric);
		});

		// Check the calculated metrics values of Campaign.
		validateKPIMetric("impressions", "10", "+150%");
		validateKPIMetric("pubrevenue", "$20.00", "+18%");
		validateKPIMetric("grosscpm", "$10,000.00", "-74%");
		validateKPIMetric("pubcpm", "$2,000.00", "-53%");
		validateKPIMetric("grossrevenue", "$100.00", "-35%");

		// Mock the RTB metrics data
		interceptPerformanceRequest("rtb");

		// Change Report Type to RTB
		cy.findByRole("tab", { name: "RTB" }).click();
		// Check all labels of RTB Types are there.
		Object.entries({
			rtbOpportunities: lc.METRIC_LABEL.RTB_OPPORTUNITIES,
			rtbBids: lc.METRIC_LABEL.RTB_BIDS,
			wins: lc.METRIC_LABEL.WINS,
			impressions: lc.METRIC_LABEL.IMPRESSIONS,
			closerate: lc.METRIC_LABEL.CLOSE_RATE,
			winprice: lc.METRIC_LABEL.CLOSE_CPM,
			winrevenue: lc.METRIC_LABEL.CLOSE_REVENUE,
		}).forEach(([key, metric]) => {
			cy.findAllByTestId(key).should("be.visible").should("have.text", metric);
		});

		// Check the calculated metrics values of RTB.
		validateKPIMetric("rtbOpportunities", "100", "+43%");
		validateKPIMetric("impressions", "30", "+20%");
		validateKPIMetric("wins", "15", "-21%");
		validateKPIMetric("closerate", "200%", "+52%");
		validateKPIMetric("winprice", "$4,000.00", "-26%");
		validateKPIMetric("winrevenue", "$120.00", "-11%");
		cy.findAllByTestId("rtbBidsValue").should("be.visible").should("have.text", "0");
		cy.findAllByTestId("rtbBidsChange").should("not.be.visible");

		// Click on run report button
		cy.clickElement(locators.runReportButton);
	});

	it("display key metrics change when today is selected", () => {
		// Mock the Network metrics data
		interceptPerformanceRequest("network");
		// Visit reporting page
		cy.visit("/dashboard/reporting");

		cy.clickElement(locators.dateRange);
		cy.clickElement(locators.dateRangeButtonToday);
		// Click on run report button
		cy.clickElement(locators.runReportButton);
		// KPI historical data of %age change is visible
		validateKPIMetric("opportunities", "5,600", "+24%");
	});

	it("on hover tooltip is  displayed based on date range type", () => {
		// Mock the Network metrics data
		interceptPerformanceRequest("network");
		// Visit reporting page
		cy.visit("/dashboard/reporting");

		//Validate tooltip for today
		cy.clickElement(locators.dateRange);
		cy.clickElement(locators.dateRangeButtonToday);
		// Click on run report button
		cy.clickElement(locators.runReportButton);
		// KPI historical data of %age change is visible
		cy.findAllByTestId("opportunitiesChange").trigger("mouseover");
		cy.findByText("Data compared to respective period Yesterday");

		//Validate tooltip for previous month
		cy.clickElement(locators.dateRange);
		cy.clickElement(locators.dateRangeButtonPreviousMonth);
		// Click on run report button
		cy.clickElement(locators.runReportButton);
		// KPI historical data of %age change is visible
		cy.findAllByTestId("opportunitiesChange").trigger("mouseover");
		cy.findByText("Data compared to respective last whole Month");

		//Validate tooltip for month to date
		cy.clickElement(locators.dateRange);
		cy.clickElement(locators.dateRangeButtonMonthToDate);
		// Click on run report button
		cy.clickElement(locators.runReportButton);
		// KPI historical data of %age change is visible
		cy.findAllByTestId("opportunitiesChange").trigger("mouseover");
		cy.findByText("Data compared to respective period Last Month");
	});

	it("on hover tooltip is displayed in rtb", () => {
		// Mock the Network metrics data
		interceptPerformanceRequest("rtb");
		// Visit reporting page
		cy.visit("/dashboard/reporting/?reportType=rtb");

		cy.findAllByTestId("rtbOpportunities").should("have.attr", "aria-label", lc.METRIC_TOOL_TIP.BID_REQUESTS);
	});

	it("default KPI and Reporting Table Validation - Metrics should be in sync", () => {
		const username = `defaultkpimetricsautomationentity@test.com`;
		// Create a user who only has access to the different metric for network report type
		cy.createUserWithPermissions({
			userRoleName: `automation_kpi_permission_role`,
			username: username,
			permissionsToEnable: [
				...getHomepagePermissions(),
				// Grant access to campaign and rtb reports
				"VIEW_NETWORK_REPORT",
				"VIEW_CAMPAIGN_REPORT",
				"VIEW_RTB_REPORT",
				// Grant access to metrics
				"VIEW_NETWORK_REPORT_METRIC_IMPRESSIONS",
				"VIEW_NETWORK_REPORT_METRIC_OPPORTUNITIES",
				"VIEW_NETWORK_REPORT_METRIC_GROSS_REVENUE",
				"VIEW_NETWORK_REPORT_METRIC_GROSS_CPM",
				"VIEW_NETWORK_REPORT_METRIC_QUARTILE_100",
			],
		});

		cy.loginProgrammatically({
			username: username,
		});

		// Visit User Settings index page
		cy.visit("/dashboard/user-settings");

		// Reset the Default Network metrics in case anyone has changed them in the environment
		cy.findByRole("combobox", { name: localeContent.FIELDS.defaultNetworkKpis.LABEL }).click(); // Click into the input to show the clear button
		cy.findByRole("combobox", { name: localeContent.FIELDS.defaultNetworkKpis.LABEL })
			.parent()
			.within(() => {
				cy.findByRole("button", { name: "Clear" }).click(); // Find the clear button within the Default Network Metrics input and click it
			});
		// Select all metrics to use as defaults
		cy.findByRole("option", userSettings.userMetricsImpressionsOption).click();
		cy.findByRole("option", userSettings.userMetricsQuartile100Option).click();
		cy.findByRole("option", userSettings.userMetricsOpportunitiesOption).click();
		cy.findByRole("option", userSettings.userMetricsGrossCPMOption).click();
		cy.findByRole("option", userSettings.userMetricsGrossRevenueOption).click();
		pressEscapeOnBody();

		// Save the user settings form
		cy.clickElement(global.saveButton);

		// TODO: After CP-4755 is delivered we don't need to logout and login again to have new user settings take effect, we can just visit the reporting page
		// Logout the current user
		cy.clickElement(sidebarLocators.logoutButton);

		cy.loginProgrammatically({
			username: username,
		});

		// Visit reporting dashboard
		cy.visit("/dashboard/reporting");

		// Check labels of Network Types are there.
		Object.entries({
			opportunities: lc.METRIC_LABEL.OPPORTUNITIES,
			impressions: lc.METRIC_LABEL.IMPRESSIONS,
			quartile100: lc.METRIC_LABEL.QUARTILE_100,
			grosscpm: lc.METRIC_LABEL.GROSS_CPM,
			grossrevenue: lc.METRIC_LABEL.GROSS_REVENUE,
		}).forEach(([key, metric]) => {
			cy.findAllByTestId(key).should("be.visible").should("have.text", metric);
		});

		cy.findByTestId("kpi-metrics-parent").within(() => {
			cy.get("span").should(
				"have.text",
				lc.METRIC_LABEL.OPPORTUNITIES +
					lc.METRIC_LABEL.IMPRESSIONS +
					lc.METRIC_LABEL.GROSS_CPM +
					lc.METRIC_LABEL.GROSS_REVENUE +
					lc.METRIC_LABEL.QUARTILE_100
			);
		});
	});

	it("Given a new user, default metrics should be displayed as KPIs and default columns in reporting table for RTB Dashboard", () => {
		const username = `trafficshapingmetricsautomationentity@test.com`;
		// Create a user who only has access to the different metric for rtb report type
		cy.createUserWithPermissions({
			userRoleName: `automation_traffic_shaping_permission_role`,
			username: username,
			permissionsToEnable: [
				...getHomepagePermissions(),
				// Grant access to netrowk, campaign and rtb reports
				"VIEW_NETWORK_REPORT",
				"VIEW_CAMPAIGN_REPORT",
				"VIEW_RTB_REPORT",
				// Grant access to metrics
				"VIEW_RTB_REPORT_METRIC_RTB_OPPS",
				"VIEW_RTB_REPORT_METRIC_RTB_BIDS",
				"VIEW_RTB_REPORT_METRIC_IMPRESSIONS",
				"VIEW_RTB_REPORT_METRIC_WIN_PRICE",
				"VIEW_RTB_REPORT_METRIC_WIN_REVENUE",
				"VIEW_RTB_REPORT_METRIC_POTENTIAL_BID_REQUESTS",
				"VIEW_RTB_REPORT_METRIC_FILTERED_REQUESTS",
			],
		});

		cy.loginProgrammatically({
			username: username,
		});

		// Visit reporting dashboard
		cy.visit("/dashboard/reporting");

		cy.findByRole("tab", { name: "RTB" }).click();

		// Check labels of RTB Types are there.
		Object.entries({
			potentialBidRequests: lc.METRIC_LABEL.POTENTIAL_BID_REQUESTS,
			filteredRequests: lc.METRIC_LABEL.FILTERED_REQUESTS,
			rtbOpportunities: lc.METRIC_LABEL.RTB_OPPORTUNITIES,
			impressions: lc.METRIC_LABEL.IMPRESSIONS,
			winprice: lc.METRIC_LABEL.CLOSE_CPM,
			winrevenue: lc.METRIC_LABEL.CLOSE_REVENUE,
		}).forEach(([key, metric]) => {
			cy.findAllByTestId(key).should("be.visible").should("have.text", metric);
		});

		cy.findByTestId("kpi-metrics-parent").within(() => {
			cy.get("span").should(
				"have.text",
				lc.METRIC_LABEL.POTENTIAL_BID_REQUESTS +
					lc.METRIC_LABEL.FILTERED_REQUESTS +
					lc.METRIC_LABEL.RTB_OPPORTUNITIES +
					lc.METRIC_LABEL.IMPRESSIONS +
					lc.METRIC_LABEL.CLOSE_CPM +
					lc.METRIC_LABEL.CLOSE_REVENUE
			);
		});
	});
});
