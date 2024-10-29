import { localeContent as lc } from "../../../locators/reportingLocators";
import pressEscapeOnBody from "../../../utils/pressEscapeOnBody";

const publisherFilterOptions = require("../../../fixtures/reporting/publisherFilterOptions.json");

describe("on click of schedule report button, navigates to scheduled reports with and preloads the form with all selected filters, slices, and metrics", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("when reporting type is Network", () => {
		const firstFilterName = Object.entries(publisherFilterOptions)[0][1];
		cy.intercept("GET", "**/search-dimension*", publisherFilterOptions).as("search-dimensions:publisher");

		cy.visit("/dashboard/reporting");

		// Select Publishers, Sites, and Placements slices
		const slicesToEnable = [lc.SLICE_LABELS.publisher, lc.SLICE_LABELS.site, lc.SLICE_LABELS.placement];
		cy.findByRole("button", {
			name: lc.ADD_DIMENSION_BUTTON_LABEL,
		}).click();
		slicesToEnable.forEach((sliceName) => {
			cy.findByRole("menuitem", { name: sliceName }).click();
		});
		pressEscapeOnBody();
		// Set a filter (NOTE: The filter options endpoint is mocked because it relies on druid data)
		cy.findByRole("button", { name: lc.ADD_FILTER_BUTTON }).click();
		cy.findByLabelText(lc.FILTER_DIMENSION_LABEL).click();
		cy.findByRole("option", { name: lc.SLICE_LABELS.publisher }).click();
		cy.findByLabelText(lc.FILTER_DIMENSION_OPTIONS_LABEL).click();
		cy.findByRole("option", { name: firstFilterName }).click();
		pressEscapeOnBody();
		cy.findByRole("button", { name: lc.FILTER_SAVE_BUTTON }).click();

		// Select all metrics
		cy.findByRole("button", { name: lc.METRICS_MENU_BUTTON }).click();
		cy.findByRole("button", { name: lc.METRICS_MENU_SHOW_ALL_BUTTON }).click();

		// Navigate to Scheduled Reports
		cy.findByRole("link", { name: lc.SCHEDULE_REPORTS_BUTTON }).click();

		// Open Data Tab
		cy.findByRole("tab", { name: lc.SCHEDULE_REPORTS_TAB_LABEL.DATA }).click();

		// All Network metrics should be selected
		[
			lc.METRIC_LABEL.OPPORTUNITIES,
			lc.METRIC_LABEL.IMPRESSIONS,
			lc.METRIC_LABEL.FILL_RATE,
			lc.METRIC_LABEL.POTENTIAL_FILL_RATE,
			lc.METRIC_LABEL.GROSS_CPM,
			lc.METRIC_LABEL.GROSS_REVENUE,
			lc.METRIC_LABEL.PUBLISHER_CPM,
			lc.METRIC_LABEL.PUBLISHER_REVENUE,
			lc.METRIC_LABEL.NET_MARGIN,
			lc.METRIC_LABEL.QUARTILE_0,
			lc.METRIC_LABEL.QUARTILE_25,
			lc.METRIC_LABEL.QUARTILE_50,
			lc.METRIC_LABEL.QUARTILE_75,
			lc.METRIC_LABEL.QUARTILE_100,
			lc.METRIC_LABEL.CLICKS,
			lc.METRIC_LABEL.CTR,
			lc.METRIC_LABEL.VIEWABLE,
			lc.METRIC_LABEL.OPPORTUNITY_COST,
			lc.METRIC_LABEL.OPPORTUNITY_COST_PERCENT,
			lc.METRIC_LABEL.DEMAND_PARTNER_FEE,
		].forEach((metricLabel) => {
			cy.findByRole("button", { name: metricLabel }).should("exist");
		});

		// Publishers, Sites, and Placements slices should be selected
		cy.findByRole("checkbox", { name: lc.SCHEDULE_REPORTS_DIMENSIONS_LABEL }).should("be.checked");
		cy.findByRole("list", { name: lc.SELECTED_SLICES_LIST }).within(() => {
			cy.findAllByRole("listitem").should("have.length", 3);
			slicesToEnable.forEach((slice) => {
				cy.contains(slice);
			});
		});

		// Filter should be applied
		cy.findByRole("button", { name: lc.SLICE_LABELS.publisher }).click();
		cy.findByRole("button", { name: firstFilterName }).should("exist");
	});

	// NOTE: We're intentionally not testing filters or slices in this test as we should be covered by the Network (Default) and RTB (includes a switch of tab) tests
	it("when reporting type is Campaign", () => {
		cy.visit("/dashboard/reporting");

		// Change Report Type to Campaign
		cy.findByRole("tab", { name: lc.TAB_LABEL_CAMPAIGN }).click();

		cy.findByRole("button", { name: lc.ADD_FILTER_BUTTON }).click();
		cy.findByLabelText(lc.FILTER_DIMENSION_LABEL).click();
		cy.findByRole("option", { name: lc.OPTION_DEAL }).should("not.exist");
		pressEscapeOnBody();
		pressEscapeOnBody();

		// Select all metrics
		cy.findByRole("button", { name: lc.METRICS_MENU_BUTTON }).click();
		cy.findByRole("button", { name: lc.METRICS_MENU_SHOW_ALL_BUTTON }).click();

		// Navigate to Scheduled Reports
		cy.findByRole("link", { name: lc.SCHEDULE_REPORTS_BUTTON }).click();

		// Open Data Tab
		cy.findByRole("tab", { name: lc.SCHEDULE_REPORTS_TAB_LABEL.DATA }).click();

		// All Campaign metrics should be selected
		[
			lc.METRIC_LABEL.DEMAND_OPPORTUNITIES,
			lc.METRIC_LABEL.AD_ATTEMPTS,
			lc.METRIC_LABEL.IMPRESSIONS,
			lc.METRIC_LABEL.FILL_RATE,
			lc.METRIC_LABEL.GROSS_CPM,
			lc.METRIC_LABEL.GROSS_REVENUE,
			lc.METRIC_LABEL.PUBLISHER_CPM,
			lc.METRIC_LABEL.PUBLISHER_REVENUE,
			lc.METRIC_LABEL.NET_MARGIN,
			lc.METRIC_LABEL.QUARTILE_0,
			lc.METRIC_LABEL.QUARTILE_25,
			lc.METRIC_LABEL.QUARTILE_50,
			lc.METRIC_LABEL.QUARTILE_75,
			lc.METRIC_LABEL.QUARTILE_100,
			lc.METRIC_LABEL.CLICKS,
			lc.METRIC_LABEL.CTR,
			lc.METRIC_LABEL.VIEWABLE,
		].forEach((metricLabel) => {
			cy.findByRole("button", { name: metricLabel }).should("exist");
		});
	});

	it("when reporting type is RTB", () => {
		const firstFilterName = Object.entries(publisherFilterOptions)[0][1];
		cy.intercept("GET", "**/search-dimension*", publisherFilterOptions).as("search-dimensions:publisher");

		cy.visit("/dashboard/reporting");

		// Change Report Type to RTB
		cy.findByRole("tab", { name: lc.TAB_LABEL_RTB }).click();

		// Select Publishers, Sites, and Placements slices
		const slicesToEnable = [lc.SLICE_LABELS.publisher, lc.SLICE_LABELS.site, lc.SLICE_LABELS.placement];
		cy.findByRole("button", {
			name: lc.ADD_DIMENSION_BUTTON_LABEL,
		}).click();
		slicesToEnable.forEach((sliceName) => {
			cy.findByRole("menuitem", { name: sliceName }).click();
		});
		pressEscapeOnBody();

		// Set a filter (NOTE: The filter options endpoint is mocked because it relies on druid data)
		cy.findByRole("button", { name: lc.ADD_FILTER_BUTTON }).click();
		cy.findByLabelText(lc.FILTER_DIMENSION_LABEL).click();
		cy.findByRole("option", { name: lc.SLICE_LABELS.publisher }).click();
		cy.findByLabelText(lc.FILTER_DIMENSION_OPTIONS_LABEL).click();
		cy.findByRole("option", { name: firstFilterName }).click();
		pressEscapeOnBody();
		cy.findByRole("button", { name: lc.FILTER_SAVE_BUTTON }).click();

		// Run reports to apply config
		cy.findByRole("button", { name: lc.RUN_REPORT_BUTTON }).click();

		// Select all metrics
		cy.findByRole("button", { name: lc.METRICS_MENU_BUTTON }).click();
		cy.findByRole("button", { name: lc.METRICS_MENU_SHOW_ALL_BUTTON }).click();

		// Navigate to Scheduled Reports
		cy.findByRole("link", { name: lc.SCHEDULE_REPORTS_BUTTON }).click();

		// Open Data Tab
		cy.findByRole("tab", { name: lc.SCHEDULE_REPORTS_TAB_LABEL.DATA }).click();

		// All RTB metrics should be selected
		[
			lc.METRIC_LABEL.POTENTIAL_BID_REQUESTS,
			lc.METRIC_LABEL.FILTERED_REQUESTS,
			lc.METRIC_LABEL.RTB_OPPORTUNITIES,
			lc.METRIC_LABEL.RTB_BIDS,
			lc.METRIC_LABEL.WINS,
			lc.METRIC_LABEL.IMPRESSIONS,
			lc.METRIC_LABEL.BID_RATE,
			lc.METRIC_LABEL.WIN_RATE,
			lc.METRIC_LABEL.CLOSE_RATE,
			lc.METRIC_LABEL.BID_CPM,
			lc.METRIC_LABEL.BID_REVENUE,
			lc.METRIC_LABEL.CLOSE_CPM,
			lc.METRIC_LABEL.CLOSE_REVENUE,
			lc.METRIC_LABEL.PUBLISHER_CPM,
			lc.METRIC_LABEL.PUBLISHER_REVENUE,
			lc.METRIC_LABEL.NET_MARGIN,
			lc.METRIC_LABEL.BID_ERRORS,
			lc.METRIC_LABEL.TCP_ERRORS,
			lc.METRIC_LABEL.TIMEOUTS,
			lc.METRIC_LABEL.QUARTILE_0,
			lc.METRIC_LABEL.QUARTILE_25,
			lc.METRIC_LABEL.QUARTILE_50,
			lc.METRIC_LABEL.QUARTILE_75,
			lc.METRIC_LABEL.QUARTILE_100,
			lc.METRIC_LABEL.VIEWABLE,
			lc.METRIC_LABEL.BID_REQUEST_COST,
		].forEach((metricLabel) => {
			cy.findByRole("button", { name: metricLabel }).should("exist");
		});

		// Publishers, Sites, and Placements slices should be selected
		cy.findByRole("checkbox", { name: lc.SCHEDULE_REPORTS_DIMENSIONS_LABEL }).should("be.checked");
		cy.findByRole("list", { name: lc.SELECTED_SLICES_LIST }).within(() => {
			cy.findAllByRole("listitem").should("have.length", 3);
			slicesToEnable.forEach((slice) => {
				cy.contains(slice);
			});
		});

		// Filter should be applied
		cy.findByRole("button", { name: lc.SLICE_LABELS.publisher }).click();
		cy.findByRole("button", { name: firstFilterName }).should("exist");
	});
});
