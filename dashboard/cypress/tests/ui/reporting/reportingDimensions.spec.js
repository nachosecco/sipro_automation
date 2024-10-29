import locators, { localeContent as lc } from "../../../locators/reportingLocators";
import { getHomepagePermissions } from "../../../utils/getBasePermissions";
import pressEscapeOnBody from "../../../utils/pressEscapeOnBody";

describe("Reporting dashboard", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});
	it("restricted dimensions should not changed the order of its placement after dragging [For the Seat ID and Deal Id]", () => {
		cy.visit("/dashboard/reporting");

		// Switch to rtb tab
		cy.clickElement(locators.rtbTab);
		// Click add dimension
		cy.findByRole("button", { name: lc.ADD_DIMENSION_BUTTON_LABEL }).click();
		// Select the option
		cy.findByRole("menuitem", { name: lc.SLICE_LABELS.placement }).click();
		// Select the option
		cy.findByRole("menuitem", { name: lc.SLICE_LABELS.buyers }).click();
		// Select the option
		cy.findByRole("menuitem", { name: lc.SLICE_LABELS.seatId }).click();
		// Select the option
		cy.findByRole("menuitem", { name: lc.SLICE_LABELS.dealid }).click();
		pressEscapeOnBody();
		// Focus on last dimension chip dnd button (second button with the same name as the delete button for the same listitem)
		// Select the seat id and try to place it before the deal id
		cy.findAllByRole("button", { name: lc.SLICE_LABELS.seatId })
			.last()
			.click()
			// Press enter on dnd button to start drag
			.type("{enter}")
			// Press left on the keyboard twice to move the item to the beginning of the dimensions
			.type("{leftArrow}{leftArrow}")
			// Press enter to drop the item
			.type("{enter}")
			// Press right on the keyboard (to prove that the previous press of enter has ended the drag sequence)
			.type("{rightArrow}")
			.type("{enter}");

		// Dimension item order should be as expected
		const expectedLabelOrder = [
			lc.SLICE_LABELS.placement,
			lc.SLICE_LABELS.buyers,
			lc.SLICE_LABELS.dealid,
			lc.SLICE_LABELS.seatId,
		];
		cy.findByRole("list", { name: "Dimensions" }).within(() => {
			cy.findAllByRole("listitem").each((el, index) => {
				cy.wrap(el).should("have.text", expectedLabelOrder[index]);
			});
		});
	});
	it("restricted dimensions should not changed the order of its placement [for the buyers and seatId]", () => {
		cy.visit("/dashboard/reporting");

		// Switch to rtb tab
		cy.clickElement(locators.rtbTab);
		// Click add dimension
		cy.findByRole("button", { name: lc.ADD_DIMENSION_BUTTON_LABEL }).click();
		// Select the option
		cy.findByRole("menuitem", { name: lc.SLICE_LABELS.placement }).click();
		// Select the option
		cy.findByRole("menuitem", { name: lc.SLICE_LABELS.buyers }).click();
		// Select the option
		cy.findByRole("menuitem", { name: lc.SLICE_LABELS.seatId }).click();
		// Select the option
		cy.findByRole("menuitem", { name: lc.SLICE_LABELS.dealid }).click();
		pressEscapeOnBody();
		// Focus on last dimension chip dnd button (second button with the same name as the delete button for the same listitem)
		// Select the seat id and try to place it before the buyers
		cy.findAllByRole("button", { name: lc.SLICE_LABELS.seatId })
			.last()
			.click()
			// Press enter on dnd button to start drag
			.type("{enter}")
			// Press left on the keyboard twice to move the item to the beginning of the dimensions
			.type("{leftArrow}{leftArrow}")
			.type("{leftArrow}{leftArrow}")
			// Press enter to drop the item
			.type("{enter}")
			// Press right on the keyboard (to prove that the previous press of enter has ended the drag sequence)
			.type("{rightArrow}")
			.type("{enter}");
		// Dimension item order should be as expected
		const expectedLabelOrder = [
			lc.SLICE_LABELS.placement,
			lc.SLICE_LABELS.buyers,
			lc.SLICE_LABELS.dealid,
			lc.SLICE_LABELS.seatId,
		];
		cy.findByRole("list", { name: "Dimensions" }).within(() => {
			cy.findAllByRole("listitem").each((el, index) => {
				cy.wrap(el).should("have.text", expectedLabelOrder[index]);
			});
		});
	});
	it("when date range is greater than 7 days then app name, app bundle, domain and content genre should be disabled and if selected date is more than 31 days in the past then hour should be disabled", () => {
		cy.visit("/dashboard/reporting");

		// Open calendar and select a previous 7 days
		cy.clickElement(locators.dateRange);
		cy.clickElement(locators.dateRangeButtonPrevious7Days);

		// click add dimensions and validate dimensions are not disabled
		cy.findByRole("button", { name: lc.ADD_DIMENSION_BUTTON_LABEL }).click();
		cy.findByRole("menuitem", { name: lc.SLICE_LABELS.appBundle })
			.should("exist")
			.should("not.have.attr", "aria-disabled");
		cy.findByRole("menuitem", { name: lc.SLICE_LABELS.appName })
			.should("exist")
			.should("not.have.attr", "aria-disabled");
		cy.findByRole("menuitem", { name: lc.SLICE_LABELS.domain })
			.should("exist")
			.should("not.have.attr", "aria-disabled");
		cy.findByRole("menuitem", { name: lc.SLICE_LABELS.contentGenre })
			.should("exist")
			.should("not.have.attr", "aria-disabled");
		pressEscapeOnBody();

		// Open calendar and select a predefined range (e.g. Today)
		cy.clickElement(locators.dateRange);
		cy.clickElement(locators.dateRangeButtonPrevious30Days);

		// Click add dimensions and check expected dimensions are now disabled
		cy.findByRole("button", { name: lc.ADD_DIMENSION_BUTTON_LABEL }).click();
		cy.findByRole("menuitem", { name: lc.SLICE_LABELS.appBundle })
			.should("exist")
			.should("have.attr", "aria-disabled");
		cy.findByRole("menuitem", { name: lc.SLICE_LABELS.appName })
			.should("exist")
			.should("have.attr", "aria-disabled");
		cy.findByRole("menuitem", { name: lc.SLICE_LABELS.domain })
			.should("exist")
			.should("have.attr", "aria-disabled");
		cy.findByRole("menuitem", { name: lc.SLICE_LABELS.hour })
			.should("exist")
			.should("not.have.attr", "aria-disabled");
		cy.findByRole("menuitem", { name: lc.SLICE_LABELS.contentGenre })
			.should("exist")
			.should("have.attr", "aria-disabled");
		pressEscapeOnBody();

		// Open calendar and select a cutom date range (e.g. Today)
		cy.clickElement(locators.dateRange);
		cy.clickElement(locators.dateRangeTabCustom);
		// Go to 2 months back
		cy.clickElement(locators.previousMonthClickFromCalendarLeftArrow);
		cy.clickElement(locators.previousMonthClickFromCalendarLeftArrow);
		cy.clickFirstElement(locators.firstDateOfTheMonth);
		cy.clickFirstElement(locators.twentiethDateOfTheMonth);
		// If selected date is of morethan 31 days in the past then hour should be disabled
		cy.findByRole("button", { name: lc.ADD_DIMENSION_BUTTON_LABEL }).click();
		cy.findByRole("menuitem", { name: lc.SLICE_LABELS.hour }).should("exist").should("have.attr", "aria-disabled");
	});
});

describe("Reporting dimensions", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});
	it("Campaign dimensions are visible based on permission", () => {
		const USERNAME = `dimension-permissions@siprocal.com`;

		// Create a user who only has access to the limited dimensions
		cy.createUserWithPermissions({
			userRoleName: `automation_dimension_permissions`,
			username: USERNAME,
			permissionsToEnable: [
				...getHomepagePermissions(),
				// Grant access to campaign and rtb reports
				"VIEW_CAMPAIGN_REPORT",
				"VIEW_RTB_REPORT",
				"VIEW_NETWORK_REPORT",
				// Grant Permissions to be validated
				"VIEW_CAMPAIGN_REPORT_DIMENSION_POD_SEQUENCE",
			],
		});

		cy.visit("/dashboard/reporting");
		cy.clickElement(locators.campaignTab);
		// Click Add Dimensions button
		cy.clickElement(locators.addDimensionButton);
		[
			lc.SLICE_LABELS.appName,
			lc.SLICE_LABELS.appBundle,
			lc.SLICE_LABELS.podSequence,
			//more to be added here for validation further
		].forEach((dimensionLabel) => {
			cy.findByRole("menuitem", { name: dimensionLabel }).should("exist");
		});
	});

	it("hour dimension could be dragged to extreme right", () => {
		cy.visit("/dashboard/reporting");

		// Click add dimension
		cy.findByRole("button", { name: lc.ADD_DIMENSION_BUTTON_LABEL }).click();
		// Select the option
		cy.findByRole("menuitem", { name: lc.SLICE_LABELS.appBundle }).click();
		// Select the option
		cy.findByRole("menuitem", { name: lc.SLICE_LABELS.hour }).click();
		// Select the option
		cy.findByRole("menuitem", { name: lc.SLICE_LABELS.appName }).click();
		// Select the option
		cy.findByRole("menuitem", { name: lc.SLICE_LABELS.domain }).click();
		pressEscapeOnBody();
		// Focus on last dimension chip dnd button (second button with the same name as the delete button for the same listitem)
		// Select the hour and try to place it at the end
		cy.findAllByRole("button", { name: lc.SLICE_LABELS.hour })
			.last()
			.click()
			// Press enter on hour chip to start drag
			.type("{enter}")
			// Press right arrow on the keyboard twice to move the item to the end of the dimensions
			.type("{rightArrow}{rightArrow}")
			// Press enter to drop the item
			.type("{enter}")
			// Press right on the keyboard (to prove that the previous press of enter has ended the drag sequence)
			.type("{rightArrow}")
			.type("{enter}");

		// Dimension item order should be as expected that hour should be placed at the end
		const expectedLabelOrder = [
			lc.SLICE_LABELS.appBundle,
			lc.SLICE_LABELS.appName,
			lc.SLICE_LABELS.domain,
			lc.SLICE_LABELS.hour,
		];
		cy.findByRole("list", { name: "Dimensions" }).within(() => {
			cy.findAllByRole("listitem").each((el, index) => {
				cy.wrap(el).should("have.text", expectedLabelOrder[index]);
			});
		});
	});

	it("when changing tabs, there should not have a dimension selected", () => {
		cy.visit("/dashboard/reporting");

		// Click add dimension
		cy.findByRole("button", { name: lc.ADD_DIMENSION_BUTTON_LABEL }).click();

		// Select the option
		cy.findByRole("menuitem", { name: lc.SLICE_LABELS.placement }).click();

		pressEscapeOnBody();

		cy.findByRole("list", { name: lc.FIELD_LABEL_SELECTED_DIMENSIONS }).within(() => {
			cy.findAllByRole("listitem").first((el) => {
				cy.wrap(el).should("have.text", lc.SLICE_LABELS.placement);
			});
		});

		// Spy on performance endpoint
		cy.intercept("GET", "**/manage/metrics/performance*").as("performance");

		// Click on run report button
		cy.clickElement(locators.runReportButton);
		// Request to performance should not throw errors
		cy.wait("@performance").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 200);
		});

		// Change Report Type to Campaign
		cy.findByRole("tab", { name: lc.TAB_LABEL_CAMPAIGN }).click();

		cy.findByRole("list", { name: lc.FIELD_LABEL_SELECTED_DIMENSIONS }).within(() => {
			cy.findAllByRole("listitem").should("not.exist");
		});
	});
});
