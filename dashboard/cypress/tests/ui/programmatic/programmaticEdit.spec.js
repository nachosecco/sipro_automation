import programmaticLocators, { localeContent } from "../../../locators/programmaticLocators";
import { getBidderName, getProgrammaticDemandNames, getTestResourceName } from "../../../utils/resourceNameUtil";
import { createOrUpdateProgrammaticDemand } from "../../../support/demandCommands";
import { globalContent } from "../../../locators/globalLocators";
import { createOrUpdateCompany } from "../../../support/companyCommands";
import { createOrUpdateBidder } from "../../../support/bidderCommands";
import { DASHBOARD_API } from "../../../utils/serviceResources";
import { bidderLocators } from "../../../locators/bidderLocators";

const cleanup = (programmaticDemand) => {
	const pathDeleteResource = (resource) => {
		console.log(resource.id);
		return DASHBOARD_API.PROGRAMMATIC_DEMAND.getOne({ id: resource.id });
	};
	const indexPathResources = DASHBOARD_API.PROGRAMMATIC_DEMAND.getIndex();
	const filterResourceToDelete = (resource) => resource.name === programmaticDemand;
	cy.cleanResources({ indexPathResources, pathDeleteResource, filterResourceToDelete });
};

describe("Programmatic edit test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Programmatic edit validations", () => {
		const resourceNames = getProgrammaticDemandNames("Programmatic Edit");
		createOrUpdateProgrammaticDemand(resourceNames).then((response) => {
			const programmatic = response.body;
			// Visit programmatic index page
			cy.visit("/dashboard/programmatic-demand");
			// Search for target programmatic demand entity
			cy.search(programmatic.name);

			// Wait for table to load and click action button and delete option
			cy.clickDataGridEditMenuItem();

			// Edit programmatic form and submit
			const updatedName = `${programmatic.name} updated`;
			cy.findByLabelText(localeContent.FIELDS.NAME.LABEL).clear().type(updatedName);
			cy.findByRole("button", { name: globalContent.SAVE }).click();

			// Validate pop up is visible and displaying correct text
			cy.validatePopupMessage(`${updatedName} ${globalContent.SUCCESSFULLY_UPDATED_SUFFIX}`);

			// Set name back to original and save form so that subsequent test runs can find it
			cy.findByLabelText(localeContent.FIELDS.NAME.LABEL).clear().type(resourceNames.programmaticName);
			cy.findByRole("button", { name: globalContent.SAVE }).click();

			// Success message should display
			cy.validatePopupMessage(`${resourceNames.programmaticName} ${globalContent.SUCCESSFULLY_UPDATED_SUFFIX}`);
		});
	});

	it("Programmatic user should be able to edit dayparting", () => {
		const resourceNames = getProgrammaticDemandNames("Programmatic Edit");
		createOrUpdateProgrammaticDemand(resourceNames).then((response) => {
			const programmatic = response.body;
			cy.visit(`/dashboard/programmatic-demand/${programmatic.id}`);
		});

		cy.clickElement(programmaticLocators.qualityTab);
		cy.findByRole("checkbox", { name: localeContent.FIELDS.DAYPARTING.LABEL }).click();

		// Click Monday to select all hours
		cy.findByRole("button", { name: localeContent.FIELDS.DAYPARTING.DAY_LABEL.MONDAY }).click();
		cy.findByRole("button", { name: globalContent.SAVE }).click();

		// Validate successful save
		cy.validatePopupMessage(`${resourceNames.programmaticName} ${globalContent.SUCCESSFULLY_UPDATED_SUFFIX}`);

		// Reload the page
		cy.reload();

		// Dayparting should be enabled with all monday hours selected
		cy.clickElement(programmaticLocators.qualityTab);
		cy.findByRole("checkbox", { name: localeContent.FIELDS.DAYPARTING.LABEL }).should("be.checked");

		cy.findByRole("table").within(() => {
			cy.findAllByRole("checkbox").each((checkbox) => {
				const ariaLabel = checkbox.attr("aria-label");
				if (ariaLabel.includes(localeContent.FIELDS.DAYPARTING.DAY_LABEL.MONDAY)) {
					cy.wrap(checkbox).should("be.checked");
				} else {
					cy.wrap(checkbox).should("not.be.checked");
				}
			});
		});
	});
});

describe("Programmatic edit test cases with global user", () => {
	beforeEach(() => {
		cy.loginGlobalUserProgrammatically();
	});

	it("Programmatic edit allowed_unallowed_bidders", () => {
		// Create a secondary company
		const alphaCompanyName = getTestResourceName("Secondary Company For Allowed Unallowed Bidders");
		const resourceNames = getProgrammaticDemandNames("Programmatic Demand Creation with deal");
		const timeStamp = new Date().getTime();
		const dealId = `UI_deal_${timeStamp}`;
		cleanup(resourceNames.programmaticName);
		createOrUpdateCompany({ companyName: alphaCompanyName }).then(({ body: { id: secondaryCompanyId } }) => {
			// Create a bidder under the primary company
			const firstGlobalBidderName = getBidderName("First Global Bidder");
			createOrUpdateBidder({ bidderName: firstGlobalBidderName });
			// Create a bidder under the primary company
			const secondGlobalBidderName = getBidderName("Second Global Bidder");
			createOrUpdateBidder({ bidderName: secondGlobalBidderName });

			// Visit the index page for the primary company
			cy.visit("/dashboard/bidders");
			//search for first global bidder
			cy.search(firstGlobalBidderName);
			// Bidder should show
			cy.findByRole("link", { name: firstGlobalBidderName }).click();
			// click on company access all dropdown
			cy.clickElement(bidderLocators.companyAccessDropdown);
			// select allowed list of bidder
			cy.clickElement(bidderLocators.allowListOption);
			// assigning secondary company to first bidder
			cy.get(bidderLocators.companyAllowedListDropdown).type(alphaCompanyName);
			cy.findByRole("option", { name: alphaCompanyName }).click();
			cy.findByRole("button", { name: globalContent.SAVE }).click();

			// Visit the index page for the primary company again
			cy.visit("/dashboard/bidders");
			// Visit the index page for the primary company
			cy.search(secondGlobalBidderName);
			// Bidder should show
			cy.findByRole("link", { name: secondGlobalBidderName }).click();
			// click on company access all dropdown
			cy.clickElement(bidderLocators.companyAccessDropdown);
			// select allowed list of bidder
			cy.clickElement(bidderLocators.allowListOption);
			// assigning secondary company to second bidder
			cy.get(bidderLocators.companyAllowedListDropdown).type(alphaCompanyName);
			cy.findByRole("option", { name: alphaCompanyName }).click();
			cy.findByRole("button", { name: globalContent.SAVE }).click();

			// Visit the index page of programmatic demand of the secondary company
			cy.visit(`dashboard/programmatic-demand?companyId=${secondaryCompanyId}`);
			// click add programmatic button
			cy.clickElement(programmaticLocators.addProgrammaticDemandButton);

			//enabling deal checkbox
			cy.findByRole("checkbox", { name: localeContent.FIELDS.DEAL.LABEL }).click();
			cy.findByLabelText(localeContent.FIELDS.DEAL_ID.LABEL).type(dealId);
			cy.findByLabelText(localeContent.FIELDS.FLOOR_PRICE.LABEL).type(5);

			cy.findByLabelText(localeContent.FIELDS.NAME.LABEL).type(resourceNames.programmaticName);

			//assigning first global bidder to programmatic demand
			cy.findByPlaceholderText(localeContent.FIELDS.BIDDER_CONFIG.SEARCH).type(firstGlobalBidderName);
			cy.findByRole("listitem", { name: firstGlobalBidderName }).within(() => {
				cy.findByRole("button", { name: localeContent.FIELDS.BIDDER_CONFIG.ADD_BIDDER }).click();
			});
			//asserting second bidder should exists in available bidder list
			cy.findByPlaceholderText(localeContent.FIELDS.BIDDER_CONFIG.SEARCH).clear().type(secondGlobalBidderName);
			cy.findByRole("list", { name: "available bidders" }).within(() => {
				cy.findByRole("listitem", { name: secondGlobalBidderName }).should("exist");
			});
			//saving with first bidder only
			cy.findByRole("button", { name: globalContent.SAVE }).click();

			// Visit the index page for the primary company
			cy.visit("/dashboard/bidders");
			//searching for second bidder for removing secondary company
			cy.search(secondGlobalBidderName);
			// Bidder should show
			cy.findByRole("link", { name: secondGlobalBidderName }).click();
			//deselecting secondary company from allowed bidder list
			cy.get(bidderLocators.companyAllowedListDropdown).type(alphaCompanyName);
			cy.findByRole("option", { name: alphaCompanyName }).click();
			cy.findByRole("button", { name: globalContent.SAVE }).click();

			// Visit the index page of progammatic demand of the secondary company
			cy.visit(`dashboard/programmatic-demand?companyId=${secondaryCompanyId}`);
			cy.search(resourceNames.programmaticName);

			//click edit button
			cy.clickDataGridEditMenuItem();

			//asserting second bidder should not exists in available bidder list
			cy.findByRole("list", { name: "available bidders" }).within(() => {
				cy.findByRole("listitem", { name: secondGlobalBidderName }).should("not.exist");
			});
		});
	});
});
