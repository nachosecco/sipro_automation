import programmaticLocators, { localeContent } from "../../../locators/programmaticLocators";
import { DASHBOARD_API } from "../../../utils/serviceResources";
import { getProgrammaticDemandNames, getBidderName } from "../../../utils/resourceNameUtil";
import { globalContent } from "../../../locators/globalLocators";
import { createOrUpdateBidder } from "../../../support/bidderCommands";

const cleanup = (programmaticDemand) => {
	const pathDeleteResource = (resource) => {
		return DASHBOARD_API.PROGRAMMATIC_DEMAND.getOne({ id: resource.id });
	};
	const indexPathResources = DASHBOARD_API.PROGRAMMATIC_DEMAND.getIndex();
	const filterResourceToDelete = (resource) => resource.name.startsWith(programmaticDemand);
	cy.cleanResources({ indexPathResources, pathDeleteResource, filterResourceToDelete });
};

describe("Programmatic creation test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Valid programmatic creation without deal", () => {
		const resourceNames = getProgrammaticDemandNames("Programmatic Creation without deal");
		cleanup(resourceNames.programmaticName);

		createOrUpdateBidder(resourceNames);

		// Visit programmatic index page
		cy.visit("/dashboard/programmatic-demand");

		cy.findByRole("heading", { name: localeContent.TITLE }).should("exist");

		// Assert and click add programmatic button
		cy.clickElement(programmaticLocators.addProgrammaticDemandButton);

		// Verify default values are selected
		cy.getByRole(programmaticLocators.statusActiveRadio).should("be.checked");
		cy.get(programmaticLocators.startDateField).invoke("val").should("not.be.empty");

		//Verify elements are visible
		cy.verifyElementsExist(
			programmaticLocators.settingsTab,
			programmaticLocators.qualityTab,
			programmaticLocators.statusActiveRadio,
			programmaticLocators.statusInactiveRadio,
			programmaticLocators.dealToggle,
			programmaticLocators.availableDealersTable,
			programmaticLocators.selectedDealersTable,
			programmaticLocators.clearSelectedBiddersButton,
			programmaticLocators.endDateField,
			programmaticLocators.priorityDropdown,
			programmaticLocators.weightDropdown
		);
		cy.get(programmaticLocators.startDateField).should("be.visible");

		// view report button should not be visible until form is saved
		cy.findByRole("link", { name: globalContent.VIEW_REPORT }).should("not.exist");

		// Complete mandatory fields
		cy.findByLabelText(localeContent.FIELDS.NAME.LABEL).type(resourceNames.programmaticName);
		cy.findByPlaceholderText(localeContent.FIELDS.BIDDER_CONFIG.SEARCH).type(resourceNames.bidderName);

		cy.findAllByRole("listitem", { name: resourceNames.bidderName })
			.first()
			.within(() => {
				cy.findByRole("button", { name: localeContent.FIELDS.BIDDER_CONFIG.ADD_BIDDER }).click();
			});

		cy.findByText(resourceNames.bidderName).click();
		cy.findByRole("button", { name: "add Seat1" }).click();

		// Submit form
		cy.findByRole("button", { name: globalContent.SAVE }).click();

		// Success message should display
		cy.validatePopupMessage(`${resourceNames.programmaticName} ${globalContent.SUCCESSFULLY_CREATED_SUFFIX}`);

		cy.findByRole("link", { name: globalContent.VIEW_REPORT }).should("exist");
	});

	it("Valid programmatic creation with deal", () => {
		const resourceNames = getProgrammaticDemandNames("Programmatic Creation with deal");
		const timeStamp = new Date().getTime();
		const programmaticName = `${resourceNames.programmaticName} ${timeStamp}`;

		cleanup(programmaticName);

		// dealId must be unique. We use soft db deletes, so we need an id that changes with each execution
		// included all special characters supported
		const dealId = `UI_deal-.${timeStamp}`;

		createOrUpdateBidder(resourceNames);

		// Visit programmatic index page
		cy.visit("/dashboard/programmatic-demand");

		cy.findByRole("heading", { name: localeContent.TITLE }).should("exist");

		// Assert and click add programmatic button
		cy.clickElement(programmaticLocators.addProgrammaticDemandButton);

		// Verify default values are selected
		cy.getByRole(programmaticLocators.statusActiveRadio).should("be.checked");
		cy.get(programmaticLocators.startDateField).invoke("val").should("not.be.empty");

		//Verify elements are visible
		cy.verifyElementsExist(
			programmaticLocators.settingsTab,
			programmaticLocators.qualityTab,
			programmaticLocators.statusActiveRadio,
			programmaticLocators.statusInactiveRadio,
			programmaticLocators.dealToggle,
			programmaticLocators.availableDealersTable,
			programmaticLocators.selectedDealersTable,
			programmaticLocators.clearSelectedBiddersButton,
			programmaticLocators.endDateField,
			programmaticLocators.priorityDropdown,
			programmaticLocators.weightDropdown
		);
		cy.get(programmaticLocators.startDateField).should("be.visible");

		// Complete mandatory fields
		cy.findByLabelText(localeContent.FIELDS.NAME.LABEL).type(programmaticName);
		cy.findByRole("checkbox", { name: localeContent.FIELDS.DEAL.LABEL }).click();
		cy.findByLabelText(localeContent.FIELDS.DEAL_ID.LABEL).type(dealId);
		cy.findByLabelText(localeContent.FIELDS.FLOOR_PRICE.LABEL).type(5);
		// Select fixed price auction type
		cy.clickElement(programmaticLocators.auctionTypeDropdown);
		cy.clickElement(programmaticLocators.fixedPriceOption);

		// Add bidder via seats and also validate remove seat link
		cy.findByPlaceholderText(localeContent.FIELDS.BIDDER_CONFIG.SEARCH).type(resourceNames.bidderName);
		// Click bidder name to see list of seats
		cy.findByRole("listitem", { name: resourceNames.bidderName }).click();
		// Add two seats
		cy.findByRole("button", { name: "add Seat1" }).click();
		cy.findByRole("button", { name: "add Seat2" }).click();
		// validate the bidder label listing 2 seats restrictions
		cy.findByText(resourceNames.bidderName + " (2 Seat Restrictions)").should("exist");
		// Remove one of the selected seat
		cy.findByRole("button", { name: "remove Seat1" }).click();
		// Validate the bidder label changed to 1 seat restriction now
		cy.findByText(resourceNames.bidderName + " (1 Seat Restriction)").should("exist");

		// Submit form
		cy.findByRole("button", { name: globalContent.SAVE }).click();

		// Success message should display
		cy.validatePopupMessage(`${programmaticName} ${globalContent.SUCCESSFULLY_CREATED_SUFFIX}`);
	});

	it("Valid programmatic creation with private deal with goal impression", () => {
		const resourceNames = getProgrammaticDemandNames("Programmatic Creation with deal with goal impression");
		const timeStamp = new Date().getTime();
		const programmaticName = `${resourceNames.programmaticName} ${timeStamp}`;

		cleanup(programmaticName);

		// dealId must be unique. We use soft db deletes, so we need an id that changes with each execution
		const dealId = `UI_deal_${timeStamp}`;

		createOrUpdateBidder(resourceNames);

		// Visit programmatic index page
		cy.visit("/dashboard/programmatic-demand");

		cy.findByRole("heading", { name: localeContent.TITLE }).should("exist");

		// Assert and click add programmatic button
		cy.clickElement(programmaticLocators.addProgrammaticDemandButton);

		// Verify default values are selected
		cy.getByRole(programmaticLocators.statusActiveRadio).should("be.checked");
		cy.get(programmaticLocators.startDateField).invoke("val").should("not.be.empty");

		// Complete mandatory fields
		cy.findByLabelText(localeContent.FIELDS.NAME.LABEL).type(programmaticName);
		cy.findByRole("checkbox", { name: localeContent.FIELDS.DEAL.LABEL }).click();
		cy.findByLabelText(localeContent.FIELDS.DEAL_ID.LABEL).type(dealId);
		cy.findByRole("checkbox", { name: localeContent.FIELDS.PRIVATE_AUCTION.LABEL }).click();

		cy.findByLabelText(localeContent.FIELDS.FLOOR_PRICE.LABEL).type(5);
		// Select fixed price auction type
		cy.clickElement(programmaticLocators.auctionTypeDropdown);
		cy.clickElement(programmaticLocators.fixedPriceOption);

		cy.findByRole("radio", { name: localeContent.FIELDS.DEAL_GOAL_TYPE.IMPRESSION.LABEL }).click();

		cy.findByLabelText(localeContent.FIELDS.DEAL_GOAL.LABEL).type("10");

		// Set Frequency capping data
		cy.clickElement(programmaticLocators.frequencyCappingSwitch);
		cy.getByRole(programmaticLocators.impressionsPerUserField).type("2");
		cy.clickElement(programmaticLocators.timeframeDropdown);
		cy.clickElement(programmaticLocators.perWeekOption);

		cy.findByPlaceholderText(localeContent.FIELDS.BIDDER_CONFIG.SEARCH).type(resourceNames.bidderName);
		cy.setDateByLabelText(localeContent.FIELDS.END_DATE.LABEL, "01/01/2030 06:00 pm");

		cy.findByRole("listitem", { name: resourceNames.bidderName }).within(() => {
			cy.findByRole("button", { name: localeContent.FIELDS.BIDDER_CONFIG.ADD_BIDDER }).click();
		});

		// Submit form
		cy.findByRole("button", { name: globalContent.SAVE }).click();

		// Success message should display
		cy.validatePopupMessage(`${programmaticName} ${globalContent.SUCCESSFULLY_CREATED_SUFFIX}`);
		cy.reload();
		// Validate that frequency capping has values
		cy.getByRole(programmaticLocators.frequencyCappingSwitch).should("be.checked");
		cy.getByRole(programmaticLocators.impressionsPerUserField).should("have.value", 2);
		cy.getByRole(programmaticLocators.perWeekSelectedButton).should("exist");
	});

	it("Programmatic edit should not show any other bidders after save", () => {
		// Create a programmatic demand
		const resourceNames = getProgrammaticDemandNames("Programmatic Demand Creation");
		cleanup(resourceNames.programmaticName);
		// Create a bidder under the primary company
		const firstGlobalBidderName = getBidderName(`First Global Bidder For Programmatic`);
		createOrUpdateBidder({ bidderName: firstGlobalBidderName });
		// Create a bidder under the primary company
		const secondGlobalBidderName = getBidderName("Second Global Bidder For Programmatic");
		createOrUpdateBidder({ bidderName: secondGlobalBidderName });

		// Visit the index page of the programmatic demand for the primary company again
		cy.visit("/dashboard/programmatic-demand");
		cy.clickElement(programmaticLocators.addProgrammaticDemandButton);

		// Type the programmatic demand name to create
		cy.findByLabelText(localeContent.FIELDS.NAME.LABEL).type(resourceNames.programmaticName);

		//assigning first global bidder to programmatic demand and select only the bidder not its seats
		cy.findByPlaceholderText(localeContent.FIELDS.BIDDER_CONFIG.SEARCH).type(firstGlobalBidderName);
		cy.findByRole("listitem", { name: firstGlobalBidderName }).within(() => {
			cy.findByRole("button", { name: "show seats" }).click();
			cy.findByRole("button", { name: localeContent.FIELDS.BIDDER_CONFIG.ADD_BIDDER }).click();
		});
		// save
		cy.findByRole("button", { name: globalContent.SAVE }).click();
		// Expect that there should be any 3 available bidder in the available bidder list
		cy.get('[aria-label="available bidders"]').children().its("length").should("eq", 2);

		// select all the seats
		cy.findByRole("button", { name: "add Seat1" }).click();
		cy.findByRole("button", { name: "add Seat2" }).click();
		// save
		cy.findByRole("button", { name: globalContent.SAVE }).click();
		// Expect that there should not be any available bidder in the available bidder list
		cy.get('[aria-label="available bidders"]').children().should("have.length", 0);
	});
});
