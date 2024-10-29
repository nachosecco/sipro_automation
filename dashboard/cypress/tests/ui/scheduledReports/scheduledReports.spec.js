import { localeContent as lc } from "../../../locators/scheduledReportsLocators";
import { globalContent } from "../../../locators/globalLocators";
import { DASHBOARD_API } from "../../../utils/serviceResources";

const cleanup = (reportName) => {
	const pathDeleteResource = (resource) => {
		return DASHBOARD_API.SCHEDULED_REPORTS.getOne({ id: resource.id });
	};
	const indexPathResources = DASHBOARD_API.SCHEDULED_REPORTS.getIndex();
	const filterResourceToDelete = (resource) => resource.fileName == reportName;
	cy.cleanResources({ indexPathResources, pathDeleteResource, filterResourceToDelete });
};

describe("Scheduled Reports Form", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("should validate that end dates are after start dates", () => {
		const reportName = "end_date_must_be_after_start_date";
		// Clean up the prior test run's saved report
		cleanup(reportName);

		// Visit the create Scheduled Report page
		cy.visit("/dashboard/scheduled-reports/INIT");

		// Input the required fields
		cy.findByRole("textbox", { name: lc.FIELDS.FILE_NAME.LABEL }).type(reportName);
		cy.findByLabelText(lc.FIELDS.REPEATS_ON.LABEL).click();
		cy.findAllByRole("option").first().click();

		// By default, the start date should be today, so set an end date of yesterday (invalid)
		// Open the end date date picker
		cy.findByLabelText(lc.FIELDS.END_DATE.LABEL).click();

		// Mui brings active focus to the button for the current day, so we press left to go back one day
		cy.document().then((doc) => {
			cy.wrap(doc.activeElement).type("{leftArrow}");
		});

		// Click the button that's now the actively focused element, which should be yesterday's date
		cy.document().then((doc) => {
			cy.wrap(doc.activeElement).click();
		});

		// Click OK to confirm the date
		cy.findByRole("button", { name: globalContent.OK }).click();

		// Submit the form
		cy.findByRole("button", { name: globalContent.SAVE }).click();

		// Check that the error message is displayed
		cy.findByText(lc.VALIDATION_MESSAGES.END_DATE_AFTER_START_DATE).should("exist");

		// Input an end date of tomorrow (valid)
		// Open the end date date picker
		cy.findByLabelText(lc.FIELDS.END_DATE.LABEL).click();
		// Mui brings active focus to the button for the selected day (yesterday), so we press right twice to select tomorrow
		cy.document().then((doc) => {
			cy.wrap(doc.activeElement).type("{rightArrow}{rightArrow}");
		});

		// Click the button that's now the actively focused element, which should be tomorrow
		cy.document().then((doc) => {
			cy.wrap(doc.activeElement).click();
		});

		// Click OK to confirm the date
		cy.findByRole("button", { name: globalContent.OK }).click();

		// Submit the form
		cy.findByRole("button", { name: globalContent.SAVE }).click();

		// Check that the form is submitted successfully
		cy.findByText(`${reportName} ${globalContent.SUCCESSFULLY_CREATED_SUFFIX}`).should("exist");
	});
});
