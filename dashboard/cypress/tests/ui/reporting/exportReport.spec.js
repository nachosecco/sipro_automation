import { globalContent } from "../../../locators/globalLocators.js";
import rl, { localeContent as lc } from "../../../locators/reportingLocators.js";
import { getHomepagePermissions } from "../../../utils/getBasePermissions.js";
import pressEscapeOnBody from "../../../utils/pressEscapeOnBody";
import replaceBaseUri from "../../../utils/replaceBaseUri.js";

function getReportUriByEnvironment(originalPath) {
	if (Cypress.env("name") === "local") {
		return replaceBaseUri(originalPath, Cypress.env("dashboardApi"));
	}
	return originalPath;
}

// Define the maximum number of retries
const MAX_RELOAD_RETRIES = 10;
// Function to reload the page and check for the element, because we use polling to mark reports as finished but this takes too long to wait for
function openReportActionsMenuWhenReportFinished(reportName, retries = 0) {
	// Reload the page.
	// NOTE: We're relying on the time it takes to load the page as a natural timeout, though this is potentially flaky. It's mitigated by having a high number of retries. The downside is that this test could take a lot of time to run when it fails but most of the time it should not fail
	cy.reload();

	// Check if the status is correct for the new report
	cy.get('[data-field="name"]')
		.filter(`:contains("${reportName}")`) // Find the cell with the report name
		.parent()
		.find('[data-field="status"]') // Within the parent row of the target report name cell, find the status cell
		.then(($element) => {
			const isFinished = $element.text() === lc.STATUS_FINISHED;

			// If the status isn't "Finished", and we haven't reached the maximum number of retries, try again
			if (!isFinished) {
				if (retries < MAX_RELOAD_RETRIES) {
					openReportActionsMenuWhenReportFinished(reportName, retries + 1);
				} else {
					throw new Error(`Exported Report generation did not finish in ${MAX_RELOAD_RETRIES} retries`);
				}
			} else {
				cy.wrap($element).parent().find("button").click();
			}
		});
}

describe("Export Report", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Network: on successful report creation, suppresses action menu for any pending reports until finished", () => {
		let completedReportsResponse;
		const timeStamp = new Date().getTime();
		const reportName = `export-network-report-${timeStamp}`;
		// Filter dimension options come from druid data and are non-deterministic so we mock them
		cy.intercept("GET", "**/search-dimension*", { fixture: "reporting/countryFilterOptions.json" }).as(
			"search-dimensions:country"
		);
		cy.visit("/dashboard/reporting");
		// Open Calendar
		cy.clickElement(rl.dateRange);
		// Set a custom range
		cy.clickElement(rl.dateRangeTabCustom);
		// Select First Date of the current month as start date
		cy.clickFirstElement(rl.firstDateOfTheMonth);
		// Select First Date of the current month as last date
		cy.clickFirstElement(rl.firstDateOfTheMonth);
		// Close the calendar popup
		cy.get("body").type(`{esc}`);

		// Open Filter
		cy.clickElement(rl.addFilterDropdown);
		// Open Dimension list
		cy.clickElement(rl.addDimensionDropdown);
		// Select country as dimension
		cy.clickElement(rl.countryOptionSelect);
		// Select a country option
		cy.findByLabelText(lc.FILTER_DIMENSION_OPTIONS_LABEL).click();
		cy.findByRole("option", { name: lc.COUNTRY_INDIA }).click();
		pressEscapeOnBody();
		// Click on save button
		cy.clickElement(rl.saveButton);

		// Select Publishers, Sites, and Placements slices
		const slicesToEnable = [lc.SLICE_LABELS.publisher, lc.SLICE_LABELS.site, lc.SLICE_LABELS.placement];

		cy.findByRole("button", {
			name: lc.ADD_DIMENSION_BUTTON_LABEL,
		}).click();
		cy.wrap(slicesToEnable).each((sliceName) => {
			cy.findByRole("menuitem", { name: sliceName }).click();
		});
		pressEscapeOnBody();

		// Open Metrics options
		cy.clickElement(rl.openMetricsOptions);
		// enable the publish CPM metrics
		cy.clickElement(rl.checkPublisherCPM);
		// Close the metrics popup
		cy.get("body").type(`{esc}`);

		// Intercept the request and set the first item (data comes back from API by createdData with most recently created first)
		cy.intercept("GET", "**/reports/run-reports", (req) => {
			req.continue((res) => {
				const transformedBody = res.body.map((item, index) => {
					if (index === 0) {
						item.status = lc.STATUS_PENDING;
					}
					return item;
				});
				res.body = transformedBody;
				completedReportsResponse = res;
				return res;
			});
		}).as("run-reports1");
		// Click on Export button
		cy.clickElement(rl.exportButton);
		// add a new report name
		cy.findByLabelText(lc.REPORT_NAME.MODAL_REPORT_NAME).then(($input) => {
			cy.wrap($input).clear();
			cy.wrap($input).type(reportName);
		});
		// save the report name
		cy.clickElement(rl.modalSaveButton);

		// Validate that success pop up shows and displays correct text
		cy.validatePopupMessage(lc.SUCCESS_MESSAGE_ON_REPORT_SAVE(reportName));

		// Go to my reports screen
		cy.visit("/dashboard/my-reports");

		// Wait for the first request to finish
		cy.wait("@run-reports1");

		// There shouldn't be any action button for the pending report
		cy.get(`[data-field="name"]:contains("${reportName}")`).parent().findByRole("button").should("not.exist");

		// Intercept the next request to add the Finished status response since there is no guarantee it actually finishes
		cy.intercept("GET", "**/reports/run-reports", (req) => {
			req.continue((res) => {
				const transformedBody = completedReportsResponse.body.map((item, index) => {
					if (index === 0) {
						item.status = lc.STATUS_FINISHED;
					}
					return item;
				});
				res.body = transformedBody;
				return res;
			});
		}).as("run-reports2");

		// Wait for the second request to finish
		cy.wait("@run-reports2", { timeout: 20000 }).its("response.statusCode").should("eq", 200);
		// verify the report name
		cy.get('[data-field="name"]').eq(1).should("have.text", reportName);

		cy.get('[data-field="status"]')
			.eq(1)
			.should("have.text", lc.STATUS_FINISHED)
			.siblings()
			.find("button") // 1st button is export
			.click();
		cy.findByRole("menuitem", { name: lc.ACTION_BUTTON_DOWNLOAD_CSV }).should("exist");
	});

	it("RTB: on successful report creation, suppresses action menu for any pending reports until finished", () => {
		let completedReportsResponse;
		const reportName = `export-rtb-report-${new Date().getTime()}`;
		// Filter dimension options come from druid data and are non-deterministic so we mock them
		cy.intercept("GET", "**/search-dimension*", { fixture: "reporting/countryFilterOptions.json" }).as(
			"search-dimensions:country"
		);
		cy.visit("/dashboard/reporting");

		// Switch to rtb tab
		cy.clickElement(rl.rtbTab);
		// Open Calendar
		cy.clickElement(rl.dateRange);
		// Set a custom range
		cy.clickElement(rl.dateRangeTabCustom);
		// Select First Date of the current month as start date
		cy.clickFirstElement(rl.firstDateOfTheMonth);
		// Select First Date of the current month as last date
		cy.clickFirstElement(rl.firstDateOfTheMonth);
		// Close the calendar popup
		cy.get("body").type(`{esc}`);

		// Open Filter
		cy.clickElement(rl.addFilterDropdown);
		// Open Dimension list
		cy.clickElement(rl.addDimensionDropdown);
		// Select country as dimension
		cy.clickElement(rl.countryOptionSelect);
		// Select a country option
		cy.findByLabelText(lc.FILTER_DIMENSION_OPTIONS_LABEL).click();
		cy.findByRole("option", { name: lc.COUNTRY_INDIA }).click();
		pressEscapeOnBody();
		// Click on save button
		cy.clickElement(rl.saveButton);

		// Select Publishers, Sites, and Placements slices
		const slicesToEnable = [lc.SLICE_LABELS.publisher, lc.SLICE_LABELS.site, lc.SLICE_LABELS.placement];

		cy.findByRole("button", {
			name: lc.ADD_DIMENSION_BUTTON_LABEL,
		}).click();
		cy.wrap(slicesToEnable).each((sliceName) => {
			cy.findByRole("menuitem", { name: sliceName }).click();
		});
		pressEscapeOnBody();

		// Open Metrics options
		cy.clickElement(rl.openMetricsOptions);
		// enable the publish CPM metrics
		cy.clickElement(rl.checkPublisherCPM);
		// Close the metrics popup
		cy.get("body").type(`{esc}`);

		// Intercept the request and set the first item (data comes back from API by createdData with most recently created first)
		cy.intercept("GET", "**/reports/run-reports", (req) => {
			req.continue((res) => {
				const transformedBody = res.body.map((item, index) => {
					if (index === 0) {
						item.status = lc.STATUS_PENDING;
					}
					return item;
				});
				res.body = transformedBody;
				completedReportsResponse = res;
				return res;
			});
		}).as("run-reports1");
		// Click on Export button
		cy.clickElement(rl.exportButton);
		// add a new report name
		cy.findByLabelText(lc.REPORT_NAME.MODAL_REPORT_NAME).then(($input) => {
			cy.wrap($input).clear();
			cy.wrap($input).type(reportName);
		});
		// save the report name
		cy.clickElement(rl.modalSaveButton);

		// Go to my reports screen
		cy.visit("/dashboard/my-reports");

		// Wait for the first request to finish
		cy.wait("@run-reports1");

		// There shouldn't be any action button for the pending report
		cy.get(`[data-field="name"]:contains("${reportName}")`).parent().findByRole("button").should("not.exist");

		// Intercept the request to add the Finished status response since there is no guarantee it actually finishes
		cy.intercept("GET", "**/reports/run-reports", (req) => {
			req.continue((res) => {
				const transformedBody = completedReportsResponse.body.map((item, index) => {
					if (index === 0) {
						item.status = lc.STATUS_FINISHED;
					}
					return item;
				});
				res.body = transformedBody;
				return res;
			});
		}).as("run-reports2");

		cy.wait("@run-reports2", { timeout: 20000 }).its("response.statusCode").should("eq", 200);

		// verify the report name
		cy.get('[data-field="name"]').eq(1).should("have.text", reportName);

		cy.get('[data-field="status"]')
			.eq(1)
			.should("have.text", lc.STATUS_FINISHED)
			.siblings()
			.find("button") // 1st button is export
			.click();
		cy.findByRole("menuitem", { name: lc.ACTION_BUTTON_DOWNLOAD_CSV }).should("exist");
	});

	it("CAMPAIGN: on successful report creation, suppresses action menu for any pending reports until finished", () => {
		let completedReportsResponse;
		const reportName = `export-campaign-report-${new Date().getTime()}`;
		// Filter dimension options come from druid data and are non-deterministic so we mock them
		cy.intercept("GET", "**/search-dimension*", { fixture: "reporting/countryFilterOptions.json" }).as(
			"search-dimensions:country"
		);
		cy.visit("/dashboard/reporting");

		// Switch to rtb tab
		cy.clickElement(rl.campaignTab);
		// Open Calendar
		cy.clickElement(rl.dateRange);
		// Set a custom range
		cy.clickElement(rl.dateRangeTabCustom);
		// Select First Date of the current month as start date
		cy.clickFirstElement(rl.firstDateOfTheMonth);
		// Select First Date of the current month as last date
		cy.clickFirstElement(rl.firstDateOfTheMonth);
		// Close the calendar popup
		cy.get("body").type(`{esc}`);

		// Open Filter
		cy.clickElement(rl.addFilterDropdown);
		// Open Dimension list
		cy.clickElement(rl.addDimensionDropdown);
		// Select country as dimension
		cy.clickElement(rl.countryOptionSelect);
		// Select a country option
		cy.findByLabelText(lc.FILTER_DIMENSION_OPTIONS_LABEL).click();
		cy.findByRole("option", { name: lc.COUNTRY_INDIA }).click();
		pressEscapeOnBody();
		// Click on save button
		cy.clickElement(rl.saveButton);

		// Select Publishers, Sites, and Placements slices
		const slicesToEnable = [lc.SLICE_LABELS.publisher, lc.SLICE_LABELS.site, lc.SLICE_LABELS.placement];

		cy.findByRole("button", {
			name: lc.ADD_DIMENSION_BUTTON_LABEL,
		}).click();
		cy.wrap(slicesToEnable).each((sliceName) => {
			cy.findByRole("menuitem", { name: sliceName }).click();
		});
		pressEscapeOnBody();

		// Open Metrics options
		cy.clickElement(rl.openMetricsOptions);
		// enable the publish CPM metrics
		cy.clickElement(rl.checkPublisherCPM);
		// Close the metrics popup
		cy.get("body").type(`{esc}`);

		// Intercept the request and set the first item (data comes back from API by createdData with most recently created first)
		cy.intercept("GET", "**/reports/run-reports", (req) => {
			req.continue((res) => {
				const transformedBody = res.body.map((item, index) => {
					if (index === 0) {
						item.status = lc.STATUS_PENDING;
					}
					return item;
				});
				res.body = transformedBody;
				completedReportsResponse = res;
				return res;
			});
		}).as("run-reports1");
		// Click on Export button
		cy.clickElement(rl.exportButton);
		// add a new report name
		cy.findByLabelText(lc.REPORT_NAME.MODAL_REPORT_NAME).then(($input) => {
			cy.wrap($input).clear();
			cy.wrap($input).type(reportName);
		});
		// save the report name
		cy.clickElement(rl.modalSaveButton);

		// Go to my reports screen
		cy.visit("/dashboard/my-reports");

		// Wait for the first request to finish
		cy.wait("@run-reports1");

		// There shouldn't be any action button for the pending report
		cy.get(`[data-field="name"]:contains("${reportName}")`).parent().findByRole("button").should("not.exist");

		// Intercept the request to add the Finished status response since there is no guarantee it actually finishes
		cy.intercept("GET", "**/reports/run-reports", (req) => {
			req.continue((res) => {
				const transformedBody = completedReportsResponse.body.map((item, index) => {
					if (index === 0) {
						item.status = lc.STATUS_FINISHED;
					}
					return item;
				});
				res.body = transformedBody;
				return res;
			});
		}).as("run-reports2");

		// Wait for the second request to finish
		cy.wait("@run-reports2", { timeout: 20000 }).its("response.statusCode").should("eq", 200);
		// verify the report name
		cy.get('[data-field="name"]').eq(1).should("have.text", reportName);

		cy.get('[data-field="status"]')
			.eq(1)
			.should("have.text", lc.STATUS_FINISHED)
			.siblings()
			.find("button") // 1st button is export
			.click();
		cy.findByRole("menuitem", { name: lc.ACTION_BUTTON_DOWNLOAD_CSV }).should("exist");
	});

	it("Network CSV Report: Validate Dimension order, it should be same as provided in slice", () => {
		const timeStamp = new Date().getTime();
		const reportName = `network-csv-report-${timeStamp}`;

		cy.visit("/dashboard/reporting");

		// Select Publishers, Hours, Sites, and Placements slices
		const slicesToEnable = [
			lc.SLICE_LABELS.publisher,
			lc.SLICE_LABELS.hour,
			lc.SLICE_LABELS.site,
			lc.SLICE_LABELS.placement,
		];

		cy.findByRole("button", {
			name: lc.ADD_DIMENSION_BUTTON_LABEL,
		}).click();
		cy.wrap(slicesToEnable).each((sliceName) => {
			cy.findByRole("menuitem", { name: sliceName }).click();
		});
		pressEscapeOnBody();

		// Click on Export button
		cy.clickElement(rl.exportButton);
		// add a new report name
		cy.findByLabelText(lc.REPORT_NAME.MODAL_REPORT_NAME).then(($input) => {
			cy.wrap($input).clear();
			cy.wrap($input).type(reportName);
		});
		// save the report name
		cy.clickElement(rl.modalSaveButton);

		// Validate that success pop up shows and displays correct text
		cy.validatePopupMessage(lc.SUCCESS_MESSAGE_ON_REPORT_SAVE(reportName));

		cy.intercept("GET", "**/reports/run-reports").as("run-reports");

		// Go to my reports screen
		cy.visit("/dashboard/my-reports");

		// Wait for the report to be ready and open action menu
		openReportActionsMenuWhenReportFinished(reportName);

		const downloadName = "network_csv_report.csv";
		// Use cypress to download the excel file
		cy.findByRole("menuitem", { name: lc.ACTION_BUTTON_DOWNLOAD_CSV }).then(($downloadButton) => {
			cy.downloadFile(getReportUriByEnvironment($downloadButton.attr("href")), "cypress/downloads", downloadName);
		});
		cy.readFile(`cypress/downloads/${downloadName}`).then((slice) => {
			expect(slice).to.contain("Report Title");
			expect(slice).to.contain("Date Range");
			expect(slice).to.contain("Generated By");
			expect(slice).to.contain("Report Title");
			expect(slice).to.contain("Publisher,Hour,Site,Placement");
		});
	});

	it("Network Export Report: Validate headers", () => {
		const timeStamp = new Date().getTime();
		const reportName = `UI-Test-Report-${timeStamp}`;

		cy.visit("/dashboard/reporting");

		// Select Publishers and Placements slices
		const slicesToEnable = [lc.SLICE_LABELS.publisher, lc.SLICE_LABELS.placement];

		cy.findByRole("button", {
			name: lc.ADD_DIMENSION_BUTTON_LABEL,
		}).click();
		cy.wrap(slicesToEnable).each((sliceName) => {
			cy.findByRole("menuitem", { name: sliceName }).click();
		});
		cy.get("body").type("{esc}");

		// Click on Export button
		cy.clickElement(rl.exportButton);
		// add a new report name
		cy.findByLabelText(lc.REPORT_NAME.MODAL_REPORT_NAME).then(($input) => {
			cy.wrap($input).clear();
			cy.wrap($input).type(reportName);
		});
		// save the report name
		cy.clickElement(rl.modalSaveButton);

		// Validate that success pop up shows and displays correct text
		cy.validatePopupMessage(lc.SUCCESS_MESSAGE_ON_REPORT_SAVE(reportName));

		// Go to my reports screen
		cy.visit("/dashboard/my-reports");

		// Wait for the report to be ready and open action menu
		openReportActionsMenuWhenReportFinished(reportName);

		const downloadName = "exportedReport.xlsx";
		// Use cypress to download the excel file
		cy.findByRole("menuitem", { name: lc.ACTION_BUTTON_DOWNLOAD_EXCEL }).then(($downloadButton) => {
			cy.downloadFile(getReportUriByEnvironment($downloadButton.attr("href")), "cypress/downloads", downloadName);
		});

		cy.task("readExcel", { file: `cypress/downloads/${downloadName}`, sheet: "Sheet0", header: 1 }).then((rows) => {
			// The first four rows are the company logo
			expect(rows[4][0]).to.equal("Report Title");
			expect(rows[5][0]).to.equal("Date Range");
			expect(rows[6][0]).to.equal("Generated By");
			expect(rows[7][0]).to.equal("Generated On");
			// We have a spacer row
			expect(rows[8]).to.be.empty;
			// Header row
			expect(rows[9]).to.deep.equal([
				lc.SLICE_LABELS.publisher,
				lc.SLICE_LABELS.placement,
				lc.METRIC_LABEL.OPPORTUNITIES,
				lc.METRIC_LABEL.IMPRESSIONS,
				lc.METRIC_LABEL.FILL_RATE,
				lc.METRIC_LABEL.GROSS_REVENUE,
			]);
		});
	});

	it("Demand Client users should see alternate labels for certain metric ", () => {
		// Create a demand client user who only has access to the Gross Revenue aka gross spend metric for campaign and network reports
		const USERNAME = `demand-client-user-export@automation.com`;
		cy.createUserWithPermissions({
			userRoleName: `demand_client_user_export`,
			username: USERNAME,
			permissionsToEnable: [
				// Grant base permissions as well as ability to view network reporting
				...getHomepagePermissions(),
				// Grant access to campaign reports
				"VIEW_CAMPAIGN_REPORT",
				"VIEW_NETWORK_REPORT",
				// Grant access to only gross revenue aka gross spend
				"VIEW_NETWORK_REPORT_METRIC_GROSS_REVENUE",
				"VIEW_CAMPAIGN_REPORT_METRIC_GROSS_REVENUE",
			],
			userModelExtension: {
				isDemandClient: true,
			},
		});

		// Login as the demand client user
		cy.loginProgrammatically({
			username: USERNAME,
		});

		// Visit the reporting dashboard
		cy.visit("/dashboard/reporting?reportType=campaign");
		// Click export button
		cy.findByRole("button", { name: lc.EXPORT_BUTTON_LABEL }).click();
		// Add a report name that will be unique between test runs
		const reportName = `Test_Campaign_Demand_Client_Labels_${new Date().getTime()}`;
		cy.findByLabelText(lc.REPORT_NAME.MODAL_REPORT_NAME).then(($input) => {
			cy.wrap($input).clear();
			cy.wrap($input).type(reportName);
		});
		// Save the report
		cy.findByRole("button", { name: globalContent.SAVE }).click();
		// Validate that success pop up shows and displays correct text
		cy.validatePopupMessage(lc.SUCCESS_MESSAGE_ON_REPORT_SAVE(reportName));

		// Go to my reports screen
		cy.visit("/dashboard/my-reports");

		// Wait for the report to be ready and open action menu
		openReportActionsMenuWhenReportFinished(reportName);

		const downloadName = "demand_client_report.xlsx";
		// Use cypress to download the excel file
		cy.findByRole("menuitem", { name: lc.ACTION_BUTTON_DOWNLOAD_EXCEL }).then(($downloadButton) => {
			cy.downloadFile(getReportUriByEnvironment($downloadButton.attr("href")), "cypress/downloads", downloadName);
		});

		// Verify the report has the alternate labels
		cy.task("readExcel", { file: `cypress/downloads/${downloadName}`, sheet: "Sheet0", header: 1 }).then((rows) => {
			// The first four rows are the company logo
			expect(rows[4][0]).to.equal("Report Title");
			expect(rows[5][0]).to.equal("Date Range");
			expect(rows[6][0]).to.equal("Generated By");
			expect(rows[7][0]).to.equal("Generated On");
			// We have a spacer row
			expect(rows[8]).to.be.empty;
			// Header row
			expect(rows[9]).to.deep.equal([lc.DEMAND_CLIENT_METRIC_LABELS.GROSS_REVENUE]);
		});
	});
});
