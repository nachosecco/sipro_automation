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
		const sliceLabels = [lc.SLICE_LABELS.publisher, lc.SLICE_LABELS.site, lc.SLICE_LABELS.placement];
		cy.findByRole("button", { name: lc.ADD_DIMENSION_BUTTON_LABEL }).click();
		sliceLabels.forEach((label) => {
			// Click add dimension
			// Select the option
			cy.findByRole("menuitem", { name: label }).click();
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

		cy.intercept("GET", "**/filter-and-group*").as("filterAndGroup");

		// Run reports to apply config
		cy.findByRole("button", { name: lc.RUN_REPORT_BUTTON }).click();

		cy.wait("@filterAndGroup").then(({ request }) => {
			const { searchParams } = new URL(request.url);
			// First selected slice should be used for the grouped request
			expect(searchParams.get("group")).to.equal("publisher");
			expect(searchParams.get("reportType")).to.equal("network");
			expect(searchParams.get("filters[publisher][]")).to.equal("guid123");
		});

		// Column headers should be added for all slices
		[lc.SLICE_LABELS.publisher, lc.SLICE_LABELS.site, lc.SLICE_LABELS.placement].forEach((label) => {
			cy.findByRole("columnheader", { name: label }).should("exist");
		});
	});
});

it("user can refresh page and preserve reporting type, filters and slice selections (date range can't be tested deterministically)", () => {
	cy.loginProgrammatically();

	cy.intercept("GET", "**/search-dimension*", publisherFilterOptions).as("search-dimensions:publisher");

	cy.visit("/dashboard/reporting");

	// Change Report Type to RTB
	cy.findByRole("tab", { name: "RTB" }).click();

	// Select Publishers, Sites, and Placements slices
	const sliceLabels = [lc.SLICE_LABELS.publisher, lc.SLICE_LABELS.site, lc.SLICE_LABELS.placement];
	// Click add dimension
	cy.findByRole("button", { name: lc.ADD_DIMENSION_BUTTON_LABEL }).click();
	sliceLabels.forEach((label) => {
		// Select the option
		cy.findByRole("menuitem", { name: label }).click();
	});
	pressEscapeOnBody();
	/**  Set a filter
	 * (NOTE: The filter options endpoint is mocked because it relies on druid data)
	 */
	// Select a filter dimension
	cy.findByRole("button", { name: lc.ADD_FILTER_BUTTON }).click();
	cy.findByLabelText(lc.FILTER_DIMENSION_LABEL).click();
	cy.findByRole("option", { name: lc.SLICE_LABELS.publisher }).click();
	// Select a filter dimension option
	cy.findByLabelText(lc.FILTER_DIMENSION_OPTIONS_LABEL).click();
	const firstFilterName = Object.entries(publisherFilterOptions)[0][1];
	cy.findByRole("option", { name: firstFilterName }).click();
	// Close dimension option selection menu and save the filter
	pressEscapeOnBody();
	cy.findByRole("button", { name: lc.FILTER_SAVE_BUTTON }).click();

	cy.intercept("GET", "**/filter-and-group*").as("filterAndGroup");

	// Run reports to apply config
	cy.findByRole("button", { name: lc.RUN_REPORT_BUTTON }).click();

	// Column headers should be added for all slices
	[lc.SLICE_LABELS.publisher, lc.SLICE_LABELS.site, lc.SLICE_LABELS.placement].forEach((label) => {
		cy.findByRole("columnheader", { name: label }).should("exist");
	});

	// Refresh the page
	cy.reload();

	// Filter and group request should be made when we load the page using pre-refresh state
	cy.wait("@filterAndGroup").then(({ request }) => {
		const { searchParams } = new URL(request.url);
		// First selected slice should be used for the grouped request
		expect(searchParams.get("group")).to.equal("publisher");
		expect(searchParams.get("reportType")).to.equal("rtb");
		expect(searchParams.get("filters[publisher][]")).to.equal("guid123");
	});

	// Column headers should be added for all active slices
	[
		lc.SLICE_LABELS.publisher,
		lc.SLICE_LABELS.site,
		lc.SLICE_LABELS.placement,
		lc.METRIC_LABEL.RTB_OPPORTUNITIES, // test for an RTB-only metric to prove we're on the RTB tab
	].forEach((label) => {
		cy.findByRole("columnheader", { name: label }).should("exist");
	});
});
