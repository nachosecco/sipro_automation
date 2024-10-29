import { localeContent as lc } from "../../../locators/scheduledReportsLocators";
import { globalContent } from "../../../locators/globalLocators";
import appendRequired from "../../../utils/appendRequired";
import { getBidderName } from "../../../utils/resourceNameUtil";
import { DASHBOARD_API } from "../../../utils/serviceResources";
import { defaultResourceCleanup } from "../../../utils/cleanupCommands";

describe("Scheduled Reports", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("requests filter options successfully", () => {
		// Visit create scheduled report
		cy.visit("/dashboard/scheduled-reports/INIT");
		cy.findByLabelText(lc.LABEL_ADD_RECIPIENTS).should("exist");
		// Navigate to data tab
		cy.findByRole("tab", { name: lc.TAB_LABEL_DATA }).click();
		cy.findByLabelText(lc.LABEL_REPORT_TYPE).click();
		cy.findByRole("option", { name: lc.OPTION_CAMPAIGN }).click();
		// Open the add filter menu
		cy.findByRole("button", { name: lc.BUTTON_LABEL_ADD_FILTER }).click();

		cy.intercept("**/search-dimension*").as("searchDimensions");
		// Select a filter dimension
		cy.findByLabelText(lc.FIELD_LABEL_DIMENSION).click();
		cy.findByRole("option", { name: lc.OPTION_DEAL }).should("not.exist");
		cy.findByRole("option", { name: "Publisher" }).click();
		// Call to endpoint should not result in errors
		cy.wait("@searchDimensions").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 200);
		});
	});

	it("Buyers search in Dimension should be case insensitive", () => {
		const bidder = getBidderName("Buyers search in Dimension should be case insensitive");
		// Visit create scheduled report
		cy.visit("/dashboard/scheduled-reports/INIT");
		// Navigate to data tab
		cy.findByRole("tab", { name: lc.TAB_LABEL_DATA }).click();
		cy.findByLabelText(lc.LABEL_REPORT_TYPE).click();
		cy.findByRole("option", { name: lc.OPTION_RTB }).click();
		// Open the add filter menu
		cy.findByRole("button", { name: lc.BUTTON_LABEL_ADD_FILTER }).click();

		cy.intercept("**/search-dimension*").as("searchDimensions");
		// Select a filter dimension
		cy.findByLabelText(lc.FIELD_LABEL_DIMENSION).click();
		cy.findByRole("option", { name: "Buyers" }).click();
		// Call to endpoint should not result in errors
		cy.wait("@searchDimensions").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 200);
			cy.findByLabelText("Values").type(bidder.toUpperCase());
			// Filter dimension options come from druid data and are non-deterministic so we mock them
			cy.intercept("GET", "**/search-dimension*", { fixture: "reporting/dimensionBuyersValues.json" }).as(
				"search-dimensions:Buyers"
			);
			cy.findByText(bidder).should("exist");
			// Select a filter dimension
			cy.findByLabelText(lc.FIELD_LABEL_DIMENSION).click();
			cy.findByRole("option", { name: "Buyers" }).click();
			cy.findByLabelText("Values").clear().type(bidder.toLowerCase());
			cy.findByText(bidder).should("exist");
		});
	});

	it("create/update email chips in Add recipients", () => {
		// We're not actually saving the form so no need to cleanup the file before each run
		const fileName = "UI_create_update_email_chips";

		// Visit create scheduled report
		cy.visit("/dashboard/scheduled-reports/INIT");
		cy.findByLabelText(lc.LABEL_ADD_RECIPIENTS).click();
		cy.findByLabelText(appendRequired(lc.FIELDS.FILE_NAME.LABEL)).type(fileName);
		cy.findByRole("combobox", { name: lc.LABEL_REPEATS_ON }).type("Sunday");
		cy.findByRole("option", { name: lc.OPTION_SUNDAY }).click();
		cy.findByRole("combobox", { name: lc.LABEL_ADD_RECIPIENTS })
			.type("firstemail@siprocal.com{enter}")
			.type("secondemail@siprocal.com{enter}");

		//check popup save should update existing email in chip
		cy.findByText("firstemail@siprocal.com").click();
		cy.findByLabelText(lc.LABEL_EMAIL_ADDRESS).clear().type("editfirstemail@siprocal.com");
		cy.findByRole("button", { name: globalContent.SAVE }).click();
		cy.findByText("editfirstemail@siprocal.com").should("exist");

		//check pop up cancel should not update email
		cy.findByText("secondemail@siprocal.com").click();
		cy.findByLabelText(lc.LABEL_EMAIL_ADDRESS).clear().type("editsecondemail@siprocal.com");
		cy.findByRole("button", { name: globalContent.CANCEL }).click();
		cy.findByText("editsecondemail@siprocal.com").should("not.exist");
	});

	it("should save the entered email address and convert it into a chip without clicking enter", () => {
		const fileName = "UI_chip_should_convert_on_save";
		defaultResourceCleanup(DASHBOARD_API.SCHEDULED_REPORTS, "fileName", fileName);
		defaultResourceCleanup(DASHBOARD_API.RUN_REPORTS, "name", fileName);

		//visit create scheduled reports page
		cy.visit("/dashboard/scheduled-reports/INIT");
		cy.findByLabelText(lc.LABEL_ADD_RECIPIENTS).click();
		cy.findByLabelText(appendRequired(lc.FIELDS.FILE_NAME.LABEL)).type(fileName);
		cy.findByRole("combobox", { name: lc.LABEL_REPEATS_ON }).type("Sunday");
		cy.findByRole("option", { name: lc.OPTION_SUNDAY }).click();
		cy.findByRole("combobox", { name: lc.LABEL_ADD_RECIPIENTS }).click();

		//Enter an email address and click the save button
		const testEmail = "testemail@siprocal.com";
		cy.findByLabelText(lc.LABEL_ADD_RECIPIENTS).type(testEmail);
		cy.findByRole("button", { name: globalContent.SAVE }).click();

		//Validate that the email address is converted into a chip
		cy.findByTestId("tags-chip").should("contain", testEmail);
	});
});
