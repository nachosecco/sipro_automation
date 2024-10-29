import locators, { localeContent as lc } from "../../../locators/reportingLocators";
import pressEscapeOnBody from "../../../utils/pressEscapeOnBody";

describe("Reporting filter", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Select filter options by typing in other then originally listed", () => {
		// Visit dashboard reporting
		cy.visit("/dashboard/reporting");
		cy.intercept("**/search-dimension*", { fixture: "reporting/dimensionPublisherValues.json" });

		// open add filter modal
		cy.findByRole("button", { name: lc.ADD_FILTER_BUTTON }).click();
		// select dimension and select preloaded value
		cy.findByLabelText(lc.FILTER_DIMENSION_LABEL).click();
		cy.findByRole("option", { name: lc.SLICE_LABELS.publisher }).click();
		cy.findByLabelText(lc.FILTER_DIMENSION_OPTIONS_LABEL).click();
		cy.findByRole("option", { name: "AMC Network" }).click();

		// Type in characters and select option not present in previously available list
		cy.intercept("**/search-dimension*", { fixture: "reporting/dimensionPublisherValues2.json" });
		cy.findByRole("combobox", { name: lc.VALUES }).type("Blo");
		cy.findByRole("option", { name: "Bloomberg" }).click();

		pressEscapeOnBody();

		// validate filter is visible on UI after save
		cy.findByRole("button", { name: lc.FILTER_SAVE_BUTTON }).click();
		cy.findByRole("button", { name: lc.SLICE_LABELS.publisher }).should("be.visible");
	});

	it("Select seatId filter options by typing and validate search-dimensions request should get called everytime user type", () => {
		// Visit dashboard reporting
		cy.visit("/dashboard/reporting");
		// switch rtb tab
		cy.clickElement(locators.rtbTab);
		// open add filter
		cy.findByRole("button", { name: lc.ADD_FILTER_BUTTON }).click();
		// select dimension and select preloaded value
		cy.findByLabelText(lc.FILTER_DIMENSION_LABEL).click();
		// intercepting a search dimension request which hits when seatId dimension selected
		cy.intercept("**/search-dimension**").as("search-dimension-api");
		// select seat id
		cy.findByRole("option", { name: lc.SLICE_LABELS.seatId }).click();
		// wait for search-dimensions network call to complete and validate response code
		cy.wait("@search-dimension-api").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 200);
		});
		// type 1 in the values field
		// eslint-disable-next-line cypress/unsafe-to-chain-command
		cy.findByLabelText(lc.FILTER_DIMENSION_OPTIONS_LABEL).click().type("1");
		// wait for search-dimensions network call to complete
		cy.intercept("**/search-dimension**").as("MyFirstRequest");
		// validate request url
		cy.wait("@MyFirstRequest").its("request.url").should("include", "searchString=1");
		// type 2 in the values field
		// eslint-disable-next-line cypress/unsafe-to-chain-command
		cy.findByText(lc.FILTER_DIMENSION_OPTIONS_LABEL).click().type("2");
		// wait for search-dimensions network call to complete
		cy.intercept("**/search-dimension**").as("MySecondRequest");
		// validate request url
		cy.wait("@MySecondRequest").its("request.url").should("include", "searchString=12");
	});

	it("user can change the timezone and timezone selector is disabled when date range is past 31 days", () => {
		// Spy on performance endpoint
		cy.intercept("GET", "**/manage/metrics/performance*").as("performance");

		// Visit reporting dashboard
		cy.visit("/dashboard/reporting");
		// UTC timezone is displayed on load
		cy.findByTestId(locators.timeZoneTestId).should("have.text", `UTC`);

		// Open timezone selector and select a Central Time
		cy.findByTestId(locators.timeZoneTestId).click();
		cy.clickElement(locators.timeZoneCTButton);
		// confirm updated timezone CT is displayed in the chip
		cy.findByTestId(locators.timeZoneTestId).should("have.text", `CT`);
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

		// Go to 2 months back
		cy.clickElement(locators.previousMonthClickFromCalendarLeftArrow);
		cy.clickElement(locators.previousMonthClickFromCalendarLeftArrow);

		// Select First Date of the 2months back as start and end date
		cy.clickFirstElement(locators.firstDateOfTheMonth);
		cy.clickFirstElement(locators.firstDateOfTheMonth);

		// Confirm timezone chip is disabled now
		cy.findByTestId(locators.timeZoneTestId).should("have.attr", "aria-disabled");
	});
});
