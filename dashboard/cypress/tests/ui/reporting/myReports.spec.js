import { localeContent as myReportLocaleContent } from "../../../locators/myReportsLocators";
import { localeContent as rlc } from "../../../locators/reportingLocators";
import { localeContent as slc } from "../../../locators/scheduledReportsLocators";
import appendRequired from "../../../utils/appendRequired";
import { globalContent } from "../../../locators/globalLocators";
import { DASHBOARD_API } from "../../../utils/serviceResources";
import { defaultResourceCleanup } from "../../../utils/cleanupCommands";

describe("on my reports ", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("schedule report manual execution with a new a network report then click in the execution button", () => {
		const FILE_NAME = "UI_Test_Schedule_Manual_Report_Test";

		defaultResourceCleanup(DASHBOARD_API.SCHEDULED_REPORTS, "fileName", FILE_NAME);
		defaultResourceCleanup(DASHBOARD_API.RUN_REPORTS, "name", FILE_NAME);

		//Going to reporting to create a new scheduled report
		cy.visit("/dashboard/reporting");
		cy.findByRole("button", { name: rlc.RUN_REPORT_BUTTON }).click();
		// Navigate to Scheduled Reports
		cy.findByRole("link", { name: rlc.SCHEDULE_REPORTS_BUTTON }).click();

		// On to Scheduled Reports, fill required fields

		cy.intercept("POST", "**/scheduled-reports*").as("scheduled-reports");

		cy.findByLabelText(appendRequired(slc.FIELDS.FILE_NAME.LABEL)).type(FILE_NAME);

		cy.findByRole("combobox", { name: slc.FIELDS.REPEATS_ON.LABEL }).click();

		Object.values(slc.FIELDS.REPEATS_ON.OPTIONS).forEach((label) =>
			cy.findByRole("option", { name: label }).click()
		);
		cy.get("body").type(`{esc}`);

		// Enable the include header button
		cy.clickElement(slc.INCLUDE_HEADER_LOCATOR);

		cy.findByRole("button", { name: globalContent.SAVE }).click();

		cy.contains(globalContent.SUCCESSFULLY_CREATED_SUFFIX);

		// Verify that after saving the schedule report the include header should be checked
		cy.getByRole(slc.INCLUDE_HEADER_LOCATOR).should("be.checked");

		//Going to my reports to do a manual execution of the created scheduled report
		cy.visit("/dashboard/my-reports");

		cy.intercept("POST", "**/run*").as("scheduled-reports-run");

		cy.findAllByRole("searchbox").eq(0).type(FILE_NAME);

		// Waiting to finish the debounce
		/* eslint-disable cypress/no-unnecessary-waiting */
		cy.wait(600);

		cy.findAllByRole("button", { name: myReportLocaleContent.SCHEDULE_ACTIONS_BUTTON.LABEL }, { timeout: 10000 })
			.eq(0)
			.click();

		cy.findByRole("menuitem", {
			name: myReportLocaleContent.SCHEDULE_ACTIONS_BUTTON.OPTIONS.MANUAL_RUN.LABEL,
		}).click();
		cy.findByRole("button", {
			name: myReportLocaleContent.SCHEDULE_ACTIONS_BUTTON.OPTIONS.MANUAL_RUN.CONFIRM_BUTTON,
		}).click();

		cy.wait("@scheduled-reports-run").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 201);
		});
	});

	it("create a schedule report wait to end then click in the execution button", () => {
		const FILE_NAME = "UI_Test_Schedule_Retry_Report_Test";

		defaultResourceCleanup(DASHBOARD_API.SCHEDULED_REPORTS, "fileName", FILE_NAME);
		defaultResourceCleanup(DASHBOARD_API.RUN_REPORTS, "name", FILE_NAME);

		//Going to reporting to create a new scheduled report
		cy.visit("/dashboard/reporting");
		cy.findByRole("button", { name: rlc.RUN_REPORT_BUTTON }).click();
		// Navigate to Scheduled Reports
		cy.findByRole("link", { name: rlc.SCHEDULE_REPORTS_BUTTON }).click();

		// On to Scheduled Reports, fill required fields

		cy.intercept("POST", "**/scheduled-reports*").as("scheduled-reports");

		cy.findByLabelText(appendRequired(slc.FIELDS.FILE_NAME.LABEL)).type(FILE_NAME);

		cy.findByRole("combobox", { name: slc.FIELDS.REPEATS_ON.LABEL }).click();

		Object.values(slc.FIELDS.REPEATS_ON.OPTIONS).forEach((label) =>
			cy.findByRole("option", { name: label }).click()
		);

		cy.findByRole("button", { name: globalContent.SAVE }).click();

		cy.wait("@scheduled-reports").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 201);
		});

		cy.contains(globalContent.SUCCESSFULLY_CREATED_SUFFIX);

		//Going to my reports to do a manual execution of the created scheduled report
		cy.visit("/dashboard/my-reports");

		cy.intercept("POST", "**/run*").as("scheduled-reports-run");

		cy.findAllByRole("searchbox").eq(0).type(FILE_NAME);

		cy.wait(600);

		cy.findAllByRole("button", { name: myReportLocaleContent.SCHEDULE_ACTIONS_BUTTON.LABEL }, { timeout: 10000 })
			.eq(0)
			.click();

		cy.findByRole("menuitem", {
			name: myReportLocaleContent.SCHEDULE_ACTIONS_BUTTON.OPTIONS.MANUAL_RUN.LABEL,
		}).click();
		cy.findByRole("button", {
			name: myReportLocaleContent.SCHEDULE_ACTIONS_BUTTON.OPTIONS.MANUAL_RUN.CONFIRM_BUTTON,
		}).click();

		//Going to my reports to do a retry execution of the created scheduled report
		cy.visit("/dashboard/my-reports");
		cy.intercept("GET", "**/run-reports*").as("run-reports");

		cy.intercept("POST", "**/retry*").as("retry");

		cy.wait("@run-reports").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 200);
		});

		//Finding the actions of file we created
		cy.findAllByRole("searchbox").eq(1).type(FILE_NAME);
		cy.wait(600);
		cy.findByText("Completed Reports")
			.parent()
			.parent()
			.parent()
			.parent()
			.siblings(".MuiDataGrid-main")
			.findAllByText(FILE_NAME)
			.first()
			.parent()
			.parent()
			.children()
			.first()
			.click();

		cy.findByRole("menuitem", {
			name: myReportLocaleContent.COMPLETED_REPORTS_ACTIONS_BUTTON.OPTIONS.RETRY.LABEL,
		}).click();
		cy.findByRole("button", {
			name: myReportLocaleContent.COMPLETED_REPORTS_ACTIONS_BUTTON.OPTIONS.RETRY.CONFIRM_BUTTON,
		}).click();

		cy.wait("@retry").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 201);
		});
	});
});
