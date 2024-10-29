import { appendCurrencyLabel } from "../../../locators/common";
import { getHomepagePermissions } from "../../../utils/getBasePermissions.js";
import locators, { localeContent as lc } from "../../../locators/reportingLocators";
import pressEscapeOnBody from "../../../utils/pressEscapeOnBody";

describe("Reporting dashboard", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("When user edits reporting form, run report submit button should have warning badge & after submitting form it should not be there", () => {
		// Visit reporting page
		cy.visit("/dashboard/reporting");
		// Assert that the warning badge on button should not exist initially
		cy.findByTestId(locators.UNSAVED_CHANGES_INDICATOR_BADGE_TEST_ID).should("have.attr", "aria-hidden", "true");

		// Edit form by selecting a dimension
		cy.findByRole("button", { name: lc.ADD_DIMENSION_BUTTON_LABEL }).click();
		// Select the option
		cy.findByRole("menuitem", { name: lc.SLICE_LABELS.publisher }).click();
		pressEscapeOnBody();
		// Assert that the warning badge on button should exist
		cy.findByTestId(locators.UNSAVED_CHANGES_INDICATOR_BADGE_TEST_ID).should("have.attr", "aria-hidden", "false");
		// Submit the form
		cy.clickElement(locators.runReportButton);
		// Assert that the warning badge on button should not exist
		cy.findByTestId(locators.UNSAVED_CHANGES_INDICATOR_BADGE_TEST_ID).should("have.attr", "aria-hidden", "true");
	});

	it("Can delete selected dimensions", () => {
		cy.visit("/dashboard/reporting");

		// Select Publishers, Sites, and Placements slices
		const sliceLabels = [lc.SLICE_LABELS.publisher, lc.SLICE_LABELS.site, lc.SLICE_LABELS.placement];
		// Click add dimension
		cy.findByRole("button", { name: lc.ADD_DIMENSION_BUTTON_LABEL }).click();
		sliceLabels.forEach((label) => {
			// Select the option
			cy.findByRole("menuitem", { name: label }).click();
		});
		pressEscapeOnBody();

		// Delete the second slice
		cy.findByRole("listitem", { name: lc.SLICE_LABELS.site }).within(() => {
			cy.findAllByTestId("CancelIcon").click();
		});

		// Verify that the slice is removed
		cy.findByRole("listitem", { name: lc.SLICE_LABELS.site }).should("not.exist");
		cy.findByRole("button", { name: lc.SLICE_LABELS.site }).should("not.exist");
		// Verify that remaining slice chips are there in the right order
		const expectedRemainingLabels = [lc.SLICE_LABELS.publisher, lc.SLICE_LABELS.placement];
		cy.findAllByTestId(locators.TEST_ID_DIMENSIONS_TOOLBAR_CHIP)
			.should("have.length", expectedRemainingLabels.length)
			.each((chip, index) => {
				cy.wrap(chip).should("have.text", expectedRemainingLabels[index]);
			});
	});

	it("dimensions can be dragged to a new order using the keyboard", () => {
		cy.visit("/dashboard/reporting");

		// Select Publishers, Sites, and Placements slices
		const sliceLabels = [lc.SLICE_LABELS.publisher, lc.SLICE_LABELS.site, lc.SLICE_LABELS.placement];
		// Click add dimension
		cy.findByRole("button", { name: lc.ADD_DIMENSION_BUTTON_LABEL }).click();
		sliceLabels.forEach((label) => {
			// Select the option
			cy.findByRole("menuitem", { name: label }).click();
		});
		pressEscapeOnBody();

		// Focus on last dimension chip dnd button (second button with the same name as the delete button for the same listitem)
		cy.findAllByRole("button", { name: lc.SLICE_LABELS.placement })
			.last()
			.click()
			// Press enter on dnd button to start drag
			.type("{enter}")
			// Press left on the keyboard twice to move the item to the beginning of the dimensions
			.type("{leftArrow}{leftArrow}")
			// Press enter to drop the item
			.type("{enter}")
			// Press right on the keyboard (to prove that the previous press of enter has ended the drag sequence)
			.type("{rightArrow}");

		// Dimension item order should be as expected
		const expectedLabelOrder = [lc.SLICE_LABELS.placement, lc.SLICE_LABELS.publisher, lc.SLICE_LABELS.site];
		cy.findByRole("list", { name: "Dimensions" }).within(() => {
			cy.findAllByRole("listitem").each((el, index) => {
				cy.wrap(el).should("have.text", expectedLabelOrder[index]);
			});
		});

		// Spy on requests to the filter-and-group endpoint to prove the new slice order has taken effect
		cy.intercept("GET", "**/filter-and-group*").as("filterAndGroup");

		// Run reports to apply config
		cy.findByRole("button", { name: lc.RUN_REPORT_BUTTON }).click();

		cy.wait("@filterAndGroup").then(({ request }) => {
			const searchParams = new URL(request.url).searchParams;
			// Dragged slice should be used for the grouped request
			expect(searchParams.get("group")).to.equal("placement");
		});
	});

	it("Tabs on Reporting Dashboard allow switching", () => {
		// Browse to reporting dashboard
		cy.visit("/dashboard/reporting");
		cy.contains("Reporting");
		// Assert that Default Metrics are present on screen for Network report type
		[
			lc.METRIC_LABEL.OPPORTUNITIES,
			lc.METRIC_LABEL.IMPRESSIONS,
			lc.METRIC_LABEL.FILL_RATE,
			appendCurrencyLabel(lc.METRIC_LABEL.GROSS_REVENUE),
		].forEach((label) => cy.findByRole("columnheader", { name: label }).should("exist"));
		// Switch to campaigns tab
		cy.clickElement(locators.campaignTab);
		// Assert that Default Metrics are present on screen for Campaign report type
		[
			lc.METRIC_LABEL.IMPRESSIONS,
			appendCurrencyLabel(lc.METRIC_LABEL.GROSS_REVENUE),
			lc.METRIC_LABEL.QUARTILE_100,
		].forEach((label) => cy.findByRole("columnheader", { name: label }).should("exist"));
		// Switch to rtb tab
		cy.clickElement(locators.rtbTab);
		// Assert that Default Metrics are present on screen for RTB report type
		[
			lc.METRIC_LABEL.RTB_OPPORTUNITIES,
			lc.METRIC_LABEL.RTB_BIDS,
			lc.METRIC_LABEL.WINS,
			lc.METRIC_LABEL.IMPRESSIONS,
			lc.METRIC_LABEL.BID_RATE,
			lc.METRIC_LABEL.WIN_RATE,
			lc.METRIC_LABEL.CLOSE_RATE,
			appendCurrencyLabel(lc.METRIC_LABEL.CLOSE_REVENUE),
		].forEach((label) => cy.findByRole("columnheader", { name: label }).should("exist"));
	});

	it("Metric options should only be visible when user has permissions", () => {
		// Intercepting Permissions API
		cy.intercept("**/permissions*", {
			body: [
				"VIEW_NETWORK_REPORT_METRIC_OPPORTUNITIES",
				"VIEW_NETWORK_REPORT_METRIC_GROSS_REVENUE",
				"VIEW_NETWORK_REPORT_METRIC_QUARTILE_100",
				"VIEW_NETWORK_REPORT",
			],
		});
		// Visit Reporting page
		cy.visit("/dashboard/reporting");
		// Click Metrics Column
		cy.clickElement(locators.selectMetricsButton);
		cy.findByRole("checkbox", { name: lc.METRIC_LABEL.OPPORTUNITIES }).should("exist");
		cy.findByRole("checkbox", { name: lc.METRIC_LABEL.QUARTILE_100 }).should("exist");
		cy.findByRole("checkbox", { name: lc.METRIC_LABEL.IMPRESSIONS }).should("not.exist");
	});

	it("Network Reporting - All Metrics should be visible in table when we select show all option under metrics menu", () => {
		// Visit Reporting page
		cy.visit("/dashboard/reporting");
		// Click Metrics Column
		cy.clickElement(locators.selectMetricsButton);
		[
			lc.METRIC_LABEL.OPPORTUNITIES,
			lc.METRIC_LABEL.IMPRESSIONS,
			lc.METRIC_LABEL.FILL_RATE,
			appendCurrencyLabel(lc.METRIC_LABEL.GROSS_CPM),
			appendCurrencyLabel(lc.METRIC_LABEL.GROSS_REVENUE),
			appendCurrencyLabel(lc.METRIC_LABEL.PUBLISHER_CPM),
			appendCurrencyLabel(lc.METRIC_LABEL.PUBLISHER_REVENUE),
			lc.METRIC_LABEL.NET_MARGIN,
			appendCurrencyLabel(lc.METRIC_LABEL.NET_REVENUE),
			lc.METRIC_LABEL.QUARTILE_0,
			lc.METRIC_LABEL.QUARTILE_25,
			lc.METRIC_LABEL.QUARTILE_50,
			lc.METRIC_LABEL.QUARTILE_75,
			lc.METRIC_LABEL.QUARTILE_100,
			lc.METRIC_LABEL.CLICKS,
			lc.METRIC_LABEL.CTR,
			lc.METRIC_LABEL.VIEWABLE,
			lc.METRIC_LABEL.POTENTIAL_FILL_RATE,
			appendCurrencyLabel(lc.METRIC_LABEL.OPPORTUNITY_COST),
		].forEach((metricLabel) => {
			cy.findByRole("checkbox", { name: metricLabel }).should("exist");
		});
	});

	it("Campaign Reporting - All Metrics should be visible in table when we select show all option under metrics menu", () => {
		// Visit Reporting page
		cy.visit("/dashboard/reporting");
		cy.clickElement(locators.campaignTab);
		// Click Metrics Column
		cy.clickElement(locators.selectMetricsButton);
		[
			lc.METRIC_LABEL.DEMAND_OPPORTUNITIES,
			lc.METRIC_LABEL.AD_ATTEMPTS,
			lc.METRIC_LABEL.IMPRESSIONS,
			lc.METRIC_LABEL.FILL_RATE,
			appendCurrencyLabel(lc.METRIC_LABEL.GROSS_CPM),
			appendCurrencyLabel(lc.METRIC_LABEL.GROSS_REVENUE),
			appendCurrencyLabel(lc.METRIC_LABEL.PUBLISHER_CPM),
			appendCurrencyLabel(lc.METRIC_LABEL.PUBLISHER_REVENUE),
			lc.METRIC_LABEL.NET_MARGIN,
			appendCurrencyLabel(lc.METRIC_LABEL.NET_REVENUE),
			lc.METRIC_LABEL.QUARTILE_0,
			lc.METRIC_LABEL.QUARTILE_25,
			lc.METRIC_LABEL.QUARTILE_50,
			lc.METRIC_LABEL.QUARTILE_75,
			lc.METRIC_LABEL.QUARTILE_100,
			lc.METRIC_LABEL.CLICKS,
			lc.METRIC_LABEL.CTR,
			lc.METRIC_LABEL.VIEWABLE,
		].forEach((metricLabel) => {
			cy.findByRole("checkbox", { name: metricLabel }).should("exist");
		});
	});

	it("RTB Reporting - All Metrics should be visible in table when we select show all option under metrics menu", () => {
		// Visit Reporting page
		cy.visit("/dashboard/reporting");
		cy.clickElement(locators.rtbTab);
		// Click Metrics Column
		cy.clickElement(locators.selectMetricsButton);
		[
			lc.METRIC_LABEL.RTB_OPPORTUNITIES,
			lc.METRIC_LABEL.RTB_BIDS,
			lc.METRIC_LABEL.BID_RATE,
			lc.METRIC_LABEL.WINS,
			lc.METRIC_LABEL.IMPRESSIONS,
			lc.METRIC_LABEL.WIN_RATE,
			lc.METRIC_LABEL.CLOSE_RATE,
			appendCurrencyLabel(lc.METRIC_LABEL.CLOSE_REVENUE),
			appendCurrencyLabel(lc.METRIC_LABEL.BID_CPM),
			appendCurrencyLabel(lc.METRIC_LABEL.CLOSE_CPM),
			appendCurrencyLabel(lc.METRIC_LABEL.BID_REVENUE),
			appendCurrencyLabel(lc.METRIC_LABEL.PUBLISHER_CPM),
			appendCurrencyLabel(lc.METRIC_LABEL.PUBLISHER_REVENUE),
			lc.METRIC_LABEL.NET_MARGIN,
			appendCurrencyLabel(lc.METRIC_LABEL.NET_REVENUE),
			lc.METRIC_LABEL.BID_ERRORS,
			lc.METRIC_LABEL.TCP_ERRORS,
			lc.METRIC_LABEL.TIMEOUTS,
			lc.METRIC_LABEL.QUARTILE_0,
			lc.METRIC_LABEL.QUARTILE_25,
			lc.METRIC_LABEL.QUARTILE_50,
			lc.METRIC_LABEL.QUARTILE_75,
			lc.METRIC_LABEL.QUARTILE_100,
			lc.METRIC_LABEL.MOAT_VIEWABILITY,
			lc.METRIC_LABEL.MOAT_AUDIBILITY,
			appendCurrencyLabel(lc.METRIC_LABEL.MOAT_VCPM),
			appendCurrencyLabel(lc.METRIC_LABEL.MOAT_VREVENUE),
			lc.METRIC_LABEL.VIEWABLE,
			appendCurrencyLabel(lc.METRIC_LABEL.BID_REQUEST_COST),
		].forEach((metricLabel) => {
			cy.findByRole("checkbox", { name: metricLabel }).should("exist");
		});
	});

	it("When slicing by Day we should always list the days in order and no column sorting method should work", () => {
		// Visit Reporting page
		cy.visit("/dashboard/reporting");
		// Select Date Range
		cy.clickElement(locators.dateRange);
		cy.clickElement(locators.previous7Days);
		// Select Day Dimension Option
		cy.clickElement(locators.sliceSelectionButton);
		cy.clickElement(locators.sliceOptionDaysMenuItem);
		pressEscapeOnBody();
		// Intercepting the Response
		cy.intercept("**/filter-and-group*", { fixture: "reporting/daysSortingData.json" });
		cy.clickElement(locators.runReportButton);
		// Sorting for Impressions
		cy.findByRole("columnheader", { name: lc.METRIC_LABEL.IMPRESSIONS }).click();
		cy.findByRole("grid").find(`[${locators.dataRowIndexAttribute}=0]`).contains("01/23/2023");
		cy.findByRole("grid").find(`[${locators.dataRowIndexAttribute}=1]`).contains("01/24/2023");
		cy.findByRole("grid").find(`[${locators.dataRowIndexAttribute}=2]`).contains("01/25/2023");
	});

	it("When slicing by Hours we should always list the days in order and no column sorting method should work", () => {
		// Visit Reporting page
		cy.visit("/dashboard/reporting");
		// Select Date Range
		cy.clickElement(locators.dateRange);
		cy.clickElement(locators.previous7Days);
		// Select Hour Dimension Option
		cy.clickElement(locators.sliceSelectionButton);
		cy.clickElement(locators.sliceOptionHoursMenuItem);
		pressEscapeOnBody();
		// Intercepting the Response
		cy.intercept("**/filter-and-group*", { fixture: "reporting/hoursSortingData.json" });
		cy.clickElement(locators.runReportButton);
		// Sorting for Impressions
		cy.findByRole("columnheader", { name: lc.METRIC_LABEL.IMPRESSIONS }).click();
		cy.findByRole("grid").find(`[${locators.dataRowIndexAttribute}=0]`).contains("01/23/2023 : 10");
		cy.findByRole("grid").find(`[${locators.dataRowIndexAttribute}=1]`).contains("01/23/2023 : 19");
		cy.findByRole("grid").find(`[${locators.dataRowIndexAttribute}=2]`).contains("01/25/2023 : 8");
	});

	it("When slicing by any dimension, if group id is available render link to that entity that opens in new tab", () => {
		// Visit Reporting page
		cy.visit("/dashboard/reporting");
		// Open slice selection menu
		cy.clickElement(locators.sliceSelectionButton);
		// Select publisher Slice option
		cy.clickElement(locators.sliceOptionPublisherButton);
		pressEscapeOnBody();
		// Intercepting the Response
		cy.intercept("**/filter-and-group*", { fixture: "reporting/filterAndGroupDataWithGroupId.json" });
		cy.clickElement(locators.runReportButton);

		cy.findByText("Test publisher").should("exist");
		// Verify that table shows 4 rows ( 1 header and 3 data rows)
		cy.findAllByRole("row").should("have.length", 3);
		// Verify row with group id has a link to entity edit page
		cy.get("[data-rowindex=0]")
			.find("[data-field=publisher]")
			.find('a[href^="/dashboard/publishers/1?companyId"]')
			.should("exist")
			.should("have.attr", "target", "_blank");
		// Verify row without group id has no link
		cy.get("[data-rowindex=1]").find("[data-field=publisher]").find("a").should("not.exist");
	});

	it("user can select a custom and predefined date range and run reports without throwing errors", () => {
		// Spy on performance endpoint
		cy.intercept("GET", "**/manage/metrics/performance*").as("performance");

		// Visit reporting dashboard
		cy.visit("/dashboard/reporting");

		// Open calendar and select a predefined range (e.g. Today)
		cy.clickElement(locators.dateRange);
		cy.clickElement(locators.dateRangeButtonPrevious30Days);
		// Click on run report button
		cy.clickElement(locators.runReportButton);
		// Request to performance should not throw errors
		cy.wait("@performance").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 200);
		});

		// Open Calendar and select a custom range
		cy.clickElement(locators.dateRange);
		// Switch the date picker tab to Custom
		cy.clickFirstElement(locators.customTab);
		// Select First Date of the current month as start date
		cy.clickFirstElement(locators.firstDateOfTheMonth);
		// Select First Date of the current month as last date
		cy.clickFirstElement(locators.firstDateOfTheMonth);
		// Click on run report button
		cy.clickElement(locators.runReportButton);
		// Request to performance should not throw errors
		cy.wait("@performance").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 200);
		});
	});

	it("If group name is 'null' or '[REPLACE]' then table cell content should be 'Not Available' & 'Not Provided' respectively", () => {
		// Visit Reporting page
		cy.visit("/dashboard/reporting");
		// Select Hour Dimension Option
		cy.clickElement(locators.sliceSelectionButton);
		// Select Slice option
		cy.clickElement(locators.sliceOptionAppBundleMenuItem);
		pressEscapeOnBody();
		// Intercepting the Response
		cy.intercept("**/filter-and-group*", { fixture: "reporting/filterAndGroupDataWithReplace.json" });
		cy.clickElement(locators.runReportButton);
		// Verify that table shows 4 rows ( 1 header and 3 data rows)
		cy.get("[role=row]").should("have.length", 4);
		cy.get("[data-rowindex=1]").find("[data-field=appBundle]").contains(locators.notAvailable);
		cy.get("[data-rowindex=2]").find("[data-field=appBundle]").contains(locators.notProvided);
		cy.findByRole("cell", { name: locators.replaceValue }).should("not.exist");
		cy.findByRole("cell", { name: locators.nullValue }).should("not.exist");
	});

	it("(smoke) user with all permissions can slice all report types", () => {
		// Spy on performance endpoint
		cy.intercept("GET", "**/manage/metrics/performanc*").as("performance");
		cy.intercept("GET", "**/manage/metrics/filter-and-group*").as("filterAndGroup");

		// Visit reporting dashboard
		cy.visit("/dashboard/reporting");

		const sliceAndRunReports = () => {
			// Slice by one dimension
			cy.findByRole("button", {
				name: lc.ADD_DIMENSION_BUTTON_LABEL,
			}).click();
			cy.findByRole("menuitem", { name: "Placement" }).click();
			pressEscapeOnBody();
			// Click run report
			cy.findByRole("button", { name: lc.RUN_REPORT_BUTTON }).click();
			// Expect 200s for performance and filterAndGroup endpoints
			cy.wait("@performance").then(({ response }) => {
				cy.wrap(response.statusCode).should("equal", 200);
			});
			cy.wait("@filterAndGroup").then(({ response }) => {
				cy.wrap(response.statusCode).should("equal", 200);
			});
		};

		// Test network report type
		sliceAndRunReports();

		// Change report type to Campaign
		cy.findByRole("tab", { name: "Campaign" }).click();
		sliceAndRunReports();

		// Change report type to RTB
		cy.findByRole("tab", { name: "RTB" }).click();
		sliceAndRunReports();
	});

	it("user with limited permissions (only one metric and permission) should be able to slice reporting data", () => {
		const USERNAME = `limited-permissions-slice-user@automation.com`;

		// Create a user who only has access to the Impressions metric for each of the three report types
		cy.createUserWithPermissions({
			userRoleName: `automation_limited_permissions_slice`,
			username: USERNAME,
			permissionsToEnable: [
				...getHomepagePermissions(),
				// Grant access to campaign and rtb reports
				"VIEW_CAMPAIGN_REPORT",
				"VIEW_RTB_REPORT",
				// Grant access to one metric per report (we're using Impressions as a reasonable assumption for a metric that every user will have)
				"VIEW_NETWORK_REPORT_METRIC_IMPRESSIONS",
				"VIEW_CAMPAIGN_REPORT_METRIC_IMPRESSIONS",
				"VIEW_RTB_REPORT_METRIC_IMPRESSIONS",
				// Grant access to one dimension per report (we're using Placements as a reasonable assumption for a dimension that every user will have)
				"VIEW_NETWORK_REPORT_DIMENSION_PLACEMENT",
				"VIEW_CAMPAIGN_REPORT_DIMENSION_PLACEMENT",
				"VIEW_RTB_REPORT_DIMENSION_PLACEMENT",
			],
		});

		cy.loginProgrammatically({
			username: USERNAME,
		});

		// Spy on performance endpoint
		cy.intercept("GET", "**/manage/metrics/performanc*").as("performance");
		cy.intercept("GET", "**/manage/metrics/filter-and-group*").as("filterAndGroup");

		// Visit reporting dashboard
		cy.visit("/dashboard/reporting");

		const sliceAndRunReports = () => {
			// Slice by one dimension
			cy.findByRole("button", {
				name: lc.ADD_DIMENSION_BUTTON_LABEL,
			}).click();
			cy.findByRole("menuitem", { name: "Placement" }).click();
			pressEscapeOnBody();
			// Click run report
			cy.findByRole("button", { name: lc.RUN_REPORT_BUTTON }).click();
			// Expect 200s for performance and filterAndGroup endpoints
			cy.wait("@performance").then(({ response }) => {
				cy.wrap(response.statusCode).should("equal", 200);
			});
			cy.wait("@filterAndGroup").then(({ response }) => {
				cy.wrap(response.statusCode).should("equal", 200);
			});
		};

		// Test network report type
		sliceAndRunReports();

		// Change report type to Campaign
		cy.findByRole("tab", { name: "Campaign" }).click();
		sliceAndRunReports();

		// Change report type to RTB
		cy.findByRole("tab", { name: "RTB" }).click();
		sliceAndRunReports();
	});

	it("Validate data formatting in reports table", () => {
		cy.visit("/dashboard/reporting");

		// Spy on performance endpoint
		cy.intercept("GET", "**/manage/metrics/performanc*", {
			fixture: "reporting/hourlyPerformanceData.json",
		});
		// Display quartile metrics on data grid
		cy.clickElement(locators.selectMetricsButton);
		cy.clickElement(locators.quartile0MetricsCheckbox);
		cy.clickElement(locators.quartile25MetricsCheckbox);
		cy.clickElement(locators.quartile50MetricsCheckbox);
		cy.clickElement(locators.quartile75MetricsCheckbox);
		cy.clickElement(locators.quartile100MetricsCheckbox);
		cy.clickElement(locators.selectMetricsButton);

		// validate data in the  column is as expected for  quartile
		cy.getDataGridData("All", "Quartile 0", "quartile0").should("eq", "100%");
		cy.getDataGridData("All", "Quartile 25", "quartile25").should("eq", "83%");
		cy.getDataGridData("All", "Quartile 50", "quartile50").should("eq", "80%");
		cy.getDataGridData("All", "Quartile 75", "quartile75").should("eq", "67%");
		cy.getDataGridData("All", "Quartile 100", "quartile100").should("eq", "33%");
	});

	it("Validate non-default metrics are retained on clicking run-report", () => {
		// Spy on performance endpoint
		cy.intercept("GET", "**/manage/metrics/performance*", {
			fixture: "reporting/hourlyPerformanceData.json",
		}).as("performance");

		cy.visit("/dashboard/reporting");
		// Confirm default metrics do not have quartile 25 and 50 set
		cy.clickElement(locators.selectMetricsButton);
		cy.getByRole(locators.quartile25MetricsCheckbox).should("not.be.checked");
		cy.getByRole(locators.quartile50MetricsCheckbox).should("not.be.checked");

		// Select quartile 25 and 50 non-default metrics
		cy.clickElement(locators.quartile25MetricsCheckbox);
		cy.clickElement(locators.quartile50MetricsCheckbox);
		cy.clickElement(locators.selectMetricsButton);

		// Click on run report and wait for response
		cy.findByRole("button", { name: lc.RUN_REPORT_BUTTON }).click();
		cy.wait("@performance").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 200);
		});

		// Confirm that non-default metrics are still selected
		cy.findByRole("columnheader", { name: lc.METRIC_LABEL.QUARTILE_25 }).should("be.visible");
		cy.findByRole("columnheader", { name: lc.METRIC_LABEL.QUARTILE_50 }).should("be.visible");

		// Go to campaign tab to confirm user selected (non-default) metrics are not visible now
		cy.clickElement(locators.campaignTab);
		cy.wait("@performance").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 200);
		});
		cy.clickElement(locators.selectMetricsButton);
		cy.getByRole(locators.quartile25MetricsCheckbox).should("not.be.checked");
		cy.getByRole(locators.quartile50MetricsCheckbox).should("not.be.checked");
	});
});
